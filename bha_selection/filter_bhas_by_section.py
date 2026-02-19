"""Filter a master BHA CSV by hole size, depth overlap, basin, formation, and BHA type.

Reads target_sections.json and all_bhas_*.csv, produces one filtered CSV per
section (e.g., bhas_Intermediate_12.25in.csv).

Filters applied per-run:
1. Basin (optional) -- offset well must be in one of the allowed basins
2. Target formation (optional, lateral only) -- offset well's target_formation must match
3. Hole size -- with configurable tolerance (default exact, option for +/- 0.25")
4. BHA type -- RSS, Conventional, or Both
5. Depth range overlap

Formation coverage is NOT filtered here -- it is applied at the
equivalent-BHA-group level in build_rop_curves.py.

Usage:
    python filter_bhas_by_section.py target_sections.json all_bhas.csv
    python filter_bhas_by_section.py target_sections.json all_bhas.csv --bha-type rss
    python filter_bhas_by_section.py target_sections.json all_bhas.csv --hole-size-tolerance 0.25
"""

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter, defaultdict

import db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_formation_tops_by_asset(csv_path):
    """Load formation tops grouped by asset_id."""
    by_asset = defaultdict(list)
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            aid = row["asset_id"].strip()
            try:
                by_asset[aid].append({
                    "formation_name": row["formation_name"].strip(),
                    "md_top": float(row["md_top"]),
                    "tvd_top": float(row["tvd_top"]),
                    "md_thickness": (float(row["md_thickness"])
                                     if row.get("md_thickness") else None),
                    "tvd_thickness": (float(row["tvd_thickness"])
                                      if row.get("tvd_thickness") else None),
                })
            except (ValueError, KeyError):
                continue
    for aid in by_asset:
        by_asset[aid].sort(key=lambda x: x["md_top"])
    return dict(by_asset)


def compute_formation_coverage(bha_row, section, fm_tops_by_asset):
    """Compute what fraction of the section's formations the BHA run covers.

    Returns (coverage_fraction, formations_covered).
    """
    target_fms = set(section.get("formations_in_section", []))
    if not target_fms:
        return 1.0, []  # no formations to check → pass

    asset_id = str(bha_row.get("asset_id", "")).strip()
    well_tops = fm_tops_by_asset.get(asset_id, [])
    if not well_tops:
        return 0.0, []

    try:
        bha_start = float(bha_row.get("start_depth", 0) or 0)
        bha_end = float(bha_row.get("end_depth", 0) or 0)
    except (ValueError, TypeError):
        return 0.0, []

    if bha_end <= bha_start:
        return 0.0, []

    # Find which canonical formations this BHA run's MD range overlaps
    covered = set()
    for ft in well_tops:
        fm_md_top = ft["md_top"]
        fm_md_bottom = fm_md_top + (ft["md_thickness"] or 500)

        # Check overlap
        if fm_md_bottom > bha_start and fm_md_top < bha_end:
            covered.add(ft["formation_name"])

    overlap = covered & target_fms
    coverage = len(overlap) / len(target_fms) if target_fms else 1.0
    return coverage, sorted(overlap)


def _formation_matches_fuzzy(target_formation, candidate_formation):
    """Fuzzy-match formation names by stripping common prefixes."""
    if not target_formation or target_formation == "N/A":
        return True
    if not candidate_formation or candidate_formation == "N/A":
        return False
    prefixes = ["lower ", "upper ", "middle ", "base ", "top ", "main "]
    t = target_formation.lower()
    c = candidate_formation.lower()
    for p in prefixes:
        if t.startswith(p):
            t = t[len(p):]
        if c.startswith(p):
            c = c[len(p):]
    return t == c


