# Circulation Volumetric (Circulation Volume Tracking)

Volumetric circulation data for tracking fluid volumes and circulation progress. This collection contains calculated volumes for circulating bottoms up, total system volumes, and pump strokes required to achieve circulation milestones.

## When to use this dataset

- You need to track circulation progress.
- You want to know volumes to circulate bottoms up.
- You need pump strokes to surface for cuttings.
- You want to track total mud system volume.
- You need circulation data for tripping decisions.

## Example queries

### Alerting
- Alert when bottoms up is achieved.
- Notify on circulation progress milestones.
- Alert when system volume changes unexpectedly.

### Visualization
- Display circulation progress indicator.
- Show volumes to various depths.
- Chart pump strokes vs lag depth.
- Display mud volume tracking.

### Q&A
- How many strokes to bottoms up?
- What is the lag time to surface?
- What is the total system volume?
- How much has been circulated so far?
- When will returns from current depth reach surface?

## Frequency

`per_interval` (updated during circulation operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the volumetric calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.strokes_to_bottoms_up` (int): Pump strokes to circulate bottoms up (inferred).
- `data.volume_to_bottoms_up` (float): Volume to circulate bottoms up (inferred).
- `data.time_to_bottoms_up` (int): Time to circulate bottoms up (inferred).
- `data.total_system_volume` (float): Total mud system volume (inferred).
- `data.annular_volume` (float): Volume in the annulus (inferred).
- `data.drillstring_volume` (float): Volume in the drillstring (inferred).
- `data.current_lag_strokes` (int): Current lag in strokes (inferred).
- `data.current_lag_time` (int): Current lag in time (inferred).
- `data.flow_rate` (float): Current flow rate (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.strokes_to_bottoms_up": "int",
  "data.volume_to_bottoms_up": "float",
  "data.time_to_bottoms_up": "int",
  "data.total_system_volume": "float",
  "data.annular_volume": "float",
  "data.drillstring_volume": "float",
  "data.current_lag_strokes": "int"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains circulation volumetric calculations.

## Keywords

`circulation`, `volumetric`, `bottoms up`, `pump strokes`, `lag time`, `mud volume`, `circulation tracking`
