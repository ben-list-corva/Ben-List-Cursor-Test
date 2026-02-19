# Completion Data Time Log (Completion Timelog)

Completion operation time log data. This collection contains structured time entries for completion activities, similar to drilling timelogs but focused on completion operations.

## When to use this dataset

- You need completion activity timelog.
- You want to track completion time breakdown.
- You need time log entries for reporting.
- You want to analyze time spent on activities.

## Example queries

### Alerting
- Alert on timelog entries for specific activities.
- Notify when activity duration exceeds threshold.

### Visualization
- Display completion timelog.
- Show activity breakdown.
- Chart time distribution.

### Q&A
- What activities were logged today?
- How much time was spent on each activity?
- What is in the completion timelog?

## Frequency

`per_entry` (one record per timelog entry)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the timelog entry.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the entry.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.activity` (string): Activity description (inferred).
- `data.start_time` (long): Activity start time (inferred).
- `data.end_time` (long): Activity end time (inferred).
- `data.duration` (int): Activity duration (inferred).
- `data.stage_number` (int): Associated stage number (inferred).
- `data.comments` (string): Additional comments (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.activity": "string",
  "data.start_time": "long",
  "data.end_time": "long",
  "data.duration": "int"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains completion timelog entries.

## Keywords

`completion time log`, `completion activities`, `activity log`, `time tracking`, `completion timelog`
