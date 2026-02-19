# Drilling Timelog Data (Well Optimization Timelog)

Drilling timelog data for well optimization. This collection contains structured time entries documenting drilling activities, operations, and events in a format suitable for time analysis and well performance optimization.

## When to use this dataset

- You need structured timelog entries for well operations.
- You want to analyze time distribution across activities.
- You need timelog data for well optimization analysis.
- You want to track operational efficiency over time.

## Example queries

### Alerting
- Alert when specific activity types are logged.
- Notify on long-duration activities.

### Visualization
- Display timelog timeline.
- Chart time distribution by activity.
- Show operational timeline with activities.

### Q&A
- What activities have been logged today?
- How much time was spent on each activity?
- What is the operational timeline?
- What are the major time consumers?

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

- `data.start_time` (long): Start time of the activity (inferred).
- `data.end_time` (long): End time of the activity (inferred).
- `data.duration` (int): Duration in seconds or minutes (inferred).
- `data.activity` (string): Activity description (inferred).
- `data.category` (string): Activity category (inferred).
- `data.depth` (float): Depth at time of entry (inferred).
- `data.comments` (string): Additional comments (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.start_time": "long",
  "data.end_time": "long",
  "data.duration": "int",
  "data.activity": "string",
  "data.category": "string",
  "data.depth": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains drilling timelog entries.

## Keywords

`timelog`, `drilling timelog`, `time analysis`, `activity log`, `well optimization`, `operational time`
