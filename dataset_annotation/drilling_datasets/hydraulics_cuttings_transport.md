# Hydraulics Cuttings Transport (Hole Cleaning Analysis)

Cuttings transport and hole cleaning calculations. This collection contains analysis of the ability to transport drill cuttings to surface based on flow rate, mud properties, hole geometry, and inclination. Essential for preventing stuck pipe and pack-offs.

## When to use this dataset

- You need to assess hole cleaning effectiveness.
- You want to analyze cuttings transport efficiency.
- You need to identify potential pack-off risks.
- You want to optimize flow rate for hole cleaning.
- You need cuttings bed height estimations.

## Example queries

### Alerting
- Alert when cuttings transport ratio drops below threshold.
- Notify on high cuttings bed accumulation.
- Alert when hole cleaning is inadequate.

### Visualization
- Display cuttings transport ratio vs depth.
- Show cuttings bed height profile.
- Chart hole cleaning efficiency over time.
- Plot transport velocity vs critical velocity.

### Q&A
- Is the current flow rate adequate for hole cleaning?
- What is the cuttings transport ratio?
- Where are potential cuttings accumulation zones?
- What flow rate is needed for effective hole cleaning?
- Is there risk of cuttings bed buildup?

## Frequency

`per_interval` (calculated at regular intervals during drilling)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.cuttings_transport_ratio` (float): Ratio of transport to critical velocity (inferred).
- `data.annular_velocity` (float): Annular velocity at key points (inferred).
- `data.critical_velocity` (float): Minimum velocity for cuttings transport (inferred).
- `data.cuttings_bed_height` (float): Estimated cuttings bed height (inferred).
- `data.hole_cleaning_index` (float): Hole cleaning quality index (inferred).
- `data.flow_rate` (float): Current flow rate (inferred).
- `data.required_flow_rate` (float): Recommended flow rate for cleaning (inferred).
- `data.inclination` (float): Hole inclination affecting transport (inferred).
- `data.depth_points` (array): Cuttings transport data at various depths (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.cuttings_transport_ratio": "float",
  "data.annular_velocity": "float",
  "data.critical_velocity": "float",
  "data.cuttings_bed_height": "float",
  "data.hole_cleaning_index": "float",
  "data.flow_rate": "float",
  "data.required_flow_rate": "float",
  "data.depth_points": "array"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains cuttings transport and hole cleaning analysis.

## Keywords

`cuttings transport`, `hole cleaning`, `annular velocity`, `cuttings bed`, `pack-off`, `hole cleaning index`
