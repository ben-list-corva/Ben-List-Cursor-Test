# WITS (Real-Time Drilling Data)

Real-time drilling data captured from the rig while drilling or performing other operations. This collection contains instantaneous sensor measurements recorded every second. Use it for operational monitoring, performance analysis, and context about rig state/activity.

## When to use this dataset

- You need second-by-second drilling rig sensor measurements.
- You need current operational status or activity state.
- You want to correlate drilling parameters (rpm, torque, WOB, ROP, pressure) over time.
- You need depth-based context (hole depth, bit depth, block height).

## Example queries

- Show the last 10 minutes of rop, weight on bit, and rotary rpm for asset 34165773.
- Find periods where state is In Slips and hook load drops sharply.
- Plot standpipe pressure vs mud flow in over the last hour.
- Compare bit depth and hole depth to identify drilling vs tripping.
- Detect spikes in diff press and correlate with rotary torque.

## Frequency

`per_second`

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the data point.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the data point.
- `asset_id` (int): Unique asset ID.

### `data` fields

- `data.hole_depth` (float): Current hole depth.
- `data.bit_depth` (float): Current bit depth.
- `data.block_height` (float): Height of the block from the kelly bushing.
- `data.rotary_rpm` (float): Rotational speed of the drill string (surface/top drive).
- `data.rotary_torque` (float): Rotational torque applied by the top drive (surface).
- `data.hook_load` (float): Total force on the hook (includes buoyancy and friction effects).
- `data.rop` (float): Rate of penetration (usually feet per hour).
- `data.weight_on_bit` (float): Weight exerted on the bit (surface-measured).
- `data.mud_flow_in` (float): Mud flow rate pumped into the drillstring (surface).
- `data.standpipe_pressure` (float): Pressure from mud pumps into the drillstring (surface).
- `data.diff_press` (float): Differential pressure across the mud motor (PDM).
- `data.gamma_ray` (float): Natural gamma radiation near the bit (MWD).
- `data.state` (string): Current rig state/activity (operational status).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "data.hole_depth": "float",
  "data.bit_depth": "float",
  "data.block_height": "float",
  "data.rotary_rpm": "float",
  "data.rotary_torque": "float",
  "data.hook_load": "float",
  "data.rop": "float",
  "data.weight_on_bit": "float",
  "data.mud_flow_in": "float",
  "data.standpipe_pressure": "float",
  "data.diff_press": "float",
  "data.gamma_ray": "float",
  "data.state": "string"
}
```

## Sample record

```json
{
  "_id": "631d4af8c5325e47790d10ee",
  "version": 1,
  "provider": "corva",
  "collection": "wits",
  "timestamp": 1662864118,
  "timestamp_read": 1662864119,
  "asset_id": 34165773,
  "company_id": 25,
  "app": "corva.witsml-source",
  "metadata": {
    "drillstring": null,
    "casing": "631baf582c540476da44f226",
    "mud": "631bd9a7b1db86336f289cb2",
    "cuttings": null,
    "surface-equipment": "6315f9aac4d1634594c2b2c4",
    "actual_survey": "6315f9a9c4d1634594c2b279",
    "plan_survey": "6315f9a9c4d1634594c2b281"
  },
  "data": {
    "bit_depth": 17841.31,
    "block_height": 44.22,
    "hole_depth": 17856,
    "diff_press": -22.24,
    "hook_load": 44.6,
    "rop": 0,
    "rotary_rpm": 0,
    "pump_spm_1": 0,
    "pump_spm_2": 0,
    "pump_spm_3": 0,
    "standpipe_pressure": 0,
    "rotary_torque": 0,
    "pump_spm_total": 0,
    "mud_flow_in": 0,
    "strks_total": 46,
    "strks_pump_3": 0,
    "gain_loss": 101.18,
    "weight_on_bit": 88.6,
    "gamma_ray": 0,
    "wilcox_ecd": 13.1,
    "casing_pressure": 0,
    "active_pit_volume": 706.78,
    "gravity_tool_face": 61.9,
    "magnetic_tool_face": 301.3,
    "trip_tank_volume_1": 1.04,
    "trip_tank_volume_2": 0,
    "mud_flow_out_percent": 0,
    "ad_diff_press_setpoint": 100,
    "continuous_inclination": 86.68,
    "true_vertical_depth": 12531.2,
    "state": "In Slips"
  }
}
```

## Keywords

`wits`, `witsml`, `real time drilling data`
