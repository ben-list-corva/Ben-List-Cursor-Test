"""Analyze a target well's planned sections from Corva.

Fetches corva#data.well-sections for the target well, maps each section
to canonical formations, and outputs target_sections.json for driving
the per-section BHA analysis pipeline.

Usage:
    python analyze_target_well.py --asset 82512872
    python analyze_target_well.py --asset 82512872 --formations formation_tops_canonical.csv
"""

import argparse
import csv
import json
import os
import sys
import requests
from dotenv import load_dotenv

import db

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_well_sections(asset_id):
    """Fetch well sections from Corva."""
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/data.well-sections/",
        headers=HEADERS,
        params={
            "limit": 20,
            "sort": json.dumps({"data.top_depth": 1}),
            "query": json.dumps({"asset_id": int(asset_id)}),
        },
        timeout=30,
    )
    if r.status_code == 200:
        return r.json()
    print(f"  WARNING: Failed to fetch well-sections (HTTP {r.status_code})")
    return []


def fetch_well_name(asset_id):
    """Fetch well name from Corva APIs.

    Tries v2/assets first, falls back to well_cache if name is null.
    """
    # Try v2 assets API
    try:
        r = requests.get(
            f"https://api.corva.ai/v2/assets/{asset_id}",
            headers=HEADERS,
            timeout=15,
        )
        if r.status_code == 200:
            name = r.json().get("name")
            if name:
                return name
    except Exception:
        pass

    # Fall back to well_cache (more reliable for well names)
    try:
        r = requests.get(
            f"{DATA_API}/api/v1/data/corva/well_cache/",
            headers=HEADERS,
            params={
                "limit": 1,
                "sort": json.dumps({"timestamp": -1}),
                "query": json.dumps({"asset_id": int(asset_id)}),
                "fields": "asset",
            },
            timeout=15,
        )
        if r.status_code == 200:
            data = r.json()
            if data:
                name = data[0].get("asset", {}).get("name")
                if name:
                    return name
    except Exception:
        pass

    return f"Asset {asset_id}"


def load_formation_tops(csv_path, asset_id):
    """Load formation tops for a specific well from the canonical CSV."""
    tops = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["asset_id"].strip() == str(asset_id):
                tops.append({
                    "formation_name": row["formation_name"].strip(),
                    "md_top": float(row["md_top"]),
                    "tvd_top": float(row["tvd_top"]),
                    "md_thickness": (float(row["md_thickness"])
                                     if row.get("md_thickness") else None),
                    "tvd_thickness": (float(row["tvd_thickness"])
                                      if row.get("tvd_thickness") else None),
                })
    tops.sort(key=lambda x: x["md_top"])
    return tops


def detect_mode(section_name):
    """Auto-detect vertical vs lateral from section name."""
    name_lower = (section_name or "").lower()
    if "lateral" in name_lower:
        return "lateral"
    return "vertical"


