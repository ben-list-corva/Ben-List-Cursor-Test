# Operation Summaries (Daily Operation Reports)

Daily operation summary reports. This collection contains summarized information about daily drilling operations, typically including footage drilled, activities performed, and operational highlights.

## When to use this dataset

- You need daily drilling summary reports.
- You want to track daily progress.
- You need high-level operational summaries.
- You want to generate daily reports.

## Example queries

### Alerting
- Alert when daily summary is available.
- Notify on significant daily progress.

### Visualization
- Display daily summary dashboard.
- Chart daily footage trends.
- Show operations timeline.

### Q&A
- What was accomplished today?
- How much footage was drilled today?
- What were the main activities today?
- What is the summary of the last 24 hours?

## Frequency

`per_day` (one record per daily report)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the summary report.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the report.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.date` (string): Report date (inferred).
- `data.daily_footage` (float): Footage drilled in reporting period (inferred).
- `data.current_depth` (float): Current hole depth (inferred).
- `data.current_activity` (string): Current activity (inferred).
- `data.24hr_summary` (string): Summary of last 24 hours (inferred).
- `data.next_24hr_plan` (string): Plan for next 24 hours (inferred).
- `data.operations` (array): List of operations performed (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.date": "string",
  "data.daily_footage": "float",
  "data.current_depth": "float",
  "data.current_activity": "string",
  "data.24hr_summary": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains daily operation summaries.

## Keywords

`operation summaries`, `daily report`, `drilling summary`, `daily operations`, `morning report`, `progress report`
