# Drilling WITS Depth (Depth-Indexed Drilling Data)

Depth-summarized WITS data for depth-based analysis. This collection contains drilling parameters indexed by measured depth rather than time, enabling depth-based correlations and formation analysis. Data is aggregated as the wellbore progresses, with each depth interval containing the associated drilling parameters.

## When to use this dataset

- You need drilling parameters indexed by depth rather than time.
- You want to correlate drilling data with formations.
- You need depth-based data for well correlation.
- You want to build depth-indexed drilling logs.
- You need to export data in LAS format.
- You want to analyze parameters as a function of depth.

## Example queries

### Alerting
- Alert on parameter anomalies at specific depths.
- Notify when approaching formation depth with characteristic parameters.

### Visualization
- Plot drilling parameters vs measured depth.
- Create depth-based parameter logs.
- Correlate parameters across multiple wells by depth.
- Display composite logs with gamma and drilling parameters.

### Q&A
- What were the drilling parameters at this depth?
- How do drilling parameters change across formations?
- What was the ROP through the target zone?
- How do parameters at this depth compare to offset wells?

## Frequency

`per_depth_increment` (one record per depth interval as drilled)

## Primary keys and meaning

- `timestamp_read`: Unix/epoch timestamp when the data was recorded.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `measured_depth`: The measured depth for this data point.
- `log_identifier`: Identifier for the log type.

## Available fields

### Top-level fields

- `timestamp_read` (long): Unix/epoch timestamp when data was recorded.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `measured_depth` (float): Measured depth for this record.
- `log_identifier` (string): Log type identifier.

### `data` fields (inferred from domain knowledge)

- `data.tvd` (float): True vertical depth at this measured depth.
- `data.rop` (float): Rate of penetration at this depth.
- `data.wob` (float): Weight on bit at this depth.
- `data.rpm` (float): Rotary RPM at this depth.
- `data.torque` (float): Rotary torque at this depth.
- `data.standpipe_pressure` (float): Standpipe pressure at this depth.
- `data.gamma_ray` (float): Gamma ray reading at this depth.
- `data.diff_press` (float): Differential pressure at this depth.
- `data.state` (string): Drilling state at this depth.

## Collection schema

```json
{
  "timestamp_read": "long",
  "asset_id": "int",
  "company_id": "int",
  "measured_depth": "float",
  "log_identifier": "string",
  "data.tvd": "float",
  "data.rop": "float",
  "data.wob": "float",
  "data.rpm": "float",
  "data.torque": "float",
  "data.standpipe_pressure": "float",
  "data.gamma_ray": "float",
  "data.diff_press": "float",
  "data.state": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains depth-indexed drilling parameters.

## Keywords

`drilling wits depth`, `depth indexed`, `depth based`, `las export`, `well correlation`, `depth log`, `drilling log`
