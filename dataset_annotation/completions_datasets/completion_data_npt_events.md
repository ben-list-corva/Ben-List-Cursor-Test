# Completion Data NPT Events (Completion Non-Productive Time)

Non-productive time events during completion operations. This collection records downtime events during frac, wireline, and other completion operations that did not contribute to well progress.

## When to use this dataset

- You need NPT tracking for completions.
- You want to analyze completion downtime.
- You need to categorize completion delays.
- You want to track completion efficiency.

## Example queries

### Alerting
- Alert when NPT event is recorded.
- Notify on NPT exceeding threshold.

### Visualization
- Display NPT timeline for completion.
- Show NPT breakdown by category.
- Chart NPT trends.

### Q&A
- What NPT events occurred during completions?
- How much total NPT was recorded?
- What caused the delays?
- How does NPT compare to other wells?

## Frequency

`per_event` (one record per NPT event)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the NPT event.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.start_time` (long): NPT start time (inferred).
- `data.end_time` (long): NPT end time (inferred).
- `data.duration` (int): NPT duration (inferred).
- `data.type` (string): NPT category (inferred).
- `data.description` (string): NPT description (inferred).
- `data.stage_number` (int): Associated stage number (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.start_time": "long",
  "data.end_time": "long",
  "data.duration": "int",
  "data.type": "string",
  "data.description": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains completion NPT events.

## Keywords

`completion npt`, `frac downtime`, `completion delays`, `non productive time`, `completion efficiency`
