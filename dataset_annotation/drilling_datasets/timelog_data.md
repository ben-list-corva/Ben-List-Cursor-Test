# Timelog Data (General Time Analysis)

General timelog data for time analysis. This collection contains time-based activity logs that can be used for analyzing operational time distribution and identifying opportunities for efficiency improvements.

## When to use this dataset

- You need general timelog entries for operations.
- You want to perform time analysis across activities.
- You need activity tracking data.
- You want to analyze operational patterns.

## Example queries

### Alerting
- Alert on new timelog entries.
- Notify on unusual activity durations.

### Visualization
- Display activity timeline.
- Chart time breakdown by category.
- Show operational summary.

### Q&A
- What activities occurred during a time period?
- How is time distributed across operations?
- What are the longest activities?
- How does time usage compare to plan?

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

- `data.start_time` (long): Start time of entry (inferred).
- `data.end_time` (long): End time of entry (inferred).
- `data.activity` (string): Activity name/description (inferred).
- `data.duration` (int): Duration in seconds (inferred).
- `data.depth` (float): Associated depth (inferred).
- `data.notes` (string): Additional notes (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.start_time": "long",
  "data.end_time": "long",
  "data.activity": "string",
  "data.duration": "int",
  "data.depth": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains general timelog entries.

## Keywords

`timelog`, `time analysis`, `activity tracking`, `operational time`, `time log`
