# Completion Stage Times (Stage Timing Data)

Stage timing and duration data. This collection provides start time, end time, and duration for each frac stage, enabling time-based analysis and scheduling comparisons.

## When to use this dataset

- You need stage start/end times.
- You want to calculate stage durations.
- You need timing data for schedule analysis.
- You want to track stage progression.

## Example queries

### Alerting
- Alert when stage duration exceeds threshold.
- Notify when stage completes.

### Visualization
- Display stage timeline.
- Show stage duration trends.
- Chart actual vs planned timing.

### Q&A
- When did this stage start and end?
- How long was the stage duration?
- How does this stage duration compare to others?
- What is the average stage time?

## Frequency

`per_stage` (one record per stage)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the stage start.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of stage start.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.
- `app_key` (string): Application that generated the record.

### `data` fields

- `data.stage_start` (long): Unix/epoch timestamp of stage start.
- `data.stage_end` (long): Unix/epoch timestamp of stage end.
- `data.stage_duration` (int): Stage duration in seconds.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "app_key": "string",
  "data.stage_start": "long",
  "data.stage_end": "long",
  "data.stage_duration": "int"
}
```

## Sample record

```json
{
  "_id": "example_completion_stage-times",
  "company_id": 81,
  "asset_id": 12345,
  "version": 1,
  "provider": "corva",
  "collection": "completion.stage-times",
  "data": {
    "stage_start": 1768760581,
    "stage_end": 1768975306,
    "stage_duration": 214725
  },
  "timestamp": 1768760581,
  "app_key": "corva.completion-engineering",
  "stage_number": 1
}
```

## Keywords

`stage times`, `stage duration`, `stage timing`, `frac schedule`, `stage start end`
