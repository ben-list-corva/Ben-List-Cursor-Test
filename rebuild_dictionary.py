"""
Rebuild the Corva Data Dictionary Markdown from the CSV.

Workflow:
  1. Edit corva_data_dictionary.csv in Excel (fill in Unit, Description, Notes)
  2. Save the CSV
  3. Run:  python rebuild_dictionary.py
  4. The Markdown file is regenerated with your edits

The CSV is the source of truth. Human edits go in the CSV; the Markdown
is auto-generated from it so Cursor always has the latest version.
"""
import csv
import os
from collections import defaultdict, OrderedDict

BASE = r'c:\Users\Ben List\Documents\GitHub\Ben-List-Cursor-Test'
CSV_IN = os.path.join(BASE, 'corva_data_dictionary.csv')
MD_OUT = os.path.join(BASE, 'corva_data_dictionary.md')

CAT_ORDER = [
    'WITS / Real-Time Drilling',
    'Drilling',
    'Drilling Efficiency',
    'Directional',
    'Torque & Drag',
    'Hydraulics',
    'PDM / Motor',
    'Circulation',
    'Activities / Operations',
    'Well Data (data.*)',
    'Completions / Frac',
    'Wireline',
    'Pumpdown',
    'Drillout',
    'Anti-Collision',
    'Cementing',
    'Geosteering',
    'Formation Evaluation',
    'Predictive Drilling / ML',
    'Alerts',
    'Well Design',
    'Well Design (design.*)',
    'Metrics / KPIs',
    'Time Log',
    'Production (Enverus)',
    'Sustainability / ESG',
    'Wellness / Check-Up',
    'Stream Quality',
    'Handover / Mission Control',
    'Interventions (Workover)',
    'Launchpad / Connectivity',
    'AskCorva / AI',
    'Bowtie / Insights',
    'Frac Third-Party',
    'Nabors Integration',
    'WITS (Other Phases)',
    'Other',
]

# ── Read CSV ────────────────────────────────────────────────────
print(f"Reading CSV: {CSV_IN}")
rows = []
with open(CSV_IN, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)
print(f"  {len(rows)} field rows loaded")

# ── Group by dataset, then by category ──────────────────────────
# Preserve dataset metadata and group fields
datasets = OrderedDict()  # dataset_name -> { meta, fields }
for row in rows:
    ds_name = row['Dataset Name']
    if ds_name not in datasets:
        datasets[ds_name] = {
            'name': ds_name,
            'friendly': row['Friendly Name'],
            'category': row['Category'],
            'data_type': row['Data Type'],
            'api_path': row['API Path'],
            'fields': []
        }
    datasets[ds_name]['fields'].append(row)

# Group by category
by_cat = defaultdict(list)
for ds in datasets.values():
    by_cat[ds['category']].append(ds)

# ── Generate Markdown ───────────────────────────────────────────
print(f"Generating Markdown: {MD_OUT}")

def esc(text):
    """Escape pipe characters for Markdown tables."""
    return (text or '').replace('|', '/').replace('\n', ' ').replace('\r', '')

