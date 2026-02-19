# Kick Detection (Well Control Monitoring)

Kick detection and well control monitoring data. This collection contains real-time kick detection analysis monitoring for influx of formation fluids into the wellbore. Essential for well control and early kick detection.

## When to use this dataset

- You need kick detection monitoring data.
- You want to assess well control status.
- You need early warning of influx events.
- You want to monitor pit volume changes.

## Example queries

### Alerting
- Alert on potential kick indication.
- Notify when pit volume increases unexpectedly.
- Alert on flow check anomalies.

### Visualization
- Display kick detection status.
- Show pit volume trend monitoring.
- Chart flow in vs flow out.

### Q&A
- Is there any kick indication?
- What is the current well control status?
- Are there any pit volume anomalies?
- What is the trend in gain/loss?

## Frequency

`per_second` (real-time monitoring)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the kick detection record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.active_string_type` (string): Type of active string in hole (e.g., "casing", "drillstring").
- `data.active_string_id` (string): ID of the active string configuration.
- `data.drillstring_number` (int): Drillstring identifier (may be null).
- `data.warning` (object): Warning information if applicable.
  - `data.warning.message` (string): Warning message about kick detection availability.
- `data.kick_indicators` (object): Kick indicator values (inferred).
- `data.pit_volume_change` (float): Change in pit volume (inferred).
- `data.flow_check_status` (string): Flow check status (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.active_string_type": "string",
  "data.active_string_id": "string",
  "data.drillstring_number": "int",
  "data.warning": "object"
}
```

## Sample record

```json
{
  "_id": "example_kick-detection",
  "version": 1,
  "provider": "corva",
  "collection": "kick-detection",
  "timestamp": 1768920599,
  "company_id": 81,
  "asset_id": 12345,
  "data": {
    "active_string_type": "casing",
    "active_string_id": "696a9452aba9ff3e2971d213",
    "drillstring_number": null,
    "warning": {
      "message": "This module does not run while casing is the active string in the well."
    }
  }
}
```

## Keywords

`kick detection`, `well control`, `influx`, `pit volume`, `early kick detection`, `well safety`
