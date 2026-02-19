"""
Usage: 
  1. Save your full JSON array to corva_datasets_raw.json
  2. Run: python save_and_catalog.py
  
This generates:
  - corva_datasets_catalog.csv  (flat table of all datasets)
  - corva_datasets_complete_reference.md (categorized Markdown reference)
"""
import json
import csv
from collections import Counter, defaultdict

INPUT = r'c:\Users\Ben List\Documents\GitHub\Ben-List-Cursor-Test\corva_datasets_raw.json'

with open(INPUT, 'r', encoding='utf-8') as f:
    datasets = json.load(f)

print(f"Loaded {len(datasets)} datasets from {INPUT}")

# ── Categorization ──────────────────────────────────────────────
def categorize(fn):
    fn = fn.lower()
    checks = [
        (('wits.', 'wits '), 'WITS / Real-Time Drilling'),
        (('wits',), 'WITS / Real-Time Drilling'),
        (('completion.wits', 'wireline.wits', 'pumpdown.wits', 'drillout.wits', 'interventions.wits'), 'WITS (Other Phases)'),
        (('completion.', 'completions.', 'completions-', 'completion-'), 'Completions / Frac'),
        (('drilling.', 'drilling-', 'drilling_'), 'Drilling'),
        (('directional.',), 'Directional'),
        (('torque-and-drag.',), 'Torque & Drag'),
        (('hydraulics.',), 'Hydraulics'),
        (('drilling-efficiency.',), 'Drilling Efficiency'),
        (('data.',), 'Well Data (data.*)'),
        (('activities', 'activity-groups', 'activity_tracker'), 'Activities / Operations'),
        (('operations',), 'Activities / Operations'),
        (('anti-collision.',), 'Anti-Collision'),
        (('drillout.',), 'Drillout'),
        (('circulation.',), 'Circulation'),
        (('design.',), 'Well Design (design.*)'),
        (('production.',), 'Production (Enverus)'),
        (('sustainability.',), 'Sustainability / ESG'),
        (('well-design.',), 'Well Design'),
        (('handover',), 'Handover / Mission Control'),
        (('wellness', 'wcu',), 'Wellness / Check-Up'),
        (('stream-quality',), 'Stream Quality'),
        (('metrics',), 'Metrics / KPIs'),
        (('python-alerts', 'predictive-alerts', 'alerts-plus', 'custom_alerts'), 'Alerts'),
        (('geosteering.',), 'Geosteering'),
        (('formation-evaluation.',), 'Formation Evaluation'),
        (('interventions.',), 'Interventions (Workover)'),
        (('launchpad',), 'Launchpad / Connectivity'),
        (('pdm.',), 'PDM / Motor'),
        (('rotary-automation', 'predictive-drilling', 'machine-learning'), 'Predictive Drilling / ML'),
        (('nabors',), 'Nabors Integration'),
        (('frac.', 'fracvision'), 'Frac Third-Party'),
        (('cement.',), 'Cementing'),
        (('downhole.sensor',), 'Downhole Sensors'),
        (('timelog',), 'Time Log'),
        (('askcorva',), 'AskCorva / AI'),
        (('wireline.',), 'Wireline'),
        (('pumpdown.',), 'Pumpdown'),
        (('bowtie.',), 'Bowtie / Insights'),
    ]
    for prefixes, cat in checks:
        for p in prefixes:
            if fn.startswith(p):
                return cat
    return 'Other'

# ── CSV Catalog ─────────────────────────────────────────────────
csv_path = r'c:\Users\Ben List\Documents\GitHub\Ben-List-Cursor-Test\corva_datasets_catalog.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['ID', 'Dataset Name', 'Friendly Name', 'Data Type', 'Plottable', 'Has Schema', 'Category', 'Description'])
    for ds in sorted(datasets, key=lambda x: x.get('friendly_name', '')):
        fn = ds.get('friendly_name', '')
        desc = (ds.get('description') or '').replace('\n', ' ').replace('\r', '').strip()
        has_schema = 'Yes' if ds.get('schema') and ds['schema'] != {} else 'No'
        plottable = 'Yes' if ds.get('plottable') else 'No'
        w.writerow([
            ds.get('id', ''), ds.get('name', ''), fn,
            ds.get('data_type', ''), plottable, has_schema,
            categorize(fn), desc[:300]
        ])
print(f"  -> CSV: {csv_path}")

# ── Markdown Reference ──────────────────────────────────────────
md_path = r'c:\Users\Ben List\Documents\GitHub\Ben-List-Cursor-Test\corva_datasets_complete_reference.md'

# Group by category
by_cat = defaultdict(list)
for ds in datasets:
    fn = ds.get('friendly_name', '')
    by_cat[categorize(fn)].append(ds)

