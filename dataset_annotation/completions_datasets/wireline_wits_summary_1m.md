# Wireline WITS Summary 1m (1-Minute Wireline Data)

1-minute aggregated wireline WITS data. This collection provides statistical summaries of wireline parameters over 1-minute intervals for trend analysis.

## When to use this dataset

- You need aggregated wireline data.
- You want lower-resolution wireline trends.
- You need statistical summaries for analysis.

## Example queries

### Alerting
- Alert on minute-level anomalies.

### Visualization
- Plot wireline trends.
- Show aggregated depth and tension.

### Q&A
- What were the average parameters?
- What is the wireline trend?

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

`wireline summary`, `wireline aggregated`, `wireline trend`, `1 minute wireline`
