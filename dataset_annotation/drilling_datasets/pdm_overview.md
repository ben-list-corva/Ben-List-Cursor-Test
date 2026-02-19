# PDM Overview (Motor Performance Summary)

PDM (Positive Displacement Motor / Drilling Motor) performance overview data. This collection provides summary metrics for mud motor performance including differential pressure status, severity indicators, and trend data for monitoring motor health during drilling operations.

## When to use this dataset

- You need a quick overview of PDM/motor status.
- You want to monitor differential pressure severity.
- You need motor performance trend data.
- You want to assess motor operating conditions.

## Example queries

### Alerting
- Alert when differential pressure severity increases.
- Notify when PDM approaches operational limits.
- Alert on motor performance degradation.

### Visualization
- Display PDM status dashboard.
- Show differential pressure trend.
- Chart motor performance over time.

### Q&A
- What is the current motor status?
- Is the differential pressure within limits?
- What is the trend in motor performance?
- Is there evidence of motor wear?

## Frequency

`per_interval` (updated at regular intervals during drilling)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the PDM overview record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.differential_pressure` (object): Differential pressure assessment.
  - `data.differential_pressure.value` (float): Current differential pressure value.
  - `data.differential_pressure.percentage` (float): Percentage of operating limit.
  - `data.differential_pressure.severity` (string): Severity level ("low", "medium", "high").
  - `data.differential_pressure.points` (array): Historical data points with timestamp, value, percentage, and severity.
- `data.status` (int): Overall status indicator.
- `data.warning` (object): Warning information if applicable.
  - `data.warning.stale` (boolean): Whether data is stale.
  - `data.warning.last_updated_at` (string): Last update timestamp.
  - `data.warning.code` (string): Warning code.
  - `data.warning.message` (string): Warning message.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.differential_pressure": "object",
  "data.differential_pressure.value": "float",
  "data.differential_pressure.percentage": "float",
  "data.differential_pressure.severity": "string",
  "data.differential_pressure.points": "array",
  "data.status": "int",
  "data.warning": "object"
}
```

## Sample record

```json
{
  "_id": "example_pdm_overview",
  "version": 1,
  "provider": "corva",
  "collection": "pdm.overview",
  "timestamp": 1768920599,
  "data": {
    "differential_pressure": {
      "points": [
        {
          "timestamp": 1768911640,
          "value": 0,
          "percentage": 0,
          "severity": "low"
        }
      ],
      "value": 0,
      "percentage": 0,
      "severity": "low"
    },
    "status": 1,
    "warning": {
      "stale": true,
      "last_updated_at": "1768920580",
      "code": "not_available_during_running_casing",
      "message": "The current status is running casing/liner, at which time the results of this app are not available."
    }
  },
  "asset_id": 12345,
  "company_id": 81
}
```

## Keywords

`pdm overview`, `mud motor`, `drilling motor`, `differential pressure`, `motor performance`, `pdm status`
