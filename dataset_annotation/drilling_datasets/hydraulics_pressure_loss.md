# Hydraulics Pressure Loss (Drillstring and Annulus Pressure)

Pressure loss calculations through drillstring and annulus. This collection contains calculated pressure losses at various points in the hydraulic system, including surface equipment, drillstring, bit, and annulus. Essential for monitoring equivalent circulating density (ECD), standpipe pressure predictions, and hydraulic optimization.

## When to use this dataset

- You need calculated pressure losses throughout the hydraulic system.
- You want to predict standpipe pressure for given conditions.
- You need ECD calculations for well control.
- You want to analyze hydraulic efficiency.
- You need pressure data for stuck pipe analysis.

## Example queries

### Alerting
- Alert when actual pressure differs from predicted.
- Notify when ECD approaches formation limits.
- Alert on hydraulic anomalies.

### Visualization
- Display pressure loss breakdown by component.
- Chart predicted vs actual standpipe pressure.
- Show ECD profile vs depth.
- Plot pressure loss trends over time.

### Q&A
- What is the predicted standpipe pressure?
- What is the ECD at the bit?
- Where is the majority of pressure being lost?
- How does actual pressure compare to predicted?
- What is the bit pressure drop?

## Frequency

`per_interval` (calculated at regular intervals during circulation)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.predicted_standpipe_pressure` (float): Calculated standpipe pressure.
- `data.actual_standpipe_pressure` (float): Measured standpipe pressure (inferred).
- `data.activity` (string): Current activity for calculation context.
- `data.hole_depth` (float): Hole depth for calculation.
- `data.bit_depth` (float): Bit depth for calculation.
- `data.surface_pressure_loss` (float): Pressure loss in surface equipment (inferred).
- `data.drillstring_pressure_loss` (float): Pressure loss in drillstring (inferred).
- `data.bit_pressure_loss` (float): Pressure loss across the bit (inferred).
- `data.annulus_pressure_loss` (float): Pressure loss in the annulus (inferred).
- `data.motor_pressure_loss` (float): Pressure loss through mud motor (inferred).
- `data.ecd` (float): Equivalent circulating density (inferred).
- `data.flow_rate` (float): Flow rate used in calculation (inferred).
- `data.mud_weight` (float): Mud weight used in calculation (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.predicted_standpipe_pressure": "float",
  "data.activity": "string",
  "data.hole_depth": "float",
  "data.bit_depth": "float",
  "data.surface_pressure_loss": "float",
  "data.drillstring_pressure_loss": "float",
  "data.bit_pressure_loss": "float",
  "data.annulus_pressure_loss": "float",
  "data.ecd": "float",
  "data.flow_rate": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains hydraulic pressure loss calculations.

## Keywords

`pressure loss`, `hydraulics`, `standpipe pressure`, `ecd`, `equivalent circulating density`, `bit pressure drop`, `annulus pressure`
