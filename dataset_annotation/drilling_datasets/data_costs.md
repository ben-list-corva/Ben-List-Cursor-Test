# Costs (Daily Well Cost Tracking)

Daily cost tracking data for well operations. This collection contains actual costs incurred during drilling operations, typically recorded daily with cost categories and descriptions. Essential for tracking well economics and comparing against AFE budgets.

## When to use this dataset

- You need to track actual daily costs for the well.
- You want to compare actual costs against budget.
- You need cost breakdown by category.
- You want to analyze cost trends during drilling.
- You need cost data for well economics.

## Example queries

### Alerting
- Alert when daily cost exceeds threshold.
- Notify on significant cost increases.

### Visualization
- Plot cumulative cost vs time.
- Show cost breakdown by category.
- Chart daily cost trend.
- Compare actual vs AFE cost.

### Q&A
- What is the total cost incurred to date?
- What are the major cost categories?
- How much was spent on a specific date?
- What is the average daily cost?
- How does cost compare to budget?

## Frequency

`per_day` (one record per day with cost entries)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the cost record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.date`, `data.cost`, `data.description`: Unique combination for each cost entry.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.date` (string/long): Date of the cost record.
- `data.cost` (float): Cost amount.
- `data.description` (string): Description of the cost item.
- `data.category` (string): Cost category (inferred).
- `data.vendor` (string): Vendor or service provider (inferred).
- `data.currency` (string): Currency for cost (inferred).
- `data.cumulative_cost` (float): Running total cost (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.date": "string",
  "data.cost": "float",
  "data.description": "string",
  "data.category": "string",
  "data.vendor": "string",
  "data.currency": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains daily cost entries with amounts and descriptions.

## Keywords

`costs`, `daily costs`, `well costs`, `drilling costs`, `cost tracking`, `well economics`, `expense tracking`
