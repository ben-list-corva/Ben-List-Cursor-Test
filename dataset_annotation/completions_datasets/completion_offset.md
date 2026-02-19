# Completion Offset (Offset Well Pressure Data)

Offset well pressure data during completion operations. This collection contains pressure readings from offset/neighboring wells during frac operations, enabling monitoring of frac hits and communication between wells.

## When to use this dataset

- You need offset well pressure monitoring.
- You want to detect frac hits on offset wells.
- You need to monitor well-to-well communication.
- You want to analyze zipper frac interference.

## Example queries

### Alerting
- Alert when offset pressure increases unexpectedly.
- Notify on potential frac hit detection.

### Visualization
- Plot offset well pressures during frac.
- Show pressure correlation between wells.
- Display frac hit analysis.

### Q&A
- What is the pressure on offset wells?
- Is there evidence of frac communication?
- When did the offset pressure spike?
- Which offset wells are being monitored?

## Frequency

`per_second` (real-time during frac operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the pressure reading.
- `asset_id`: Unique ID of the primary asset (well).

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Primary well asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.offset_well_id` (int): Offset well asset ID (inferred).
- `data.offset_pressure` (float): Offset well pressure reading (inferred).
- `data.offset_well_name` (string): Offset well name (inferred).
- `data.pressure_change` (float): Pressure change from baseline (inferred).
- `data.frac_hit_indicator` (boolean): Frac hit detection flag (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.offset_well_id": "int",
  "data.offset_pressure": "float",
  "data.offset_well_name": "string",
  "data.pressure_change": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains offset well pressure monitoring data.

## Keywords

`completion offset`, `offset pressure`, `frac hit`, `well communication`, `offset monitoring`, `zipper frac`
