# Wireline Activity Summary Stage (Wireline Activity Breakdown)

Stage-level wireline activity summary providing activity breakdown during wireline operations per stage.

## When to use this dataset

- You need wireline activity breakdown per stage.
- You want to analyze wireline time distribution.
- You need activity tracking for wireline operations.

## Example queries

### Alerting
- Alert when wireline activity exceeds duration.

### Visualization
- Display wireline activity timeline.
- Show activity breakdown.

### Q&A
- What activities occurred during wireline operations?
- How long was each wireline phase?
- What was the rig up time?

## Frequency

`per_stage` (one record per stage)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp.
- `asset_id`: Unique ID of the asset (well).
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields

- `data.activities` (array): Array of activity objects with:
  - `activity` (string): Activity name (e.g., "Rig Up", "Run In Hole", "Correlate", "Perf", "Pull Out of Hole", "Rig Down").
  - `start` (long): Start timestamp.
  - `end` (long): End timestamp.
  - `duration` (int): Duration in seconds.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.activities": "array"
}
```

## Sample record

Note: Sample record not available in source documentation. Structure similar to completion.activity.summary-stage.

## Keywords

`wireline activity`, `wireline summary`, `wireline breakdown`, `perforating activities`, `wireline operations`
