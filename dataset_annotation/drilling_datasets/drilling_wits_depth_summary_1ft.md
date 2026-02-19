# Drilling WITS Depth Summary 1ft (1-Foot Depth Summary)

One-foot depth summary of WITS data for depth-based analysis. This collection provides aggregated drilling parameters at 1-foot depth intervals, similar to the time-based wits.summary-1ft but organized in the depth-based collection structure.

## When to use this dataset

- You need standardized 1-foot depth interval data.
- You want to build formation correlation logs.
- You need consistent depth spacing for well comparisons.
- You want depth-based summary data for target formation analysis.

## Example queries

### Alerting
- Alert on parameter changes at specific depth intervals.
- Notify when approaching target formation depth.

### Visualization
- Create 1-foot resolution depth logs.
- Plot parameter variations at consistent depth intervals.
- Build formation top correlations.

### Q&A
- What were the averaged parameters for each foot drilled?
- How does this depth compare to the same depth in offset wells?
- What is the formation response at this depth interval?

## Frequency

`per_foot` (one record per 1-foot depth interval)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the summary.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `measured_depth`: The measured depth for this 1-foot interval.
- `log_identifier`: Identifier for the log type.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `measured_depth` (float): Measured depth for this record.
- `log_identifier` (string): Log type identifier.

### `data` fields (inferred from domain knowledge)

- `data.rop` (float): Average ROP for this foot.
- `data.wob` (float): Average WOB for this foot.
- `data.rpm` (float): Average RPM for this foot.
- `data.torque` (float): Average torque for this foot.
- `data.standpipe_pressure` (float): Average standpipe pressure.
- `data.gamma_ray` (float): Average gamma ray value.
- `data.tvd` (float): TVD at this depth.
- `data.state` (string): Predominant state during this foot.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "measured_depth": "float",
  "log_identifier": "string",
  "data.rop": "float",
  "data.wob": "float",
  "data.rpm": "float",
  "data.torque": "float",
  "data.standpipe_pressure": "float",
  "data.gamma_ray": "float",
  "data.tvd": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains 1-foot depth summaries.

## Keywords

`depth summary`, `1 foot summary`, `depth indexed`, `well correlation`, `formation analysis`, `depth log`
