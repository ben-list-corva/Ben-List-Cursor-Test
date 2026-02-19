"""Find offset wells across ALL operators in the same basin/formation.

Usage:
    python find_offsets_all_operators.py <asset_id> [radius_miles] [max_results]
    python find_offsets_all_operators.py 18840303 100 500
    python find_offsets_all_operators.py 18840303 100 500 --export-csv
"""
import csv
import requests
import json
import math
import sys
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import db

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
PLATFORM_API = "https://api.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}


def haversine_miles(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def epoch_to_date(epoch):
    if not epoch:
        return "N/A"
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return "N/A"


def get_well_cache(asset_id):
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/well_cache/",
        headers=HEADERS,
        params={
            "limit": 1,
            "sort": json.dumps({"timestamp": -1}),
            "query": json.dumps({"asset_id": asset_id}),
        },
    )
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


def _fetch_asset_ids_from_api():
    """Pull ALL well asset IDs from the platform API (no cache)."""
    all_ids = []
    page = 1
    while True:
        r = requests.get(
            f"{PLATFORM_API}/v2/assets",
            headers=HEADERS,
            params={"limit": 100, "page": page, "types[]": "well"},
        )
        if r.status_code != 200:
            print(f"  Assets API error on page {page}: {r.status_code}")
            break
        data = r.json().get("data", [])
        if not data:
            break
        all_ids.extend(int(a["id"]) for a in data)
        if len(data) < 100:
            break
        page += 1
        if page % 50 == 0:
            print(f"    ... {len(all_ids)} asset IDs (page {page})")
    return all_ids


def get_all_asset_ids():
    """Get all asset IDs, using SQLite cache with 1-hour TTL."""
    cached = db.get_cached_asset_ids(max_age_seconds=3600)
    if cached:
        print(f"  Using cached asset IDs ({len(cached)} assets, < 1 hr old)")
        return cached

    print("  Cache miss or expired -- fetching from API...")
    ids = _fetch_asset_ids_from_api()
    if ids:
        db.save_asset_ids_cache(ids)
    return ids


def fetch_well_cache_batch(batch):
    """Fetch well_cache for a single batch of asset IDs. Used by thread pool."""
    fields = (
        "asset_id,well_id,company_id,location,"
        "asset,rig,program,company,"
        "corva#data-well-sections,corva#wits,"
        "corva#data-drillstring,corva#data-mud,"
        "corva#data-casing"
    )
    try:
        r = requests.get(
            f"{DATA_API}/api/v1/data/corva/well_cache/",
            headers=HEADERS,
            params={
                "limit": len(batch),
                "sort": json.dumps({"timestamp": -1}),
                "query": json.dumps({"asset_id": {"$in": batch}}),
                "fields": fields,
            },
            timeout=30,
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []


def _fetch_and_extract_missing(asset_ids, target_lat, target_lon):
    """Fetch well_cache from API for the given asset_ids, extract info, return list of info dicts."""
    all_wells = []
    batch_size = 50
    batches = [asset_ids[i: i + batch_size] for i in range(0, len(asset_ids), batch_size)]
    total_batches = len(batches)

    if total_batches == 0:
        return []

    print(f"  Fetching {len(asset_ids)} uncached wells in {total_batches} batches...")
    start = time.time()

    completed = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_well_cache_batch, batch): i
                   for i, batch in enumerate(batches)}
        for future in as_completed(futures):
            results = future.result()
            for well in results:
                info = extract_well_info(well, target_lat, target_lon)
                if info:
                    all_wells.append(info)
            completed += 1
            if completed % 50 == 0:
                elapsed = time.time() - start
                rate = completed / elapsed if elapsed > 0 else 0
                eta = (total_batches - completed) / rate if rate > 0 else 0
                print(f"    {completed}/{total_batches} batches, "
                      f"{len(all_wells)} wells extracted, ETA: {eta:.0f}s")

    elapsed = time.time() - start
    print(f"  Fetched & extracted {len(all_wells)} wells in {elapsed:.1f}s")
    return all_wells


