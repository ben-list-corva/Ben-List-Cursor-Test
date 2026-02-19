# Plan Survey (Planned Wellbore Trajectory)

Planned wellbore trajectory survey data. This collection contains the designed/planned well path that defines how the well should be drilled. The plan survey serves as the reference trajectory against which actual drilling progress is compared. It includes planned survey stations with target inclination, azimuth, and positional coordinates.

## When to use this dataset

- You need the planned/designed wellbore trajectory.
- You want to compare actual drilling against the plan.
- You need target coordinates for directional drilling.
- You want to calculate distance to plan or deviation from design.
- You need plan data for anti-collision calculations with offset wells.
- You want to display the target trajectory for directional guidance.

## Example queries

### Alerting
- Alert when approaching planned target depth.
- Notify when actual trajectory deviates significantly from plan.

### Visualization
- Plot planned wellbore trajectory.
- Overlay plan and actual trajectories for comparison.
- Display target landing zone with planned approach.
- Show plan survey on 3D well visualization.

### Q&A
- What is the planned inclination at target depth?
- What is the planned landing zone coordinates?
- What is the total planned measured depth?
- What is the maximum planned dogleg severity?
- What are the target coordinates at TD?

## Frequency

`per_plan` (one record containing all planned survey stations for the well)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the plan was created or updated.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the plan.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

Plan survey data typically contains an array of planned survey stations:

- `data.surveys` (array): Array of planned survey station objects.
- Survey station fields:
  - `measured_depth` (float): Planned measured depth.
  - `inclination` (float): Planned inclination in degrees.
  - `azimuth` (float): Planned azimuth in degrees.
  - `tvd` (float): Planned true vertical depth.
  - `northing` (float): Planned north-south position.
  - `easting` (float): Planned east-west position.
  - `vertical_section` (float): Planned vertical section.
  - `dogleg_severity` (float): Maximum allowed dogleg severity.

### `metadata` fields

- `metadata.name` (string): Plan name or identifier (e.g., "Design 1", "Final Plan").
- `metadata.plan_type` (string): Type of well plan.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.surveys": "array",
  "metadata.name": "string",
  "metadata.plan_type": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains arrays of planned survey stations defining the target wellbore trajectory.

## Keywords

`plan survey`, `planned trajectory`, `well plan`, `target trajectory`, `designed path`, `wellbore design`
