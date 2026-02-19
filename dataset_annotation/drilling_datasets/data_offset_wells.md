# Offset Wells (Comparison Well Configuration)

Offset well configurations for comparison analysis. This collection defines which wells should be used as offsets or comparators for the current well, enabling performance benchmarking and geological correlation.

## When to use this dataset

- You need to identify offset wells for comparison.
- You want to retrieve offset well IDs for data queries.
- You need offset configurations for composite curves.
- You want to correlate current well with nearby wells.
- You need offset data for planning purposes.

## Example queries

### Alerting
- Alert when offset wells are modified.
- Notify when new offset is added.

### Visualization
- Display offset wells on map.
- Show comparison charts with offsets.
- Plot composite curves including offsets.

### Q&A
- What are the offset wells for this well?
- How many offset wells are configured?
- What is the distance to offset wells?
- Which offsets had similar drilling conditions?

## Frequency

`per_well` (one record per well defining its offset configuration)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when offset configuration was created.
- `asset_id`: Unique ID of the asset (well) for which offsets are defined.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.offset_well_ids` (array): Array of offset well asset IDs (inferred).
- `data.offset_wells` (array): Array of offset well objects with details (inferred).
- `data.primary_offset` (int): Primary offset well ID (inferred).
- `data.selection_criteria` (string): How offsets were selected (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.offset_well_ids": "array",
  "data.offset_wells": "array",
  "data.primary_offset": "int"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains offset well configurations.

## Keywords

`offset wells`, `comparison wells`, `offset analysis`, `benchmark wells`, `well comparison`, `offset selection`
