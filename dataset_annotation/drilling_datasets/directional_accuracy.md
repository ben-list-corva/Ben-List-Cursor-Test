# Directional Accuracy (Wellbore Trajectory Comparison)

The directional accuracy of the wellbore. Actual wellbore surveys are compared with the planned trajectory to determine the accuracy of the wellbore trajectory. The latest actual survey point and the corresponding planned survey point are available in this collection. The comparison is essentially the distance between the plan point and the actual survey. This can be center to center or in a particular plane. The comparison for all horizontal, vertical and minimum distance planes are available in the collection. General distance to plan, severity of the deviation and right/left or high/low is also available in the collection.

## When to use this dataset

- You want to know how closely the wellbore trajectory matches the planned trajectory.
- You need to monitor directional deviation and make drilling adjustments.
- You want to track severity of trajectory deviations (high, medium, low).
- You need to compare planned vs actual survey points (inclination, azimuth, northing, easting, TVD).
- You want to determine if the well is drilling high/low or right/left of plan.
- You need to visualize the deviation from the planned trajectory over time.
- You want to answer questions about current or historical directional accuracy.

## Example queries

### Alerting
- Alert when I am more than 10 feet away from the planned trajectory in any direction.
- Alert when my inclination is more than 1 degree away from the planned trajectory.
- Alert when my azimuth is more than 1 degree away from the planned trajectory.
- Alert when I am higher than planned by more than 10 feet.
- Notify me when severity changes from low to medium or high.

### Visualization
- Show the distance to plan trend over the last 5 surveys.
- Plot the deviation history (high/low and right/left) over time.
- Chart the planned vs actual inclination and azimuth over depth.
- Visualize the severity changes throughout the drilling operation.

### Q&A
- What is the current distance to plan?
- How far off am I from the planned trajectory right now?
- Am I drilling high or low compared to the plan?
- What was the maximum deviation from plan during this well?
- What is the current severity of the directional deviation?
- How has the distance to plan changed over the last few surveys?

## Frequency

`per_survey` (triggered on new survey or survey update)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the data point.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the data point.
- `asset_id` (int): Unique asset ID.

### `data.plan_point` fields

Planned survey point from the well plan. This is how they want to drill the well directionally.

- `data.plan_point.measured_depth` (float): Hole depth of the planned survey point.
- `data.plan_point.inclination` (float): Inclination of the planned survey point.
- `data.plan_point.azimuth` (float): Azimuth of the planned survey point.
- `data.plan_point.northing` (float): Northing of the planned survey point.
- `data.plan_point.easting` (float): Easting of the planned survey point.
- `data.plan_point.tvd` (float): True vertical depth of the planned survey point.

### `data.actual_point` fields

Actual survey point of the wellbore at a given depth. This is from the directional surveys taken as they drill the well. The actual trajectory will deviate from the planned trajectory due to various reasons. Actual surveys will not necessarily be at the same depth as the planned survey because planned surveys are usually calculated at fixed depths and actual surveys are taken as drilling progresses (roughly every 100 feet, sometimes 30 feet).

- `data.actual_point.measured_depth` (float): Hole depth of the actual survey point.
- `data.actual_point.inclination` (float): Inclination at the actual survey point.
- `data.actual_point.azimuth` (float): Azimuth at the actual survey point.
- `data.actual_point.northing` (float): Northing at the actual survey point.
- `data.actual_point.easting` (float): Easting at the actual survey point.
- `data.actual_point.tvd` (float): True vertical depth at the actual survey point.

### `data.accuracy` fields

- `data.accuracy.severity` (string): Severity of the deviation based on distance to plan. Can be `high`, `medium`, or `low`.
- `data.accuracy.distance_to_plan` (float): Center to center distance between the planned survey point and the actual survey point in 3D space. This is the shortest distance between the two points.

### `data.recommendation` fields

Distance to plan in specific directions relative to the wellbore.

- `data.recommendation.high` (float): Distance to plan in the high direction (high side of the wellbore).
- `data.recommendation.right` (float): Distance to plan in the right direction (right side of the wellbore).
- `data.recommendation.low` (float): Distance to plan in the low direction (low side of the wellbore).
- `data.recommendation.left` (float): Distance to plan in the left direction (left side of the wellbore).

### `data.minimum_distance_plane` fields

Minimum distance plane comparison between actual and planned survey points.

- `data.minimum_distance_plane.actual_point` (object): Actual survey point in the minimum distance plane.
- `data.minimum_distance_plane.plan_point` (object): Plan point in the minimum distance plane.
- `data.minimum_distance_plane.high` (float): Vertical offset in the high direction.
- `data.minimum_distance_plane.right` (float): Lateral offset in the right direction.
- `data.minimum_distance_plane.distance` (float): Distance in the minimum distance plane.

### Other fields

