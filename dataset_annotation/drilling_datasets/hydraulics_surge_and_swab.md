# Hydraulics Surge and Swab (Tripping Pressure Calculations)

Surge and swab pressure calculations for tripping operations. This collection contains calculated pressure variations caused by pipe movement during tripping in and out of the hole. Critical for well control and preventing formation damage or kicks during tripping operations.

## When to use this dataset

- You need surge/swab pressures during tripping.
- You want to ensure tripping speeds are safe.
- You need ECD values during pipe movement.
- You want to prevent formation damage from excessive surge.
- You need to avoid kicks from excessive swab pressures.

## Example queries

### Alerting
- Alert when surge pressure approaches fracture gradient.
- Notify when swab pressure approaches pore pressure.
- Alert on excessive tripping speeds.

### Visualization
- Plot surge/swab pressures vs tripping speed.
- Show safe operating window for tripping.
- Chart ECD during tripping operations.
- Display surge/swab vs depth profile.

### Q&A
- What is the maximum safe tripping speed?
- What is the surge pressure at current speed?
- Is there risk of swabbing the well?
- What is the ECD during tripping?
- How does surge compare to fracture gradient?

## Frequency

`per_interval` (calculated during tripping operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.surge_pressure` (float): Calculated surge pressure (inferred).
- `data.swab_pressure` (float): Calculated swab pressure (inferred).
- `data.surge_ecd` (float): ECD including surge effect (inferred).
- `data.swab_ecd` (float): ECD including swab effect (inferred).
- `data.trip_speed` (float): Tripping speed used in calculation (inferred).
- `data.bit_depth` (float): Bit depth for calculation.
- `data.hole_depth` (float): Hole depth for calculation.
- `data.pore_pressure` (float): Pore pressure at depth (inferred).
- `data.fracture_gradient` (float): Fracture gradient at depth (inferred).
- `data.mud_weight` (float): Mud weight used in calculation (inferred).
- `data.max_safe_trip_in_speed` (float): Maximum safe speed for trip in (inferred).
- `data.max_safe_trip_out_speed` (float): Maximum safe speed for trip out (inferred).
- `data.depth_points` (array): Array of surge/swab values at different depths (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.surge_pressure": "float",
  "data.swab_pressure": "float",
  "data.surge_ecd": "float",
  "data.swab_ecd": "float",
  "data.trip_speed": "float",
  "data.bit_depth": "float",
  "data.hole_depth": "float",
  "data.max_safe_trip_in_speed": "float",
  "data.max_safe_trip_out_speed": "float",
  "data.depth_points": "array"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains surge and swab pressure calculations for tripping safety.

## Keywords

`surge`, `swab`, `tripping`, `trip speed`, `surge pressure`, `swab pressure`, `well control`, `tripping safety`
