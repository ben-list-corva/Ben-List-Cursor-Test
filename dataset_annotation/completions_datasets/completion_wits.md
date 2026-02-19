# Completion WITS (Real-Time Frac Data)

Real-time completion WITS data from frac operations. This collection contains per-second sensor measurements during hydraulic fracturing operations including pump rates, pressures, proppant concentrations, and volumes. Essential for frac monitoring, treatment analysis, and real-time decision making.

## When to use this dataset

- You need real-time fracturing operation data.
- You want to monitor pump rates and pressures during frac.
- You need proppant concentration and mass data.
- You want to track treatment volumes.
- You need data for frac analysis and diagnostics.

## Example queries

### Alerting
- Alert when wellhead pressure exceeds threshold.
- Notify when pump rate drops unexpectedly.
- Alert on proppant concentration changes.

### Visualization
- Plot treatment curve (pressure, rate, concentration vs time).
- Display real-time frac dashboard.
- Chart cumulative volumes and proppant mass.
- Show Nolte-Smith analysis plot.

### Q&A
- What is the current treating pressure?
- What is the current pump rate?
- How much proppant has been pumped?
- What stage are we currently fracking?
- What is the total slurry volume pumped?

## Frequency

`per_second` (real-time during frac operations)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the data point.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `stage_number`: Current frac stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the data point.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Current stage number being fractured.
- `app_key` (string): Application that generated the record.

### `data` fields

- `data.wellhead_pressure` (float): Treating pressure at wellhead (psi).
- `data.backside_pressure` (float): Annulus/backside pressure (psi).
- `data.clean_flow_rate_in` (float): Clean fluid pump rate (bpm).
- `data.slurry_flow_rate_in` (float): Slurry pump rate (bpm).
- `data.total_clean_volume_in` (float): Cumulative clean volume (bbl).
- `data.total_slurry_volume_in` (float): Cumulative slurry volume (bbl).
- `data.total_proppant_concentration` (float): Current proppant concentration (ppa).
- `data.total_proppant_mass` (float): Cumulative proppant mass (lbs).
- `data.proppant_1_concentration` (float): Proppant 1 concentration.
- `data.proppant_1_mass` (float): Proppant 1 cumulative mass.
- `data.hydraulic_horse_power` (float): Hydraulic horsepower being applied.
- `data.friction_reducer` (float): Friction reducer rate.
- `data.powder_friction_reducer` (float): Powder friction reducer rate.
- `data.elapsed_time` (int): Elapsed time in seconds.
- `data.pressure_slope_1min_rolling` (float): 1-minute rolling pressure slope.
- `data.pressure_to_rate_ratio` (float): Pressure to rate ratio.
- `data.cumulative_chemicals` (object): Cumulative chemical volumes by type.
- `data.is_valid` (boolean): Data validity flag.

Note: This dataset contains many dynamic/custom fields that vary by operator and data provider. Standard fields are documented above; dynamic fields exist but are operator-specific.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.wellhead_pressure": "float",
  "data.backside_pressure": "float",
  "data.clean_flow_rate_in": "float",
  "data.slurry_flow_rate_in": "float",
  "data.total_clean_volume_in": "float",
  "data.total_slurry_volume_in": "float",
  "data.total_proppant_concentration": "float",
  "data.total_proppant_mass": "float",
  "data.hydraulic_horse_power": "float",
  "data.elapsed_time": "int",
  "data.cumulative_chemicals": "object"
}
```

## Sample record

```json
{
  "_id": "example_completion_wits",
  "company_id": 81,
  "asset_id": 12345,
  "version": 1,
  "provider": "corva",
  "collection": "completion.wits",
  "data": {
    "total_clean_volume_in_streamed": 662.6,
    "total_slurry_volume_in_streamed": 667.9,
    "proppant_1_mass_streamed": 3713.1,
    "hydrostatic_pressure_streamed": 4583,
    "elapsed_time": 214729,
    "clean_flow_rate_in": 83.061,
    "total_clean_volume_in": 85973.473,
    "total_slurry_volume_in": 90521.9355,
    "total_proppant_concentration": 0.25,
    "total_proppant_mass": 4224791.2826,
    "hydraulic_horse_power": 19662.132,
    "wellhead_pressure": 9554,
    "slurry_flow_rate_in": 84,
    "backside_pressure": 166,
    "cumulative_chemicals": {
      "friction_reducer": 0.674,
      "powder_friction_reducer": 12577.9828
    },
    "is_valid": true
  },
  "timestamp": 1768975310,
  "stage_number": 1
}
```

## Keywords

`completion wits`, `frac data`, `treating pressure`, `pump rate`, `proppant concentration`, `hydraulic fracturing`, `frac monitoring`
