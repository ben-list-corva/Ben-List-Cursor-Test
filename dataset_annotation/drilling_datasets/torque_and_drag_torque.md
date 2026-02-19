# Torque and Drag Torque (Drillstring Torque Analysis)

Torque calculations along the drillstring. This collection contains calculated torque values at each point along the drill string, along with torsional yield limits for comparison. Essential for preventing twist-offs and optimizing rotary drilling parameters.

## When to use this dataset

- You need torque distribution along the drillstring.
- You want to check torque vs torsional yield limits.
- You need to verify drillstring design for torque capacity.
- You want to analyze torque during drilling operations.
- You need downhole torque estimates.

## Example queries

### Alerting
- Alert when surface torque approaches connection limits.
- Notify when torque exceeds safe percentages of yield.
- Alert on sudden torque increases indicating problems.

### Visualization
- Plot torque vs measured depth.
- Show torque with yield limits overlay.
- Display torque distribution along the string.
- Chart surface vs downhole torque.

### Q&A
- What is the torque at the motor?
- What percentage of yield is being used?
- Is there risk of twist-off?
- What is the torque at each connection?
- Where is the highest torque in the string?

## Frequency

`per_calculation` (calculated during drilling operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the torque calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.activity` (string): Current drilling activity.
- `data.points` (array): Torque values along the string. Each point contains:
  - `measured_depth` (float): Measured depth of the calculation point.
  - `torque` (float): Calculated torque at this depth (ft-lbs or kN-m).
  - `torsional_yield` (float): Torsional yield limit of the pipe at this point.

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
  "_id": "example_torque-and-drag_torque",
  "version": 1,
  "provider": "corva",
  "collection": "torque-and-drag.torque",
  "timestamp": 1769006919,
  "data": {
    "activity": "Dry Reaming Down",
    "points": [
      {
        "measured_depth": 0,
        "torque": 14.3,
        "torsional_yield": 74.37
      },
      {
        "measured_depth": 166,
        "torque": 14.19,
        "torsional_yield": 74.37
      },
      {
        "measured_depth": 242,
        "torque": 14.15,
        "torsional_yield": 74.37
      }
    ]
  },
  "asset_id": 12345,
  "company_id": 81
}
```

## Keywords

`torque`, `torque and drag`, `torsional yield`, `drillstring torque`, `twist off`, `rotary torque`
