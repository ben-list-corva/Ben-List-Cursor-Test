# Surface Equipment (Rig Surface Equipment Configuration)

Surface equipment configuration data. This collection contains information about the rig's surface equipment including top drive, rotary table, block, kelly bushing elevation, and other surface components relevant to drilling calculations.

## When to use this dataset

- You need rig surface equipment specifications.
- You want kelly bushing elevation for depth calculations.
- You need equipment data for engineering calculations.
- You want to enrich drilling data with surface equipment context.

## Example queries

### Alerting
- Alert when surface equipment configuration changes.

### Visualization
- Display rig equipment summary.
- Show equipment specifications on rig schematic.

### Q&A
- What is the kelly bushing elevation?
- What type of top drive is on the rig?
- What are the drawworks specifications?
- What is the maximum hookload capacity?

## Frequency

`per_configuration` (one record per rig configuration, updated when changes occur)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when configuration was created or updated.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.kelly_bushing_elevation` (float): KB elevation above sea level (inferred).
- `data.rotary_table_elevation` (float): Rotary table elevation (inferred).
- `data.top_drive_capacity` (float): Top drive torque capacity (inferred).
- `data.drawworks_capacity` (float): Drawworks capacity (inferred).
- `data.max_hookload` (float): Maximum hookload capacity (inferred).
- `data.pump_count` (int): Number of mud pumps (inferred).
- `data.rig_name` (string): Name of the rig (inferred).
- `data.rig_type` (string): Type of rig (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.kelly_bushing_elevation": "float",
  "data.rotary_table_elevation": "float",
  "data.top_drive_capacity": "float",
  "data.max_hookload": "float",
  "data.rig_name": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains surface equipment configurations.

## Keywords

`surface equipment`, `rig equipment`, `kelly bushing`, `top drive`, `drawworks`, `rig configuration`, `rig specifications`
