"""Pull BHAs for offset wells, filtered by section type or unfiltered.

Reads an offset wells CSV, queries corva#data.drillstring for each well,
filters to runs in the target section type, and extracts bit + motor details.

Supports section types: lateral (default), intermediate, vertical, surface, curve.
Use --all-runs to skip section filtering and pull every BHA run.

Usage:
    python pull_lateral_bhas.py [wells_csv]                         # lateral (default)
    python pull_lateral_bhas.py [wells_csv] --section-type intermediate
    python pull_lateral_bhas.py [wells_csv] --all-runs              # no section filter
    python pull_lateral_bhas.py [wells_csv] --export-csv            # also export to exports/
"""
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

import requests

import db

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Patterns used to match section names from corva#data.well-sections.
# Each section type maps to a list of substrings (case-insensitive).
SECTION_TYPE_PATTERNS = {
    "lateral": ["lateral"],
    "intermediate": ["intermediate", "int "],
    "vertical": ["vertical", "vert "],
    "surface": ["surface", "surf "],
    "curve": ["curve"],
}


def section_name_matches(section_name, section_type):
    """Check if a well-section name matches the target section type."""
    name_lower = (section_name or "").lower()
    patterns = SECTION_TYPE_PATTERNS.get(section_type, [section_type])
    return any(p in name_lower for p in patterns)


def epoch_to_date(epoch):
    if not epoch:
        return "N/A"
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return "N/A"


def sanitize(text):
    if not isinstance(text, str):
        return str(text) if text is not None else "N/A"
    return text.encode("ascii", errors="replace").decode("ascii")


def load_offset_wells(csv_path):
    """Load offset wells from CSV."""
    wells = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            wells.append(row)
    return wells


def fetch_drillstrings(asset_id):
    """Fetch ALL drillstring records for an asset."""
    all_records = []
    skip = 0
    batch = 100
    while True:
        r = requests.get(
            f"{DATA_API}/api/v1/data/corva/data.drillstring/",
            headers=HEADERS,
            params={
                "limit": batch,
                "skip": skip,
                "sort": json.dumps({"timestamp": 1}),
                "query": json.dumps({"asset_id": int(asset_id)}),
            },
            timeout=30,
        )
        if r.status_code != 200:
            break
        records = r.json()
        if not records:
            break
        all_records.extend(records)
        if len(records) < batch:
            break
        skip += batch
    return all_records


def fetch_well_sections(asset_id):
    """Fetch well sections to identify lateral intervals."""
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/data.well-sections/",
        headers=HEADERS,
        params={
            "limit": 20,
            "sort": json.dumps({"timestamp": 1}),
            "query": json.dumps({"asset_id": int(asset_id)}),
        },
        timeout=30,
    )
    if r.status_code == 200:
        return r.json()
    return []


def extract_bit_info(components):
    """Extract bit details from BHA components."""
    bits = [c for c in components if c.get("family") == "bit"]
    if not bits:
        return {}
    bit = bits[0]
    # Try to extract model info from the name field
    return {
        "bit_size": bit.get("size", bit.get("outer_diameter", "N/A")),
        "bit_type": bit.get("bit_type", "N/A"),
        "bit_name": sanitize(bit.get("name", "N/A")),
        "bit_manufacturer": sanitize(bit.get("manufacturer", bit.get("make", "N/A"))),
        "bit_model": sanitize(bit.get("model", "N/A")),
        "bit_serial": sanitize(bit.get("serial_number", bit.get("serial", "N/A"))),
        "bit_tfa": bit.get("tfa", "N/A"),
        "bit_nozzles": sanitize(str(bit.get("nozzles", bit.get("nozzle_sizes", "N/A")))),
        "bit_blade_count": bit.get("blade_count", "N/A"),
        "bit_cutter_size": bit.get("cutter_size", "N/A"),
    }


def extract_motor_info(components):
    """Extract motor (PDM) details from BHA components."""
    motors = [c for c in components if c.get("family") == "pdm"]
    if not motors:
        return {}
    motor = motors[0]
    return {
        "motor_name": sanitize(motor.get("name", "N/A")),
        "motor_manufacturer": sanitize(motor.get("manufacturer", motor.get("make", "N/A"))),
        "motor_model": sanitize(motor.get("model", "N/A")),
        "motor_od": motor.get("outer_diameter", "N/A"),
        "motor_length": motor.get("length", "N/A"),
        "motor_rpg": motor.get("rpg", motor.get("rev_per_gal", "N/A")),
        "motor_max_diff": motor.get("max_differential_pressure", motor.get("max_diff", "N/A")),
        "motor_bend": motor.get("bend_angle", motor.get("bend", "N/A")),
        "motor_stages": motor.get("stages", "N/A"),
        "motor_lobes": motor.get("lobes", motor.get("lobe_ratio", "N/A")),
    }


