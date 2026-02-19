# Pressure Gradient (Pore Pressure and Fracture Gradient)

Pressure gradient profiles including pore pressure and fracture gradient data. This collection contains depth-based pressure profiles essential for mud weight selection, well control planning, and kick tolerance calculations.

## When to use this dataset

- You need pore pressure and fracture gradient for mud weight planning.
- You want to display mud weight window visualization.
- You need pressure data for well control calculations.
- You want to analyze kick tolerance at specific depths.
- You need pressure gradients for hydraulics modeling.

## Example queries

### Alerting
- Alert when approaching narrow mud weight window.
- Notify when mud weight is outside safe window.

### Visualization
- Display pore pressure and fracture gradient vs depth.
- Show mud weight window with current mud weight.
- Plot pressure gradients on wellbore schematic.

### Q&A
- What is the pore pressure at this depth?
- What is the fracture gradient at TD?
- What is the safe mud weight window?
- What is the minimum overbalance required?

## Frequency

`per_well` (typically one record per well with depth-based profile)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the profile was created.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.pressure_points` (array): Array of depth-based pressure values (inferred).
- Pressure point fields:
  - `depth` (float): Measured depth or TVD.
  - `pore_pressure` (float): Pore pressure gradient in ppg equivalent.
  - `fracture_gradient` (float): Fracture gradient in ppg equivalent.
  - `overburden` (float): Overburden gradient (inferred).
- `data.source` (string): Source of pressure data (predicted, measured) (inferred).
- `data.units` (string): Units for pressure values (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.pressure_points": "array",
  "data.source": "string",
  "data.units": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains pressure gradient profiles with depth-based values.

## Keywords

`pressure gradient`, `pore pressure`, `fracture gradient`, `mud weight window`, `well control`, `kick tolerance`, `pressure profile`
