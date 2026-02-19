# Completion Data Files (Completion Documents)

File attachments and documents associated with completion operations. This collection contains metadata about files uploaded for completion wells including reports, treatment summaries, and analysis documents.

## When to use this dataset

- You need documents for completion operations.
- You want to find completion-related files.
- You need to list attachments for a completion well.
- You want to track document uploads.

## Example queries

### Alerting
- Alert when new documents are uploaded.

### Visualization
- List files for completion operations.
- Show document timeline.

### Q&A
- What documents are available for this completion?
- What reports have been uploaded?
- When was the last document added?

## Frequency

`per_file` (one record per uploaded file)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the file was uploaded.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the upload.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.file_name` (string): File name or identifier (inferred).
- `data.display_name` (string): Display name for the file (inferred).
- `data.file_type` (string): File type (inferred).
- `data.category` (string): File category (inferred).
- `data.user` (string): Uploading user (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.file_name": "string",
  "data.display_name": "string",
  "data.file_type": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains completion document metadata.

## Keywords

`completion files`, `completion documents`, `frac reports`, `treatment reports`, `completion attachments`
