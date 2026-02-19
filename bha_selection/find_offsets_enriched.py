"""Find and filter offset wells with full metadata: basin, formation, rig, MD, spud date.

Usage:
    python find_offsets_enriched.py <asset_id> [radius_miles] [max_results]
    python find_offsets_enriched.py 18840303 500 500
    python find_offsets_enriched.py 18840303 500 500 --export-csv
"""
import csv
import requests
import json
import math
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

import db

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
PLATFORM_API = "https://api.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}


def haversine_miles(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon points in miles."""
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def epoch_to_date(epoch):
    """Convert Unix epoch to YYYY-MM-DD string."""
    if not epoch:
        return "N/A"
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return "N/A"


def get_well_cache(asset_id):
    """Get full well_cache record for a single asset."""
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


def get_company_asset_ids(company_id):
    """Get all well asset IDs for a company via v2 Assets API."""
    all_ids = []
    page = 1
    while True:
        r = requests.get(
            f"{PLATFORM_API}/v2/assets",
            headers=HEADERS,
            params={"limit": 100, "page": page, "types[]": "well", "company_id": company_id},
        )
        if r.status_code != 200:
            break
        data = r.json().get("data", [])
        if not data:
            break
        all_ids.extend(int(a["id"]) for a in data)
        if len(data) < 100:
            break
        page += 1
    return all_ids


def get_well_cache_batch(asset_ids):
    """Batch-query well_cache with enriched fields."""
    all_wells = []
    batch_size = 50
    fields = (
        "asset_id,well_id,company_id,location,"
        "asset,rig,program,company,"
        "corva#data-well-sections,corva#wits,"
        "corva#data-drillstring,corva#data-mud,"
        "corva#data-casing"
    )
    for i in range(0, len(asset_ids), batch_size):
        batch = asset_ids[i: i + batch_size]
        r = requests.get(
            f"{DATA_API}/api/v1/data/corva/well_cache/",
            headers=HEADERS,
            params={
                "limit": batch_size,
                "sort": json.dumps({"timestamp": -1}),
                "query": json.dumps({"asset_id": {"$in": batch}}),
                "fields": fields,
            },
        )
        if r.status_code == 200:
            all_wells.extend(r.json())
        if (i // batch_size + 1) % 5 == 0:
            print(f"    Batch {i // batch_size + 1}/{(len(asset_ids) + batch_size - 1) // batch_size}: "
                  f"{len(all_wells)} wells fetched")
    return all_wells


def get_spud_dates(asset_ids):
    """Get spud dates from v2 Assets API (original_well_created_at)."""
    spud_map = {}
    page = 1
    # We need to query per-company but we already have the IDs
    # Fetch all and match
    asset_set = set(asset_ids)
    # Unfortunately the v2 assets API doesn't support $in, so we page through
    # We'll just get what we can from the well_cache operations timestamp
    return spud_map


def extract_well_info(well, target_lat, target_lon):
    """Extract all relevant fields from a well_cache record."""
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
    casing = well.get("corva#data-casing", {}).get("data", {})

    # Extract BHA info
    components = drillstring.get("components", [])
    bit = next((c for c in components if c.get("family") == "bit"), {})
    motor = next((c for c in components if c.get("family") == "pdm"), {})

    # Spud date: use the earliest section start_time or drillstring setting_timestamp
    section_start = sections.get("start_time")
    # The surface section would have the spud date, but well_cache only has latest section
    # Use the asset stats if available
    stats = asset_info.get("stats", {})
    drilling_stats = stats.get("drilling", {})
    spud_ts = drilling_stats.get("start_time") or section_start
    spud_date = epoch_to_date(spud_ts) if spud_ts else "N/A"

    return {
        "asset_id": asset_id,
        "well_name": asset_info.get("name", "N/A"),
        "company": company_info.get("name", "N/A"),
        "basin": program_info.get("name", "N/A"),
        "target_formation": asset_info.get("target_formation", "N/A"),
        "rig": rig_info.get("name", "N/A"),
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
    """Check if candidate formation is in the same formation group as target.
    
    E.g., 'Lower Eagle Ford' matches 'Upper Eagle Ford', 'Eagle Ford', etc.
    """
    if not target_formation or target_formation == "N/A":
        return True
    if not candidate_formation or candidate_formation == "N/A":
        return False

    target_lower = target_formation.lower()
    candidate_lower = candidate_formation.lower()

    # Extract the base formation name by stripping common prefixes
    prefixes = ["lower ", "upper ", "middle ", "base ", "top ", "main "]
    target_base = target_lower
    candidate_base = candidate_lower
    for prefix in prefixes:
        if target_base.startswith(prefix):
            target_base = target_base[len(prefix):]
        if candidate_base.startswith(prefix):
            candidate_base = candidate_base[len(prefix):]

    # Match if base formation names are the same
    return target_base == candidate_base


def find_offsets_enriched(target_asset_id, radius_miles=500, max_results=500,
                          export_csv_flag=False, spud_after=None):
    """Find offset wells filtered by basin and formation, with full metadata."""
    print(f"\n{'=' * 70}")
    print(f"  ENRICHED OFFSET WELL FINDER")
    print(f"  Target Asset: {target_asset_id} | Radius: {radius_miles} mi | Max: {max_results}")
    if spud_after:
        print(f"  Spud Date Filter: after {spud_after}")
    print(f"{'=' * 70}\n")

    # Step 1: Get target well
    print("Step 1: Getting target well details...")
    target = get_well_cache(target_asset_id)
    if not target:
        print(f"  ERROR: No well_cache data for asset {target_asset_id}")
        return []

    target_loc = target.get("location", {}).get("coordinates", [])
    if not target_loc or len(target_loc) < 2:
        print("  ERROR: Target well has no location data")
        return []

    target_lon, target_lat = target_loc[0], target_loc[1]
    target_company_id = target.get("company_id")
    target_asset = target.get("asset", {})
    target_program = target.get("program", {})
    target_rig = target.get("rig", {})
    target_wits = target.get("corva#wits", {}).get("data", {})

    target_basin = target_program.get("name", "N/A")
    target_formation = target_asset.get("target_formation", "N/A")

    print(f"  Well Name:        {target_asset.get('name', 'N/A')}")
    print(f"  Company:          {target.get('company', {}).get('name', 'N/A')} (ID: {target_company_id})")
    print(f"  Basin/Program:    {target_basin}")
    print(f"  Target Formation: {target_formation}")
    print(f"  Rig:              {target_rig.get('name', 'N/A')}")
    print(f"  Location:         lat={target_lat}, lon={target_lon}")
    print(f"  Hole Depth:       {target_wits.get('hole_depth', 'N/A')} ft")

    print(f"\n  Filters: basin='{target_basin}', formation group='{target_formation}'")

    # Step 2: Get all company assets
    print(f"\nStep 2: Getting all assets for company {target_company_id}...")
    asset_ids = get_company_asset_ids(target_company_id)
    print(f"  Found {len(asset_ids)} assets")

    # Step 3: Batch-query well_cache
    print(f"\nStep 3: Fetching enriched well_cache data...")
    all_wells = get_well_cache_batch(asset_ids)
    print(f"  Got {len(all_wells)} well_cache records")

    # Step 4: Filter and enrich
    print(f"\nStep 4: Filtering by basin, formation, and distance...")
    offsets = []
    skipped_basin = 0
    skipped_formation = 0
    skipped_no_loc = 0
    skipped_distance = 0
    skipped_spud = 0

    for well in all_wells:
        info = extract_well_info(well, target_lat, target_lon)
        if not info:
            skipped_no_loc += 1
            continue
        if info["asset_id"] == target_asset_id:
            continue

        # Filter: same basin
        if target_basin != "N/A" and info["basin"] != target_basin:
            skipped_basin += 1
            continue

        # Filter: same formation group
        if not formation_matches(target_formation, info["target_formation"]):
            skipped_formation += 1
            continue

        # Filter: within radius
        if info["distance_miles"] > radius_miles:
            skipped_distance += 1
            continue

        # Filter: spud date cutoff
        if spud_after and info.get("spud_date", "N/A") != "N/A":
            if info["spud_date"] < spud_after:
                skipped_spud += 1
                continue

        offsets.append(info)

    offsets.sort(key=lambda x: x["distance_miles"])
    if len(offsets) > max_results:
        offsets = offsets[:max_results]

    print(f"\n  Filtering summary:")
    print(f"    Passed:              {len(offsets)}")
    print(f"    Skipped (no loc):    {skipped_no_loc}")
    print(f"    Skipped (basin):     {skipped_basin}")
    print(f"    Skipped (formation): {skipped_formation}")
    print(f"    Skipped (distance):  {skipped_distance}")
    if spud_after:
        print(f"    Skipped (spud before {spud_after}): {skipped_spud}")

    # Print table
    print(f"\n{'=' * 70}")
    print(f"  RESULTS: {len(offsets)} offset wells")
    print(f"  Basin: {target_basin} | Formation Group: {target_formation}")
    print(f"{'=' * 70}\n")

    header = (
        f"{'Asset ID':<12} {'Well Name':<30} {'Basin':<15} {'Formation':<22} "
        f"{'Rig':<18} {'Dist(mi)':<10} {'MD(ft)':<12} {'Spud Date':<12} "
        f"{'Hole Dia':<10} {'State'}"
    )
    print(header)
    print("-" * len(header))
    for o in offsets:
        name = str(o["well_name"])[:28]
        formation = str(o["target_formation"])[:20]
        rig = str(o["rig"])[:16]
        basin = str(o["basin"])[:13]
        print(
            f"{o['asset_id']:<12} {name:<30} {basin:<15} {formation:<22} "
            f"{rig:<18} {o['distance_miles']:<10} {str(o['hole_depth_ft']):<12} "
            f"{o['spud_date']:<12} {str(o['hole_diameter']):<10} {o['state']}"
        )

    # Save to CSV (backward compatibility)
    output_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(output_dir, "offset_wells.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "asset_id", "well_name", "company", "basin", "target_formation",
            "rig", "distance_miles", "hole_depth_ft", "section", "hole_diameter",
            "mud_type", "mud_density", "bit_size", "bit_type", "state",
            "spud_date", "lat", "lon", "string_design", "well_state",
        ])
        writer.writeheader()
        writer.writerows(offsets)
    print(f"\nSaved to: {csv_path}")

    # Save to database
    run_id = db.get_or_create_run(str(target_asset_id), radius_miles)
    offsets_for_db = [{**o, "operator": o.get("company", "N/A")} for o in offsets]
    db.save_offset_wells(run_id, offsets_for_db)
    if export_csv_flag:
        db.export_csv(offsets_for_db, f"offset_wells_{radius_miles}mi")

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
    radius = float(filtered_args[1]) if len(filtered_args) > 1 else 500
    max_results = int(filtered_args[2]) if len(filtered_args) > 2 else 500

    find_offsets_enriched(
        target_asset_id=asset_id,
        radius_miles=radius,
        max_results=max_results,
        export_csv_flag=export_csv_flag,
        spud_after=spud_after,
    )
