# Casing (Wellbore Casing and Liner Data)

Casing and liner data for wellbore construction. This collection contains information about the casing strings installed in the wellbore including conductor, surface casing, intermediate casing, production casing, and liners. Essential for wellbore integrity, hydraulics calculations, and completion planning.

## When to use this dataset

- You need casing configuration for hydraulics calculations.
- You want to know wellbore diameters at specific depths.
- You need casing data for torque and drag analysis.
- You want to track casing installation history.
- You need casing specifications for well control calculations.
- You want to display wellbore schematic with casing strings.

## Example queries

### Alerting
- Alert when casing shoe depth is approaching.
- Notify when operations are occurring near casing transition.

### Visualization
- Display wellbore schematic with casing strings.
- Show casing program vs actual installation.
- Chart casing depths and diameters.
- Overlay casing on formation/depth displays.

### Q&A
- What is the casing configuration for this well?
- What is the shoe depth of the production casing?
- What casing size is at this depth?
- What is the casing weight and grade?
- How much open hole is below the casing shoe?

## Frequency

`per_casing` (one record per casing string installation)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the casing was created or updated.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.top_depth` and `data.bottom_depth`: Depth range of the casing string.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.name` (string): Casing string name (e.g., "Surface", "Intermediate", "Production").
- `data.casing_type` (string): Type of casing string.
- `data.top_depth` (float): Top depth of casing string.
- `data.bottom_depth` (float): Bottom depth (shoe depth) of casing string.
- `data.od` (float): Outer diameter in inches.
- `data.id` (float): Inner diameter in inches.
- `data.weight` (float): Casing weight in pounds per foot.
- `data.grade` (string): Casing grade (e.g., "J-55", "L-80", "P-110").
- `data.connection` (string): Connection type.
- `data.burst_pressure` (float): Burst pressure rating.
- `data.collapse_pressure` (float): Collapse pressure rating.
- `data.tensile_strength` (float): Tensile strength rating.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.name": "string",
  "data.casing_type": "string",
  "data.top_depth": "float",
  "data.bottom_depth": "float",
  "data.od": "float",
  "data.id": "float",
  "data.weight": "float",
  "data.grade": "string",
  "data.connection": "string",
  "data.burst_pressure": "float",
  "data.collapse_pressure": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains casing string configurations with depth ranges and specifications.

## Keywords

`casing`, `liner`, `wellbore construction`, `casing string`, `shoe depth`, `casing program`, `wellbore integrity`
