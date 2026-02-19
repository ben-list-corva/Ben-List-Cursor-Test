# Files (Well Document Attachments)

File attachments and documents associated with wells. This collection contains metadata about files uploaded and attached to well records, including reports, surveys, images, and other documentation.

## When to use this dataset

- You need to find documents associated with a well.
- You want to retrieve file metadata and download links.
- You need to list available attachments for a well.
- You want to track document uploads over time.

## Example queries

### Alerting
- Alert when new documents are uploaded.
- Notify on specific file type uploads.

### Visualization
- List files associated with a well.
- Show document timeline.
- Display file category breakdown.

### Q&A
- What documents are attached to this well?
- When was the latest report uploaded?
- What file types are available?
- Who uploaded specific documents?

## Frequency

`per_file` (one record per uploaded file)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the file was uploaded.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.file_name`: Name of the uploaded file.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the upload.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.file_name` (string): Internal file name or identifier.
- `data.display_name` (string): Display name for the file.
- `data.user` (string): User who uploaded the file.
- `data.file_type` (string): File type or extension (inferred).
- `data.file_size` (int): File size in bytes (inferred).
- `data.category` (string): File category (inferred).
- `data.url` (string): Download URL or file path (inferred).
- `data.description` (string): File description (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.file_name": "string",
  "data.display_name": "string",
  "data.user": "string",
  "data.file_type": "string",
  "data.file_size": "int",
  "data.category": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains file metadata for well attachments.

## Keywords

`files`, `documents`, `attachments`, `uploads`, `reports`, `well documents`, `file management`
