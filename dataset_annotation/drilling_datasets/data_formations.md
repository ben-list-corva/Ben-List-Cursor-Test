# Formations (Geological Formation Data)

Geological formation data for the wellbore. This collection contains information about the geological formations encountered during drilling, including formation tops, depths, and properties. Essential for geosteering, formation correlation, and drilling parameter optimization by formation.

## When to use this dataset

- You need to identify formations at specific depths.
- You want to correlate drilling parameters with formations.
- You need formation data for geosteering displays.
- You want to compare formation tops across wells.
- You need formation information for LWD/MWD interpretation.
- You want to analyze drilling performance by formation.

## Example queries

### Alerting
- Alert when approaching a target formation.
- Notify when drilling into a known problem formation.
- Alert when formation top differs from prognosis.

### Visualization
- Display formation tops on depth-based charts.
- Show formation correlation across offset wells.
- Overlay formations on gamma ray curves.
- Chart drilling parameters by formation.

### Q&A
- What formation are we currently drilling?
- What depth is the top of the target formation?
- How does this formation top compare to offset wells?
- What formations have we drilled through so far?
- What is the expected TD formation?

## Frequency

`per_formation` (one record per formation top)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the formation was created or updated.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.formation_name`: Name of the geological formation.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.formation_name` (string): Name of the formation.
- `data.md` (float): Measured depth of formation top.
- `data.td` (float): True vertical depth of formation top (inferred - may use `tvd`).
- `data.tvd` (float): True vertical depth of formation top.
- `data.bottom_md` (float): Measured depth of formation bottom (inferred).
- `data.bottom_tvd` (float): TVD of formation bottom (inferred).
- `data.thickness` (float): Formation thickness (inferred).
- `data.lithology` (string): Lithology description (inferred).
- `data.source` (string): Source of formation pick (e.g., "prognosis", "actual", "offset").
- `data.confidence` (string): Confidence level of formation pick (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.formation_name": "string",
  "data.md": "float",
  "data.td": "float",
  "data.tvd": "float",
  "data.bottom_md": "float",
  "data.thickness": "float",
  "data.lithology": "string",
  "data.source": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains geological formation tops with depth information.

## Keywords

`formations`, `geological formations`, `formation tops`, `geosteering`, `lithology`, `stratigraphy`, `formation correlation`
