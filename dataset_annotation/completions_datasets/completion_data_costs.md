# Completion Data Costs (Completion Cost Tracking)

Cost tracking data for completion operations. This collection contains cost entries for frac operations including daily costs, stage costs, and cost breakdowns.

## When to use this dataset

- You need completion cost tracking.
- You want to analyze frac costs.
- You need cost breakdown by category.
- You want to compare completion costs.

## Example queries

### Alerting
- Alert when costs exceed budget.
- Notify on significant cost entries.

### Visualization
- Display completion cost summary.
- Show cost breakdown chart.
- Chart cost trends.

### Q&A
- What is the total completion cost?
- What are the major cost categories?
- How do costs compare to budget?
- What is the cost per stage?

## Frequency

`per_entry` (one record per cost entry)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the cost entry.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the entry.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.cost` (float): Cost amount (inferred).
- `data.category` (string): Cost category (inferred).
- `data.description` (string): Cost description (inferred).
- `data.date` (string): Cost date (inferred).
- `data.stage_number` (int): Associated stage number (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.cost": "float",
  "data.category": "string",
  "data.description": "string",
  "data.date": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains completion cost entries.

## Keywords

`completion costs`, `frac costs`, `completion economics`, `stage costs`, `completion budget`
