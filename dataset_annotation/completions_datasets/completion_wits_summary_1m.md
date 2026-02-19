# Completion WITS Summary 1m (1-Minute Aggregated Data)

1-minute aggregated completion WITS data. This collection provides statistical summaries of frac parameters over 1-minute intervals, further reducing data volume for longer-term trend analysis and historical reviews.

## When to use this dataset

- You need aggregated frac data at 1-minute resolution.
- You want statistical summaries for trend analysis.
- You need lower-resolution data for historical review.
- You want to analyze treatment performance over time.

## Example queries

### Alerting
- Alert on minute-level anomalies.
- Notify when trends indicate problems.

### Visualization
- Plot long-term treatment trends.
- Show stage-level parameter trends.
- Chart historical treatment analysis.

### Q&A
- What was the average pressure during the stage?
- How did pump rate vary over time?
- What were the parameter ranges for the treatment?

## Frequency

`per_minute` (one record per 1-minute interval)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the 1-minute interval end.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `stage_number`: Current frac stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the interval end.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Current stage number.

### `data` fields

- `data.min` (object): Minimum values for all parameters in the interval.
- `data.max` (object): Maximum values for all parameters in the interval.
- `data.mean` (object): Mean values for all parameters in the interval.
- `data.median` (object): Median values for all parameters in the interval.
- `data.start_timestamp` (long): Start of the 1-minute interval.
- `data.end_timestamp` (long): End of the 1-minute interval.

Each statistics object contains the same fields as completion.wits.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.min": "object",
  "data.max": "object",
  "data.mean": "object",
  "data.median": "object",
  "data.start_timestamp": "long",
  "data.end_timestamp": "long"
}
```

## Sample record

Note: Structure is similar to completion.wits.summary-10s but aggregated over 1-minute intervals.

## Keywords

`completion wits summary`, `1 minute summary`, `aggregated frac data`, `minute resolution`, `frac trend`
