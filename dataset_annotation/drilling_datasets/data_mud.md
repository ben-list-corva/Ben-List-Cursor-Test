# Mud (Drilling Fluid Properties)

Drilling fluid (mud) properties data. This collection contains information about the drilling fluid used during operations including mud weight, viscosity, fluid loss, and other rheological properties. Essential for hydraulics calculations, well control, and hole cleaning analysis.

## When to use this dataset

- You need current mud properties for hydraulics calculations.
- You want to track mud weight changes throughout the well.
- You need rheological data for ECD calculations.
- You want to analyze mud program effectiveness.
- You need mud data for well control scenarios.
- You want to correlate mud properties with hole problems.

## Example queries

### Alerting
- Alert when mud weight changes significantly.
- Notify when fluid loss exceeds threshold.
- Alert when mud properties are out of specification.

### Visualization
- Plot mud weight vs depth throughout the well.
- Chart rheological properties over time.
- Show mud weight window with current properties.
- Display mud properties trend during drilling.

### Q&A
- What is the current mud weight?
- What type of mud system are we using?
- What are the current rheological properties?
- How has mud weight changed throughout the well?
- What is the plastic viscosity and yield point?

## Frequency

`per_report` (updated with each mud report, typically every 12-24 hours)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the mud report was created.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the mud report.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.mud_weight` (float): Mud weight in ppg (pounds per gallon).
- `data.mud_type` (string): Type of mud system (e.g., "Water-base", "Oil-base", "Synthetic").
- `data.plastic_viscosity` (float): Plastic viscosity in centipoise.
- `data.yield_point` (float): Yield point in lb/100sqft.
- `data.gel_strength_10s` (float): 10-second gel strength.
- `data.gel_strength_10m` (float): 10-minute gel strength.
- `data.fluid_loss` (float): API fluid loss in ml/30min.
- `data.ph` (float): pH value of the mud.
- `data.chlorides` (float): Chloride content.
- `data.solids_content` (float): Total solids percentage.
- `data.oil_water_ratio` (string): Oil/water ratio for OBM/SBM.
- `data.funnel_viscosity` (float): Marsh funnel viscosity in seconds.
- `data.depth` (float): Depth at time of mud report.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.mud_weight": "float",
  "data.mud_type": "string",
  "data.plastic_viscosity": "float",
  "data.yield_point": "float",
  "data.gel_strength_10s": "float",
  "data.gel_strength_10m": "float",
  "data.fluid_loss": "float",
  "data.ph": "float",
  "data.chlorides": "float",
  "data.solids_content": "float",
  "data.oil_water_ratio": "string",
  "data.funnel_viscosity": "float",
  "data.depth": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains drilling fluid properties from mud reports.

## Keywords

`mud`, `drilling fluid`, `mud weight`, `rheology`, `plastic viscosity`, `yield point`, `mud properties`, `drilling mud`