def get_nearby_wells(target_lat, target_lon, radius_miles):
    """Get well info near the target, using SQLite bounding-box query.

    Fast path: loads only wells within the search radius from the SQLite
    cache (indexed by lat/lon). If the cache has wells, this skips ALL
    Corva API calls -- just a SQLite query + haversine math.

    If the cache is empty, falls back to the full API pull (get all
    asset IDs, fetch well_cache from Corva, save to SQLite).
    """
    # Fast path: bounding-box query on SQLite cache
    nearby = db.get_cached_wells_near(target_lat, target_lon, radius_miles)

    if nearby:
        # Recalculate exact distance from current target well
        result = []
        for rec in nearby:
            lat = rec.get("lat")
            lon = rec.get("lon")
            if lat is not None and lon is not None:
                rec["distance_miles"] = round(
                    haversine_miles(target_lat, target_lon, float(lat), float(lon)), 1
                )
                result.append(rec)
        print(f"  SQLite fast path: {len(result)} wells within ~{radius_miles} mi "
              f"(from {db.count_well_cache_records()} total cached)")
        return result

    # Cache is empty -- full API pull required (first-time only)
    print("  Cache empty -- running full API pull (one-time)...")
    return _full_api_pull(target_lat, target_lon, radius_miles)


def _full_api_pull(target_lat, target_lon, radius_miles):
    """Fallback: fetch ALL wells from Corva API, save to cache, return nearby."""
    asset_ids = get_all_asset_ids()
    print(f"  Found {len(asset_ids)} total assets")

    cached_ids = db.get_cached_well_asset_ids()
    missing_ids = [aid for aid in asset_ids if str(aid) not in cached_ids]
    print(f"  Well cache: {len(cached_ids)} cached, {len(missing_ids)} to fetch")

    if missing_ids:
        new_infos = _fetch_and_extract_missing(missing_ids, target_lat, target_lon)
        if new_infos:
            db.save_well_cache_records(new_infos)

    # Now use the fast path
    nearby = db.get_cached_wells_near(target_lat, target_lon, radius_miles)
    result = []
    for rec in nearby:
        lat = rec.get("lat")
        lon = rec.get("lon")
        if lat is not None and lon is not None:
            rec["distance_miles"] = round(
                haversine_miles(target_lat, target_lon, float(lat), float(lon)), 1
            )
            result.append(rec)

    print(f"  Total nearby well records: {len(result)}")
    return result


def sanitize(text):
    """Remove non-ASCII characters for safe Windows console output."""
    if not isinstance(text, str):
        return str(text)
    return text.encode("ascii", errors="replace").decode("ascii")


def extract_well_info(well, target_lat, target_lon):
    loc = well.get("location", {}).get("coordinates", [])
    if not loc or len(loc) < 2:
        return None

    w_lon, w_lat = loc[0], loc[1]
    asset_id = well.get("asset_id")
    dist = haversine_miles(target_lat, target_lon, w_lat, w_lon)

    asset_info = well.get("asset", {})
    rig_info = well.get("rig", {})
    program_info = well.get("program", {})
    company_info = well.get("company", {})
    wits = well.get("corva#wits", {}).get("data", {})
    sections = well.get("corva#data-well-sections", {}).get("data", {})
    mud = well.get("corva#data-mud", {}).get("data", {})
    drillstring = well.get("corva#data-drillstring", {}).get("data", {})

    components = drillstring.get("components", [])
    bit = next((c for c in components if c.get("family") == "bit"), {})
    motor = next((c for c in components if c.get("family") == "pdm"), {})

    stats = asset_info.get("stats", {})
    drilling_stats = stats.get("drilling", {})
    spud_ts = drilling_stats.get("start_time") or sections.get("start_time")
    spud_date = epoch_to_date(spud_ts) if spud_ts else "N/A"

    return {
        "asset_id": asset_id,
        "well_name": sanitize(asset_info.get("name", "N/A")),
        "operator": sanitize(company_info.get("name", "N/A")),
        "basin": program_info.get("name", "N/A"),
        "target_formation": asset_info.get("target_formation", "N/A"),
        "rig": sanitize(rig_info.get("name", "N/A")),
        "distance_miles": round(dist, 1),
        "hole_depth_ft": wits.get("hole_depth", "N/A"),
        "section": sections.get("name", "N/A"),
        "hole_diameter": sections.get("diameter", "N/A"),
        "mud_type": mud.get("mud_type", "N/A"),
        "mud_density": mud.get("mud_density", "N/A"),
        "bit_size": bit.get("size", "N/A"),
        "bit_type": bit.get("bit_type", "N/A"),
        "state": wits.get("state", "N/A"),
        "spud_date": spud_date,
        "lat": w_lat,
        "lon": w_lon,
        "string_design": asset_info.get("string_design", "N/A"),
        "well_state": asset_info.get("state", "N/A"),
    }


