"""Full Corva bit scan: enumerate ALL wells, fetch recent BHAs, parse bit models.

Phase 1: Enumerate all well asset IDs via v2 Assets API -> all_well_ids.json
Phase 2: Batch-fetch drillstrings (past 18 months), parse bit/motor models -> full_bit_scan.csv
Phase 3: Rebuild bit catalog from full_bit_scan.csv

Usage:
    python full_corva_bit_scan.py                # runs all phases
    python full_corva_bit_scan.py --phase1       # enumerate wells only
    python full_corva_bit_scan.py --phase2       # process wells (resumes automatically)
    python full_corva_bit_scan.py --phase3       # rebuild catalog only
    python full_corva_bit_scan.py --workers 5    # override parallel worker count (default 10)
    python full_corva_bit_scan.py --export-csv   # also export to exports/full_bit_scan.csv
"""
import csv
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests
from dotenv import load_dotenv

import db

# Import parsing functions from parse_bit_motors.py (same directory)
from parse_bit_motors import parse_bit, parse_motor_lobes

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
PLATFORM_API = "https://api.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WELL_IDS_FILE = os.path.join(SCRIPT_DIR, "all_well_ids.json")
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "scan_progress.json")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "full_bit_scan.csv")

BATCH_SIZE = 500
MONTHS_BACK = 18

CSV_FIELDNAMES = [
    "asset_id", "well_name", "well_status", "well_state",
    "bha_number", "bha_timestamp", "set_date",
    "start_depth", "end_depth", "run_length", "num_components",
    "bit_size", "bit_type", "bit_name", "bit_manufacturer", "bit_model",
    "bit_serial", "bit_tfa", "bit_nozzles", "bit_blade_count", "bit_cutter_size",
    "motor_name", "motor_manufacturer", "motor_model", "motor_od", "motor_length",
    "motor_rpg", "motor_max_diff", "motor_bend", "motor_stages", "motor_lobes",
    "motor_rotor_lobes", "motor_stator_lobes",
    "parsed_blades", "parsed_cutter_mm", "parse_confidence", "parse_method",
    "motor_lobe_config", "motor_rpg_band",
]


def sanitize(text):
    if not isinstance(text, str):
        return str(text) if text is not None else "N/A"
    return text.encode("ascii", errors="replace").decode("ascii")


def epoch_to_date(epoch):
    if not epoch:
        return "N/A"
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return "N/A"


def get_cutoff_epoch():
    """Compute epoch timestamp for 18 months ago."""
    now = datetime.now(tz=timezone.utc)
    cutoff = now - relativedelta(months=MONTHS_BACK)
    return int(cutoff.timestamp())


# ============================================================
# PHASE 1: Enumerate all well asset IDs
# ============================================================

def enumerate_wells():
    """Paginate through v2 Assets API and collect all well IDs + names."""
    print(f"\n{'=' * 80}")
    print(f"  PHASE 1: ENUMERATE ALL WELL ASSETS")
    print(f"{'=' * 80}\n")

    all_wells = []
    page = 1
    t0 = time.time()

    while True:
        try:
            r = requests.get(
                f"{PLATFORM_API}/v2/assets",
                headers=HEADERS,
                params={"limit": 100, "page": page, "types[]": "well"},
                timeout=30,
            )
        except requests.exceptions.RequestException as e:
            print(f"  Network error on page {page}: {e}")
            time.sleep(5)
            continue

        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 10))
            print(f"  Rate limited on page {page}, waiting {wait}s...")
            time.sleep(wait)
            continue

        if r.status_code != 200:
            print(f"  API error on page {page}: {r.status_code} {r.text[:200]}")
            break

        data = r.json().get("data", [])
        if not data:
            break

        for asset in data:
            attrs = asset.get("attributes", {})
            all_wells.append({
                "id": int(asset["id"]),
                "name": sanitize(attrs.get("name", "N/A")),
                "status": attrs.get("status", ""),
                "state": attrs.get("state", ""),
            })

        if len(data) < 100:
            break
        page += 1
        if page % 50 == 0:
            elapsed = time.time() - t0
            print(f"    Page {page}: {len(all_wells)} wells enumerated ({elapsed:.0f}s)")

    elapsed = time.time() - t0
    print(f"\n  Total wells found: {len(all_wells)} in {elapsed:.1f}s ({page} pages)")

    # Save to JSON
    with open(WELL_IDS_FILE, "w") as f:
        json.dump({"timestamp": datetime.now(tz=timezone.utc).isoformat(),
                    "total": len(all_wells),
                    "wells": all_wells}, f)
    print(f"  Saved to: {WELL_IDS_FILE}")

    return all_wells


