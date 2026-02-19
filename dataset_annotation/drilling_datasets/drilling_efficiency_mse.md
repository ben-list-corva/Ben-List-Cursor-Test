# Drilling Efficiency MSE (Mechanical Specific Energy)

Mechanical Specific Energy (MSE) calculations for drilling efficiency analysis. MSE represents the energy required to remove a unit volume of rock and is a key indicator of drilling efficiency. Lower MSE values generally indicate more efficient drilling.

## When to use this dataset

- You need to analyze drilling efficiency using MSE.
- You want to identify drilling dysfunctions (vibrations, inefficient parameters).
- You need to optimize weight on bit and RPM combinations.
- You want to compare drilling efficiency across formations.
- You need MSE data for parameter optimization.

## Example queries

### Alerting
- Alert when MSE exceeds baseline indicating dysfunction.
- Notify when MSE trends suggest parameter optimization opportunity.
- Alert on sustained high MSE values.

### Visualization
- Plot MSE vs depth or time.
- Create MSE heatmaps for parameter optimization.
- Chart MSE against drilling parameters.
- Display MSE efficiency zones.

### Q&A
- What is the current MSE?
- What parameters give the lowest MSE?
- How does MSE compare across formations?
- Is there evidence of drilling dysfunction based on MSE?
- What is the MSE baseline for efficient drilling?

## Frequency

`per_interval` (calculated at regular intervals during drilling)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the MSE calculation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.mse` (float): Calculated Mechanical Specific Energy.
- `data.status` (string): Status of the MSE calculation.
- `data.hole_depth` (float): Hole depth at calculation time.
- `data.bit_depth` (float): Bit depth at calculation time.
- `data.rop` (float): Rate of penetration used in calculation.
- `data.wob` (float): Weight on bit used in calculation.
- `data.rpm` (float): Rotary RPM used in calculation.
- `data.torque` (float): Torque used in calculation.
- `data.bit_diameter` (float): Bit diameter for calculation.
- `data.mse_corrected` (float): Corrected MSE (hydraulics adjusted) (inferred).
- `data.efficiency` (float): Drilling efficiency percentage (inferred).
- `data.baseline_mse` (float): Baseline/minimum MSE for formation (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.mse": "float",
  "data.status": "string",
  "data.hole_depth": "float",
  "data.bit_depth": "float",
  "data.rop": "float",
  "data.wob": "float",
  "data.rpm": "float",
  "data.torque": "float",
  "data.bit_diameter": "float",
  "data.mse_corrected": "float",
  "data.efficiency": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains MSE calculations and drilling efficiency data.

## Keywords

`mse`, `mechanical specific energy`, `drilling efficiency`, `drilling optimization`, `bit efficiency`, `drilling performance`
