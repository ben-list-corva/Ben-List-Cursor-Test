# Circulation Lag Depth (Formation Returns Tracking)

Lag depth calculations for tracking where formation returns currently at surface originated from. This collection calculates the depth origin of cuttings currently being circulated to surface based on pump strokes and volumes.

## When to use this dataset

- You need to know what depth cuttings at shakers came from.
- You want to correlate surface samples with depth.
- You need lag depth for gas shows correlation.
- You want to track formation returns during drilling.
- You need to correlate mud log data with depth.

## Example queries

### Alerting
- Alert when lag depth reaches target formation.
- Notify when returns from specific depth arrive.

### Visualization
- Display current lag depth indicator.
- Show lag depth vs time.
- Chart formation returns timeline.
- Overlay lag depth on gamma ray logs.

### Q&A
- What depth are current shaker returns from?
- When will returns from the current bit depth arrive?
- What is the current lag time?
- At what depth did we encounter the gas show?

## Frequency

`per_interval` (continuously updated during circulation)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the lag depth calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.lag_depth` (float): Current lag depth - where surface returns originated (inferred).
- `data.bit_depth` (float): Current bit depth (inferred).
- `data.lag_strokes` (int): Number of strokes since depth was drilled (inferred).
- `data.lag_time` (int): Time lag in seconds (inferred).
- `data.lag_volume` (float): Volume lag (inferred).
- `data.flow_rate` (float): Current flow rate (inferred).
- `data.cumulative_strokes` (long): Total pump strokes (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.lag_depth": "float",
  "data.bit_depth": "float",
  "data.lag_strokes": "int",
  "data.lag_time": "int",
  "data.lag_volume": "float",
  "data.flow_rate": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains lag depth calculations for correlating surface returns with formation depth.

## Keywords

`lag depth`, `circulation lag`, `formation returns`, `cuttings lag`, `mud logging`, `sample depth`, `gas show correlation`
