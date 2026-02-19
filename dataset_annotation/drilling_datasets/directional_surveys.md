# Directional Surveys (Enriched Survey Data)

Enriched directional survey data with calculated values. This collection contains processed survey data with additional computed fields beyond the raw survey measurements. Surveys are taken at regular depth intervals during directional drilling to determine the wellbore position and trajectory.

## When to use this dataset

- You need enriched survey data with calculated positional values.
- You want to visualize the wellbore trajectory in 3D.
- You need survey data with computed northing, easting, and TVD values.
- You want to analyze dogleg severity and build angles.
- You need processed survey data for engineering calculations.

## Example queries

### Alerting
- Alert when dogleg severity exceeds a threshold.
- Notify when inclination or azimuth changes significantly from previous survey.

### Visualization
- Plot 3D wellbore trajectory using survey points.
- Chart inclination and azimuth vs measured depth.
- Display TVD vs horizontal departure.
- Show survey stations on a plan view.

### Q&A
- What is the current wellbore inclination and azimuth?
- What is the dogleg severity at the last survey?
- How does the actual trajectory compare to planned?
- What is the current TVD and lateral position?

## Frequency

`per_survey` (one record per survey station, typically every 30-100 feet)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the survey was recorded.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the survey.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.measured_depth` (float): Measured depth of the survey station.
- `data.inclination` (float): Inclination angle in degrees from vertical.
- `data.azimuth` (float): Azimuth direction in degrees from north.
- `data.tvd` (float): True vertical depth at the survey station.
- `data.northing` (float): North-south position relative to surface location.
- `data.easting` (float): East-west position relative to surface location.
- `data.vertical_section` (float): Vertical section distance.
- `data.dogleg_severity` (float): Rate of wellbore curvature (degrees per 100 feet).
- `data.build_rate` (float): Rate of inclination change.
- `data.turn_rate` (float): Rate of azimuth change.
- `data.closure_distance` (float): Horizontal distance from surface to survey point.
- `data.closure_direction` (float): Direction of closure from surface to survey point.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.measured_depth": "float",
  "data.inclination": "float",
  "data.azimuth": "float",
  "data.tvd": "float",
  "data.northing": "float",
  "data.easting": "float",
  "data.vertical_section": "float",
  "data.dogleg_severity": "float",
  "data.build_rate": "float",
  "data.turn_rate": "float",
  "data.closure_distance": "float",
  "data.closure_direction": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains enriched directional survey data with calculated positional values.

## Keywords

`directional surveys`, `survey data`, `wellbore trajectory`, `inclination`, `azimuth`, `dogleg severity`, `tvd`, `northing`, `easting`
