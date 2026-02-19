# Completion Data Actual Stages (Executed Stage Data)

Actual executed stage data with measurements. This collection contains the actual results from completed frac stages including final volumes, proppant mass, pressures, and performance metrics.

## When to use this dataset

- You need actual stage execution results.
- You want to compare design vs actual performance.
- You need stage completion metrics.
- You want to analyze stage performance.

## Example queries

### Alerting
- Alert when actual differs significantly from design.
- Notify when stage performance is below target.

### Visualization
- Display actual vs design comparison.
- Show stage performance metrics.
- Chart actual results across stages.

### Q&A
- What was the actual proppant placed?
- How did actual compare to design?
- What was the max pressure during the stage?
- What were the final stage volumes?

## Frequency

`per_stage` (one record per completed stage)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the stage completion.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields (inferred from domain knowledge)

- `data.stage_number` (int): Stage number.
- `data.actual_proppant` (float): Actual proppant mass placed (inferred).
- `data.actual_clean_volume` (float): Actual clean fluid volume (inferred).
- `data.actual_slurry_volume` (float): Actual slurry volume (inferred).
- `data.max_pressure` (float): Maximum treating pressure (inferred).
- `data.avg_rate` (float): Average pump rate (inferred).
- `data.stage_duration` (int): Stage duration in seconds (inferred).
- `data.isip` (float): Instantaneous shut-in pressure (inferred).
- `data.breakdown_pressure` (float): Breakdown pressure (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.actual_proppant": "float",
  "data.actual_clean_volume": "float",
  "data.actual_slurry_volume": "float",
  "data.max_pressure": "float",
  "data.avg_rate": "float",
  "data.stage_duration": "int",
  "data.isip": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains actual stage execution results.

## Keywords

`actual stages`, `stage results`, `stage execution`, `frac results`, `stage performance`, `actual vs design`