def detect_rss(components):
    """Detect if BHA contains a Rotary Steerable System."""
    for c in components:
        family = (c.get("family") or "").lower()
        if family == "rss":
            return True
        name = (c.get("name") or "").lower()
        model = (c.get("model") or "").lower()
        for text in (name, model):
            if "rotary steerable" in text or "rss" in text.split():
                return True
    return False


def detect_agitator(components):
    """Detect if BHA contains an agitator / friction reduction tool."""
    for c in components:
        family = (c.get("family") or "").lower()
        if family == "agitator":
            return True
        name = (c.get("name") or "").lower()
        model = (c.get("model") or "").lower()
        for text in (name, model):
            if "agitator" in text:
                return True
    return False


def get_section_start_depth(sections, section_type):
    """Get the shallowest top depth among matching sections."""
    tops = []
    for section in sections:
        sec_data = section.get("data", {})
        sec_name = sec_data.get("name") or ""
        if not section_name_matches(sec_name, section_type):
            continue
        top = sec_data.get("top_depth")
        if top is not None:
            tops.append(float(top))
    return min(tops) if tops else None


def get_lateral_start_depth(lateral_sections):
    """Get the shallowest lateral section top depth (backward compat)."""
    return get_section_start_depth(lateral_sections, "lateral")


def is_section_bha(drillstring_record, sections, section_type):
    """Determine if a BHA run overlaps with a target section type.

    Checks if the BHA's depth range overlaps with any section matching
    the given section_type.
    """
    data = drillstring_record.get("data", {})
    start_depth = data.get("start_depth")
    end_depth = data.get("end_depth")

    if start_depth is None and end_depth is None:
        return False

    for section in sections:
        sec_data = section.get("data", {})
        sec_name = sec_data.get("name") or ""
        if not section_name_matches(sec_name, section_type):
            continue

        sec_top = sec_data.get("top_depth", 0)
        sec_bottom = sec_data.get("bottom_depth", float("inf"))

        # BHA overlaps if its depth range intersects the section range
        if end_depth is not None and end_depth > sec_top:
            if start_depth is not None and start_depth < sec_bottom:
                return True
            elif start_depth is None:
                return True
        if start_depth is not None and start_depth >= sec_top and start_depth < sec_bottom:
            return True

    return False


def is_lateral_bha(drillstring_record, lateral_sections):
    """Backward-compatible wrapper for lateral filtering."""
    return is_section_bha(drillstring_record, lateral_sections, "lateral")


def process_well(well_row, section_type="lateral", all_runs=False):
    """Process a single well: fetch drillstrings, filter to target section, extract components.

    If all_runs=True, skips section filtering and returns every BHA run.
    """
    asset_id = well_row["asset_id"]
    well_name = well_row.get("well_name", "N/A")

    # Fetch drillstrings and sections
    drillstrings = fetch_drillstrings(asset_id)
    sections = fetch_well_sections(asset_id)

    if all_runs:
        target_sections = []
        section_start = None
    else:
        # Find matching sections for the target type
        target_sections = [
            s for s in sections
            if section_name_matches(s.get("data", {}).get("name") or "", section_type)
        ]
        section_start = get_section_start_depth(sections, section_type)

    # For lateral mode, also compute lateral_start_depth
    lateral_start = None
    if section_type == "lateral" and not all_runs:
        lateral_start = section_start

    results = []
    for ds in drillstrings:
        data = ds.get("data", {})
        components = data.get("components", [])

        # Check if this BHA has a bit (it's a drilling BHA)
        has_bit = any(c.get("family") == "bit" for c in components)
        if not has_bit:
            continue

        # Check if BHA overlaps the target section (skip in all_runs mode)
        if not all_runs and target_sections and not is_section_bha(ds, target_sections, section_type):
            continue

        start_depth = data.get("start_depth", "N/A")
        end_depth = data.get("end_depth", "N/A")
        run_length = "N/A"
        if isinstance(start_depth, (int, float)) and isinstance(end_depth, (int, float)):
            run_length = round(end_depth - start_depth, 1)

        bit_info = extract_bit_info(components)
        motor_info = extract_motor_info(components)

        is_rss = detect_rss(components)
        has_agitator = detect_agitator(components)

        bha_id = data.get("id", "N/A")
        setting_ts = data.get("setting_timestamp")

        result = {
            "asset_id": asset_id,
            "well_name": sanitize(well_name),
            "operator": well_row.get("operator", "N/A"),
            "distance_miles": well_row.get("distance_miles", "N/A"),
            "section_type": section_type,
            "bha_number": bha_id,
            "start_depth": start_depth,
            "end_depth": end_depth,
            "run_length": run_length,
            "section_start_depth": section_start if section_start is not None else "N/A",
            "lateral_start_depth": lateral_start if lateral_start is not None else "N/A",
            "set_date": epoch_to_date(setting_ts),
            "num_components": len(components),
            "is_rss": is_rss,
            "has_agitator": has_agitator,
            **bit_info,
            **motor_info,
        }
        results.append(result)

    return results


