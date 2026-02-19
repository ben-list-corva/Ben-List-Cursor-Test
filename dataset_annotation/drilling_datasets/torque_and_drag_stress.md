# Torque and Drag Stress (Von Mises Stress Analysis)

Von Mises stress calculations along the drillstring. This collection contains combined stress calculations (axial, torsional, and bending) at each point along the drill string, compared to yield stress limits. Essential for preventing drillstring failures.

## When to use this dataset

- You need combined stress analysis along the drillstring.
- You want to check stress vs yield limits.
- You need to verify drillstring design for stress capacity.
- You want to identify high-stress locations.
- You need stress data for fatigue analysis.

## Example queries

### Alerting
- Alert when von Mises stress exceeds 80% of yield.
- Notify when stress concentrations are identified.
- Alert on stress approaching failure limits.

### Visualization
- Plot von Mises stress vs measured depth.
- Show stress with yield limit overlays (100%, 80%, 60%).
- Display stress components (axial, twist, bending).
- Chart stress distribution along the string.

### Q&A
- What is the maximum stress in the drillstring?
- Where is the highest stress concentration?
- What percentage of yield is being used?
- Is there risk of failure at current conditions?
- What is the safety factor at critical points?

## Frequency

`per_calculation` (calculated during drilling operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the stress calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.activity` (string): Current drilling activity.
- `data.points` (array): Stress values along the string. Each point contains:
  - `measured_depth` (float): Measured depth of the calculation point.
  - `yield_stress` (float): Material yield stress (psi).
  - `yield_stress_80_percent` (float): 80% of yield stress.
  - `yield_stress_60_percent` (float): 60% of yield stress.
  - `axial_stress` (float): Stress from axial load (psi).
  - `twist_stress` (float): Stress from torque (psi).
  - `bending_stress` (float): Stress from bending (psi).
  - `von_mises_stress` (float): Combined von Mises stress (psi).

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
  "_id": "example_torque-and-drag_stress",
  "version": 1,
  "provider": "corva",
  "collection": "torque-and-drag.stress",
  "timestamp": 1769006919,
  "data": {
    "activity": "Dry Reaming Down",
    "points": [
      {
        "measured_depth": 0,
        "yield_stress": 110000,
        "yield_stress_80_percent": 88000,
        "yield_stress_60_percent": 66000,
        "axial_stress": 25956.2,
        "twist_stress": 12203.4,
        "bending_stress": 0,
        "von_mises_stress": 33473.7
      },
      {
        "measured_depth": 166,
        "yield_stress": 110000,
        "yield_stress_80_percent": 88000,
        "yield_stress_60_percent": 66000,
        "axial_stress": 25321.1,
        "twist_stress": 12108.6,
        "bending_stress": 914.9,
        "von_mises_stress": 33708.1
      }
    ]
  },
  "asset_id": 12345,
  "company_id": 81
}
```

## Keywords

`stress`, `von mises stress`, `torque and drag`, `yield stress`, `axial stress`, `bending stress`, `drillstring failure`
