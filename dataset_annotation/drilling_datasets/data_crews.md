# Crews (Crew Information and Shifts)

Crew information and shift data. This collection contains information about the rig crews, shift schedules, and personnel assignments. Used for attributing performance metrics to specific crews and analyzing operational patterns by shift.

## When to use this dataset

- You need to identify which crew is on duty.
- You want to analyze performance by crew or shift.
- You need crew information for operational reports.
- You want to correlate activities with crew assignments.
- You need to track crew rotations.

## Example queries

### Alerting
- Alert on crew change events.
- Notify when specific crew comes on duty.

### Visualization
- Show crew schedule timeline.
- Chart performance metrics by crew.
- Display crew rotation calendar.

### Q&A
- Which crew is currently on duty?
- What is the crew rotation schedule?
- How does performance compare between crews?
- When is the next crew change?

## Frequency

`per_crew` (one record per crew or shift definition)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the crew record was created.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.name`: Name of the crew or shift.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.name` (string): Crew or shift name.
- `data.shift_start` (string): Shift start time (inferred).
- `data.shift_end` (string): Shift end time (inferred).
- `data.crew_type` (string): Type of crew (day/night) (inferred).
- `data.members` (array): Crew member list (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.name": "string",
  "data.shift_start": "string",
  "data.shift_end": "string",
  "data.crew_type": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains crew and shift information.

## Keywords

`crews`, `shift`, `personnel`, `crew rotation`, `day shift`, `night shift`, `rig crew`