# ============================================================
# PHASE 2: Batch-fetch drillstrings and parse
# ============================================================

def load_well_ids():
    """Load well IDs from Phase 1 output."""
    if not os.path.exists(WELL_IDS_FILE):
        print(f"  ERROR: {WELL_IDS_FILE} not found. Run --phase1 first.")
        sys.exit(1)
    with open(WELL_IDS_FILE) as f:
        data = json.load(f)
    wells = data["wells"]
    print(f"  Loaded {len(wells)} wells from {WELL_IDS_FILE}")
    return wells


def load_progress():
    """Load resume progress file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"processed_ids": [], "total_bhas": 0, "total_wells_with_bhas": 0,
            "batches_completed": 0, "last_batch_time": None}


def save_progress(progress):
    """Save progress file atomically."""
    tmp = PROGRESS_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(progress, f)
    os.replace(tmp, PROGRESS_FILE)


def fetch_drillstrings_with_filter(asset_id, cutoff_epoch, max_retries=3):
    """Fetch drillstrings for one asset with timestamp filter and retry logic."""
    all_records = []
    skip = 0
    batch = 100
    retries = 0

    while True:
        try:
            r = requests.get(
                f"{DATA_API}/api/v1/data/corva/data.drillstring/",
                headers=HEADERS,
                params={
                    "limit": batch,
                    "skip": skip,
                    "sort": json.dumps({"timestamp": 1}),
                    "query": json.dumps({
                        "asset_id": int(asset_id),
                        "timestamp": {"$gte": cutoff_epoch},
                    }),
                },
                timeout=30,
            )
        except requests.exceptions.RequestException:
            retries += 1
            if retries > max_retries:
                return all_records
            time.sleep(2 ** retries)
            continue

        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 5))
            time.sleep(wait)
            continue

        if r.status_code != 200:
            retries += 1
            if retries > max_retries:
                return all_records
            time.sleep(2 ** retries)
            continue

        records = r.json()
        if not records:
            break
        all_records.extend(records)
        if len(records) < batch:
            break
        skip += batch
        retries = 0

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


def process_single_well(well_info, cutoff_epoch):
    """Fetch and process all BHAs for a single well. Returns list of row dicts."""
    asset_id = well_info["id"]
    well_name = well_info.get("name", "N/A")
    well_status = well_info.get("status", "")
    well_state = well_info.get("state", "")

    drillstrings = fetch_drillstrings_with_filter(asset_id, cutoff_epoch)

    results = []
    for ds in drillstrings:
        data = ds.get("data", {})
        components = data.get("components", [])

        bits = [c for c in components if c.get("family") == "bit"]
        if not bits:
            continue

        bit_info = extract_bit_info(components)
        motor_info = extract_motor_info(components)

        # Parse bit model inline
        bit_parsed = parse_bit(
            bit_info.get("bit_manufacturer", ""),
            bit_info.get("bit_model", ""),
        )
        motor_parsed = parse_motor_lobes(
            motor_info.get("motor_model", ""),
            str(motor_info.get("motor_rpg", "")),
        )

        start_depth = data.get("start_depth", "N/A")
        end_depth = data.get("end_depth", "N/A")
        run_length = "N/A"
        if isinstance(start_depth, (int, float)) and isinstance(end_depth, (int, float)):
            run_length = round(end_depth - start_depth, 1)

        bha_id = data.get("id", "N/A")
        bha_ts = ds.get("timestamp", "")
        setting_ts = data.get("setting_timestamp")

        row = {
            "asset_id": asset_id,
            "well_name": sanitize(well_name),
            "well_status": well_status,
            "well_state": well_state,
            "bha_number": bha_id,
            "bha_timestamp": bha_ts,
            "set_date": epoch_to_date(setting_ts),
            "start_depth": start_depth,
            "end_depth": end_depth,
            "run_length": run_length,
            "num_components": len(components),
            **bit_info,
            **motor_info,
            "parsed_blades": bit_parsed["blades"],
            "parsed_cutter_mm": bit_parsed["cutter_mm"],
            "parse_confidence": bit_parsed["confidence"],
            "parse_method": bit_parsed["parse_method"],
            "motor_lobe_config": motor_parsed["motor_lobe_config"],
            "motor_rpg_band": motor_parsed["motor_rpg_band"],
        }
        results.append(row)

    return results


def append_to_csv(rows):
    """Append rows to the output CSV. Creates file with header if it doesn't exist."""
    file_exists = os.path.exists(OUTPUT_CSV) and os.path.getsize(OUTPUT_CSV) > 0
    try:
        with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerows(rows)
    except PermissionError:
        backup = OUTPUT_CSV.replace(".csv", f"_{int(time.time())}.csv")
        print(f"  WARNING: CSV locked, writing to {backup}")
        with open(backup, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            writer.writerows(rows)


def run_phase2(max_workers=10, export_csv=False):
    """Main Phase 2 loop: batch-process wells with resume."""
    print(f"\n{'=' * 80}")
    print(f"  PHASE 2: BATCH DRILLSTRING FETCH & PARSE")
    print(f"{'=' * 80}\n")

    cutoff_epoch = get_cutoff_epoch()
    cutoff_date = datetime.fromtimestamp(cutoff_epoch, tz=timezone.utc).strftime("%Y-%m-%d")
    print(f"  Timestamp cutoff: {cutoff_date} (epoch {cutoff_epoch})")
    print(f"  Parallel workers: {max_workers}")

    wells = load_well_ids()
    progress = load_progress()

    processed_set = set(progress["processed_ids"])
    remaining = [w for w in wells if w["id"] not in processed_set]

    print(f"  Already processed: {len(processed_set)}")
    print(f"  Remaining:         {len(remaining)}")
    print(f"  BHAs found so far: {progress['total_bhas']}")

    if not remaining:
        print("\n  All wells already processed!")
        if os.path.exists(OUTPUT_CSV) and os.path.getsize(OUTPUT_CSV) > 0:
            try:
                df = pd.read_csv(OUTPUT_CSV)
                db.save_bit_scan(df)
            except Exception as e:
                print(f"  Parquet save warning: {e}")
        if export_csv and os.path.exists(OUTPUT_CSV) and os.path.getsize(OUTPUT_CSV) > 0:
            try:
                df = pd.read_csv(OUTPUT_CSV)
                db.export_csv(df, "full_bit_scan")
            except Exception as e:
                print(f"  CSV export warning: {e}")
        return

    total_remaining = len(remaining)
    batches = [remaining[i:i + BATCH_SIZE] for i in range(0, total_remaining, BATCH_SIZE)]

    print(f"  Batches to process: {len(batches)} (batch size={BATCH_SIZE})")
    print()

    global_t0 = time.time()
    cumulative_bhas = progress["total_bhas"]
    cumulative_wells_with_bhas = progress["total_wells_with_bhas"]
    new_models_this_run = set()

    for batch_idx, batch in enumerate(batches):
        batch_t0 = time.time()
        batch_num = progress["batches_completed"] + batch_idx + 1
        batch_bhas = []
        batch_wells_with_bhas = 0

        print(f"  --- Batch {batch_num} ({len(batch)} wells) ---")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(process_single_well, w, cutoff_epoch): w
                for w in batch
            }
            completed = 0
            for future in as_completed(futures):
                well_info = futures[future]
                try:
                    rows = future.result()
                except Exception as e:
                    print(f"    ERROR processing {well_info['id']}: {e}")
                    rows = []

                if rows:
                    batch_bhas.extend(rows)
                    batch_wells_with_bhas += 1
                    for r in rows:
                        model = r.get("bit_model", "")
                        if model and model != "N/A":
                            new_models_this_run.add(model)

                completed += 1
                if completed % 100 == 0:
                    elapsed = time.time() - batch_t0
                    print(f"    {completed}/{len(batch)} wells, "
                          f"{len(batch_bhas)} BHAs, {elapsed:.0f}s")

        # Append results to CSV
        if batch_bhas:
            append_to_csv(batch_bhas)

        cumulative_bhas += len(batch_bhas)
        cumulative_wells_with_bhas += batch_wells_with_bhas

        # Update progress
        progress["processed_ids"].extend(w["id"] for w in batch)
        progress["total_bhas"] = cumulative_bhas
        progress["total_wells_with_bhas"] = cumulative_wells_with_bhas
        progress["batches_completed"] = batch_num
        progress["last_batch_time"] = datetime.now(tz=timezone.utc).isoformat()
        save_progress(progress)

        batch_elapsed = time.time() - batch_t0
        total_elapsed = time.time() - global_t0
        processed_count = len(progress["processed_ids"])
        remaining_count = len(wells) - processed_count

        # Parse confidence stats for this batch
        conf_counts = {"high": 0, "check": 0, "unknown": 0, "skip": 0}
        for r in batch_bhas:
            c = r.get("parse_confidence", "")
            if c in conf_counts:
                conf_counts[c] += 1
            elif c:
                conf_counts["unknown"] += 1

        print(f"    Batch {batch_num} done: {len(batch_bhas)} BHAs from "
              f"{batch_wells_with_bhas} wells in {batch_elapsed:.1f}s")
        print(f"    Parse confidence: high={conf_counts['high']} check={conf_counts['check']} "
              f"unknown={conf_counts['unknown']} skip={conf_counts['skip']}")
        print(f"    Cumulative: {cumulative_bhas} BHAs, {processed_count}/{len(wells)} wells")

        if remaining_count > 0:
            rate = processed_count / total_elapsed if total_elapsed > 0 else 1
            eta_s = remaining_count / rate if rate > 0 else 0
            eta_m = eta_s / 60
            print(f"    ETA: {eta_m:.1f} min ({remaining_count} wells remaining)")
        print()

    total_elapsed = time.time() - global_t0
    print(f"\n{'=' * 80}")
    print(f"  PHASE 2 COMPLETE")
    print(f"  Total BHAs:           {cumulative_bhas}")
    print(f"  Wells with BHAs:      {cumulative_wells_with_bhas}")
    print(f"  Unique bit models:    {len(new_models_this_run)}")
    print(f"  Total time:           {total_elapsed / 60:.1f} min")
    print(f"  Output:               {OUTPUT_CSV}")
    print(f"{'=' * 80}\n")

    # Save full scan to Parquet (read from CSV for complete dataset)
    if os.path.exists(OUTPUT_CSV) and os.path.getsize(OUTPUT_CSV) > 0:
        try:
            df = pd.read_csv(OUTPUT_CSV)
            db.save_bit_scan(df)
        except Exception as e:
            print(f"  Parquet save warning: {e}")
    if export_csv and os.path.exists(OUTPUT_CSV) and os.path.getsize(OUTPUT_CSV) > 0:
        try:
            df = pd.read_csv(OUTPUT_CSV)
            db.export_csv(df, "full_bit_scan")
        except Exception as e:
            print(f"  CSV export warning: {e}")


