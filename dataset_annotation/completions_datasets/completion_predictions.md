# Completion Predictions (Frac Predictions and Calculations)

Completion operation predictions and calculations. This collection contains predictive analytics and calculated values for frac operations including breakdown predictions, target ramp rates, and treatment analysis.

## When to use this dataset

- You need frac operation predictions.
- You want breakdown and ramp-up analysis.
- You need calculated treatment parameters.
- You want predictive insights for frac operations.

## Example queries

### Alerting
- Alert when predictions differ significantly from actual.
- Notify when approaching predicted breakdown.

### Visualization
- Display predicted vs actual treatment.
- Show breakdown analysis.
- Chart predicted parameters.

### Q&A
- What is the predicted breakdown pressure?
- What was the calculated ISIP?
- What are the target ramp rates?
- How accurate were the predictions?

## Frequency

`per_stage` (predictions for each stage)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the prediction.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields

- `data.target_ramp_rate` (array): Target ramp rate data.
- `data.breakdown` (array): Breakdown analysis data with treatment parameters at breakdown time including:
  - `clean_flow_rate_in_streamed`, `total_clean_volume_in_streamed`
  - `proppant_1_mass_streamed`, `hydrostatic_pressure_streamed`
  - `elapsed_time`, `clean_flow_rate_in`
  - `total_proppant_concentration`, `total_proppant_mass`
  - `hydraulic_horse_power`, `wellhead_pressure`
  - `backside_pressure`, and other treatment parameters at breakdown
- `data.isip` (float): Predicted ISIP (inferred).
- `data.closure_pressure` (float): Predicted closure pressure (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.target_ramp_rate": "array",
  "data.breakdown": "array",
  "data.isip": "float",
  "data.closure_pressure": "float"
}
```

## Sample record

```json
{
  "_id": "example_completion_predictions",
  "company_id": 81,
  "asset_id": 12345,
  "version": 1,
  "provider": "corva",
  "collection": "completion.predictions",
  "data": {
    "target_ramp_rate": [],
    "breakdown": [
      {
        "clean_flow_rate_in_streamed": 59.4,
        "total_clean_volume_in_streamed": 191,
        "elapsed_time": 23411,
        "clean_flow_rate_in": 59.4,
        "total_clean_volume_in": 214.0934,
        "total_proppant_concentration": 0,
        "total_proppant_mass": 0,
        "hydraulic_horse_power": 15740.5248,
        "wellhead_pressure": 10816,
        "backside_pressure": 96
      }
    ]
  },
  "timestamp": 1768975310,
  "stage_number": 1
}
```

## Keywords

`completion predictions`, `frac predictions`, `breakdown analysis`, `isip prediction`, `frac analytics`
