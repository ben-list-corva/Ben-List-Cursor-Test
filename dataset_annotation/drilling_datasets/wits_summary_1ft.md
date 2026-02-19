# WITS Summary 1-Foot (Depth-Based Aggregated Data)

One-foot depth-based aggregated WITS data. This collection contains WITS sensor measurements aggregated by depth intervals (1-foot increments) rather than time intervals. Use this dataset for depth-based analysis, formation correlation, geosteering, and scenarios where drilling parameters need to be indexed by depth rather than time.

## When to use this dataset

- You need depth-indexed drilling data rather than time-indexed data.
- You want to correlate drilling parameters with formations or depth intervals.
- You need data for geosteering or formation analysis applications.
- You want to analyze parameter changes as a function of depth.
- You need to build depth-based crossplots or parameter comparisons.
- You want to correlate drilling data with geological features.

## Example queries

### Alerting
- Alert when drilling parameters change significantly at certain depths.
- Notify when approaching target formation depths.
- Alert on parameter anomalies at specific depth intervals.

### Visualization
- Plot drilling parameters vs depth (depth on Y-axis).
- Create crossplots of ROP vs WOB at each depth.
- Show gamma ray curve vs depth for formation identification.
- Display parameter variations across the wellbore depth.
- Build composite logs with multiple parameters vs depth.

### Q&A
- What were the drilling parameters at a specific depth?
- How did ROP change through the target formation?
- What was the average WOB through the lateral section?
- At what depth did we see the gamma ray spike?
- What was the drilling state at each foot of the lateral?

## Frequency

`per_foot` (one record per foot of drilled depth)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when this depth was drilled.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.hole_depth`: The measured depth for this record.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp when this depth interval was drilled.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

Fields include aggregated statistics with min/max suffixes for the depth interval:

- `data.hole_depth` (float): Hole depth for this record.
- `data.hole_depth_min` (float): Minimum hole depth in the interval.
- `data.hole_depth_max` (float): Maximum hole depth in the interval.
- `data.bit_depth` (float): Bit depth at this interval.
- `data.rop` (float): Rate of penetration for this foot.
- `data.rotary_rpm` (float): Rotary RPM during this depth interval.
- `data.rotary_torque` (float): Rotary torque during this depth interval.
- `data.hook_load` (float): Hook load during this depth interval.
- `data.weight_on_bit` (float): Weight on bit during this depth interval.
- `data.standpipe_pressure` (float): Standpipe pressure during this depth interval.
- `data.diff_press` (float): Differential pressure during this depth interval.
- `data.mud_flow_in` (float): Mud flow rate during this depth interval.
- `data.gamma_ray` (float): Gamma ray reading at this depth.
- `data.state` (string): Predominant rig state during this depth interval.
- `data.state_max` (string): Most common state during this foot (for filtering).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.hole_depth": "float",
  "data.hole_depth_min": "float",
  "data.hole_depth_max": "float",
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
  "data.state_max": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains 1-foot depth-indexed versions of WITS data fields with min/max statistics.

## Keywords

`wits summary`, `1 foot summary`, `depth based`, `depth indexed`, `formation correlation`, `geosteering`, `depth vs parameter`
