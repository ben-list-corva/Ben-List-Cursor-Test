# Anti-Collision Alert (Collision Warnings)

Anti-collision alerts and warnings. This collection contains alerts generated when wellbore proximity thresholds are breached or collision risks are identified. Used for real-time collision avoidance during drilling operations.

## When to use this dataset

- You need anti-collision alert history.
- You want to monitor collision warnings.
- You need to track proximity alert trends.
- You want to review alert conditions.

## Example queries

### Alerting
- This dataset IS the alert source for anti-collision.
- Alert conditions are already captured here.

### Visualization
- Display anti-collision alert timeline.
- Show alert locations on wellbore view.
- Chart alert severity distribution.

### Q&A
- What anti-collision alerts have been generated?
- Which offset well triggered the alert?
- What was the clearance at the alert?
- How many alerts have occurred on this well?

## Frequency

`per_alert` (one record per anti-collision alert)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the alert.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the alert.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.offset_well_id` (string): ID of the offset well triggering alert.
- `data.offset_wellbore_id` (string): ID of the offset wellbore.
- `data.offset_design_id` (string): ID of the offset well design.
- `data.max_center_distance` (float): Center distance threshold.
- `data.max_separation_factor` (float): Separation factor threshold.
- `data.north_reference` (string): North reference used.
- `data.offset_well_properties` (object): Properties of the alerting offset well.
  - `data.offset_well_properties.well_name` (string): Offset well name.
  - `data.offset_well_properties.wellbore_name` (string): Wellbore name.
  - `data.offset_well_properties.design_name` (string): Design name.
  - `data.offset_well_properties.phase_name` (string): Phase (ACTUAL, PLAN).
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
  "data.offset_well_properties": "object"
}
```

## Sample record

```json
{
  "_id": "example_anti-collision_alert",
  "company_id": 81,
  "asset_id": 12345,
  "version": 3,
  "provider": "corva",
  "collection": "anti-collision.alert",
  "data": {
    "offset_well_id": "y25tPdNMfN",
    "offset_wellbore_id": "2cQ8xiin7L",
    "offset_design_id": "Cix1v",
    "max_center_distance": 2500,
    "max_separation_factor": 10,
    "north_reference": "grid",
    "offset_well_properties": {
      "well_name": "MABEE DDA E15 403AH",
      "wellbore_name": "OWB",
      "design_name": "PWP2",
      "phase_name": "PLAN",
      "datum": 2912.0058240000003,
      "casing_size": 5.5
    }
  }
}
```

## Keywords

`anti collision alert`, `collision warning`, `proximity alert`, `wellbore collision`, `anti collision`, `safety alert`
