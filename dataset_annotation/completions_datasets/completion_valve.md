# Completion Valve (Valve Status Data)

Completion valve status and control data. This collection tracks valve positions, status changes, and control information during completion operations, particularly for zipper frac and simultaneous operations.

## When to use this dataset

- You need valve status information.
- You want to track valve positions during zipper operations.
- You need valve control data.
- You want to monitor valve changes.

## Example queries

### Alerting
- Alert on valve status changes.
- Notify on unexpected valve positions.

### Visualization
- Display valve status dashboard.
- Show valve position timeline.
- Track zipper valve coordination.

### Q&A
- What is the current valve status?
- When did the valve last change?
- What is the valve configuration?
- Are valves in correct position for current operation?

## Frequency

`per_change` (updated when valve status changes)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the valve status.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.valve_id` (string): Valve identifier (inferred).
- `data.valve_position` (string): Current valve position (inferred).
- `data.valve_status` (string): Valve operational status (inferred).
- `data.last_change` (long): Timestamp of last change (inferred).
- `data.operation_mode` (string): Current operation mode (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.valve_id": "string",
  "data.valve_position": "string",
  "data.valve_status": "string",
  "data.last_change": "long"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains valve status data.

## Keywords

`completion valve`, `valve status`, `zipper frac`, `valve control`, `valve position`
