# Hydraulics Pressure Trend (Circulating Pressure Trends)

Pressure trend analysis for monitoring circulating pressure behavior over time. This collection tracks standpipe pressure trends to identify changes that may indicate downhole issues such as washouts, plugged nozzles, or formation changes.

## When to use this dataset

- You need to monitor standpipe pressure trends.
- You want to detect pressure anomalies during drilling.
- You need to identify potential downhole issues.
- You want to track circulating pressure history.

## Example queries

### Alerting
- Alert on sudden pressure changes.
- Notify when pressure trend indicates potential washout.
- Alert when pressure deviates from baseline.

### Visualization
- Plot pressure trend over time.
- Chart predicted vs actual pressure trend.
- Show pressure anomaly detection.
- Display rolling pressure averages.

### Q&A
- Is the standpipe pressure trending normally?
- Are there any pressure anomalies?
- Has there been a sudden pressure change?
- What is the pressure baseline for current conditions?

## Frequency

`per_interval` (tracked continuously during circulation)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the trend data point.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the data point.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.standpipe_pressure` (float): Current standpipe pressure (inferred).
- `data.predicted_pressure` (float): Predicted/expected pressure (inferred).
- `data.pressure_deviation` (float): Deviation from predicted (inferred).
- `data.trend_direction` (string): Pressure trend direction (inferred).
- `data.baseline_pressure` (float): Baseline pressure for comparison (inferred).
- `data.flow_rate` (float): Flow rate at measurement (inferred).
- `data.hole_depth` (float): Hole depth at measurement (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.standpipe_pressure": "float",
  "data.predicted_pressure": "float",
  "data.pressure_deviation": "float",
  "data.trend_direction": "string",
  "data.baseline_pressure": "float",
  "data.flow_rate": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains circulating pressure trend analysis.

## Keywords

`pressure trend`, `circulating pressure`, `standpipe pressure`, `pressure monitoring`, `pressure anomaly`, `washout detection`
