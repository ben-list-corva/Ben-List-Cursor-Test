# PDM Operating Condition (Motor Operating Parameters)

PDM operating condition monitoring data providing detailed motor operating parameters. This collection contains real-time PDM performance metrics including flow rate, differential pressure, torque output, RPM, and operating limits for motor optimization and protection.

## When to use this dataset

- You need detailed PDM operating parameters.
- You want to monitor motor flowrate and differential pressure.
- You need motor torque and RPM data.
- You want to check if operating within motor limits.
- You need PDM data for drilling optimization.

## Example queries

### Alerting
- Alert when operating outside motor flowrate limits.
- Notify when differential pressure exceeds threshold.
- Alert when approaching motor stall conditions.

### Visualization
- Display PDM operating envelope.
- Plot differential pressure vs torque.
- Show current operating point on motor curve.
- Chart motor RPM and power output.

### Q&A
- Is the motor operating within recommended limits?
- What is the current motor torque output?
- What is the total bit RPM (surface + motor)?
- What are the motor operating limits?
- Is flowrate adequate for motor performance?

## Frequency

`per_interval` (real-time during drilling)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the operating condition record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.bit_depth` (float): Current bit depth.
- `data.hole_depth` (float): Current hole depth.
- `data.bit_depth_tvd` (float): Bit depth TVD.
- `data.hole_depth_tvd` (float): Hole depth TVD.
- `data.flow_rate` (float): Current mud flow rate.
- `data.differential_pressure` (float): Motor differential pressure.
- `data.torque` (float): Motor torque output.
- `data.rpm` (float): Motor output RPM.
- `data.total_bit_rpm` (float): Total bit RPM (surface + motor).
- `data.total_bit_torque` (float): Total bit torque.
- `data.pdm_power` (float): Motor power output.
- `data.limits` (object): Motor operating limits.
  - `data.limits.min_rpm` (float): Minimum recommended RPM.
  - `data.limits.max_rpm` (float): Maximum recommended RPM.
  - `data.limits.min_standard_flowrate` (float): Minimum flowrate.
  - `data.limits.max_standard_flowrate` (float): Maximum flowrate.
  - `data.limits.max_differential_pressure` (float): Maximum differential pressure.
  - `data.limits.transitional_differential_pressure_limit` (float): Warning threshold for diff pressure.
- `data.torque_line` (array): Motor torque curve with differential_pressure and torque points.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.bit_depth": "float",
  "data.hole_depth": "float",
  "data.flow_rate": "float",
  "data.differential_pressure": "float",
  "data.torque": "float",
  "data.rpm": "float",
  "data.total_bit_rpm": "float",
  "data.total_bit_torque": "float",
  "data.pdm_power": "float",
  "data.limits": "object",
  "data.torque_line": "array"
}
```

## Sample record

```json
{
  "_id": "example_pdm_operating-condition",
  "version": 1,
  "provider": "corva",
  "collection": "pdm.operating-condition",
  "timestamp": 1768920599,
  "data": {
    "bit_depth": 1611.2,
    "hole_depth": 21250,
    "bit_depth_tvd": 1610.98,
    "hole_depth_tvd": 8712.45,
    "flow_rate": 0,
    "differential_pressure": 0,
    "torque": 0,
    "rpm": 0,
    "total_bit_rpm": 0,
    "total_bit_torque": 0,
    "pdm_power": 0,
    "limits": {
      "min_rpm": 101.5,
      "max_rpm": 203,
      "min_standard_flowrate": 350,
      "max_standard_flowrate": 700,
      "max_differential_pressure": 1840,
      "transitional_differential_pressure_limit": 1656
    },
    "torque_line": [
      {"differential_pressure": 0, "torque": 0},
      {"differential_pressure": 1840, "torque": 15730}
    ]
  },
  "asset_id": 12345,
  "company_id": 81
}
```

## Keywords

`pdm operating condition`, `motor parameters`, `differential pressure`, `motor rpm`, `motor torque`, `flowrate limits`, `pdm performance`
