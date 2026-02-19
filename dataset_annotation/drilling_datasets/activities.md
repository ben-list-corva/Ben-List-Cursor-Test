# Activities (Automated Rig Activity Detection)

Automated rig activity detection and classification data. This collection contains detected drilling activities with start/end times, duration, and associated depth changes. Activities are automatically classified based on real-time sensor data patterns and represent discrete operational periods during drilling.

## When to use this dataset

- You need to identify what activity the rig was performing during a specific time period.
- You want to analyze time spent on different drilling activities.
- You need to correlate depth progress with specific activities.
- You want to track activity transitions and duration patterns.
- You need to break down operational time by day/night shifts.
- You want to analyze drilling efficiency by activity type.

## Example queries

### Alerting
- Alert when a specific activity (e.g., "Circulating") exceeds a certain duration.
- Notify when the rig has been "In Slips" for more than 30 minutes.
- Alert on unexpected activity transitions.

### Visualization
- Plot activity timeline showing different activities color-coded over time.
- Chart time distribution across different activity types.
- Show depth progress correlated with activity changes.
- Visualize day vs night shift activity breakdown.

### Q&A
- What activity was the rig performing at a specific time?
- How much time was spent on "Rotary Drilling" today?
- What was the total footage drilled during "Rotary Drilling" activities?
- How does activity distribution compare between day and night shifts?
- What is the average duration of connection activities?

## Frequency

`per_activity` (one record per detected activity period)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp marking the end of the activity.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.start_time`: Unix/epoch timestamp marking the start of the activity (unique per asset).

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the data point (typically the end time).
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.start_time` (long): Unix/epoch timestamp when the activity started.
- `data.end_time` (long): Unix/epoch timestamp when the activity ended.
- `data.operation_time` (int): Duration of the activity in seconds.
- `data.activity_name` (string): Name/classification of the detected activity (e.g., "Rotary Drilling", "In Slips", "Circulating").
- `data.hole_depth_change` (float): Change in hole depth during the activity (feet or meters).
- `data.bit_depth_change` (float): Change in bit depth during the activity.
- `data.block_height_change` (float): Change in block height during the activity.
- `data.hole_depth` (float): Hole depth at the end of the activity.
- `data.bit_depth` (float): Bit depth at the end of the activity.
- `data.block_height` (float): Block height at the end of the activity.
- `data.shift_time.day` (int): Seconds of this activity that occurred during day shift.
- `data.shift_time.night` (int): Seconds of this activity that occurred during night shift.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.start_time": "long",
  "data.end_time": "long",
  "data.operation_time": "int",
  "data.activity_name": "string",
  "data.hole_depth_change": "float",
  "data.bit_depth_change": "float",
  "data.block_height_change": "float",
  "data.hole_depth": "float",
  "data.bit_depth": "float",
  "data.block_height": "float",
  "data.shift_time": "object",
  "data.shift_time.day": "int",
  "data.shift_time.night": "int"
}
```

## Sample record

```json
{
  "_id": "example_activities",
  "version": 1,
  "provider": "corva",
  "collection": "activities",
  "timestamp": 1768399040,
  "asset_id": 12345,
  "company_id": 81,
  "data": {
    "start_time": 1768397400,
    "end_time": 1768399040,
    "operation_time": 1640,
    "activity_name": "Rotary Drilling",
    "hole_depth_change": 91.21,
    "bit_depth_change": 91.18,
    "block_height_change": -91.15,
    "hole_depth": 14230.53,
    "bit_depth": 14230.53,
    "block_height": 93.21,
    "shift_time": {
      "day": 1640,
      "night": 0
    }
  }
}
```

## Keywords

`activities`, `rig activity`, `activity detection`, `drilling activity`, `operational activity`, `activity classification`
