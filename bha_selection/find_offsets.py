"""Find offset wells near a target asset using the Corva API.

Uses the well_cache dataset with geospatial queries for fast lookups.
"""
import requests
import json
import math
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
PLATFORM_API = "https://api.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}


def haversine_miles(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon points in miles."""
    R = 3958.8  # Earth radius in miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def get_well_cache(asset_id):
    """Get well details from well_cache dataset."""
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
    """Get all well asset IDs for a company via the v2 Assets API."""
    all_ids = []
    page = 1
    while True:
        r = requests.get(
            f"{PLATFORM_API}/v2/assets",
            headers=HEADERS,
            params={"limit": 100, "page": page, "types[]": "well", "company_id": company_id},
        )
        if r.status_code != 200:
            print(f"  Assets API error: {r.status_code}")
            break
        data = r.json().get("data", [])
        if not data:
            break
        all_ids.extend(int(a["id"]) for a in data)
        if len(data) < 100:
            break
        page += 1
        if page % 10 == 0:
            print(f"  ... {len(all_ids)} asset IDs so far (page {page})")
    return all_ids


def get_company_wells(company_id):
    """Two-step: get asset IDs via Assets API, then batch-query well_cache."""
    # Step A: Get all asset IDs for the company
    print(f"  Getting asset IDs for company {company_id}...")
    asset_ids = get_company_asset_ids(company_id)
    print(f"  Found {len(asset_ids)} assets")

    # Step B: Batch-query well_cache by asset_id $in
    print(f"  Fetching well_cache data in batches...")
    all_wells = []
    batch_size = 50
    for i in range(0, len(asset_ids), batch_size):
        batch = asset_ids[i: i + batch_size]
        r = requests.get(
            f"{DATA_API}/api/v1/data/corva/well_cache/",
            headers=HEADERS,
            params={
                "limit": batch_size,
                "sort": json.dumps({"timestamp": -1}),
                "query": json.dumps({"asset_id": {"$in": batch}}),
                "fields": (
                    "asset_id,well_id,company_id,location,"
                    "corva#data-well-sections,corva#wits,"
                    "corva#data-drillstring,corva#data-mud"
                ),
            },
        )
        if r.status_code == 200:
            results = r.json()
            all_wells.extend(results)
        if (i // batch_size + 1) % 5 == 0:
            print(f"    Batch {i // batch_size + 1}/{(len(asset_ids) + batch_size - 1) // batch_size}: {len(all_wells)} wells with cache data")

    print(f"  Total: {len(all_wells)} wells with location data")
    return all_wells


def find_nearby_wells_geo(target_lat, target_lon, radius_miles, company_id, exclude_asset_id=None):
    """Use MongoDB $geoWithin to find wells within radius.
    
    Falls back to company-based query if geo query not supported.
    """
    # Convert miles to radians for MongoDB $centerSphere
    radius_radians = radius_miles / 3958.8

    # Try geo query first -- must include company_id per Corva API rules
    geo_query = {
        "company_id": company_id,
        "location": {
            "$geoWithin": {
                "$centerSphere": [[target_lon, target_lat], radius_radians]
            }
        }
    }

    print(f"  Trying geospatial query (company_id={company_id}, radius={radius_miles} mi)...")
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/well_cache/",
        headers=HEADERS,
        params={
            "limit": 500,
            "sort": json.dumps({"timestamp": -1}),
            "query": json.dumps(geo_query),
            "fields": (
                "asset_id,well_id,company_id,location,"
                "corva#data-well-sections,corva#wits,"
                "corva#data-drillstring,corva#data-mud"
            ),
        },
    )

    if r.status_code == 200:
        wells = r.json()
        print(f"  Geo query returned {len(wells)} wells")
        return wells

    # Fallback: query by company_id with bounding box post-filter
    print(f"  Geo query failed ({r.status_code}: {r.text[:200]})")
    print("  Falling back to company query with post-filter...")
    return find_nearby_wells_fallback(target_lat, target_lon, radius_miles, company_id, exclude_asset_id)


def find_nearby_wells_fallback(target_lat, target_lon, radius_miles, company_id, exclude_asset_id=None):
    """Fallback: pull wells by company and filter by distance."""
    # Use a bounding box approximation first (1 degree lat ~ 69 miles)
    lat_delta = radius_miles / 69.0
    lon_delta = radius_miles / (69.0 * math.cos(math.radians(target_lat)))

    bbox_query = {
        "company_id": company_id,
        "location.coordinates.1": {"$gte": target_lat - lat_delta, "$lte": target_lat + lat_delta},
        "location.coordinates.0": {"$gte": target_lon - lon_delta, "$lte": target_lon + lon_delta},
    }

    print(f"  Using bounding box query...")
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/well_cache/",
        headers=HEADERS,
        params={
            "limit": 500,
            "sort": json.dumps({"timestamp": -1}),
            "query": json.dumps(bbox_query),
            "fields": (
                "asset_id,well_id,company_id,location,"
                "corva#data-well-sections,corva#wits,"
                "corva#data-drillstring,corva#data-mud"
            ),
        },
    )

    if r.status_code == 200:
        wells = r.json()
        print(f"  Bounding box returned {len(wells)} wells")
        return wells

    print(f"  Bounding box also failed ({r.status_code}: {r.text[:200]})")
    return []


def find_offsets(target_asset_id, radius_miles=500, max_results=500):
    """Find all wells within radius_miles of the target asset."""
    print(f"\n{'='*60}")
    print(f"  OFFSET WELL FINDER")
    print(f"  Target Asset: {target_asset_id}")
    print(f"  Search Radius: {radius_miles} miles")
    print(f"{'='*60}\n")

    # Step 1: Get target well details
    print("Step 1: Getting target well details from well_cache...")
    target = get_well_cache(target_asset_id)
    if not target:
        print(f"  ERROR: No well_cache data for asset {target_asset_id}")
        return []

    target_loc = target.get("location", {}).get("coordinates", [])
    if not target_loc or len(target_loc) < 2:
        print("  ERROR: Target well has no location data")
        return []

    target_lon, target_lat = target_loc[0], target_loc[1]
    target_company = target.get("company_id")

    # Extract target well info
    wits = target.get("corva#wits", {}).get("data", {})
    sections = target.get("corva#data-well-sections", {}).get("data", {})
    mud = target.get("corva#data-mud", {}).get("data", {})
    ds = target.get("corva#data-drillstring", {}).get("data", {})

    print(f"  Name/Asset:   asset_id={target_asset_id}, well_id={target.get('well_id')}")
    print(f"  Company ID:   {target_company}")
    print(f"  Location:     lat={target_lat}, lon={target_lon}")
    print(f"  State:        {wits.get('state', 'N/A')}")
    print(f"  Hole Depth:   {wits.get('hole_depth', 'N/A')} ft")
    print(f"  Section:      {sections.get('name', 'N/A')} ({sections.get('diameter', '?')}\")")
    print(f"  Depth Range:  {sections.get('top_depth', '?')} - {sections.get('bottom_depth', '?')} ft")
    print(f"  Mud:          {mud.get('mud_type', 'N/A')}, {mud.get('mud_density', 'N/A')} ppg")

    # Show BHA components if available
    components = ds.get("components", [])
    if components:
        bit = next((c for c in components if c.get("family") == "bit"), None)
        motor = next((c for c in components if c.get("family") == "pdm"), None)
        print(f"  Bit:          {bit.get('size', '?')}\" {bit.get('bit_type', '')} (length: {bit.get('length', '?')} ft)" if bit else "  Bit:          N/A")
        print(f"  Motor:        length={motor.get('length', '?')} ft" if motor else "  Motor:        N/A")

    # Step 2: Pull all wells for the same company, then filter by distance
    print(f"\nStep 2: Pulling all wells for company_id={target_company}...")
    nearby_wells = get_company_wells(target_company)

    # Step 3: Calculate exact distances and build results
    print(f"\nStep 3: Calculating distances and filtering...")
    offsets = []
    for well in nearby_wells:
        loc = well.get("location", {}).get("coordinates", [])
        if not loc or len(loc) < 2:
            continue
        w_lon, w_lat = loc[0], loc[1]
        w_asset_id = well.get("asset_id")
        if w_asset_id == target_asset_id:
            continue

        dist = haversine_miles(target_lat, target_lon, w_lat, w_lon)
        if dist > radius_miles:
            continue

        w_wits = well.get("corva#wits", {}).get("data", {})
        w_sections = well.get("corva#data-well-sections", {}).get("data", {})
        w_mud = well.get("corva#data-mud", {}).get("data", {})

        offsets.append({
            "asset_id": w_asset_id,
            "well_id": well.get("well_id"),
            "company_id": well.get("company_id"),
            "lat": w_lat,
            "lon": w_lon,
            "distance_miles": round(dist, 1),
            "section_name": w_sections.get("name", "N/A"),
            "hole_diameter": w_sections.get("diameter", "N/A"),
            "hole_depth": w_wits.get("hole_depth", "N/A"),
            "state": w_wits.get("state", "N/A"),
            "mud_type": w_mud.get("mud_type", "N/A"),
            "mud_density": w_mud.get("mud_density", "N/A"),
        })

    offsets.sort(key=lambda x: x["distance_miles"])

    # Limit results
    if len(offsets) > max_results:
        offsets = offsets[:max_results]

    # Print results
    print(f"\n{'='*60}")
    print(f"  RESULTS: {len(offsets)} wells within {radius_miles} miles (max {max_results})")
    print(f"{'='*60}\n")

    if offsets:
        print(f"{'Asset ID':<12} {'Dist (mi)':<10} {'Depth (ft)':<12} {'Diameter':<10} {'Section':<20} {'State':<25} {'Mud'}")
        print("-" * 120)
        for o in offsets:
            mud_str = f"{o['mud_type']} {o['mud_density']}ppg" if o['mud_type'] != 'N/A' else 'N/A'
            print(
                f"{o['asset_id']:<12} "
                f"{o['distance_miles']:<10} "
                f"{str(o['hole_depth']):<12} "
                f"{str(o['hole_diameter']):<10} "
                f"{str(o['section_name']):<20} "
                f"{str(o['state']):<25} "
                f"{mud_str}"
            )
    else:
        print("No wells found within the search radius.")

    return offsets


if __name__ == "__main__":
    import sys

    asset_id = int(sys.argv[1]) if len(sys.argv) > 1 else 18840303
    radius = float(sys.argv[2]) if len(sys.argv) > 2 else 500
    max_offsets = int(sys.argv[3]) if len(sys.argv) > 3 else 500

    offsets = find_offsets(target_asset_id=asset_id, radius_miles=radius, max_results=max_offsets)