# Category display order (most important first)
cat_order = [
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
    'Downhole Sensors',
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

# Stats
type_counts = Counter(ds.get('data_type') for ds in datasets)
cat_counts = Counter(categorize(ds.get('friendly_name', '')) for ds in datasets)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# Corva Platform – Complete Datasets Reference\n\n")
    f.write(f"> **Total Datasets**: {len(datasets)}  \n")
    f.write(f"> **Source**: Corva Dataset Explorer API (`/api/v1/data/corva/dataset/`)  \n")
    f.write(f"> **Generated**: 2026-02-11  \n\n")
    
    f.write("---\n\n")
    f.write("## Summary Statistics\n\n")
    
    f.write("### By Data Type\n\n")
    f.write("| Data Type | Count |\n|---|---|\n")
    for dt, c in type_counts.most_common():
        f.write(f"| {dt} | {c} |\n")
    
    f.write("\n### By Category\n\n")
    f.write("| Category | Count |\n|---|---|\n")
    for cat in cat_order:
        if cat in cat_counts:
            f.write(f"| {cat} | {cat_counts[cat]} |\n")
    
    f.write("\n---\n\n")
    f.write("## Dataset Catalog by Category\n\n")
    
    section = 1
    for cat in cat_order:
        if cat not in by_cat:
            continue
        ds_list = sorted(by_cat[cat], key=lambda x: x.get('friendly_name', ''))
        f.write(f"### {section}. {cat} ({len(ds_list)} datasets)\n\n")
        f.write("| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |\n")
        f.write("|---|---|---|---|---|---|\n")
        for i, ds in enumerate(ds_list, 1):
            name = ds.get('name', '')
            fn = ds.get('friendly_name', '')
            dt = ds.get('data_type', '')
            desc = (ds.get('description') or '').replace('\n', ' ').replace('\r', '').replace('|', '/').strip()
            if len(desc) > 120:
                desc = desc[:117] + '...'
            plottable = 'Yes' if ds.get('plottable') else ''
            f.write(f"| {i} | `{name}` | {fn} | {dt} | {plottable} | {desc} |\n")
        f.write("\n")
        section += 1
    
    # Datasets with schemas (most useful for app development)
    f.write("---\n\n")
    f.write("## Datasets with Defined Schemas\n\n")
    f.write("The following datasets have schema definitions, making them the most useful for app development:\n\n")
    schema_ds = [ds for ds in datasets if ds.get('schema') and ds['schema'] != {}]
    schema_ds.sort(key=lambda x: x.get('friendly_name', ''))
    f.write(f"**{len(schema_ds)} datasets** have schema definitions.\n\n")
    f.write("| Dataset | Type | Category | Schema Fields (top-level) |\n")
    f.write("|---|---|---|---|\n")
    for ds in schema_ds:
        name = ds.get('name', '')
        fn = ds.get('friendly_name', '')
        dt = ds.get('data_type', '')
        cat = categorize(fn)
        schema = ds.get('schema', {})
        # Get top-level keys
        if isinstance(schema, dict):
            top_keys = list(schema.keys())[:8]
            schema_str = ', '.join(f'`{k}`' for k in top_keys)
            if len(schema.keys()) > 8:
                schema_str += f' ... (+{len(schema.keys())-8} more)'
        else:
            schema_str = str(type(schema))
        f.write(f"| `{name}` | {dt} | {cat} | {schema_str} |\n")
    
    # API Access patterns
    f.write("\n---\n\n")
    f.write("## API Access Patterns\n\n")
    f.write("### Data API (Recommended for Apps)\n\n")
    f.write("```\n")
    f.write("GET /api/v1/data/{provider}/{dataset}/\n")
    f.write("```\n\n")
    f.write("**Common query parameters:**\n\n")
    f.write("| Parameter | Description | Example |\n")
    f.write("|---|---|---|\n")
    f.write('| `query` | MongoDB-style query (JSON string) | `{"asset_id": 12345}` |\n')
    f.write('| `sort` | Sort order (JSON string) | `{"timestamp": -1}` |\n')
    f.write('| `limit` | Max records to return | `500` |\n')
    f.write('| `skip` | Records to skip (pagination) | `0` |\n')
    f.write('| `fields` | Comma-separated field list | `timestamp,data.hole_depth` |\n')
    f.write("\n")
    f.write("### Example: Pull WITS data\n\n")
    f.write("```python\n")
    f.write("# Python SDK (inside a Corva app)\n")
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
    f.write("| `timeseries` | MongoDB time-series collection (newer format) |\n")

print(f"  -> Markdown: {md_path}")

# Final summary
print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"Total datasets: {len(datasets)}")
print(f"With schemas:   {len(schema_ds)}")
print(f"Categories:     {len(cat_counts)}")
print(f"\nData types: {dict(type_counts.most_common())}")
print(f"\nFiles generated:")
print(f"  1. {csv_path}")
print(f"  2. {md_path}")
