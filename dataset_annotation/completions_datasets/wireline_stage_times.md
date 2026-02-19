# Wireline Stage Times (Wireline Timing Data)

Wireline stage timing and duration data. This collection provides start time, end time, and duration for wireline operations per stage.

## When to use this dataset

- You need wireline operation timing.
- You want to calculate wireline durations.
- You need timing data for schedule analysis.
- You want to track wireline progression.

## Example queries

### Alerting
- Alert when wireline duration exceeds threshold.
- Notify when wireline operation completes.

### Visualization
- Display wireline timeline.
- Show wireline duration trends.
- Chart actual vs planned timing.

### Q&A
- When did the wireline run start and end?
- How long was the wireline operation?
- How does timing compare to plan?

## Frequency

`per_stage` (one record per wireline run per stage)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the wireline operation start.
- `asset_id`: Unique ID of the asset (well).
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields

- `data.stage_start` (long): Wireline operation start time.
- `data.stage_end` (long): Wireline operation end time.
- `data.stage_duration` (int): Duration in seconds.
- `data.run_type` (string): Type of wireline run (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.stage_start": "long",
  "data.stage_end": "long",
  "data.stage_duration": "int"
}
```

## Sample record

Note: Sample record not available in source documentation. Structure similar to completion.stage-times.

## Keywords

`wireline times`, `wireline duration`, `wireline timing`, `perforating time`, `wireline schedule`
