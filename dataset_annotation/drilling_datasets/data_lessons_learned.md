# Lessons Learned (Operational Knowledge Documentation)

Lessons learned documentation from drilling operations. This collection captures knowledge and insights gained during drilling, including best practices, problem resolutions, and recommendations for future wells.

## When to use this dataset

- You need to retrieve lessons learned for a well.
- You want to find relevant experiences from similar situations.
- You need to document operational insights.
- You want to build a knowledge base from drilling experiences.

## Example queries

### Alerting
- Alert when new lessons are documented.
- Notify on lessons related to current operations.

### Visualization
- List lessons learned by category.
- Show lessons timeline for a well.
- Display lessons by formation or depth.

### Q&A
- What lessons were learned on this well?
- Are there lessons from similar situations?
- What recommendations were made?
- What problems were encountered and how were they solved?

## Frequency

`per_entry` (one record per lesson learned entry)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the lesson was documented.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.title` (string): Title of the lesson learned (inferred).
- `data.description` (string): Detailed description (inferred).
- `data.category` (string): Category of the lesson (inferred).
- `data.depth` (float): Depth at which lesson applies (inferred).
- `data.formation` (string): Formation related to lesson (inferred).
- `data.recommendation` (string): Recommended action (inferred).
- `data.severity` (string): Impact severity (inferred).
- `data.author` (string): Person who documented the lesson (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.title": "string",
  "data.description": "string",
  "data.category": "string",
  "data.depth": "float",
  "data.recommendation": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains lessons learned entries.

## Keywords

`lessons learned`, `best practices`, `knowledge management`, `operational insights`, `recommendations`, `drilling lessons`
