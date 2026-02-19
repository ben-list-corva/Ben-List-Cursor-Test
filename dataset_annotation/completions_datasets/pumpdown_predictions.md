# Pumpdown Predictions (Plug Tracking Predictions)

Pumpdown operation predictions and plug tracking calculations. This collection contains predictive analytics for pumpdown operations including estimated time to set, ball/plug position predictions, and expected pressure responses.

## When to use this dataset

- You need pumpdown predictions.
- You want estimated plug arrival time.
- You need predicted plug position.
- You want predictive analytics for pumpdown.

## Example queries

### Alerting
- Alert when prediction accuracy changes.
- Notify on predicted plug arrival.

### Visualization
- Display predicted vs actual plug depth.
- Show time to set estimate.
- Chart prediction accuracy.

### Q&A
- When is the plug expected to set?
- What is the predicted plug depth?
- How accurate are the predictions?

## Frequency

`per_calculation` (updated during pumpdown)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the prediction.
- `asset_id`: Unique ID of the asset (well).
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields (inferred from domain knowledge)

- `data.predicted_set_time` (long): Predicted plug set time (inferred).
- `data.predicted_ball_depth` (float): Predicted ball/plug depth (inferred).
- `data.time_to_set` (int): Estimated time to plug set (inferred).
- `data.volume_to_set` (float): Volume remaining to set plug (inferred).
- `data.confidence` (float): Prediction confidence (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.predicted_set_time": "long",
  "data.predicted_ball_depth": "float",
  "data.time_to_set": "int"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains pumpdown predictions.

## Keywords

`pumpdown predictions`, `plug tracking`, `ball tracking`, `time to set`, `pumpdown analytics`
