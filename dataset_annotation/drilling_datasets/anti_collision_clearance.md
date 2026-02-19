# Anti-Collision Clearance (Wellbore Separation Calculations)

Anti-collision clearance calculations between wellbores. This collection contains separation factor and center distance calculations between the current well and nearby offset wells, ensuring safe drilling distances are maintained.

## When to use this dataset

- You need wellbore separation calculations.
- You want to monitor anti-collision status.
- You need clearance data for offset wells.
- You want to plan drilling trajectory for collision avoidance.

## Example queries

### Alerting
- Alert when clearance falls below threshold.
- Notify when approaching offset wellbores.
- Alert on collision risk changes.

### Visualization
- Display anti-collision scan results.
- Show closest approach to each offset.
- Chart clearance profile vs depth.

### Q&A
- What is the minimum clearance to offset wells?
- Which offset well is closest?
- What is the separation factor at current depth?
- Is there collision risk ahead?

## Frequency

`per_update` (updated when surveys change or projections are made)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the clearance calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.offset_well_id` (string): ID of the offset well.
- `data.offset_wellbore_id` (string): ID of the offset wellbore.
- `data.offset_design_id` (string): ID of the offset well design.
- `data.max_center_distance` (float): Maximum center-to-center distance threshold.
- `data.max_separation_factor` (float): Maximum separation factor threshold.
- `data.north_reference` (string): North reference used ("grid", "true").
- `data.offset_well_properties` (object): Properties of the offset well.
  - `data.offset_well_properties.well_name` (string): Offset well name.
  - `data.offset_well_properties.wellbore_name` (string): Wellbore name.
  - `data.offset_well_properties.design_name` (string): Design name.
  - `data.offset_well_properties.phase_name` (string): Phase (ACTUAL, PLAN).
  - `data.offset_well_properties.datum` (float): Datum elevation.
  - `data.offset_well_properties.casing_size` (float): Casing size.
  - `data.offset_well_properties.survey_program` (object): Survey program details.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.offset_well_id": "string",
  "data.offset_wellbore_id": "string",
  "data.offset_design_id": "string",
  "data.max_center_distance": "float",
  "data.max_separation_factor": "float",
  "data.north_reference": "string",
  "data.offset_well_properties": "object"
}
```

## Sample record

```json
{
  "_id": "example_anti-collision_clearance",
  "company_id": 81,
  "asset_id": 12345,
  "version": 3,
  "provider": "corva",
  "collection": "anti-collision.clearance",
  "data": {
    "offset_well_id": "h4whkZ9kEA",
    "offset_wellbore_id": "rJ2iwJzb2i",
    "offset_design_id": "HRZPr",
    "max_center_distance": 2500,
    "max_separation_factor": 10,
    "north_reference": "grid",
    "offset_well_properties": {
      "well_name": "MABEE 239 1SW",
      "wellbore_name": "OWB",
      "design_name": "AWP",
      "phase_name": "ACTUAL",
      "datum": 2897.005794,
      "casing_size": 5.5
    }
  }
}
```

## Keywords

`anti collision`, `clearance`, `separation factor`, `offset wells`, `wellbore collision`, `wellbore proximity`
