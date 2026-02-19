# Completion Activity Summary Stage (Stage Activity Breakdown)

Stage-level activity summary providing a breakdown of activities performed during each frac stage. This collection contains detected activities with their timing, enabling analysis of time distribution across different phase of the frac treatment.

## When to use this dataset

- You need activity breakdown per stage.
- You want to analyze time distribution across activities.
- You need to identify activity patterns.
- You want to compare activity timing across stages.

## Example queries

### Alerting
- Alert when specific activity exceeds duration threshold.
- Notify on unusual activity sequences.

### Visualization
- Display stage activity timeline.
- Show activity distribution pie chart.
- Chart activity durations across stages.

### Q&A
- What activities occurred during this stage?
- How much time was spent fracturing vs testing?
- What was the pad time?
- How does activity distribution compare across stages?

## Frequency

`per_stage` (one record per stage with activity array)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the stage.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields

- `data.activities` (array): Array of activity objects. Each activity contains:
  - `activity` (string): Activity name (e.g., "Pressure Testing", "Pad", "Fracturing", "Flush", "Pump Off").
  - `start` (long): Activity start timestamp.
  - `end` (long): Activity end timestamp.
  - `duration` (int): Activity duration in seconds.

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

```json
{
  "_id": "example_completion_activity_summary-stage",
  "company_id": 81,
  "asset_id": 12345,
  "version": 2,
  "provider": "corva",
  "collection": "completion.activity.summary-stage",
  "data": {
    "activities": [
      {
        "activity": "Pressure Testing",
        "start": 1768760581,
        "end": 1768783631,
        "duration": 23050
      },
      {
        "activity": "Pad",
        "start": 1768783632,
        "end": 1768784089,
        "duration": 457
      },
      {
        "activity": "Fracturing",
        "start": 1768784090,
        "end": 1768792435,
        "duration": 8345
      },
      {
        "activity": "Flush",
        "start": 1768792436,
        "end": 1768792694,
        "duration": 258
      },
      {
        "activity": "Pump Off",
        "start": 1768792695,
        "end": 1768792900,
        "duration": 205
      }
    ]
  },
  "timestamp": 1768760581,
  "stage_number": 1
}
```

## Keywords

`activity summary`, `stage activities`, `frac activities`, `pressure testing`, `fracturing`, `flush`, `pump off`
