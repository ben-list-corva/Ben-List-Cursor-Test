"""Fetch and display rotational tendency (DLS in rotation) for a given asset."""
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv(r'c:\Users\Ben List\Documents\GitHub\Ben-List-Cursor-Test\Cursor Training\Cursor Training\.env')

ASSET_ID = 41387083
BASE_URL = "https://data.corva.ai"
TOKEN = os.getenv("CORVA_BEARER_TOKEN")

headers = {"Authorization": f"Bearer {TOKEN}"}

url = f"{BASE_URL}/api/v1/data/corva/directional.rotational-tendency/"
params = {
    "query": json.dumps({"asset_id": ASSET_ID}),
    "sort": json.dumps({"timestamp": -1}),
    "limit": 100,
}

print(f"Fetching rotational tendency for asset {ASSET_ID}...")
resp = httpx.get(url, headers=headers, params=params, timeout=30)
print(f"Status: {resp.status_code}")

if resp.status_code != 200:
    print(f"Error: {resp.text[:500]}")
    exit(1)

records = resp.json()
print(f"Records returned: {len(records)}")

if not records:
    print("No rotational tendency data found for this asset.")
    exit(0)

print(f"\n{'='*90}")
print(f"  DLS in Rotation - Asset {ASSET_ID}")
print(f"{'='*90}")
print(f"{'From MD':>10} {'To MD':>10} {'DLS':>8} {'Build':>8} {'Turn':>8} {'WOB':>8} {'RPM':>8} {'Torque':>8}")
print(f"{'(ft)':>10} {'(ft)':>10} {'(d/100)':>8} {'(d/100)':>8} {'(d/100)':>8} {'(klbs)':>8} {'':>8} {'':>8}")
print("-" * 90)

total_points = 0
for record in records:
    data = record.get("data", {})
    tendency = data.get("rotational_tendency", [])
    for pt in tendency:
        from_md = pt.get("from_measured_depth", "")
        to_md = pt.get("to_measured_depth", "")
        dls = pt.get("dls", "")
        build = pt.get("build_rate", "")
        turn = pt.get("turn_rate", "")
        wob = pt.get("weight_on_bit", "")
        rpm = pt.get("rotary_rpm", "")
        torque = pt.get("rotary_torque", "")

        dls_str = f"{dls:.3f}" if isinstance(dls, (int, float)) else str(dls)
        build_str = f"{build:.3f}" if isinstance(build, (int, float)) else str(build)
        turn_str = f"{turn:.3f}" if isinstance(turn, (int, float)) else str(turn)
        wob_str = f"{wob:.1f}" if isinstance(wob, (int, float)) else str(wob)
        rpm_str = f"{rpm:.1f}" if isinstance(rpm, (int, float)) else str(rpm)
        torque_str = f"{torque:.2f}" if isinstance(torque, (int, float)) else str(torque)

        print(f"{from_md:>10} {to_md:>10} {dls_str:>8} {build_str:>8} {turn_str:>8} {wob_str:>8} {rpm_str:>8} {torque_str:>8}")
        total_points += 1

print("-" * 90)
print(f"Total data points: {total_points}")
