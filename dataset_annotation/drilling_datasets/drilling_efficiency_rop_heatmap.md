# Drilling Efficiency ROP Heatmap (ROP Parameter Analysis)

ROP heatmap data for visualizing rate of penetration across parameter combinations. This dataset contains ROP values calculated across a matrix of WOB and RPM combinations, enabling identification of parameter combinations that maximize drilling speed.

## When to use this dataset

- You need to visualize ROP across parameter combinations.
- You want to identify parameters that maximize drilling rate.
- You need data for ROP heatmap displays.
- You want to analyze ROP sensitivity to WOB and RPM.

## Example queries

### Alerting
- Alert when ROP drops below historical range for parameters.
- Notify when parameter changes could improve ROP.

### Visualization
- Display ROP heatmap with WOB vs RPM axes.
- Show maximum ROP zones.
- Overlay current parameters on ROP heatmap.

### Q&A
- What WOB/RPM combination gives highest ROP?
- How does current ROP compare to maximum achievable?
- What is the ROP sensitivity to parameter changes?
- Where is the ROP plateau in the parameter space?

## Frequency

`per_analysis` (generated during ROP analysis periods)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the heatmap calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.heatmap_data` (array): Array of ROP values for parameter grid (inferred).
- `data.wob_bins` (array): WOB bin values for heatmap axes (inferred).
- `data.rpm_bins` (array): RPM bin values for heatmap axes (inferred).
- `data.max_rop_wob` (float): WOB with highest ROP (inferred).
- `data.max_rop_rpm` (float): RPM with highest ROP (inferred).
- `data.max_rop` (float): Maximum ROP value in heatmap (inferred).
- `data.hole_depth` (float): Depth range for heatmap.
- `data.formation` (string): Formation for heatmap (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.heatmap_data": "array",
  "data.wob_bins": "array",
  "data.rpm_bins": "array",
  "data.max_rop_wob": "float",
  "data.max_rop_rpm": "float",
  "data.max_rop": "float",
  "data.hole_depth": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains ROP heatmap data for parameter optimization visualization.

## Keywords

`rop heatmap`, `drilling heatmap`, `parameter optimization`, `rate of penetration`, `wob rpm analysis`, `rop optimization`