with open(MD_OUT, 'w', encoding='utf-8') as f:
    # ── Header ──
    f.write("# Corva Data Dictionary\n\n")
    f.write(f"> **Scope**: {len(datasets)} datasets with known field schemas\n")
    f.write("> **Source**: Corva Dataset Explorer API + schema extraction\n")
    f.write("> **Editable CSV**: `corva_data_dictionary.csv` (edit in Excel, then run `rebuild_dictionary.py`)\n\n")
    f.write("---\n\n")

    # ── Quick Lookup Table ──
    f.write("## Quick Lookup Table\n\n")
    f.write("| Dataset | Category | Type | API Path | Fields | Description |\n")
    f.write("|---|---|---|---|---|---|\n")
    for ds in sorted(datasets.values(), key=lambda x: x['friendly']):
        name = ds['name']
        cat = ds['category']
        dtype = ds['data_type']
        api = ds['api_path']
        num_fields = len(ds['fields'])
        # Use the Description from the first field that has one, or check Notes
        desc = ''
        for fld in ds['fields']:
            if fld.get('Description'):
                desc = esc(fld['Description'])[:80]
                break
        f.write(f"| `{name}` | {cat} | {dtype} | `{api}` | {num_fields} | {desc} |\n")

    f.write("\n---\n\n")

    # ── Datasets by Category ──
    f.write("## Datasets by Category\n\n")

    section = 1
    for cat in CAT_ORDER:
        if cat not in by_cat:
            continue
        cat_ds = sorted(by_cat[cat], key=lambda x: x['friendly'])
        if not cat_ds:
            continue

        f.write(f"### {section}. {cat}\n\n")

        for ds in cat_ds:
            f.write(f"#### `{ds['name']}`\n\n")
            f.write(f"- **Friendly Name**: {ds['friendly']}\n")
            f.write(f"- **Data Type**: {ds['data_type']}\n")
            f.write(f"- **API Path**: `{ds['api_path']}`\n")
            f.write("\n")

            # Field table
            fields = ds['fields']
            if fields:
                f.write("| Field Path | Type | Example | Unit | Description | Notes | Tags |\n")
                f.write("|---|---|---|---|---|---|---|\n")
                for fld in fields:
                    fp = fld['Field Path']
                    ft = fld['Field Type']
                    ex = esc(fld.get('Example', ''))
                    if len(ex) > 50:
                        ex = ex[:47] + '...'
                    unit = esc(fld.get('Unit', ''))
                    desc_f = esc(fld.get('Description', ''))
                    notes = esc(fld.get('Notes', ''))
                    tags = esc(fld.get('Tags', ''))
                    f.write(f"| `{fp}` | {ft} | {ex} | {unit} | {desc_f} | {notes} | {tags} |\n")
                f.write("\n")

        section += 1

    # ── API Access Patterns ──
    f.write("---\n\n")
    f.write("## API Access Patterns\n\n")
    f.write("### Data API Endpoint\n\n")
    f.write("```\n")
    f.write("GET /api/v1/data/{provider}/{dataset}/\n")
    f.write("```\n\n")
    f.write("### Common Query Parameters\n\n")
    f.write("| Parameter | Description | Example |\n")
    f.write("|---|---|---|\n")
    f.write('| `query` | MongoDB-style query (JSON string) | `{"asset_id": 12345}` |\n')
    f.write('| `sort` | Sort order (JSON string) | `{"timestamp": -1}` |\n')
    f.write('| `limit` | Max records to return | `500` |\n')
    f.write('| `skip` | Records to skip (pagination) | `0` |\n')
    f.write('| `fields` | Comma-separated field list | `timestamp,data.hole_depth` |\n')
    f.write("\n")

    f.write("### Python SDK Example\n\n")
    f.write("```python\n")
    f.write("# Inside a Corva app\n")
    f.write("response = api.get(\n")
    f.write("    '/api/v1/data/corva/wits/',\n")
    f.write("    params={\n")
    f.write("        'query': json.dumps({'asset_id': event.asset_id}),\n")
    f.write("        'limit': 500,\n")
    f.write("        'sort': json.dumps({'timestamp': -1}),\n")
    f.write("        'fields': 'timestamp,data.hole_depth,data.bit_depth,data.weight_on_bit'\n")
    f.write("    }\n")
    f.write(")\n")
    f.write("records = response.json()\n")
    f.write("```\n\n")

    f.write("### Dataset Naming Convention\n\n")
    f.write("- Format: `{provider}#{collection_name}` (e.g., `corva#wits`)\n")
    f.write("- API path: `/api/v1/data/{provider}/{collection_name}/`\n")
    f.write("- The `#` in the name becomes `/` in the API path\n\n")

    f.write("### Data Types\n\n")
    f.write("| Type | Description |\n|---|---|\n")
    f.write("| `time` | Time-indexed data, queried by `timestamp` and `asset_id` |\n")
    f.write("| `depth` | Depth-indexed data, queried by `measured_depth` and `asset_id` |\n")
    f.write("| `reference` | Reference/configuration data, not time-series |\n")
    f.write("| `timeseries` | MongoDB time-series collection (newer format) |\n\n")

    # ── Glossary ──
    f.write("---\n\n")
    f.write("## Glossary of Common Drilling Terms\n\n")
    f.write("| Term | Definition |\n|---|---|\n")
    f.write("| **BHA** | Bottom Hole Assembly - the lower portion of the drill string |\n")
    f.write("| **WITS** | Wellsite Information Transfer Specification - real-time drilling data |\n")
    f.write("| **ROP** | Rate of Penetration - speed of drilling (ft/hr) |\n")
    f.write("| **WOB** | Weight on Bit - downward force applied to the drill bit (klbs) |\n")
    f.write("| **MSE** | Mechanical Specific Energy - energy required to remove rock |\n")
    f.write("| **SPP** | Standpipe Pressure - pump pressure at surface (psi) |\n")
    f.write("| **RPM** | Rotations Per Minute - rotary speed of the drill string |\n")
    f.write("| **TVD** | True Vertical Depth - vertical distance from surface |\n")
    f.write("| **MD** | Measured Depth - length of wellbore from surface |\n")
    f.write("| **ECD** | Equivalent Circulating Density - effective mud weight while circulating (ppg) |\n")
    f.write("| **PDM** | Positive Displacement Motor - downhole motor for directional drilling |\n")
    f.write("| **MWD** | Measurement While Drilling - downhole sensors for surveys |\n")
    f.write("| **NPT** | Non-Productive Time - time lost to unplanned events |\n")
    f.write("| **TFA** | Total Flow Area - combined nozzle area of the drill bit |\n")
    f.write("| **DLS** | Dog Leg Severity - rate of wellbore curvature (deg/100ft) |\n")
    f.write("| **Frac** | Hydraulic fracturing - completions stimulation technique |\n")
    f.write("| **ISIP** | Instantaneous Shut-In Pressure - pressure after pumping stops |\n")
    f.write("| **ppg** | Pounds per gallon - unit for mud weight / density |\n")
    f.write("| **klbs** | Thousands of pounds - unit for hookload, WOB |\n")

print(f"\nDone! Regenerated {MD_OUT}")
print(f"  {len(datasets)} datasets, {len(rows)} field rows")
