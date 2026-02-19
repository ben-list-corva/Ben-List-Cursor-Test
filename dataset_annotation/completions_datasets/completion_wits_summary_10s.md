# Completion WITS Summary 10s (10-Second Aggregated Data)

10-second aggregated completion WITS data. This collection provides statistical summaries (min, max, mean, median) of frac parameters over 10-second intervals, reducing data volume while preserving key statistics for analysis.

## When to use this dataset

- You need aggregated frac data at 10-second resolution.
- You want statistical summaries of treatment parameters.
- You need lower-resolution data for trend analysis.
- You want min/max/mean values for quality checks.

## Example queries

### Alerting
- Alert when parameter ranges exceed thresholds.
- Notify on statistical anomalies.

### Visualization
- Plot treatment curves with reduced data density.
- Show parameter ranges over time.
- Chart statistical trends.

### Q&A
- What was the pressure range during this period?
- What is the average pump rate over time?
- How variable were the parameters?

## Frequency

`per_10_seconds` (one record per 10-second interval)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the 10-second interval end.
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
- `data.start_timestamp` (long): Start of the 10-second interval.
- `data.end_timestamp` (long): End of the 10-second interval.

Each statistics object contains the same fields as completion.wits including:
- `wellhead_pressure`, `backside_pressure`
- `clean_flow_rate_in`, `slurry_flow_rate_in`
- `total_clean_volume_in`, `total_slurry_volume_in`
- `total_proppant_concentration`, `total_proppant_mass`
- `hydraulic_horse_power`, `elapsed_time`
- And other standard/dynamic fields

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

```json
{
  "_id": "example_completion_wits_summary-10s",
  "company_id": 81,
  "asset_id": 12345,
  "version": 1,
  "provider": "corva",
  "collection": "completion.wits.summary-10s",
  "data": {
    "min": {
      "wellhead_pressure": 9525,
      "slurry_flow_rate_in": 83.9,
      "total_proppant_concentration": 0.24
    },
    "max": {
      "wellhead_pressure": 9548,
      "slurry_flow_rate_in": 84,
      "total_proppant_concentration": 0.25
    },
    "mean": {
      "wellhead_pressure": 9537.5,
      "slurry_flow_rate_in": 83.98,
      "total_proppant_concentration": 0.247
    },
    "start_timestamp": 1768975300,
    "end_timestamp": 1768975309
  },
  "timestamp": 1768975309,
  "stage_number": 1
}
```

## Keywords

`completion wits summary`, `10 second summary`, `aggregated frac data`, `frac statistics`, `min max mean`
