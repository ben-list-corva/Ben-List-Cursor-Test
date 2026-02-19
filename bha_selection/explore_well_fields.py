"""Explore available fields for basin, formation, rig, spud date in Corva."""
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
PLATFORM_API = "https://api.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}

ASSET_ID = 18840303


def explore_well_cache():
    """Get the FULL well_cache record to see all available fields."""
    print("=== well_cache (full record) ===")
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/well_cache/",
        headers=HEADERS,
        params={
            "limit": 1,
            "sort": json.dumps({"timestamp": -1}),
            "query": json.dumps({"asset_id": ASSET_ID}),
        },
    )
    if r.status_code == 200 and r.json():
        record = r.json()[0]
        # Print all top-level keys
        print(f"Top-level keys: {list(record.keys())}")
        for key in sorted(record.keys()):
            val = record[key]
            if isinstance(val, dict):
                print(f"\n  {key}: (dict with keys: {list(val.keys())[:20]})")
                # Go one level deeper
                for k2, v2 in val.items():
                    if isinstance(v2, dict):
                        print(f"    {key}.{k2}: (dict with keys: {list(v2.keys())[:15]})")
                    elif isinstance(v2, list):
                        print(f"    {key}.{k2}: (list, len={len(v2)})")
                    else:
                        print(f"    {key}.{k2}: {v2}")
            elif isinstance(val, list):
                print(f"\n  {key}: (list, len={len(val)})")
            else:
                print(f"\n  {key}: {val}")
    else:
        print(f"  Error: {r.status_code} - {r.text[:300]}")


def explore_asset_v2():
    """Check asset v2 API for additional metadata."""
    print("\n\n=== Asset v2 API (full response) ===")
    r = requests.get(
        f"{PLATFORM_API}/v2/assets/{ASSET_ID}",
        headers=HEADERS,
    )
    if r.status_code == 200:
        print(json.dumps(r.json(), indent=2))
    else:
        print(f"  Error: {r.status_code} - {r.text[:300]}")


def explore_formations():
    """Check data.formations for this well."""
    print("\n\n=== corva#data.formations ===")
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/data.formations/",
        headers=HEADERS,
        params={
            "limit": 10,
            "sort": json.dumps({"timestamp": -1}),
            "query": json.dumps({"asset_id": ASSET_ID}),
        },
    )
    if r.status_code == 200:
        data = r.json()
        print(f"  Records: {len(data)}")
        if data:
            print(json.dumps(data[0], indent=2)[:2000])
    else:
        print(f"  Error: {r.status_code} - {r.text[:300]}")


def explore_well_sections():
    """Check data.well-sections for basin/section info."""
    print("\n\n=== corva#data.well-sections ===")
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/data.well-sections/",
        headers=HEADERS,
        params={
            "limit": 10,
            "sort": json.dumps({"timestamp": -1}),
            "query": json.dumps({"asset_id": ASSET_ID}),
        },
    )
    if r.status_code == 200:
        data = r.json()
        print(f"  Records: {len(data)}")
        for rec in data:
            d = rec.get("data", {})
            print(f"  Section: {d.get('name')}, diameter: {d.get('diameter')}, "
                  f"top: {d.get('top_depth')}, bottom: {d.get('bottom_depth')}, "
                  f"start_time: {d.get('start_time')}")
    else:
        print(f"  Error: {r.status_code} - {r.text[:300]}")


def explore_assets_api_wellhub():
    """Try the wellhub or assets API for basin, rig, spud date."""
    print("\n\n=== Trying wellhub/assets endpoints ===")
    
    # Try wellhub endpoint
    for endpoint in [
        f"{PLATFORM_API}/v2/assets/{ASSET_ID}/wellhub",
        f"{PLATFORM_API}/v1/api/wells/{ASSET_ID}",
        f"{PLATFORM_API}/v2/wells/{ASSET_ID}",
    ]:
        r = requests.get(endpoint, headers=HEADERS)
        print(f"  {endpoint}: {r.status_code}")
        if r.status_code == 200:
            print(json.dumps(r.json(), indent=2)[:3000])
            break
        else:
            print(f"    {r.text[:200]}")


def explore_operations():
    """Check corva#operations for rig info and spud date."""
    print("\n\n=== corva#operations ===")
    r = requests.get(
        f"{DATA_API}/api/v1/data/corva/operations/",
        headers=HEADERS,
        params={
            "limit": 3,
            "sort": json.dumps({"timestamp": 1}),
            "query": json.dumps({"asset_id": ASSET_ID}),
        },
    )
    if r.status_code == 200:
        data = r.json()
        print(f"  Records: {len(data)}")
        if data:
            print(json.dumps(data[0], indent=2)[:3000])
    else:
        print(f"  Error: {r.status_code} - {r.text[:300]}")


if __name__ == "__main__":
    explore_well_cache()
    explore_asset_v2()
    explore_formations()
    explore_well_sections()
    explore_assets_api_wellhub()
    explore_operations()
