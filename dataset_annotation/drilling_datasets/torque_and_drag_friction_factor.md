# Torque and Drag Friction Factor (Wellbore Friction)

Friction factor calculations for torque and drag modeling. This collection contains predicted and actual friction factors for casing and open hole sections, used to calibrate T&D models and identify changes in wellbore conditions.

## When to use this dataset

- You need friction factors for T&D modeling.
- You want to calibrate T&D models with actual data.
- You need to track friction factor changes over time.
- You want to identify hole condition changes.
- You need friction factor inputs for predictions.

## Example queries

### Alerting
- Alert when friction factor increases significantly.
- Notify when calibration indicates hole problems.
- Alert on friction factor divergence from baseline.

### Visualization
- Chart friction factor trend over depth/time.
- Show casing vs open hole friction comparison.
- Display friction factor calibration results.

### Q&A
- What is the current open hole friction factor?
- How does casing friction compare to open hole?
- Has friction factor changed since last calibration?
- What friction factors are being used in the model?
- Is there evidence of hole deterioration?

## Frequency

`per_calibration` (updated when friction factors are calibrated)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the friction factor record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.casing_depth` (float): Depth of casing shoe.
- `data.hole_depth` (float): Current hole depth.
- `data.predicted` (object): Predicted/default friction factors.
  - `data.predicted.casing` (float): Predicted casing friction factor.
  - `data.predicted.open_hole_slackoff` (float): Predicted open hole friction for slack-off.
  - `data.predicted.open_hole_pickup` (float): Predicted open hole friction for pick-up.
  - `data.predicted.open_hole_rotating` (float): Predicted open hole friction for rotating.
- `data.current_usage` (object): Currently applied friction factors.
  - `data.current_usage.casing` (float): Applied casing friction factor.
  - `data.current_usage.open_hole_slackoff` (float): Applied open hole slack-off friction.
  - `data.current_usage.open_hole_pickup` (float): Applied open hole pick-up friction.
  - `data.current_usage.open_hole_rotating` (float): Applied open hole rotating friction.
- `data.usage_type` (string): How friction factors are set ("override", "calibrated", "default").
- `data.status` (int): Calculation status.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.casing_depth": "float",
  "data.hole_depth": "float",
  "data.predicted": "object",
  "data.current_usage": "object",
  "data.usage_type": "string",
  "data.status": "int"
}
```

## Sample record

```json
{
  "_id": "example_torque-and-drag_friction-factor",
  "version": 1,
  "provider": "corva",
  "collection": "torque-and-drag.friction-factor",
  "timestamp": 1768862575,
  "data": {
    "casing_depth": 5809.7,
    "hole_depth": 21112,
    "predicted": {
      "casing": 0.15,
      "open_hole_slackoff": 0.25,
      "open_hole_pickup": 0.25,
      "open_hole_rotating": 0.25
    },
    "current_usage": {
      "casing": 0.15,
      "open_hole_slackoff": 0.25,
      "open_hole_pickup": 0.25,
      "open_hole_rotating": 0.25
    },
    "usage_type": "override",
    "status": 0
  },
  "asset_id": 12345,
  "company_id": 81
}
```

## Keywords

`friction factor`, `torque and drag`, `wellbore friction`, `casing friction`, `open hole friction`, `t&d calibration`
