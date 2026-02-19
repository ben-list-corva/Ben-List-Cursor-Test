"""Pull formation tops for offset wells from Corva.

Fetches corva#data.formations for each well, sorts by measured depth,
computes formation thicknesses, and outputs a CSV with one row per
formation per well.

This data is used by pull_1ft_for_runs.py (--mode vertical) to map
each drilled foot to a formation position (% through the formation).

Usage:
    python pull_formation_tops.py [wells_csv_or_bha_csv]
"""
import csv
import json
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

import requests

import db

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_formations(asset_id, max_retries=3):
    """Fetch formation tops for a single well from corva#data.formations."""
    all_records = []
    skip = 0
    batch = 100

    query = {"asset_id": int(asset_id)}

    for attempt in range(max_retries):
        try:
            r = requests.get(
                f"{DATA_API}/api/v1/data/corva/data.formations/",
                headers=HEADERS,
                params={
                    "limit": batch,
                    "skip": skip,
                    "sort": json.dumps({"data.md": 1}),
                    "query": json.dumps(query),
                    "fields": "data.formation_name,data.md,data.td,data.lithology",
                },
                timeout=30,
            )
            if r.status_code == 200:
                records = r.json()
                all_records.extend(records)
                # Paginate if full batch
                while len(records) == batch:
                    skip += batch
                    r = requests.get(
                        f"{DATA_API}/api/v1/data/corva/data.formations/",
                        headers=HEADERS,
                        params={
                            "limit": batch,
                            "skip": skip,
                            "sort": json.dumps({"data.md": 1}),
                            "query": json.dumps(query),
                            "fields": "data.formation_name,data.md,data.td,data.lithology",
                        },
                        timeout=30,
                    )
                    if r.status_code != 200:
                        break
                    records = r.json()
                    all_records.extend(records)
                break
            if r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            break
        except requests.exceptions.RequestException:
            time.sleep(2 ** attempt)

    return all_records


def parse_formation_tops(records):
    """Parse formation records into a sorted list of formation tops.

    Returns list of dicts with: formation_name, md_top, tvd_top, lithology
    sorted by md_top ascending.
    """
    tops = []
    for rec in records:
        data = rec.get("data", {})
        name = data.get("formation_name", "")
        md = data.get("md")
        td = data.get("td")

        if not name or md is None:
            continue

        tops.append({
            "formation_name": name.strip(),
            "md_top": float(md),
            "tvd_top": float(td) if td is not None else float(md),
            "lithology": data.get("lithology", ""),
        })

    # Sort by measured depth
    tops.sort(key=lambda x: x["md_top"])

    # Deduplicate: if same formation appears at same depth, keep first
    seen = set()
    unique = []
    for t in tops:
        key = (t["formation_name"], round(t["md_top"]))
        if key not in seen:
            seen.add(key)
            unique.append(t)

    return unique


def compute_thicknesses(tops, section_end_md=None):
    """Compute formation thicknesses (MD-based and TVD-based).

    Each formation's thickness is the distance to the next formation top.
    The last formation extends to section_end_md if provided.
    """
    for i, top in enumerate(tops):
        if i + 1 < len(tops):
            top["md_thickness"] = round(tops[i + 1]["md_top"] - top["md_top"], 1)
            top["tvd_thickness"] = round(tops[i + 1]["tvd_top"] - top["tvd_top"], 1)
        elif section_end_md is not None:
            top["md_thickness"] = round(section_end_md - top["md_top"], 1)
            top["tvd_thickness"] = top["md_thickness"]  # approximate
        else:
            top["md_thickness"] = None
            top["tvd_thickness"] = None

    return tops


def process_well(asset_id, well_name=""):
    """Fetch and parse formation tops for a single well."""
    records = fetch_formations(asset_id)
    if not records:
        return []

    tops = parse_formation_tops(records)
    tops = compute_thicknesses(tops)

    # Add well metadata
    for t in tops:
        t["asset_id"] = asset_id
        t["well_name"] = well_name

    return tops


def load_wells_from_csv(csv_path):
    """Load unique (asset_id, well_name) pairs from any CSV with those columns."""
    wells = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            aid = row.get("asset_id", "").strip()
            name = row.get("well_name", "").strip()
            if aid and aid not in wells:
                wells[aid] = name
    return wells


def main():
    export_csv_flag = "--export-csv" in sys.argv
    sys.argv = [a for a in sys.argv if a != "--export-csv"]

    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
        if not os.path.isabs(csv_path):
            csv_path = os.path.join(SCRIPT_DIR, csv_path)
    else:
        csv_path = os.path.join(SCRIPT_DIR, "offset_wells_15mi.csv")

    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found")
        sys.exit(1)

    wells = load_wells_from_csv(csv_path)
    print(f"\n{'=' * 70}")
    print(f"  PULL FORMATION TOPS")
    print(f"  Input: {os.path.basename(csv_path)}")
    print(f"  Unique wells: {len(wells)}")
    print(f"{'=' * 70}\n")

    all_tops = []
    t0 = time.time()
    completed = 0
    wells_with_data = 0

    max_workers = 10
    print(f"  Fetching formation data with {max_workers} parallel workers...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for aid, wname in wells.items():
            future = executor.submit(process_well, aid, wname)
            futures[future] = (aid, wname)

        for future in as_completed(futures):
            aid, wname = futures[future]
            try:
                tops = future.result()
                if tops:
                    all_tops.extend(tops)
                    wells_with_data += 1
            except Exception as e:
                print(f"  ERROR on {wname} ({aid}): {e}")

            completed += 1
            if completed % 10 == 0 or completed == len(wells):
                elapsed = time.time() - t0
                print(f"  {completed}/{len(wells)} wells processed, "
                      f"{len(all_tops)} formation tops, {elapsed:.0f}s")

    elapsed = time.time() - t0
    print(f"\n  Done: {len(all_tops)} formation tops from "
          f"{wells_with_data}/{len(wells)} wells in {elapsed:.1f}s")

    # Summary: most common formations
    fm_counts = defaultdict(int)
    for t in all_tops:
        fm_counts[t["formation_name"]] += 1
    print(f"\n  Top formations by occurrence:")
    for fm, cnt in sorted(fm_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"    {fm:<30} {cnt:>4} wells")

    wells_missing = len(wells) - wells_with_data
    if wells_missing > 0:
        print(f"\n  WARNING: {wells_missing} wells had no formation data")

    # Save
    if not all_tops:
        print("\nNo formation data retrieved.")
        return

    out_path = os.path.join(SCRIPT_DIR, "formation_tops.csv")
    fieldnames = [
        "asset_id", "well_name", "formation_name", "md_top", "tvd_top",
        "md_thickness", "tvd_thickness", "lithology",
    ]
    try:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(all_tops)
        print(f"\n  Saved to: {out_path}")
    except PermissionError:
        backup = out_path.replace(".csv", f"_{int(time.time())}.csv")
        with open(backup, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(all_tops)
        print(f"\n  WARNING: File locked. Saved to: {backup}")

    # Save to database
    db.save_formation_tops(all_tops)

    if export_csv_flag:
        db.export_csv(all_tops, "formation_tops")


if __name__ == "__main__":
    main()
