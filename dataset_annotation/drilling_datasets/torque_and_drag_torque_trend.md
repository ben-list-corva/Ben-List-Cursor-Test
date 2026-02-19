# Torque and Drag Torque Trend (Torque Broomstick Data)

Torque trend analysis data providing calculated torque curves (broomstick charts) for rotary operations at various friction factors. Enables comparison of actual surface torque with modeled predictions for T&D calibration.

## When to use this dataset

- You need torque broomstick curves for T&D analysis.
- You want to compare actual torque vs modeled predictions.
- You need to calibrate friction factors from torque data.
- You want torque predictions for different operations.

## Example queries

### Alerting
- Alert when actual torque exceeds model predictions.
- Notify when torque trend indicates friction increase.

### Visualization
- Display torque broomstick chart.
- Plot actual torque on modeled curves.
- Show friction factor envelopes for torque.
- Chart torque trend during drilling.

### Q&A
- What torque should we expect at this depth?
- What friction factor matches current torque?
- Is torque trending higher than normal?
- What is the predicted rotating torque?

## Frequency

`per_update` (updated when BHA or conditions change)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the torque trend record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.config` (object): Configuration used for calculations.
- `data.hole_depth` (float): Current hole depth.
- `data.is_extended` (boolean): Whether extended reach calculations apply.
- `data.curves` (object): Torque curves for different operations.
  - `data.curves.rotary_off_bottom` (array): Rotating off-bottom torque curves.
  - Each curve contains `casing_friction_factor`, `openhole_friction_factor`, and `points` array with `measured_depth`, `hookload`, and `torque`.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.config": "object",
  "data.hole_depth": "float",
  "data.is_extended": "boolean",
  "data.curves": "object"
}
```

## Sample record

```json
{
  "_id": "example_torque-and-drag_torque-trend",
  "version": 2,
  "provider": "corva",
  "collection": "torque-and-drag.torque-trend",
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
      "rotary_off_bottom": [
        {
          "casing_friction_factor": 0.15,
          "openhole_friction_factor": 0.1,
          "points": [
            {"measured_depth": 0, "hookload": 55, "torque": 0},
            {"measured_depth": 1062.5, "hookload": 64.84, "torque": 0.02}
          ]
        }
      ]
    }
  }
}
```

## Keywords

`torque trend`, `torque broomstick`, `torque and drag`, `rotating torque`, `friction factor`, `torque calibration`
