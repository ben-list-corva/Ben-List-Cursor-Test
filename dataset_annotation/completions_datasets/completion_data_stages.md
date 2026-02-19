# Completion Data Stages (Stage Configuration)

Stage configuration and execution data. This collection contains the design and configuration parameters for each frac stage including target depths, cluster information, and design parameters.

## When to use this dataset

- You need stage design/configuration data.
- You want to compare design vs actual stage execution.
- You need stage depth and cluster information.
- You want to track stage configuration for the well.

## Example queries

### Alerting
- Alert when stage configuration changes.
- Notify when approaching target stage.

### Visualization
- Display stage design table.
- Show stage locations on wellbore.
- Chart stage configuration parameters.

### Q&A
- What are the design parameters for this stage?
- How many stages are planned for this well?
- What are the cluster details for each stage?
- What is the design proppant for this stage?

## Frequency

`per_stage` (one record per designed stage)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the stage record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `stage_number`: Stage number.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.
- `stage_number` (int): Stage number.

### `data` fields (inferred from domain knowledge)

- `data.stage_number` (int): Stage number.
- `data.top_perf_md` (float): Top perforation measured depth (inferred).
- `data.bottom_perf_md` (float): Bottom perforation measured depth (inferred).
- `data.cluster_count` (int): Number of clusters (inferred).
- `data.design_proppant` (float): Design proppant mass (inferred).
- `data.design_clean_volume` (float): Design clean fluid volume (inferred).
- `data.design_rate` (float): Design pump rate (inferred).
- `data.design_pressure` (float): Design treating pressure (inferred).
- `data.status` (string): Stage status (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "stage_number": "int",
  "data.top_perf_md": "float",
  "data.bottom_perf_md": "float",
  "data.cluster_count": "int",
  "data.design_proppant": "float",
  "data.design_clean_volume": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains stage design configuration data.

## Keywords

`completion stages`, `stage design`, `stage configuration`, `frac stages`, `perforation`, `cluster design`
