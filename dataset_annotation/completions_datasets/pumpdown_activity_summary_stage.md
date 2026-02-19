# Pumpdown Activity Summary Stage (Pumpdown Activity Breakdown)

Stage-level pumpdown activity summary providing activity breakdown during pumpdown operations per stage.

## When to use this dataset

- You need pumpdown activity breakdown per stage.
- You want to analyze pumpdown time distribution.
- You need activity tracking for pumpdown operations.

## Example queries

### Alerting
- Alert when pumpdown activity exceeds duration.

### Visualization
- Display pumpdown activity timeline.
- Show activity breakdown.

### Q&A
- What activities occurred during pumpdown?
- How long was each pumpdown phase?

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
  - `activity` (string): Activity name.
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

`pumpdown activity`, `pumpdown summary`, `pumpdown breakdown`, `stage pumpdown`
