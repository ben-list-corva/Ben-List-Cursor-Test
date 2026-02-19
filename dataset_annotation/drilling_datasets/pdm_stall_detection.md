# PDM Stall Detection (Motor Stall Events)

PDM stall detection events and analysis. This collection records motor stall events detected during drilling, including stall characteristics and conditions that led to the stall. Used for motor protection, drilling optimization, and post-run analysis.

## When to use this dataset

- You need to track motor stall events.
- You want to analyze stall conditions.
- You need stall history for motor performance evaluation.
- You want to optimize parameters to avoid stalls.

## Example queries

### Alerting
- Alert when motor stall is detected.
- Notify on repeated stall events.
- Alert when approaching stall conditions.

### Visualization
- Display stall event timeline.
- Chart stall frequency over time.
- Show stall conditions on motor operating envelope.

### Q&A
- How many stalls have occurred on this run?
- What conditions caused the last stall?
- What is the stall frequency trend?
- When did the last stall occur?

## Frequency

`per_event` (one record per detected stall event)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the stall detection.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the stall event.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.total_bit_torque` (float): Total bit torque at stall.
- `data.differential_pressure` (float): Differential pressure at stall (inferred).
- `data.flow_rate` (float): Flow rate at stall (inferred).
- `data.bit_depth` (float): Bit depth at stall (inferred).
- `data.hole_depth` (float): Hole depth at stall (inferred).
- `data.duration` (int): Stall duration in seconds (inferred).
- `data.severity` (string): Stall severity (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.total_bit_torque": "float",
  "data.differential_pressure": "float",
  "data.flow_rate": "float",
  "data.bit_depth": "float",
  "data.hole_depth": "float",
  "data.duration": "int"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains PDM stall detection events.

## Keywords

`pdm stall`, `motor stall`, `stall detection`, `motor protection`, `stall event`, `drilling motor`
