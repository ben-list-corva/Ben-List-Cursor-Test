# Completion Metrics (Calculated KPIs)

Completion operation calculated metrics and KPIs. This collection contains computed performance indicators for completion operations including efficiency metrics, time analysis, and stage performance summaries.

## When to use this dataset

- You need completion performance KPIs.
- You want to analyze operational efficiency.
- You need aggregated completion metrics.
- You want to compare performance across wells.

## Example queries

### Alerting
- Alert when metrics fall below threshold.
- Notify on performance changes.

### Visualization
- Display completion KPI dashboard.
- Show metrics comparison charts.
- Chart performance trends.

### Q&A
- What is the average stage time?
- What are the efficiency metrics?
- How does this well compare to others?
- What are the key performance indicators?

## Frequency

`per_well` or `per_stage` (calculated metrics at various aggregation levels)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the metrics calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.metric_key` (string): Metric identifier (inferred).
- `data.metric_value` (float): Calculated metric value (inferred).
- `data.metric_type` (string): Type of metric (inferred).
- `data.stage_number` (int): Associated stage number (inferred).
- `data.aggregation_level` (string): Level of aggregation (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.metric_key": "string",
  "data.metric_value": "float",
  "data.metric_type": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains calculated completion metrics.

## Keywords

`completion metrics`, `frac kpi`, `completion kpi`, `performance metrics`, `efficiency metrics`
