# NPT Events (Non-Productive Time Events)

Non-Productive Time (NPT) events data. This collection records downtime events that do not contribute to well progress, including equipment failures, waiting on weather, stuck pipe incidents, well control events, and other operational delays. Essential for efficiency analysis and lessons learned.

## When to use this dataset

- You need to track non-productive time during drilling.
- You want to analyze causes of operational delays.
- You need to calculate invisible lost time and NPT percentages.
- You want to identify recurring problem areas.
- You need NPT data for well cost analysis.
- You want to generate lessons learned from incidents.

## Example queries

### Alerting
- Alert when NPT event is recorded.
- Notify on NPT events exceeding certain duration.
- Alert on repeated NPT events of same type.

### Visualization
- Plot NPT events on well timeline.
- Chart NPT breakdown by category.
- Show cumulative NPT vs depth.
- Display NPT Pareto analysis.

### Q&A
- What NPT events have occurred on this well?
- What is the total NPT for this well?
- What category has the most NPT?
- What was the longest NPT event?
- How does NPT compare to offset wells?

## Frequency

`per_event` (one record per NPT event)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the NPT event.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.start_time`, `data.end_time`, `data.depth`, `data.type`: Composite key for unique identification.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.start_time` (long): Start time of the NPT event.
- `data.end_time` (long): End time of the NPT event.
- `data.duration` (int): Duration of NPT in seconds or minutes.
- `data.depth` (float): Depth at which NPT occurred.
- `data.type` (string): NPT category/type (e.g., "Equipment Failure", "Stuck Pipe", "Weather").
- `data.subtype` (string): More specific NPT classification (inferred).
- `data.description` (string): Detailed description of the event.
- `data.cause` (string): Root cause analysis (inferred).
- `data.cost` (float): Cost associated with NPT (inferred).
- `data.severity` (string): Severity level (inferred).
- `data.preventable` (boolean): Whether event was preventable (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.start_time": "long",
  "data.end_time": "long",
  "data.duration": "int",
  "data.depth": "float",
  "data.type": "string",
  "data.subtype": "string",
  "data.description": "string",
  "data.cause": "string",
  "data.cost": "float",
  "data.severity": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains NPT event records with timing and categorization.

## Keywords

`npt`, `non-productive time`, `downtime`, `lost time`, `npt events`, `drilling delays`, `equipment failure`, `stuck pipe`
