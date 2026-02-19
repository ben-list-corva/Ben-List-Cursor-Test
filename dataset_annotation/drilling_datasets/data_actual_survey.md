# Actual Survey (Raw MWD/LWD Survey Data)

Raw survey measurements from MWD (Measurement While Drilling) and LWD (Logging While Drilling) tools. This collection contains the actual directional survey data taken during drilling operations, representing the true position and trajectory of the wellbore. Survey data is collected at regular intervals and forms the basis for wellbore positioning and directional calculations.

## When to use this dataset

- You need raw survey measurements from downhole tools.
- You want to calculate wellbore position and trajectory.
- You need survey data for anti-collision calculations.
- You want to compare actual wellbore position against the planned trajectory.
- You need survey inputs for torque and drag models.
- You want to build wellbore diagrams or 3D visualizations.

## Example queries

### Alerting
- Alert when a new survey shows significant deviation from plan.
- Notify when inclination exceeds maximum design limits.
- Alert when azimuth change indicates well is turning off course.

### Visualization
- Plot actual wellbore trajectory in 3D.
- Chart inclination and azimuth vs depth.
- Display plan vs actual trajectory comparison.
- Show survey stations on wellbore schematic.

### Q&A
- What is the latest survey position?
- How many surveys have been taken in this well?
- What is the maximum inclination reached?
- What is the current TVD and horizontal departure?
- How does the actual trajectory compare to planned at this depth?

## Frequency

`per_survey` (one record per survey station, typically every 30-100 feet)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the survey was taken.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the survey.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

Survey data typically contains an array of survey stations with the following fields per station:

- `data.surveys` (array): Array of survey station objects.
- Survey station fields:
  - `measured_depth` (float): Measured depth of the survey point.
  - `inclination` (float): Inclination angle in degrees from vertical.
  - `azimuth` (float): Azimuth direction in degrees from north.
  - `tvd` (float): Calculated true vertical depth.
  - `northing` (float): North-south displacement from surface.
  - `easting` (float): East-west displacement from surface.
  - `vertical_section` (float): Vertical section distance.
  - `dogleg_severity` (float): Dogleg severity at this station.
  - `closure_distance` (float): Horizontal closure distance.
  - `closure_direction` (float): Closure direction in degrees.

### `metadata` fields

- `metadata.name` (string): Survey name or identifier.
- `metadata.survey_type` (string): Type of survey (e.g., "MWD", "gyro").

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.surveys": "array",
  "metadata.name": "string",
  "metadata.survey_type": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains arrays of actual survey stations with measured depth, inclination, azimuth, and calculated positional values.

## Keywords

`actual survey`, `mwd survey`, `lwd survey`, `directional survey`, `wellbore position`, `survey stations`, `trajectory`
