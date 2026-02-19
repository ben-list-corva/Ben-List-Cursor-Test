"""Group BHA runs into Equivalent BHA categories for performance comparison.

An Equivalent BHA is defined by:
  - Bit blade count (parsed)
  - Bit cutter size in mm (parsed)
  - Motor lobe configuration (e.g., "5/6")
  - Motor RPG band (lo/mid/hi/vhi)

Usage:
    python group_equivalent_bhas.py <bha_csv>
    python group_equivalent_bhas.py lateral_bhas.csv
"""
import csv
import os
import re
import sys
from collections import defaultdict

import db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def make_group_key(row):
    """Build the Equivalent BHA group key from a parsed BHA row.

    RSS BHAs get their own motor key ('RSS') since they behave completely
    differently from motor-based BHAs (all rotary, no slide).
    Agitator presence is NOT part of the group key -- it's tracked as an
    overlay within each group's slide performance curve.
    """
    blades = row.get("parsed_blades", "").strip()
    cutter = row.get("parsed_cutter_mm", "").strip()
    lobes = row.get("motor_lobe_config", "").strip()
    rpg_band = row.get("motor_rpg_band", "").strip()
    is_rss = str(row.get("is_rss", "")).strip().lower() in ("true", "1", "yes")

    if not blades or blades == "?" or "?" in str(cutter):
        bit_key = "unparsed"
    else:
        bit_key = f"{blades}B-{cutter}mm"

    if is_rss:
        motor_key = "RSS"
    elif not lobes or lobes == "?":
        motor_key = "no_motor"
    else:
        motor_key = f"{lobes}-{rpg_band}" if rpg_band and rpg_band != "?" else f"{lobes}"

    return f"{bit_key} | {motor_key}"


def group_bhas(rows):
    """Group rows by equivalent BHA key."""
    groups = defaultdict(list)
    for row in rows:
        key = make_group_key(row)
        groups[key].append(row)
    return dict(groups)


def summarize_group(key, runs):
    """Build a summary dict for one equivalent BHA group."""
    run_lengths = []
    operators = set()
    wells = set()
    bit_models = set()
    motor_models = set()
    bit_mfgs = set()
    start_depths = []
    end_depths = []
    agitator_count = 0
    rss_count = 0

    for r in runs:
        rl = r.get("run_length", "")
        if rl and rl != "N/A":
            try:
                run_lengths.append(float(rl))
            except ValueError:
                pass

        operators.add(r.get("operator", "N/A"))
        wells.add(r.get("well_name", "N/A"))

        bm = r.get("bit_model", "")
        if bm and bm != "N/A":
            bit_models.add(bm)

        bmfg = r.get("bit_manufacturer", "")
        if bmfg and bmfg != "N/A":
            bit_mfgs.add(bmfg)

        mm = r.get("motor_model", "")
        if mm and mm != "N/A":
            motor_models.add(mm)

        sd = r.get("start_depth", "")
        ed = r.get("end_depth", "")
        try:
            start_depths.append(float(sd))
        except (ValueError, TypeError):
            pass
        try:
            end_depths.append(float(ed))
        except (ValueError, TypeError):
            pass

        if str(r.get("has_agitator", "")).strip().lower() in ("true", "1", "yes"):
            agitator_count += 1
        if str(r.get("is_rss", "")).strip().lower() in ("true", "1", "yes"):
            rss_count += 1

    avg_run = sum(run_lengths) / len(run_lengths) if run_lengths else 0
    min_run = min(run_lengths) if run_lengths else 0
    max_run = max(run_lengths) if run_lengths else 0
    total_ft = sum(run_lengths)

    return {
        "group_key": key,
        "num_runs": len(runs),
        "num_wells": len(wells),
        "num_operators": len(operators),
        "operators": ", ".join(sorted(operators)),
        "avg_run_ft": round(avg_run, 0),
        "min_run_ft": round(min_run, 0),
        "max_run_ft": round(max_run, 0),
        "total_ft": round(total_ft, 0),
        "runs_with_agitator": agitator_count,
        "runs_with_rss": rss_count,
        "bit_manufacturers": ", ".join(sorted(bit_mfgs)),
        "bit_models_seen": ", ".join(sorted(bit_models)),
        "motor_models_seen": ", ".join(sorted(motor_models)[:5]),
        "avg_start_depth": round(sum(start_depths) / len(start_depths), 0) if start_depths else "N/A",
        "avg_end_depth": round(sum(end_depths) / len(end_depths), 0) if end_depths else "N/A",
    }


