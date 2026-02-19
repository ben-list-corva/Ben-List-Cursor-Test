# WITS Summary 30-Minute (Aggregated Drilling Data)

Thirty-minute aggregated WITS data for trend analysis. This collection contains WITS sensor measurements aggregated over 30-minute intervals, providing statistical summaries of drilling parameters at a coarser resolution. Use this dataset for long-term trend analysis, days-vs-depth charts, and scenarios where high-level drilling progression is more important than detailed parameter analysis.

## When to use this dataset

- You need half-hour level drilling data for trend analysis.
- You want to analyze drilling progression over days or weeks.
- You need to build days-vs-depth charts or similar long-term visualizations.
- You want minimal data volume while still capturing drilling trends.
- You need to compare drilling performance across long time periods.
- You want to analyze shift-level or daily drilling patterns.

## Example queries

### Alerting
- Alert on sustained poor performance over 30-minute periods.
- Notify when depth progress falls behind plan at half-hour intervals.

### Visualization
- Plot days-vs-depth chart for the entire well.
- Chart long-term ROP trends over the drilling campaign.
- Show depth progression compared to planned timeline.
- Display TVD vs measured depth progression.

### Q&A
- What was the average drilling rate over the past day?
- How does today's footage compare to yesterday?
- What is the overall trend in drilling efficiency?
- How many 30-minute intervals were spent drilling vs non-drilling?
- What was the depth at each 30-minute mark?

## Frequency

`per_30_minutes` (one record per 30-minute interval)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp marking the start of the 30-minute interval.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the 30-minute interval start.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

The data fields mirror the WITS dataset fields but aggregated over 30-minute intervals. Common fields include:

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
- `data.state` (string): Predominant rig state during the interval.
- `data.true_vertical_depth` (float): True vertical depth.

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
  "data.state": "string",
  "data.true_vertical_depth": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains 30-minute aggregated versions of WITS data fields.

## Keywords

`wits summary`, `30 minute summary`, `aggregated wits`, `days vs depth`, `long term trend`, `drilling progression`
