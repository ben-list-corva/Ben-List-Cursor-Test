# Directional Trend (Wellbore Trend Analysis)

Directional trend analysis data providing time-series tracking of wellbore direction and position changes. This collection contains trend data showing how the wellbore trajectory is evolving over time, including toolface readings, inclination/azimuth changes, and positional trends useful for real-time directional monitoring.

## When to use this dataset

- You need real-time directional trend monitoring.
- You want to track toolface consistency over time.
- You need to analyze inclination and azimuth trends.
- You want to correlate directional changes with drilling parameters.
- You need trend data for directional decision support.

## Example queries

### Alerting
- Alert when directional trend shows unexpected change.
- Notify when toolface drifts outside acceptable range.
- Alert on sudden inclination or azimuth changes.

### Visualization
- Plot toolface vs time during slide drilling.
- Chart inclination trend over the lateral section.
- Display azimuth walk patterns over depth.
- Show continuous inclination and azimuth readings.

### Q&A
- What is the current toolface trend?
- Is the inclination building or dropping?
- What is the azimuth walk rate?
- How stable has the toolface been during this slide?
- What is the trend in continuous inclination readings?

## Frequency

`per_interval` (high-frequency trend data during directional drilling)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the trend reading.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the trend reading.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.measured_depth` (float): Current measured depth.
- `data.bit_depth` (float): Current bit depth.
- `data.gravity_toolface` (float): Gravity (high-side) toolface reading.
- `data.magnetic_toolface` (float): Magnetic toolface reading.
- `data.continuous_inclination` (float): Continuous inclination from MWD.
- `data.continuous_azimuth` (float): Continuous azimuth from MWD (if available).
- `data.toolface_trend` (float): Smoothed toolface trend value.
- `data.inclination_trend` (float): Inclination trend direction.
- `data.azimuth_trend` (float): Azimuth trend direction.
- `data.state` (string): Current drilling state.
- `data.tvd` (float): True vertical depth.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.measured_depth": "float",
  "data.bit_depth": "float",
  "data.gravity_toolface": "float",
  "data.magnetic_toolface": "float",
  "data.continuous_inclination": "float",
  "data.continuous_azimuth": "float",
  "data.toolface_trend": "float",
  "data.inclination_trend": "float",
  "data.azimuth_trend": "float",
  "data.state": "string",
  "data.tvd": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains time-series directional trend data for monitoring wellbore direction changes.

## Keywords

`directional trend`, `toolface trend`, `inclination trend`, `azimuth trend`, `continuous inclination`, `directional monitoring`
