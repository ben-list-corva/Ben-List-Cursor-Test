# Torque and Drag Axial Load (String Tension Analysis)

Axial load calculations along the drillstring. This collection contains calculated axial loads at each point along the drill string, including buckling force thresholds for sinusoidal and helical buckling. Essential for drillstring design verification and buckling prevention.

## When to use this dataset

- You need axial load distribution along the drillstring.
- You want to check for buckling potential.
- You need to verify drillstring design limits.
- You want to analyze string tension during operations.
- You need buckling force comparisons.

## Example queries

### Alerting
- Alert when axial load approaches buckling threshold.
- Notify when compression exceeds safe limits.
- Alert on potential helical buckling conditions.

### Visualization
- Plot axial load vs measured depth.
- Show buckling envelopes along the string.
- Display tension/compression profile.
- Chart axial load with buckling limits overlay.

### Q&A
- Is there risk of buckling at current conditions?
- Where is the neutral point?
- What is the axial load at the motor?
- Is the string in tension or compression at specific depths?
- What are the buckling limits at current depth?

## Frequency

`per_calculation` (calculated during drilling operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the axial load calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.activity` (string): Current drilling activity.
- `data.points` (array): Axial load values along the string. Each point contains:
  - `measured_depth` (float): Measured depth of the calculation point.
  - `axial_load` (float): Calculated axial load at this depth (positive = tension, negative = compression).
  - `sinusoidal_buckling_force` (float): Threshold force for sinusoidal buckling (negative value).
  - `helical_buckling_force` (float): Threshold force for helical buckling (negative value).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.activity": "string",
  "data.points": "array"
}
```

## Sample record

```json
{
  "_id": "example_torque-and-drag_axial-load",
  "version": 1,
  "provider": "corva",
  "collection": "torque-and-drag.axial-load",
  "timestamp": 1769006919,
  "data": {
    "activity": "Dry Reaming Down",
    "points": [
      {
        "measured_depth": 0,
        "axial_load": 146.37,
        "sinusoidal_buckling_force": -8.04,
        "helical_buckling_force": -22.73
      },
      {
        "measured_depth": 166,
        "axial_load": 143.55,
        "sinusoidal_buckling_force": -22.67,
        "helical_buckling_force": -64.13
      }
    ]
  },
  "asset_id": 12345,
  "company_id": 81
}
```

## Keywords

`axial load`, `torque and drag`, `buckling`, `sinusoidal buckling`, `helical buckling`, `string tension`, `compression`