- `data.actual_name` (string): Name of the actual survey.
- `data.plan_name` (string): Name of the well plan.
- `data.points` (array): Array of directional accuracy points for the wellbore. Contains objects with severity, distance_to_plan, and timestamp for each survey point or survey update.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "data.plan_point": "object",
  "data.plan_point.measured_depth": "float",
  "data.plan_point.inclination": "float",
  "data.plan_point.azimuth": "float",
  "data.plan_point.northing": "float",
  "data.plan_point.easting": "float",
  "data.plan_point.tvd": "float",
  "data.actual_point": "object",
  "data.actual_point.measured_depth": "float",
  "data.actual_point.inclination": "float",
  "data.actual_point.azimuth": "float",
  "data.actual_point.northing": "float",
  "data.actual_point.easting": "float",
  "data.actual_point.tvd": "float",
  "data.accuracy.severity": "string",
  "data.accuracy.distance_to_plan": "float",
  "data.recommendation.high": "float",
  "data.recommendation.right": "float",
  "data.recommendation.low": "float",
  "data.recommendation.left": "float",
  "data.minimum_distance_plane": "object",
  "data.minimum_distance_plane.actual_point": "object",
  "data.minimum_distance_plane.actual_point.measured_depth": "float",
  "data.minimum_distance_plane.actual_point.inclination": "float",
  "data.minimum_distance_plane.actual_point.azimuth": "float",
  "data.minimum_distance_plane.actual_point.northing": "float",
  "data.minimum_distance_plane.actual_point.easting": "float",
  "data.minimum_distance_plane.actual_point.tvd": "float",
  "data.actual_name": "string",
  "data.plan_name": "string",
  "data.points": "array"
}
```

## Sample record

```json
{
  "_id": "67d50adfd7caa200174ca7b7",
  "version": 1,
  "provider": "corva",
  "collection": "directional.accuracy",
  "timestamp": 1742015180,
  "asset_id": 74178917,
  "company_id": 25,
  "data": {
    "plan_point": {
      "measured_depth": 17929.69,
      "inclination": 91.8,
      "azimuth": 318.75,
      "northing": 2814.37,
      "easting": -4860.71,
      "tvd": 11244.79
    },
    "actual_point": {
      "measured_depth": 17889.0,
      "inclination": 91.16,
      "azimuth": 318.53,
      "northing": 2814.57,
      "easting": -4860.65,
      "tvd": 11247.91
    },
    "horizontal_plane": {
      "actual_point": {
        "measured_depth": 17889.0,
        "inclination": 91.16,
        "azimuth": 318.53,
        "northing": 2814.57,
        "easting": -4860.65,
        "tvd": 11247.91
      },
      "plan_point": {
        "measured_depth": 17830.63,
        "inclination": 91.8,
        "azimuth": 318.75,
        "northing": 2739.92,
        "easting": -4795.43,
        "tvd": 11247.91
      },
      "ahead_azimuth": 318.75,
      "ahead": 99.13,
      "right": 0.18,
      "distance": 99.13
    },
    "survey_measured_depth": 17889.0,
    "vertical_plane": {
      "actual_point": {
        "measured_depth": 17889.0,
        "inclination": 91.16,
        "azimuth": 318.53,
        "northing": 2814.57,
        "easting": -4860.65,
        "tvd": 11247.91
      },
      "plan_point": {
        "measured_depth": 17929.81,
        "inclination": 91.8,
        "azimuth": 318.75,
        "northing": 2814.45,
        "easting": -4860.79,
        "tvd": 11244.79
      },
      "ahead_azimuth": 318.75,
      "below": 3.12,
      "right": 0.18,
      "distance": 3.12
    },
    "accuracy": {
      "severity": "low",
      "distance_to_plan": 3.119008929550836
    },
    "recommendation": {
      "high": -3.113686483623981,
      "right": 0.1821350716179991
    },
    "actual_name": "",
    "minimum_distance_plane": {
      "actual_point": {
        "measured_depth": 17889.0,
        "inclination": 91.16,
        "azimuth": 318.53,
        "northing": 2814.57,
        "easting": -4860.65,
        "tvd": 11247.91
      },
      "plan_point": {
        "measured_depth": 17929.69,
        "inclination": 91.8,
        "azimuth": 318.75,
        "northing": 2814.37,
        "easting": -4860.71,
        "tvd": 11244.79
      },
      "high": -3.11,
      "right": 0.18,
      "distance": 3.12
    },
    "plan_name": "Design 2",
    "points": [
      {
        "severity": "low",
        "distance_to_plan": 13.29,
        "timestamp": 1741994746
      },
      {
        "severity": "low",
        "distance_to_plan": 8.29,
        "timestamp": 1741997150
      },
      {
        "severity": "low",
        "distance_to_plan": 6.78,
        "timestamp": 1741999554
      },
      {
        "severity": "low",
        "distance_to_plan": 4.98,
        "timestamp": 1742001357
      }
    ],
    "status": 0
  }
}
```

## Keywords

`directional accuracy`, `directional deviation`, `directional survey`, `directional survey accuracy`, `directional survey deviation`, `distance to plan`, `wellbore trajectory`
