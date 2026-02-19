"""Pull BHAs filtered by bit size for offset wells.

Usage:
    python pull_bhas_by_size.py <offset_csv> <bit_sizes>

    bit_sizes: comma-separated bit sizes, e.g. "12.25,8.75"

Example:
    python pull_bhas_by_size.py offset_wells_15.0mi_20260213_175913.csv 12.25,8.75
"""
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

import requests

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


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


def extract_bit_info(components):
    bits = [c for c in components if c.get("family") == "bit"]
    if not bits:
        return {}
    bit = bits[0]
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
        "motor_max_diff": motor.get("max_differential_pressure",
                                     motor.get("max_operating_differential_pressure",
                                               motor.get("max_diff", "N/A"))),
        "motor_bend": motor.get("bend_angle", motor.get("bend_range", "N/A")),
        "motor_stages": motor.get("stages", "N/A"),
        "motor_lobes": motor.get("lobes", motor.get("lobe_ratio", "N/A")),
        "motor_rotor_lobes": motor.get("number_rotor_lobes", "N/A"),
        "motor_stator_lobes": motor.get("number_stator_lobes", "N/A"),
    }


def process_well(well_row, target_sizes):
    """Process a single well: fetch drillstrings, filter by bit size."""
    asset_id = well_row["asset_id"]
    well_name = well_row.get("well_name", "N/A")

    drillstrings = fetch_drillstrings(asset_id)

    results = []
    for ds in drillstrings:
        data = ds.get("data", {})
        components = data.get("components", [])

        # Must have a bit
        bits = [c for c in components if c.get("family") == "bit"]
        if not bits:
            continue

        # Check bit size against target sizes
        bit_size = bits[0].get("size", bits[0].get("outer_diameter"))
        if bit_size is None:
            continue

        try:
            bit_size_f = float(bit_size)
        except (ValueError, TypeError):
            continue

        # Match with tolerance (±0.01 to handle float rounding)
        if not any(abs(bit_size_f - ts) < 0.01 for ts in target_sizes):
            continue

        start_depth = data.get("start_depth", "N/A")
        end_depth = data.get("end_depth", "N/A")
        run_length = "N/A"
        if isinstance(start_depth, (int, float)) and isinstance(end_depth, (int, float)):
            run_length = round(end_depth - start_depth, 1)

        bit_info = extract_bit_info(components)
        motor_info = extract_motor_info(components)

        bha_id = data.get("id", "N/A")
        setting_ts = data.get("setting_timestamp")

        result = {
            "asset_id": asset_id,
            "well_name": sanitize(well_name),
            "operator": well_row.get("operator", "N/A"),
            "distance_miles": well_row.get("distance_miles", "N/A"),
            "bha_number": bha_id,
            "start_depth": start_depth,
            "end_depth": end_depth,
            "run_length": run_length,
            "set_date": epoch_to_date(setting_ts),
            "num_components": len(components),
            **bit_info,
            **motor_info,
        }
        results.append(result)

    return results


def main():
    if len(sys.argv) < 3:
        print("Usage: python pull_bhas_by_size.py <offset_csv> <bit_sizes>")
        print("  bit_sizes: comma-separated, e.g. 12.25,8.75")
        sys.exit(1)

    csv_path = sys.argv[1]
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(SCRIPT_DIR, csv_path)

    target_sizes = [float(s.strip()) for s in sys.argv[2].split(",")]
    size_label = "_".join(str(s) for s in target_sizes)

    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found")
        sys.exit(1)

    wells = load_offset_wells(csv_path)
    print(f"\n{'=' * 80}")
    print(f"  BHA EXTRACTION BY BIT SIZE")
    print(f"  Target bit sizes: {target_sizes}")
    print(f"  Wells to process: {len(wells)}")
    print(f"{'=' * 80}\n")

    all_bhas = []
    t0 = time.time()

    for i, well in enumerate(wells):
        bhas = process_well(well, target_sizes)
        all_bhas.extend(bhas)
        if (i + 1) % 10 == 0 or i == len(wells) - 1:
            print(f"  {i + 1}/{len(wells)} wells processed, {len(all_bhas)} BHAs found")

    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s")

    # Summary by bit size
    size_counts = {}
    for b in all_bhas:
        sz = b.get("bit_size", "?")
        size_counts[sz] = size_counts.get(sz, 0) + 1

    print(f"\n{'=' * 80}")
    print(f"  RESULTS: {len(all_bhas)} BHAs from {len(wells)} wells")
    for sz, cnt in sorted(size_counts.items(), key=lambda x: -x[1]):
        print(f"    {sz}\" bit: {cnt} runs")
    print(f"{'=' * 80}\n")

    if not all_bhas:
        print("No BHAs found matching target bit sizes.")
        return

    # Print table
    header = (
        f"{'Asset ID':<12} {'Well Name':<28} {'BHA#':<5} "
        f"{'Start':<10} {'End':<10} {'RunLen':<8} "
        f"{'BitSz':<7} {'Type':<5} {'Bit Mfg':<16} {'Bit Model':<20} "
        f"{'Mtr Mfg':<16} {'Mtr Model':<22} {'MtrOD':<6} {'RPG':<6}"
    )
    print(header)
    print("-" * len(header))
    for b in all_bhas:
        name = str(b.get("well_name", ""))[:26]
        bit_mfg = str(b.get("bit_manufacturer", ""))[:14]
        bit_model = str(b.get("bit_model", ""))[:18]
        mtr_mfg = str(b.get("motor_manufacturer", ""))[:14]
        mtr_model = str(b.get("motor_model", ""))[:20]
        print(
            f"{b['asset_id']:<12} {name:<28} {str(b.get('bha_number', '')):<5} "
            f"{str(b.get('start_depth', '')):<10} {str(b.get('end_depth', '')):<10} "
            f"{str(b.get('run_length', '')):<8} "
            f"{str(b.get('bit_size', '')):<7} {str(b.get('bit_type', '')):<5} "
            f"{bit_mfg:<16} {bit_model:<20} "
            f"{mtr_mfg:<16} {mtr_model:<22} "
            f"{str(b.get('motor_od', '')):<6} {str(b.get('motor_rpg', '')):<6}"
        )

    # Save to CSV
    input_basename = os.path.splitext(os.path.basename(csv_path))[0]
    out_name = f"bhas_{size_label}in_{input_basename}.csv"
    out_path = os.path.join(SCRIPT_DIR, out_name)
    fieldnames = list(all_bhas[0].keys())
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_bhas)
    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()
