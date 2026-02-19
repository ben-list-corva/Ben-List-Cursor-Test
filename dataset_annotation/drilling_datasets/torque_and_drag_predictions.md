# Torque and Drag Predictions (Real-Time T&D Predictions)

Torque and drag predictions for drilling optimization. This collection contains real-time predicted values for hookload and surface torque based on current drilling conditions, enabling comparison with actual measurements for anomaly detection.

## When to use this dataset

- You need real-time hookload and torque predictions.
- You want to compare actual vs predicted T&D values.
- You need T&D data for drilling optimization.
- You want to detect anomalies from prediction deviations.
- You need downhole WOB and torque estimates.

## Example queries

### Alerting
- Alert when actual hookload differs from predicted.
- Notify when actual torque exceeds prediction.
- Alert on T&D prediction anomalies.

### Visualization
- Plot predicted vs actual hookload over time.
- Chart predicted vs actual torque.
- Display T&D prediction accuracy.
- Show downhole parameter estimates.

### Q&A
- What is the predicted hookload?
- What is the predicted surface torque?
- What is the estimated downhole WOB?
- How does actual compare to predicted?
- What is the downhole torque estimate?

## Frequency

`per_second` (real-time predictions during operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the prediction.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the prediction.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.activity` (string): Current drilling activity.
- `data.predicted_hookload` (float): Predicted hookload.
- `data.predicted_surface_torque` (float): Predicted surface torque.
- `data.bit_depth` (float): Current bit depth.
- `data.hole_depth` (float): Current hole depth.
- `data.bit_depth_tvd` (float): Bit depth TVD.
- `data.hole_depth_tvd` (float): Hole depth TVD.
- `data.differential_pressure` (float): Differential pressure.
- `data.downhole_weight_on_bit` (float): Estimated downhole WOB.
- `data.downhole_torque` (float): Estimated downhole torque.
- `data.bit_rpm` (float): Bit RPM.
- `data.status` (int): Prediction status.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.activity": "string",
  "data.predicted_hookload": "float",
  "data.predicted_surface_torque": "float",
  "data.bit_depth": "float",
  "data.hole_depth": "float",
  "data.bit_depth_tvd": "float",
  "data.hole_depth_tvd": "float",
  "data.differential_pressure": "float",
  "data.downhole_weight_on_bit": "float",
  "data.downhole_torque": "float",
  "data.bit_rpm": "float",
  "data.status": "int"
}
```

## Sample record

```json
{
  "_id": "example_torque-and-drag_predictions",
  "version": 1,
  "provider": "corva",
  "collection": "torque-and-drag.predictions",
  "timestamp": 1768920597,
  "data": {
    "activity": "Run in Hole",
    "predicted_hookload": 97.92,
    "predicted_surface_torque": 0,
    "bit_depth": 1619.2,
    "hole_depth": 21250,
    "bit_depth_tvd": 1618.98,
    "hole_depth_tvd": 8712.45,
    "differential_pressure": 0,
    "downhole_weight_on_bit": 0,
    "downhole_torque": 0,
    "bit_rpm": 0,
    "status": 0
  },
  "asset_id": 12345,
  "company_id": 81
}
```

## Keywords

`torque and drag predictions`, `predicted hookload`, `predicted torque`, `downhole wob`, `t&d model`, `drilling optimization`