def main():
    # Parse arguments
    csv_path = None
    section_type = "lateral"
    all_runs = False
    run_id_override = None
    export_csv_flag = "--export-csv" in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a != "--export-csv"]
    i = 0
    while i < len(args):
        if args[i] == "--section-type" and i + 1 < len(args):
            section_type = args[i + 1].lower()
            i += 2
        elif args[i] == "--run-id" and i + 1 < len(args):
            run_id_override = int(args[i + 1])
            i += 2
        elif args[i] == "--all-runs":
            all_runs = True
            i += 1
        elif not args[i].startswith("--"):
            csv_path = args[i]
            i += 1
        else:
            i += 1

    if csv_path is None:
        csv_path = os.path.join(SCRIPT_DIR, "offset_wells_15mi.csv")
    elif not os.path.isabs(csv_path):
        csv_path = os.path.join(SCRIPT_DIR, csv_path)

    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found")
        sys.exit(1)

    if not all_runs and section_type not in SECTION_TYPE_PATTERNS:
        print(f"WARNING: Unknown section type '{section_type}'. "
              f"Known types: {', '.join(SECTION_TYPE_PATTERNS.keys())}. "
              f"Will match '{section_type}' as a substring.")

    if all_runs:
        section_label = "ALL RUNS"
    else:
        section_label = section_type.upper()

    wells = load_offset_wells(csv_path)
    print(f"\n{'=' * 70}")
    print(f"  {section_label} BHA EXTRACTION")
    if all_runs:
        print(f"  Mode: ALL RUNS (no section filtering)")
    else:
        print(f"  Section type: {section_type}")
    print(f"  Wells to process: {len(wells)}")
    print(f"{'=' * 70}\n")

    # Process all wells
    print(f"Processing {len(wells)} wells...")
    all_bhas = []
    t0 = time.time()

    for idx, well in enumerate(wells):
        bhas = process_well(well, section_type=section_type, all_runs=all_runs)
        all_bhas.extend(bhas)
        if (idx + 1) % 10 == 0 or idx == len(wells) - 1:
            label = "all" if all_runs else section_type
            print(f"  {idx + 1}/{len(wells)} wells processed, "
                  f"{len(all_bhas)} {label} BHAs found")

    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s")

    # Print summary
    print(f"\n{'=' * 70}")
    print(f"  RESULTS: {len(all_bhas)} {section_type} BHAs from {len(wells)} wells")
    print(f"{'=' * 70}\n")

    if not all_bhas:
        print(f"No {section_type} BHAs found.")
        return

    # Print table
    header = (
        f"{'Asset ID':<12} {'Well Name':<26} {'Operator':<18} {'BHA#':<5} "
        f"{'Start':<10} {'End':<10} {'RunLen':<8} "
        f"{'Bit Size':<9} {'Bit Type':<10} {'Bit Model':<20} "
        f"{'Mtr OD':<7} {'RPG':<8} {'MaxDiff':<8} {'Bend':<6}"
    )
    print(header)
    print("-" * len(header))
    for b in all_bhas:
        name = str(b.get("well_name", ""))[:24]
        operator = str(b.get("operator", ""))[:16]
        bit_model = str(b.get("bit_model", b.get("bit_name", "")))[:18]
        print(
            f"{b['asset_id']:<12} {name:<26} {operator:<18} {str(b.get('bha_number', '')):<5} "
            f"{str(b.get('start_depth', '')):<10} {str(b.get('end_depth', '')):<10} "
            f"{str(b.get('run_length', '')):<8} "
            f"{str(b.get('bit_size', '')):<9} {str(b.get('bit_type', '')):<10} "
            f"{bit_model:<20} "
            f"{str(b.get('motor_od', '')):<7} {str(b.get('motor_rpg', '')):<8} "
            f"{str(b.get('motor_max_diff', '')):<8} {str(b.get('motor_bend', '')):<6}"
        )

    # Save to CSV -- derive name from input file and section type
    input_basename = os.path.splitext(os.path.basename(csv_path))[0]
    if all_runs:
        out_name = f"all_bhas_{input_basename}.csv"
    else:
        out_name = f"{section_type}_bhas_{input_basename}.csv"
    out_path = os.path.join(SCRIPT_DIR, out_name)
    fieldnames = list(all_bhas[0].keys())
    try:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_bhas)
        print(f"\nSaved to: {out_path}")
    except PermissionError:
        backup = out_path.replace(".csv", f"_{int(time.time())}.csv")
        with open(backup, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_bhas)
        print(f"\nWARNING: File locked. Saved to: {backup}")

    # Save to database
    output_basename = os.path.splitext(out_name)[0]
    try:
        target_run_id = run_id_override
        if target_run_id is None:
            latest = db.get_latest_run()
            target_run_id = latest["id"] if latest else None
        if target_run_id is not None:
            db.save_bha_runs(target_run_id, all_bhas)
    except Exception as e:
        print(f"  DB save warning: {e}")

    if export_csv_flag:
        db.export_csv(all_bhas, output_basename)


if __name__ == "__main__":
    main()