def filter_for_section(all_bhas, section, fm_tops_by_asset,
                       basin_filter=None, target_formations=None,
                       hole_size_tolerance=0.0, bha_type="both"):
    """Filter BHA rows for a single target section.

    Filters: basin, target formation (lateral only), hole size (with
    tolerance), BHA type, depth overlap.  Formation coverage is NOT
    applied here -- it moves to the group level in build_rop_curves.py.

    Returns (filtered_rows, stats_dict).
    """
    hole_size = section.get("hole_size")
    top_md = section.get("top_md", 0)
    bottom_md = section.get("bottom_md", float("inf"))
    mode = section.get("mode", "vertical")
    tol = max(hole_size_tolerance, 0.1)

    passed = []
    stats = {
        "total": len(all_bhas),
        "basin_pass": 0,
        "formation_pass": 0,
        "hole_size_match": 0,
        "bha_type_match": 0,
        "depth_overlap": 0,
        "excluded_no_hole_size": 0,
    }

    basin_set = set(basin_filter) if basin_filter else None
    fm_set = set(target_formations) if target_formations else None

    for row in all_bhas:
        # Filter 1: basin
        if basin_set:
            well_basin = row.get("basin", "") or row.get("program", "") or ""
            if well_basin and well_basin != "N/A" and well_basin not in basin_set:
                continue
        stats["basin_pass"] += 1

        # Filter 2: target formation (lateral only)
        if mode == "lateral" and fm_set:
            well_fm = row.get("target_formation", "") or ""
            match = any(_formation_matches_fuzzy(f, well_fm) for f in fm_set)
            if not match:
                continue
        stats["formation_pass"] += 1

        # Filter 3: hole size (with tolerance)
        try:
            row_size = float(row.get("bit_size", 0) or 0)
        except (ValueError, TypeError):
            stats["excluded_no_hole_size"] += 1
            continue

        if hole_size is not None and abs(row_size - hole_size) > tol:
            continue
        stats["hole_size_match"] += 1

        # Filter 4: BHA type
        is_rss = str(row.get("is_rss", "")).strip().lower() in ("true", "1", "yes")
        if bha_type == "rss" and not is_rss:
            continue
        if bha_type == "conventional" and is_rss:
            continue
        stats["bha_type_match"] += 1

        # Filter 5: depth range overlap
        try:
            bha_start = float(row.get("start_depth", 0) or 0)
            bha_end = float(row.get("end_depth", 0) or 0)
        except (ValueError, TypeError):
            continue

        if bha_end <= top_md or bha_start >= bottom_md:
            continue
        stats["depth_overlap"] += 1

        row = dict(row)
        row["formation_coverage"] = ""
        row["formations_covered"] = ""
        passed.append(row)

    return passed, stats


