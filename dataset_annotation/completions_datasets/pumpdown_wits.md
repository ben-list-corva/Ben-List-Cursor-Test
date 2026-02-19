# Pumpdown WITS (Real-Time Pumpdown Data)

Real-time WITS data for pumpdown operations. This collection contains sensor measurements during plug deployment and pumpdown operations, tracking pump rates, pressures, and ball/dart status as plugs are pumped to setting depth.

## When to use this dataset

- You need real-time pumpdown operation data.
- You want to monitor plug deployment.
- You need pressure and rate data during pumpdown.
- You want to track ball/dart progress.

## Example queries

### Alerting
- Alert when pump rate drops unexpectedly.
- Notify when pressure indicates plug set.
- Alert on pumpdown anomalies.

### Visualization
- Plot pumpdown treatment curve.
- Display plug tracking progress.
- Chart pressure and rate vs time.

### Q&A
- What is the current pumpdown status?
- Has the plug reached setting depth?
- What is the current pump rate and pressure?
- How long until plug sets?

## Frequency

`per_second` (real-time during pumpdown)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the data point.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `stage_number`: Current stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the data point.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields (inferred from domain knowledge)

- `data.wellhead_pressure` (float): Wellhead pressure (inferred).
- `data.pump_rate` (float): Pump rate (inferred).
- `data.total_volume` (float): Total volume pumped (inferred).
- `data.ball_depth` (float): Estimated ball/plug depth (inferred).
- `data.strokes` (int): Pump strokes (inferred).
- `data.plug_status` (string): Plug deployment status (inferred).
- `data.elapsed_time` (int): Elapsed time (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.wellhead_pressure": "float",
  "data.pump_rate": "float",
  "data.total_volume": "float",
  "data.ball_depth": "float",
  "data.plug_status": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains pumpdown operation sensor data.

## Keywords

`pumpdown wits`, `pumpdown data`, `plug deployment`, `frac plug`, `ball drop`, `pumpdown monitoring`
