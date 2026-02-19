# AFE (Authorization for Expenditure)

Authorization for Expenditure (AFE) data for well cost tracking. This collection contains the approved budget estimates for the well, typically expressed as cost vs depth or cost vs days curves. Essential for comparing actual drilling progress against planned budget milestones.

## When to use this dataset

- You need the planned cost curve for the well.
- You want to compare actual cost vs AFE.
- You need budget data for days vs depth/cost charts.
- You want to track well performance against financial targets.
- You need AFE milestones for progress reporting.

## Example queries

### Alerting
- Alert when actual cost exceeds AFE at current depth.
- Notify when days on well exceed AFE timeline.

### Visualization
- Plot AFE cost curve on days vs depth chart.
- Show actual vs planned cost comparison.
- Display AFE milestones on well timeline.
- Chart cost variance from AFE.

### Q&A
- What is the total AFE for this well?
- Are we ahead or behind the AFE curve?
- What was the AFE cost estimate at this depth?
- How many days were budgeted to reach TD?
- What is the current cost variance from AFE?

## Frequency

`per_well` (typically one AFE record with milestone points per well)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the AFE was created.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.depth`, `data.days`, `data.cost`: Unique combination of budget parameters.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.depth` (float): Planned depth milestone.
- `data.days` (float): Planned days to reach milestone.
- `data.cost` (float): Planned cost at milestone.
- `data.afe_number` (string): AFE reference number (inferred).
- `data.afe_total` (float): Total AFE budget (inferred).
- `data.currency` (string): Currency for cost values (inferred).
- `data.version` (int): AFE version number (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.depth": "float",
  "data.days": "float",
  "data.cost": "float",
  "data.afe_number": "string",
  "data.afe_total": "float",
  "data.currency": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains AFE budget milestones with depth, days, and cost values.

## Keywords

`afe`, `authorization for expenditure`, `well budget`, `cost estimate`, `days vs depth`, `well cost`, `drilling budget`
