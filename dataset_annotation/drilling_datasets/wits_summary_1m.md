# WITS Summary 1-Minute (Aggregated Drilling Data)

One-minute aggregated WITS data for performance analysis. This collection contains WITS sensor measurements aggregated over 1-minute intervals, providing statistical summaries (min, max, average) of drilling parameters. Use this dataset when you need lower-resolution data for trend analysis, dashboards, or when processing large time ranges where per-second granularity is not required.

## When to use this dataset

- You need minute-level drilling data rather than per-second resolution.
- You want to analyze trends over longer time periods without overwhelming data volume.
- You need aggregated statistics (min, max, avg) for drilling parameters.
- You want to build dashboards or visualizations with reasonable data density.
- You need to correlate drilling parameters with state/activity at minute resolution.
- You want to perform time-series analysis on drilling data.

## Example queries

### Alerting
- Alert when average ROP drops below threshold for consecutive minutes.
- Notify when standpipe pressure exceeds limits during drilling state.
- Alert on sustained high differential pressure.

### Visualization
- Plot ROP trend over the last 24 hours.
- Chart standpipe pressure vs time during drilling operations.
- Show hole depth progression over the well timeline.
- Display heatmaps of drilling parameters over time and depth.

### Q&A
- What was the average ROP over the last hour?
- When did the highest standpipe pressure occur today?
- How has hole depth progressed over the last shift?
- What was the drilling state during specific time periods?
- What is the trend in differential pressure over the last 6 hours?

## Frequency

`per_minute` (one record per minute)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp marking the start of the 1-minute interval.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the 1-minute interval start.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

The data fields mirror the WITS dataset fields but may include aggregated statistics. Common fields include:

- `data.hole_depth` (float): Hole depth (typically max value in the interval).
- `data.bit_depth` (float): Bit depth at the interval.
- `data.rop` (float): Rate of penetration (typically average for the interval).
- `data.rotary_rpm` (float): Rotary RPM measurement.
- `data.rotary_torque` (float): Rotary torque measurement.
- `data.hook_load` (float): Hook load measurement.
- `data.weight_on_bit` (float): Weight on bit measurement.
- `data.standpipe_pressure` (float): Standpipe pressure measurement.
- `data.diff_press` (float): Differential pressure measurement.
- `data.mud_flow_in` (float): Mud flow in rate.
- `data.gamma_ray` (float): Gamma ray measurement (MWD).
- `data.state` (string): Predominant rig state during the interval.
- `data.entry_at` (long): Entry timestamp for the record.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.hole_depth": "float",
  "data.bit_depth": "float",
  "data.rop": "float",
  "data.rotary_rpm": "float",
  "data.rotary_torque": "float",
  "data.hook_load": "float",
  "data.weight_on_bit": "float",
  "data.standpipe_pressure": "float",
  "data.diff_press": "float",
  "data.mud_flow_in": "float",
  "data.gamma_ray": "float",
  "data.state": "string",
  "data.entry_at": "long"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains 1-minute aggregated versions of WITS data fields.

## Keywords

`wits summary`, `1 minute summary`, `aggregated wits`, `drilling trend`, `time series`, `minute data`
