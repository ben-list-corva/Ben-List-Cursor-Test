# Completion Tracking (Operational Tracking Data)

Completion operation tracking data. This collection tracks the overall progress and status of completion operations including current stage, operational state, and tracking metrics.

## When to use this dataset

- You need to track completion operation progress.
- You want to know the current operational state.
- You need completion status information.
- You want to monitor operation progression.

## Example queries

### Alerting
- Alert on operation status changes.
- Notify when specific milestones are reached.

### Visualization
- Display completion progress dashboard.
- Show current operation status.
- Track stage progression.

### Q&A
- What stage is currently being completed?
- What is the current operation status?
- How many stages have been completed?
- What is the overall completion progress?

## Frequency

`per_update` (updated as operations progress)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the tracking record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.current_stage` (int): Current stage number (inferred).
- `data.total_stages` (int): Total planned stages (inferred).
- `data.status` (string): Current operational status (inferred).
- `data.completion_type` (string): Type of completion operation (inferred).
- `data.progress_percentage` (float): Completion progress percentage (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.current_stage": "int",
  "data.total_stages": "int",
  "data.status": "string",
  "data.completion_type": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains completion operation tracking data.

## Keywords

`completion tracking`, `operation tracking`, `stage progress`, `completion status`, `frac tracking`