def formation_matches(target_formation, candidate_formation):
    if not target_formation or target_formation == "N/A":
        return True
    if not candidate_formation or candidate_formation == "N/A":
        return False

    target_lower = target_formation.lower()
    candidate_lower = candidate_formation.lower()

    prefixes = ["lower ", "upper ", "middle ", "base ", "top ", "main "]
    target_base = target_lower
    candidate_base = candidate_lower
    for prefix in prefixes:
        if target_base.startswith(prefix):
            target_base = target_base[len(prefix):]
        if candidate_base.startswith(prefix):
            candidate_base = candidate_base[len(prefix):]

    return target_base == candidate_base


def find_offsets_all_operators(target_asset_id, radius_miles=100, max_results=500,
                               export_csv_flag=False, spud_after=None):
    print(f"\n{'=' * 70}")
    print(f"  CROSS-OPERATOR OFFSET WELL FINDER")
    print(f"  Target Asset: {target_asset_id} | Radius: {radius_miles} mi | Max: {max_results}")
    if spud_after:
        print(f"  Spud Date Filter: after {spud_after}")
    print(f"{'=' * 70}\n")

    # Step 1: Target well
    print("Step 1: Getting target well details...")
    target = get_well_cache(target_asset_id)
    if not target:
        print(f"  ERROR: No data for asset {target_asset_id}")
        return []

    target_loc = target.get("location", {}).get("coordinates", [])
    if not target_loc or len(target_loc) < 2:
        print("  ERROR: No location data")
        return []

    target_lon, target_lat = target_loc[0], target_loc[1]
    target_asset = target.get("asset", {})
    target_program = target.get("program", {})

    target_basin = target_program.get("name", "N/A")
    target_formation = target_asset.get("target_formation", "N/A")

    print(f"  Well Name:        {target_asset.get('name', 'N/A')}")
    print(f"  Operator:         {target.get('company', {}).get('name', 'N/A')}")
    print(f"  Basin/Program:    {target_basin}")
    print(f"  Target Formation: {target_formation}")
    print(f"  Rig:              {target.get('rig', {}).get('name', 'N/A')}")
    print(f"  Location:         lat={target_lat}, lon={target_lon}")

    # Step 2: Get nearby wells (SQLite bounding-box, or full API pull if cache empty)
    print(f"\nStep 2: Loading nearby wells...")
    t0 = time.time()
    all_infos = get_nearby_wells(target_lat, target_lon, radius_miles)
    print(f"  {len(all_infos)} nearby wells loaded in {time.time() - t0:.1f}s")

    # Step 3: Filter (distance + min depth only; basin/formation filters
    # are applied later in the per-section analysis pipeline)
    print(f"\nStep 3: Filtering (radius={radius_miles} mi, min_depth=1000 ft)...")
    offsets = []
    min_hole_depth = 1000
    stats = {"distance": 0, "self": 0, "shallow": 0, "spud_date": 0}

    for info in all_infos:
        if str(info.get("asset_id")) == str(target_asset_id):
            stats["self"] += 1
            continue
        if info["distance_miles"] > radius_miles:
            stats["distance"] += 1
            continue
        hd = info.get("hole_depth_ft")
        if hd is None or hd == "N/A" or not isinstance(hd, (int, float)) or hd < min_hole_depth:
            stats["shallow"] += 1
            continue
        spud = info.get("spud_date")
        if spud_after and spud and spud != "N/A":
            if spud < spud_after:
                stats["spud_date"] += 1
                continue
        offsets.append(info)

    offsets.sort(key=lambda x: x["distance_miles"])
    if len(offsets) > max_results:
        offsets = offsets[:max_results]

    print(f"\n  Filter summary:")
    print(f"    Total well records:       {len(all_infos)}")
    print(f"    Passed all filters:       {len(offsets)}")
    print(f"    Skipped (outside radius): {stats['distance']}")
    print(f"    Skipped (shallow/<{min_hole_depth}ft): {stats['shallow']}")
    if spud_after:
        print(f"    Skipped (spud before {spud_after}): {stats['spud_date']}")

    # Count unique operators
    operators = set(o["operator"] for o in offsets if o["operator"] != "N/A")
    print(f"    Unique operators found:   {len(operators)} ({', '.join(sorted(operators))})")

    # Print table
    print(f"\n{'=' * 70}")
    print(f"  RESULTS: {len(offsets)} offset wells (all operators)")
    print(f"  Basin: {target_basin} | Formation Group: {target_formation}")
    print(f"{'=' * 70}\n")

    header = (
        f"{'Asset ID':<12} {'Well Name':<28} {'Operator':<18} {'Formation':<20} "
        f"{'Rig':<16} {'Dist(mi)':<10} {'MD(ft)':<12} {'Spud Date':<12} "
        f"{'Dia':<6} {'State'}"
    )
    print(header)
    print("-" * len(header))
    for o in offsets:
        name = str(o.get("well_name") or "N/A")[:26]
        formation = str(o.get("target_formation") or "N/A")[:18]
        rig = str(o.get("rig") or "N/A")[:14]
        operator = str(o.get("operator") or "N/A")[:16]
        dist = o.get("distance_miles", "N/A")
        md = o.get("hole_depth_ft", "N/A")
        spud = o.get("spud_date") or "N/A"
        dia = str(o.get("hole_diameter") or "N/A")
        state = o.get("state") or "N/A"
        print(
            f"{o.get('asset_id', 'N/A'):<12} {name:<28} {operator:<18} {formation:<20} "
            f"{rig:<16} {str(dist):<10} {str(md):<12} "
            f"{str(spud):<12} {dia:<6} {state}"
        )

    # Save CSV (replace None with "N/A" for CSV compatibility)
    output_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"offset_wells_{radius_miles}mi_{timestamp_str}.csv")
    csv_fields = [
        "asset_id", "well_name", "operator", "basin", "target_formation",
        "rig", "distance_miles", "hole_depth_ft", "section", "hole_diameter",
        "mud_type", "mud_density", "bit_size", "bit_type", "state",
        "spud_date", "lat", "lon", "string_design", "well_state",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for o in offsets:
            row = {k: (o.get(k) if o.get(k) is not None else "N/A") for k in csv_fields}
            writer.writerow(row)
    print(f"\nSaved to: {csv_path}")

    # Save to database
    run_id = db.get_or_create_run(str(target_asset_id), radius_miles)
    db.save_offset_wells(run_id, offsets)
    if export_csv_flag:
        db.export_csv(offsets, f"offset_wells_{radius_miles}mi")

    return offsets


if __name__ == "__main__":
    export_csv_flag = "--export-csv" in sys.argv
    sys.argv = [a for a in sys.argv if a != "--export-csv"]

    # Parse --spud-after YYYY-MM-DD
    spud_after = None
    filtered_args = []
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--spud-after" and i + 1 < len(sys.argv):
            spud_after = sys.argv[i + 1]
            i += 2
        else:
            filtered_args.append(sys.argv[i])
            i += 1

    asset_id = int(filtered_args[0]) if len(filtered_args) > 0 else 18840303
    radius = float(filtered_args[1]) if len(filtered_args) > 1 else 100
    max_results = int(filtered_args[2]) if len(filtered_args) > 2 else 500

    find_offsets_all_operators(
        target_asset_id=asset_id,
        radius_miles=radius,
        max_results=max_results,
        export_csv_flag=export_csv_flag,
        spud_after=spud_after,
    )
