# Wireline WITS (Real-Time Wireline Data)

Real-time WITS data for wireline operations. This collection contains sensor measurements during wireline perforating and logging operations including depth, tension, speed, and CCL (casing collar locator) data.

## When to use this dataset

- You need real-time wireline operation data.
- You want to monitor wireline depth and tension.
- You need CCL correlation data.
- You want to track wireline runs.

## Example queries

### Alerting
- Alert when wireline tension exceeds threshold.
- Notify when approaching target depth.
- Alert on wireline anomalies.

### Visualization
- Plot wireline depth and tension vs time.
- Display CCL signature.
- Chart wireline run progress.

### Q&A
- What is the current wireline depth?
- What is the cable tension?
- Where is the CCL relative to depth?
- What is the wireline speed?

## Frequency

`per_second` (real-time during wireline operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the data point.
- `asset_id`: Unique ID of the asset (well).
- `stage_number`: Stage number (if applicable).

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields (inferred from domain knowledge)

- `data.wireline_depth` (float): Current wireline depth (inferred).
- `data.cable_tension` (float): Cable tension (inferred).
- `data.line_speed` (float): Wireline speed (inferred).
- `data.ccl` (float): CCL signal value (inferred).
- `data.gamma_ray` (float): Gamma ray reading (inferred).
- `data.direction` (string): Run direction (in/out) (inferred).
- `data.elapsed_time` (int): Elapsed time (inferred).

Note: This dataset may contain many dynamic/custom fields that vary by operator.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.wireline_depth": "float",
  "data.cable_tension": "float",
  "data.line_speed": "float",
  "data.ccl": "float",
  "data.gamma_ray": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains wireline operation sensor data.

## Keywords

`wireline wits`, `wireline data`, `perforating`, `ccl`, `cable tension`, `wireline depth`, `logging`