def main():
    parser = argparse.ArgumentParser(
        description="Filter BHA runs by section.")
    parser.add_argument("sections_json",
                        help="Path to target_sections.json")
    parser.add_argument("bha_csv",
                        help="Path to all_bhas_*.csv (master BHA file)")
    parser.add_argument("--min-coverage", type=float, default=0.0,
                        help="(Deprecated) Per-run formation coverage. Default 0 (disabled).")
    parser.add_argument("--formations", default=None,
                        help="Path to formation_tops_canonical.csv")
    parser.add_argument("--export-csv", action="store_true",
                        help="Export each section's BHAs via db.export_csv")
    parser.add_argument("--run-id", type=int, default=None,
                        help="DB run ID to save filtered BHAs to")
    parser.add_argument("--basin-filter", default=None,
                        help="Comma-separated list of allowed basins")
    parser.add_argument("--target-formations", default=None,
                        help="Comma-separated list of allowed target formations (lateral only)")
    parser.add_argument("--hole-size-tolerance", type=float, default=0.0,
                        help="Hole size tolerance in inches (default 0 = exact, 0.25 = +/- 0.25\")")
    parser.add_argument("--bha-type", default="both",
                        choices=["rss", "conventional", "both"],
                        help="BHA type filter (default: both)")
    args = parser.parse_args()

    basin_filter = [b.strip() for b in args.basin_filter.split(",") if b.strip()] if args.basin_filter else None
    target_formations = [f.strip() for f in args.target_formations.split(",") if f.strip()] if args.target_formations else None

    sections_path = args.sections_json
    if not os.path.isabs(sections_path):
        sections_path = os.path.join(SCRIPT_DIR, sections_path)

    bha_path = args.bha_csv
    if not os.path.isabs(bha_path):
        bha_path = os.path.join(SCRIPT_DIR, bha_path)

    fm_path = args.formations
    if fm_path and not os.path.isabs(fm_path):
        fm_path = os.path.join(SCRIPT_DIR, fm_path)
    if fm_path is None:
        for candidate in ["formation_tops_canonical.csv", "formation_tops.csv"]:
            p = os.path.join(SCRIPT_DIR, candidate)
            if os.path.exists(p):
                fm_path = p
                break

    # Load data
    with open(sections_path, encoding="utf-8") as f:
        target = json.load(f)

    all_bhas = []
    with open(bha_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            all_bhas.append(row)

    fm_tops_by_asset = {}
    if fm_path and os.path.exists(fm_path):
        fm_tops_by_asset = load_formation_tops_by_asset(fm_path)
    elif not fm_path:
        # DB fallback when --formations CSV not provided
        try:
            asset_ids = {str(r.get("asset_id", "")).strip() for r in all_bhas if r.get("asset_id")}
            for aid in asset_ids:
                tops = db.get_formation_tops(aid)
                if tops:
                    fm_tops_by_asset[aid] = [
                        {
                            "formation_name": t.get("formation_name", ""),
                            "md_top": t.get("md_top"),
                            "tvd_top": t.get("tvd_top"),
                            "md_thickness": t.get("md_thickness"),
                            "tvd_thickness": t.get("tvd_thickness"),
                        }
                        for t in tops
                    ]
                    fm_tops_by_asset[aid].sort(key=lambda x: x["md_top"] or 0)
        except Exception as e:
            print(f"  DB formation tops fallback warning: {e}")

    print(f"\n{'=' * 70}")
    print(f"  FILTER BHAs BY SECTION")
    print(f"  Target well: {target.get('target_well_name', '?')}")
    print(f"  Total BHA runs: {len(all_bhas)}")
    print(f"  Hole size tolerance: +/- {args.hole_size_tolerance}\"")
    print(f"  BHA type: {args.bha_type}")
    if basin_filter:
        print(f"  Basin filter: {', '.join(basin_filter)}")
    if target_formations:
        print(f"  Target formations: {', '.join(target_formations)}")
    print(f"{'=' * 70}\n")

    sections = target.get("sections", [])
    output_files = []

    for section in sections:
        name = section["name"]
        hs = section.get("hole_size")
        mode = section.get("mode", "vertical")
        fms = section.get("formations_in_section", [])

        hs_str = f"{hs}in" if hs else "unknown"
        safe_name = name.replace(" ", "_").replace("/", "-")
        out_name = f"bhas_{safe_name}_{hs_str}.csv"
        out_path = os.path.join(SCRIPT_DIR, out_name)

        print(f"  Section: {name} ({hs_str}, {mode})")
        print(f"    Formations: {', '.join(fms) if fms else 'N/A'}")

        filtered, stats = filter_for_section(
            all_bhas, section, fm_tops_by_asset,
            basin_filter=basin_filter,
            target_formations=target_formations,
            hole_size_tolerance=args.hole_size_tolerance,
            bha_type=args.bha_type)

        print(f"    Basin pass:      {stats['basin_pass']}")
        print(f"    Formation pass:  {stats['formation_pass']}")
        print(f"    Hole size match: {stats['hole_size_match']}")
        print(f"    BHA type match:  {stats['bha_type_match']}")
        print(f"    Depth overlap:   {stats['depth_overlap']}")

        if not filtered:
            print(f"    WARNING: No BHA runs passed all filters.")
            continue

        # Save
        fieldnames = list(filtered[0].keys())
        try:
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(filtered)
            print(f"    Saved: {out_name} ({len(filtered)} runs)")
        except PermissionError:
            backup = out_path.replace(".csv", f"_{int(time.time())}.csv")
            with open(backup, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(filtered)
            print(f"    WARNING: File locked. Saved to: {os.path.basename(backup)}")
            out_path = backup

        # Save filtered BHAs to DB (append to correct run)
        try:
            target_run_id = args.run_id
            if target_run_id is None:
                latest = db.get_latest_run()
                target_run_id = latest["id"] if latest else None
            if target_run_id is not None:
                section_bhas = []
                for bha in filtered:
                    bha_copy = dict(bha)
                    bha_copy["section_name"] = safe_name
                    bha_copy["hole_size_filter"] = hs
                    section_bhas.append(bha_copy)
                # Prevent duplicate accumulation across repeated runs for
                # the same section within the same analysis run.
                with db.connection() as conn:
                    conn.execute(
                        "DELETE FROM bha_runs WHERE run_id = ? AND section_name = ?",
                        (target_run_id, safe_name),
                    )
                db.save_bha_runs(target_run_id, section_bhas, replace=False)
        except Exception as e:
            print(f"    DB save warning: {e}")

        if args.export_csv:
            try:
                db.export_csv(filtered, f"bhas_{safe_name}_{hs_str}", quiet=False)
            except Exception as e:
                print(f"    Export CSV warning: {e}")

        output_files.append({
            "section_name": name,
            "hole_size": hs,
            "mode": mode,
            "file": out_name,
            "runs": len(filtered),
            "formations": fms,
        })
        print()

    # Summary
    print(f"\n  {'=' * 60}")
    print(f"  SUMMARY")
    print(f"  {'=' * 60}")
    for of in output_files:
        hs = f"{of['hole_size']}\"" if of["hole_size"] else "?"
        print(f"  {of['section_name']:<30} {hs:>7}  {of['mode']:<10} "
              f"{of['runs']:>4} runs  -> {of['file']}")

    if not output_files:
        print("  No sections produced output files.")


if __name__ == "__main__":
    main()
