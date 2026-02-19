# Drilling Efficiency MSE Heatmap (MSE Parameter Analysis)

MSE heatmap data for visualizing drilling efficiency across parameter combinations. This dataset contains MSE values calculated across a matrix of WOB and RPM combinations, enabling identification of optimal drilling windows.

## When to use this dataset

- You need to visualize MSE across parameter combinations.
- You want to identify the "sweet spot" for drilling parameters.
- You need data for drilling parameter heatmap displays.
- You want to analyze MSE sensitivity to WOB and RPM.

## Example queries

### Alerting
- Alert when drilling outside optimal MSE zone.
- Notify when parameter combination shows high MSE.

### Visualization
- Display MSE heatmap with WOB vs RPM axes.
- Show optimal drilling window overlay.
- Chart current parameters on MSE heatmap.

### Q&A
- What WOB/RPM combination gives lowest MSE?
- Where is the optimal drilling window?
- How does current drilling compare to optimal?
- What is the MSE sensitivity to parameter changes?

## Frequency

`per_analysis` (generated during MSE analysis periods)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the heatmap calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.heatmap_data` (array): Array of MSE values for parameter grid (inferred).
- `data.wob_bins` (array): WOB bin values for heatmap axes (inferred).
- `data.rpm_bins` (array): RPM bin values for heatmap axes (inferred).
- `data.optimal_wob` (float): WOB with lowest MSE (inferred).
- `data.optimal_rpm` (float): RPM with lowest MSE (inferred).
- `data.min_mse` (float): Minimum MSE value in heatmap (inferred).
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
  "data.optimal_wob": "float",
  "data.optimal_rpm": "float",
  "data.min_mse": "float",
  "data.hole_depth": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains MSE heatmap data for parameter optimization visualization.

## Keywords

`mse heatmap`, `drilling heatmap`, `parameter optimization`, `drilling efficiency`, `wob rpm analysis`, `drilling window`
