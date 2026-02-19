# Completion WITS Raw (Unprocessed Frac Data)

Raw unprocessed completion WITS data. This collection contains the original data as received from frac data sources before any enrichment or standardization. Used for data quality checks, troubleshooting, and accessing original values before processing.

## When to use this dataset

- You need original unprocessed frac data.
- You want to troubleshoot data quality issues.
- You need to verify data transformations.
- You want to access raw channel values.

## Example queries

### Alerting
- Alert on raw data anomalies.
- Notify when raw data stops flowing.

### Visualization
- Compare raw vs processed values.
- Display raw channel data for debugging.

### Q&A
- What was the original raw value for this channel?
- How does raw data compare to processed?
- What channels are available in raw data?

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
- `stage_number` (int): Current stage number.
- `app` (string): Source application that provided the data.
- `source_app` (string): Original source application.

### `data` fields

Raw data fields vary by data provider and include original channel names. Common fields include:
- `data.wellhead_pressure` (float): Raw wellhead pressure.
- `data.backside_pressure` (float): Raw backside pressure.
- `data.slurry_flow_rate_in` (float): Raw slurry flow rate.
- `data.proppant_1_mass` (float): Raw proppant mass.
- `data.proppant_1_concentration` (float): Raw proppant concentration.
- `data.friction_reducer` (float): Raw friction reducer rate.
- `data.powder_friction_reducer` (float): Raw powder FR rate.

Note: This dataset contains many dynamic/custom fields that vary by operator and data provider.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "app": "string",
  "source_app": "string",
  "data": "object"
}
```

## Sample record

```json
{
  "_id": "example_completion_wits_raw",
  "version": 1,
  "provider": "corva",
  "collection": "completion.wits.raw",
  "timestamp": 1768975310,
  "stage_number": 1,
  "company_id": 81,
  "asset_id": 12345,
  "app": "corva.completion-column-mapper",
  "data": {
    "proppant_1_mass": 3713.1,
    "friction_reducer": 0,
    "backside_pressure": 166,
    "wellhead_pressure": 9554,
    "slurry_flow_rate_in": 84,
    "powder_friction_reducer": 3.4239,
    "proppant_1_concentration": 0.25,
    "hydrostatic_pressure_streamed": 4583,
    "total_clean_volume_in_streamed": 662.6,
    "total_slurry_volume_in_streamed": 667.9
  },
  "source_app": "corva.stream-frac-source"
}
```

## Keywords

`completion wits raw`, `raw frac data`, `unprocessed data`, `frac source data`, `raw channels`
