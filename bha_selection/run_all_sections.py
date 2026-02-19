"""Orchestrator: run the full BHA performance curve pipeline for every
section of a target well.

Steps:
  1. Analyze target well sections  → target_sections.json
  2. Pull ALL BHA runs from offsets (--all-runs) → all_bhas_*.csv
  3. Parse bit & motor models on all_bhas and per-section files
  4. Filter BHA runs per section  → bhas_<section>_<hole_size>.csv
  5. For each section:
       a. group_equivalent_bhas
       b. pull_1ft_for_runs
       c. normalize_formations (vertical only)
       d. build_rop_curves
       e. plot_type_curves

Usage:
    python run_all_sections.py --asset 82512872
    python run_all_sections.py --asset 82512872 --wells offset_wells_15mi.csv --skip-pull
"""

import argparse
import json
import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable


def run_step(description, cmd, cwd=None):
    """Run a subprocess, print output, return exit code."""
    print(f"\n{'-' * 70}")
    print(f"  STEP: {description}")
    print(f"  CMD:  {' '.join(cmd)}")
    print(f"{'-' * 70}")
    t0 = time.time()
    result = subprocess.run(cmd, cwd=cwd or SCRIPT_DIR,
                            capture_output=False, text=True)
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"  !! Step failed with exit code {result.returncode} "
              f"({elapsed:.1f}s)")
    else:
        print(f"  OK ({elapsed:.1f}s)")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run full BHA analysis pipeline for all sections.")
    parser.add_argument("--asset", required=True,
                        help="Target well asset ID")
    parser.add_argument("--wells", default="offset_wells_15mi.csv",
                        help="Offset wells CSV file")
    parser.add_argument("--skip-pull", action="store_true",
                        help="Skip pulling BHA runs (use existing all_bhas CSV)")
    parser.add_argument("--skip-1ft", action="store_true",
                        help="Skip pulling 1ft data (use existing)")
    parser.add_argument("--min-coverage", type=float, default=0.5,
                        help="Min formation coverage for vertical sections")
    parser.add_argument("--max-missing-formations", type=int, default=1,
                        help="Max formations with no rotary data before "
                             "excluding a group (default: 1)")
    parser.add_argument("--formations", default=None,
                        help="Path to formation_tops_canonical.csv")
    parser.add_argument("--export-csv", action="store_true",
                        help="Pass --export-csv to all subprocess scripts")
    args = parser.parse_args()

    csv_flag = ["--export-csv"] if args.export_csv else []

    asset_id = args.asset
    wells_csv = args.wells
    if not os.path.isabs(wells_csv):
        wells_csv = os.path.join(SCRIPT_DIR, wells_csv)

    fm_csv = args.formations
    if fm_csv and not os.path.isabs(fm_csv):
        fm_csv = os.path.join(SCRIPT_DIR, fm_csv)
    if fm_csv is None:
        for candidate in ["formation_tops_canonical.csv", "formation_tops.csv"]:
            p = os.path.join(SCRIPT_DIR, candidate)
            if os.path.exists(p):
                fm_csv = p
                break

    print(f"\n{'=' * 70}")
    print(f"  FULL SECTION-DRIVEN BHA ANALYSIS PIPELINE")
    print(f"  Target asset: {asset_id}")
    print(f"  Offset wells: {os.path.basename(wells_csv)}")
    print(f"  Formations:   {os.path.basename(fm_csv) if fm_csv else 'N/A'}")
    print(f"{'=' * 70}")

    t_start = time.time()

    # ── Step 1: Analyze target well sections ──
    sections_json = os.path.join(SCRIPT_DIR, "target_sections.json")
    fm_arg = ["--formations", fm_csv] if fm_csv else []
    rc = run_step(
        "Analyze target well sections",
        [PYTHON, os.path.join(SCRIPT_DIR, "analyze_target_well.py"),
         "--asset", asset_id, "--output", sections_json] + fm_arg + csv_flag,
    )
    if rc != 0:
        print("FATAL: Could not analyze target well.")
        sys.exit(1)

    with open(sections_json, encoding="utf-8") as f:
        target = json.load(f)

    sections = target.get("sections", [])
    well_name = target.get("target_well_name", "Unknown")
    print(f"\n  Target well: {well_name}")
    print(f"  Sections found: {len(sections)}")
    for s in sections:
        hs = f"{s['hole_size']}\"" if s.get("hole_size") else "?"
        print(f"    {s['name']:<30} {hs:>7}  {s['mode']}")

    # ── Step 2: Pull ALL BHA runs from offsets ──
    wells_basename = os.path.splitext(os.path.basename(wells_csv))[0]
    all_bhas_csv = os.path.join(SCRIPT_DIR, f"all_bhas_{wells_basename}.csv")

    if not args.skip_pull:
        rc = run_step(
            "Pull ALL BHA runs from offset wells",
            [PYTHON, os.path.join(SCRIPT_DIR, "pull_lateral_bhas.py"),
             wells_csv, "--all-runs"] + csv_flag,
        )
        if rc != 0:
            print("FATAL: Could not pull BHA runs.")
            sys.exit(1)

    if not os.path.exists(all_bhas_csv):
        print(f"FATAL: {all_bhas_csv} not found")
        sys.exit(1)

    # ── Step 3: Parse bit & motor models ──
    run_step(
        "Parse bit & motor models (all BHA files)",
        [PYTHON, os.path.join(SCRIPT_DIR, "parse_bit_motors.py")] + csv_flag,
    )

    # ── Step 4: Filter BHA runs per section ──
    fm_arg = ["--formations", fm_csv] if fm_csv else []
    rc = run_step(
        "Filter BHA runs by section (hole size + formations)",
        [PYTHON, os.path.join(SCRIPT_DIR, "filter_bhas_by_section.py"),
         sections_json, all_bhas_csv,
         "--min-coverage", str(args.min_coverage)] + fm_arg + csv_flag,
    )
    if rc != 0:
        print("WARNING: Section filtering had issues. Continuing...")

    # Re-run parse on the newly created per-section files
    run_step(
        "Parse bit & motor models (per-section files)",
        [PYTHON, os.path.join(SCRIPT_DIR, "parse_bit_motors.py")] + csv_flag,
    )

    # ── Step 5: Per-section pipeline ──
    for section in sections:
        sec_name = section["name"]
        hole_size = section.get("hole_size")
        mode = section.get("mode", "vertical")
        sec_length = int(section.get("section_length_md", 5000))
        hs_str = f"{hole_size}in" if hole_size else "unknown"
        safe_name = sec_name.replace(" ", "_").replace("/", "-")

        # Section-specific BHA CSV
        sec_bha_csv = os.path.join(SCRIPT_DIR, f"bhas_{safe_name}_{hs_str}.csv")
        if not os.path.exists(sec_bha_csv):
            print(f"\n  SKIP: {sec_name} ({hs_str}) - no filtered BHA file found")
            continue

        # Section label for chart titles
        section_label = f"{sec_name} ({hs_str})"

        # Output directory for this section
        sec_out_dir = os.path.join(SCRIPT_DIR, "sections", safe_name)
        os.makedirs(sec_out_dir, exist_ok=True)

        print(f"\n{'=' * 70}")
        print(f"  SECTION: {section_label}  [{mode} mode]")
        print(f"  Output:  {sec_out_dir}")
        print(f"{'=' * 70}")

        # 5a. Group equivalent BHAs
        run_step(
            f"Group equivalent BHAs: {sec_name}",
            [PYTHON, os.path.join(SCRIPT_DIR, "group_equivalent_bhas.py"),
             sec_bha_csv] + csv_flag,
        )

        # 5b. Pull 1ft data
        if not args.skip_1ft:
            pull_cmd = [
                PYTHON, os.path.join(SCRIPT_DIR, "pull_1ft_for_runs.py"),
                sec_bha_csv,
                "--mode", mode,
                "--output-dir", sec_out_dir,
            ] + csv_flag
            if mode == "vertical" and fm_csv:
                pull_cmd += ["--formations", fm_csv]
            run_step(
                f"Pull 1ft data: {sec_name}",
                pull_cmd,
            )

        # 5c. Build ROP curves
        if mode == "vertical":
            onefoot_csv = os.path.join(sec_out_dir, "rop_1ft_data_vertical.csv")
        else:
            onefoot_csv = os.path.join(sec_out_dir, "rop_1ft_data.csv")

        if not os.path.exists(onefoot_csv):
            print(f"  SKIP curves: {onefoot_csv} not found")
            continue

        build_cmd = [
            PYTHON, os.path.join(SCRIPT_DIR, "build_rop_curves.py"),
            onefoot_csv,
            "--mode", mode,
            "--section-length", str(sec_length),
            "--output-dir", sec_out_dir,
        ] + csv_flag
        if mode == "vertical":
            build_cmd += ["--max-missing-formations",
                          str(args.max_missing_formations)]
        run_step(f"Build ROP curves: {sec_name}", build_cmd)

        # 5d. Plot charts
        chart_out = os.path.join(sec_out_dir, "charts")
        os.makedirs(chart_out, exist_ok=True)
        run_step(
            f"Plot type curves: {sec_name}",
            [PYTHON, os.path.join(SCRIPT_DIR, "plot_type_curves.py"),
             "--mode", mode,
             "--data-dir", sec_out_dir,
             "--output-dir", chart_out,
             "--section-label", section_label] + csv_flag,
        )

    # ── Summary ──
    total_time = time.time() - t_start
    print(f"\n{'=' * 70}")
    print(f"  PIPELINE COMPLETE")
    print(f"  Total time: {total_time:.1f}s ({total_time / 60:.1f} min)")
    print(f"{'=' * 70}")

    print(f"\n  Section outputs:")
    sections_dir = os.path.join(SCRIPT_DIR, "sections")
    if os.path.exists(sections_dir):
        for d in sorted(os.listdir(sections_dir)):
            sec_path = os.path.join(sections_dir, d)
            if os.path.isdir(sec_path):
                charts_path = os.path.join(sec_path, "charts")
                n_charts = 0
                if os.path.exists(charts_path):
                    n_charts = len([f for f in os.listdir(charts_path)
                                    if f.endswith(".png")])
                print(f"    {d:<30} {n_charts} charts")


if __name__ == "__main__":
    main()