def map_section_to_formations(section, formation_tops):
    """Map a section's MD range to canonical formations.

    Returns list of formation names within the section, plus start/end
    formation details.
    """
    top_md = section["top_md"]
    bottom_md = section["bottom_md"]

    formations_in = []
    for i, ft in enumerate(formation_tops):
        fm_md = ft["md_top"]
        # Formation top is within section, or section starts within formation
        fm_bottom_md = (formation_tops[i + 1]["md_top"]
                        if i + 1 < len(formation_tops)
                        else fm_md + (ft["md_thickness"] or 1000))

        # Check overlap: formation interval overlaps section interval
        if fm_bottom_md > top_md and fm_md < bottom_md:
            formations_in.append(ft)

    if not formations_in:
        return {
            "formations_in_section": [],
            "start_formation": None,
            "end_formation": None,
            "top_tvd": None,
            "bottom_tvd": None,
        }

    return {
        "formations_in_section": [f["formation_name"] for f in formations_in],
        "start_formation": formations_in[0]["formation_name"],
        "end_formation": formations_in[-1]["formation_name"],
        "top_tvd": formations_in[0]["tvd_top"],
        "bottom_tvd": (formations_in[-1]["tvd_top"]
                       + (formations_in[-1]["tvd_thickness"] or 500)),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze target well's planned sections.")
    parser.add_argument("--asset", required=True,
                        help="Target well asset ID")
    parser.add_argument("--formations", default=None,
                        help="Path to formation_tops_canonical.csv")
    parser.add_argument("--output", default=None,
                        help="Output JSON path (default: target_sections.json)")
    parser.add_argument("--export-csv", action="store_true",
                        help="Export sections to CSV via db.export_csv")
    args = parser.parse_args()

    asset_id = args.asset
    fm_path = args.formations
    if fm_path and not os.path.isabs(fm_path):
        fm_path = os.path.join(SCRIPT_DIR, fm_path)

    # Try default formation paths
    if fm_path is None:
        for candidate in ["formation_tops_canonical.csv", "formation_tops.csv"]:
            p = os.path.join(SCRIPT_DIR, candidate)
            if os.path.exists(p):
                fm_path = p
                break

    out_path = args.output or os.path.join(SCRIPT_DIR, "target_sections.json")
    if not os.path.isabs(out_path):
        out_path = os.path.join(SCRIPT_DIR, out_path)

    print(f"\n{'=' * 70}")
    print(f"  ANALYZE TARGET WELL SECTIONS")
    print(f"  Target asset: {asset_id}")
    print(f"{'=' * 70}\n")

    # Fetch well name
    well_name = fetch_well_name(asset_id)
    print(f"  Well name: {well_name}")

    # Fetch sections
    raw_sections = fetch_well_sections(asset_id)
    if not raw_sections:
        print("  ERROR: No sections found for this well.")
        sys.exit(1)

    print(f"  Found {len(raw_sections)} sections")

    # Load formation tops if available
    formation_tops = []
    if fm_path and os.path.exists(fm_path):
        formation_tops = load_formation_tops(fm_path, asset_id)
        print(f"  Loaded {len(formation_tops)} formation tops from "
              f"{os.path.basename(fm_path)}")
    elif db.formation_tops_exist(str(args.asset)):
        db_tops = db.get_formation_tops(str(args.asset))
        formation_tops = [
            {
                "formation_name": t["formation_name"],
                "md_top": t["md_top"],
                "tvd_top": t["tvd_top"],
                "md_thickness": t["md_thickness"],
                "tvd_thickness": t["tvd_thickness"],
            }
            for t in db_tops
        ]
        print(f"  Loaded {len(formation_tops)} formation tops from DB")
    else:
        print("  WARNING: No formation tops file found. "
              "Formation mapping will be skipped.")

    # Process sections
    sections = []
    print(f"\n  {'Section':<30} {'Hole':>6} {'Mode':<10} "
          f"{'MD Range':<20} {'Formations'}")
    print(f"  {'-' * 90}")

    for raw in raw_sections:
        d = raw.get("data", {})
        name = d.get("name", "Unknown")
        diameter = d.get("diameter", None)
        top_md = d.get("top_depth", 0)
        bottom_md = d.get("bottom_depth", 0)
        mode = detect_mode(name)

        section = {
            "name": name,
            "hole_size": float(diameter) if diameter else None,
            "mode": mode,
            "top_md": float(top_md),
            "bottom_md": float(bottom_md),
            "section_length_md": round(float(bottom_md) - float(top_md), 1),
        }

        # Map to formations
        if formation_tops:
            fm_info = map_section_to_formations(section, formation_tops)
            section.update(fm_info)
        else:
            section["formations_in_section"] = []
            section["start_formation"] = None
            section["end_formation"] = None
            section["top_tvd"] = None
            section["bottom_tvd"] = None

        sections.append(section)

        fm_list = ", ".join(section["formations_in_section"][:4])
        if len(section["formations_in_section"]) > 4:
            fm_list += f" (+{len(section['formations_in_section']) - 4})"
        hs = f"{section['hole_size']}\"" if section["hole_size"] else "?"
        print(f"  {name:<30} {hs:>6} {mode:<10} "
              f"MD {top_md}-{bottom_md:<11} {fm_list or 'N/A'}")

    # Build output
    output = {
        "target_asset_id": str(asset_id),
        "target_well_name": well_name,
        "formations_file": os.path.basename(fm_path) if fm_path else None,
        "sections": sections,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved to: {out_path}")

    try:
        latest = db.get_latest_run()
        if latest:
            db.save_target_sections(latest["id"], sections)
    except Exception as e:
        print(f"  DB save warning: {e}")

    if args.export_csv:
        db.export_csv(sections, "target_sections")

    print(f"\n  Next steps:")
    print(f"    1. Review sections above; toggle mode if needed")
    print(f"    2. python pull_lateral_bhas.py offset_wells_15mi.csv --all-runs")
    print(f"    3. python filter_bhas_by_section.py target_sections.json "
          f"all_bhas_offset_wells.csv")


if __name__ == "__main__":
    main()