# ============================================================
# PHASE 3: Rebuild catalog
# ============================================================

def run_phase3():
    """Rebuild the bit catalog from the full scan CSV."""
    print(f"\n{'=' * 80}")
    print(f"  PHASE 3: REBUILD BIT CATALOG")
    print(f"{'=' * 80}\n")

    if not os.path.exists(OUTPUT_CSV):
        print(f"  ERROR: {OUTPUT_CSV} not found. Run --phase2 first.")
        return

    catalog = {}

    with open(OUTPUT_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        row_count = 0
        for row in reader:
            row_count += 1
            mfg = (row.get("bit_manufacturer") or "").strip()
            model = (row.get("bit_model") or "").strip()

            if not model or model == "N/A" or "Placeholder" in model:
                continue

            key = (mfg, model)
            if key not in catalog:
                catalog[key] = {
                    "bit_manufacturer": mfg,
                    "bit_model": model,
                    "bit_sizes": set(),
                    "parsed_blades": row.get("parsed_blades", ""),
                    "parsed_cutter_mm": row.get("parsed_cutter_mm", ""),
                    "parse_confidence": row.get("parse_confidence", ""),
                    "parse_method": row.get("parse_method", ""),
                    "total_runs": 0,
                    "well_states": set(),
                }

            info = catalog[key]
            info["total_runs"] += 1

            bit_size = row.get("bit_size", "")
            if bit_size and bit_size != "N/A":
                info["bit_sizes"].add(str(bit_size))

            ws = (row.get("well_state") or "").strip()
            if ws:
                info["well_states"].add(ws)

    conf_order = {"high": 0, "check": 1, "unknown": 2, "": 3}
    entries = sorted(
        catalog.values(),
        key=lambda x: (conf_order.get(x["parse_confidence"], 3),
                        -x["total_runs"], x["bit_manufacturer"], x["bit_model"])
    )

    total_models = len(entries)
    high = sum(1 for e in entries if e["parse_confidence"] == "high")
    check = sum(1 for e in entries if e["parse_confidence"] == "check")
    unknown = sum(1 for e in entries if e["parse_confidence"] in ("unknown", ""))

    print(f"  Total rows in scan CSV: {row_count}")
    print(f"  Unique bit models:      {total_models}")
    print(f"  Confident (high):       {high}")
    print(f"  Needs check:            {check}")
    print(f"  Unknown:                {unknown}")

    out_path = os.path.join(SCRIPT_DIR, "bit_catalog.csv")
    fieldnames = [
        "bit_manufacturer", "bit_model", "bit_diameters",
        "parsed_blades", "parsed_cutter_mm", "parse_confidence", "parse_method",
        "total_runs", "sources",
    ]
    try:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for e in entries:
                writer.writerow({
                    "bit_manufacturer": e["bit_manufacturer"],
                    "bit_model": e["bit_model"],
                    "bit_diameters": "; ".join(sorted(e["bit_sizes"])),
                    "parsed_blades": e["parsed_blades"],
                    "parsed_cutter_mm": e["parsed_cutter_mm"],
                    "parse_confidence": e["parse_confidence"],
                    "parse_method": e["parse_method"],
                    "total_runs": e["total_runs"],
                    "sources": "full_bit_scan",
                })
        print(f"\n  Catalog saved to: {out_path}")
    except PermissionError:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        alt_path = os.path.join(SCRIPT_DIR, f"bit_catalog_{ts}.csv")
        with open(alt_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for e in entries:
                writer.writerow({
                    "bit_manufacturer": e["bit_manufacturer"],
                    "bit_model": e["bit_model"],
                    "bit_diameters": "; ".join(sorted(e["bit_sizes"])),
                    "parsed_blades": e["parsed_blades"],
                    "parsed_cutter_mm": e["parsed_cutter_mm"],
                    "parse_confidence": e["parse_confidence"],
                    "parse_method": e["parse_method"],
                    "total_runs": e["total_runs"],
                    "sources": "full_bit_scan",
                })
        print(f"\n  WARNING: bit_catalog.csv is locked. Saved to: {alt_path}")

    needs_review = [e for e in entries if e["parse_confidence"] in ("check", "unknown", "")]
    if needs_review:
        print(f"\n  Models needing review ({len(needs_review)}):")
        for e in needs_review[:30]:
            print(f"    {e['bit_manufacturer']:<16} {e['bit_model']:<22} -> "
                  f"blades={e['parsed_blades']}, cutter={e['parsed_cutter_mm']}  "
                  f"({e['parse_method'].split(':')[0]})")
        if len(needs_review) > 30:
            print(f"    ... and {len(needs_review) - 30} more")


# ============================================================
# Main
# ============================================================

def main():
    args = sys.argv[1:]

    # Parse --workers flag
    max_workers = 10
    if "--workers" in args:
        idx = args.index("--workers")
        if idx + 1 < len(args):
            max_workers = int(args[idx + 1])
            args = [a for i, a in enumerate(args) if i != idx and i != idx + 1]

    export_csv = "--export-csv" in args
    if export_csv:
        args = [a for a in args if a != "--export-csv"]

    run_all = not any(a in args for a in ("--phase1", "--phase2", "--phase3"))

    if run_all or "--phase1" in args:
        enumerate_wells()

    if run_all or "--phase2" in args:
        run_phase2(max_workers=max_workers, export_csv=export_csv)

    if run_all or "--phase3" in args:
        run_phase3()


if __name__ == "__main__":
    main()