def main():
    export_csv_flag = "--export-csv" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--export-csv"]
    if len(args) < 1:
        print("Usage: python group_equivalent_bhas.py <bha_csv> [--export-csv]")
        sys.exit(1)

    csv_path = args[0]
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(SCRIPT_DIR, csv_path)

    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found")
        sys.exit(1)

    # Load rows
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)

    print(f"\n{'=' * 100}")
    print(f"  EQUIVALENT BHA GROUPING")
    print(f"  Input: {os.path.basename(csv_path)} ({len(rows)} BHA runs)")
    print(f"{'=' * 100}\n")

    # Group
    groups = group_bhas(rows)
    summaries = []
    for key, runs in groups.items():
        summaries.append(summarize_group(key, runs))

    # Sort by run count descending
    summaries.sort(key=lambda s: -s["num_runs"])

    # Print summary table
    print(f"  {'#':<4} {'Equivalent BHA':<28} {'Runs':<6} {'Wells':<7} "
          f"{'Avg Ft':<9} {'Min Ft':<9} {'Max Ft':<9} {'Total Ft':<10} "
          f"{'Operators'}")
    print(f"  {'-' * 98}")

    for i, s in enumerate(summaries, 1):
        print(f"  {i:<4} {s['group_key']:<28} {s['num_runs']:<6} {s['num_wells']:<7} "
              f"{s['avg_run_ft']:<9} {s['min_run_ft']:<9} {s['max_run_ft']:<9} "
              f"{s['total_ft']:<10} {s['operators'][:40]}")

    # Detailed breakdown per group
    print(f"\n{'=' * 100}")
    print(f"  DETAILED GROUP BREAKDOWN")
    print(f"{'=' * 100}")

    for i, s in enumerate(summaries, 1):
        key = s["group_key"]
        runs = groups[key]

        print(f"\n  --- Group {i}: {key} ({s['num_runs']} runs, {s['num_wells']} wells) ---")
        print(f"  Bit manufacturers: {s['bit_manufacturers']}")
        print(f"  Bit models:        {s['bit_models_seen']}")
        print(f"  Motor models:      {s['motor_models_seen']}")
        print(f"  Avg depth range:   {s['avg_start_depth']} - {s['avg_end_depth']} ft")
        print(f"  Run lengths:       avg={s['avg_run_ft']} ft, min={s['min_run_ft']}, max={s['max_run_ft']}")
        print()

        # Individual runs table
        hdr = (f"    {'Well Name':<28} {'Operator':<16} {'BHA#':<5} "
               f"{'Start':<10} {'End':<10} {'RunLen':<9} "
               f"{'Bit Model':<18} {'Motor':<20}")
        print(hdr)
        print(f"    {'-' * (len(hdr) - 4)}")

        def safe_run_length(x):
            v = x.get("run_length", 0)
            try:
                return -float(v)
            except (ValueError, TypeError):
                return 0
        for r in sorted(runs, key=safe_run_length):
            name = str(r.get("well_name", ""))[:26]
            op = str(r.get("operator", ""))[:14]
            bm = str(r.get("bit_model", ""))[:16]
            mm = str(r.get("motor_model", ""))[:18]
            print(f"    {name:<28} {op:<16} {str(r.get('bha_number','')):<5} "
                  f"{str(r.get('start_depth','')):<10} {str(r.get('end_depth','')):<10} "
                  f"{str(r.get('run_length','')):<9} {bm:<18} {mm:<20}")

    # Save group summaries to CSV
    input_basename = os.path.splitext(os.path.basename(csv_path))[0]
    out_path = os.path.join(SCRIPT_DIR, f"equiv_bha_groups_{input_basename}.csv")
    fieldnames = list(summaries[0].keys())
    try:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(summaries)
        print(f"\n  Group summaries saved to: {out_path}")
    except PermissionError:
        print(f"\n  WARNING: Could not save to {out_path} (file locked)")

    # DB save: get latest run, save groups, update equiv_bha_key on BHA runs
    run = db.get_latest_run()
    if run:
        run_id = run["id"]
        # Extract section_name from filename (e.g. "bhas_Production_Vertical_8.75in.csv" -> "Production_Vertical")
        for prefix in ("lateral_bhas_", "bhas_"):
            if input_basename.startswith(prefix):
                section_name = input_basename[len(prefix):]
                break
        else:
            section_name = input_basename
        section_name = re.sub(r"_\d+\.?\d*in$", "", section_name)

        db.save_equiv_bha_groups(run_id, section_name, summaries)

        updates = []
        for key, runs in groups.items():
            for r in runs:
                asset_id = r.get("asset_id", "")
                bha_number = r.get("bha_number", "")
                if asset_id:
                    updates.append((asset_id, str(bha_number), key))
        if updates:
            db.update_bha_equiv_keys(run_id, updates)

    if export_csv_flag:
        db.export_csv(summaries, "equiv_bha_groups")


if __name__ == "__main__":
    main()
