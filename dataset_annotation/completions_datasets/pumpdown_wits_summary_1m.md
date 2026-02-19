# Pumpdown WITS Summary 1m (1-Minute Pumpdown Data)

1-minute aggregated pumpdown WITS data. This collection provides statistical summaries of pumpdown parameters over 1-minute intervals for trend analysis.

## When to use this dataset

- You need aggregated pumpdown data.
- You want lower-resolution pumpdown trends.
- You need statistical summaries for analysis.

## Example queries

### Alerting
- Alert on minute-level anomalies.

### Visualization
- Plot pumpdown trends.
- Show aggregated pressure and rate.

### Q&A
- What were the average parameters?
- What is the pumpdown trend?

## Frequency

`per_minute` (one record per 1-minute interval)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the interval end.
- `asset_id`: Unique ID of the asset (well).
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields

- `data.min` (object): Minimum values for the interval.
- `data.max` (object): Maximum values for the interval.
- `data.mean` (object): Mean values for the interval.
- `data.start_timestamp` (long): Interval start.
- `data.end_timestamp` (long): Interval end.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.min": "object",
  "data.max": "object",
  "data.mean": "object"
}
```

## Sample record

Note: Sample record not available in source documentation. Structure similar to completion.wits.summary-1m.

## Keywords

`pumpdown summary`, `pumpdown aggregated`, `pumpdown trend`, `1 minute pumpdown`
