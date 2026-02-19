# Torque and Drag Hookload Trend (Hookload Broomstick Data)

Hookload trend analysis for torque and drag monitoring. This collection contains calculated hookload curves (broomstick charts) for different operations like slack-off and pick-up at various friction factors, enabling comparison with actual hookload measurements.

## When to use this dataset

- You need hookload broomstick curves for T&D analysis.
- You want to compare actual hookload vs modeled predictions.
- You need to calibrate friction factors from hookload data.
- You want to identify changes in wellbore friction.
- You need hookload predictions for different operations.

## Example queries

### Alerting
- Alert when actual hookload deviates from model.
- Notify when friction factor calibration is needed.
- Alert on overpull during tripping.

### Visualization
- Display hookload broomstick chart.
- Plot actual hookload on modeled curves.
- Show friction factor envelopes.
- Chart hookload trend during tripping.

### Q&A
- What hookload should we expect at this depth?
- What friction factor matches current hookload?
- Is there evidence of increasing drag?
- What is the predicted pickup weight?
- What is the expected slack-off weight?

## Frequency

`per_update` (updated when BHA or conditions change)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the hookload trend record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.config` (object): Configuration used for calculations.
  - `data.config._id` (string): Configuration document ID.
  - `data.config.hole_size` (float): Hole size in inches.
  - `data.config.type` (string): Configuration type (e.g., "CasingString").
  - `data.config.outer_diameter` (float): Outer diameter of string.
- `data.hole_depth` (float): Current hole depth.
- `data.is_extended` (boolean): Whether extended reach calculations apply.
- `data.curves` (object): Hookload curves for different operations.
  - `data.curves.slack_off` (array): Slack-off hookload curves at different friction factors.
  - `data.curves.pick_up` (array): Pick-up hookload curves at different friction factors.
  - Each curve contains `casing_friction_factor`, `openhole_friction_factor`, and `points` array with `measured_depth` and `hookload`.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.config": "object",
  "data.hole_depth": "float",
  "data.is_extended": "boolean",
  "data.curves": "object",
  "data.curves.slack_off": "array",
  "data.curves.pick_up": "array"
}
```

## Sample record

```json
{
  "_id": "example_torque-and-drag_hookload-trend",
  "version": 2,
  "provider": "corva",
  "collection": "torque-and-drag.hookload-trend",
  "timestamp": 1768920599,
  "data": {
    "config": {
      "_id": "696a9452aba9ff3e2971d213",
      "hole_size": 7.875,
      "type": "CasingString",
      "outer_diameter": 5.5
    },
    "hole_depth": 21250,
    "is_extended": false,
    "curves": {
      "slack_off": [
        {
          "casing_friction_factor": 0.15,
          "openhole_friction_factor": 0.1,
          "points": [
            {"measured_depth": 0, "hookload": 55},
            {"measured_depth": 1062.5, "hookload": 64.73}
          ]
        }
      ]
    }
  }
}
```

## Keywords

`hookload trend`, `broomstick chart`, `torque and drag`, `friction factor`, `pickup weight`, `slack off`, `drag analysis`
