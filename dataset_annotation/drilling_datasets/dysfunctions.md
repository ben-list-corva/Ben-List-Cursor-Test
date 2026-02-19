# Dysfunctions (Drilling Dysfunction Detection)

Drilling dysfunction detection events. This collection records detected drilling dysfunctions such as stick-slip, whirl, bit bounce, and other vibration-related issues that can damage equipment and reduce drilling efficiency.

## When to use this dataset

- You need to track drilling dysfunction events.
- You want to analyze vibration-related issues.
- You need dysfunction data for BHA optimization.
- You want to identify problematic drilling conditions.

## Example queries

### Alerting
- Alert when dysfunction is detected.
- Notify on stick-slip events.
- Alert on high-severity dysfunctions.

### Visualization
- Display dysfunction event timeline.
- Chart dysfunction frequency by type.
- Show dysfunction correlation with parameters.

### Q&A
- What dysfunctions have been detected?
- What parameters were associated with the dysfunction?
- What is the dysfunction history for this BHA?
- How can we adjust parameters to avoid dysfunctions?

## Frequency

`per_event` (one record per detected dysfunction)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the dysfunction detection.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the detection.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.dysfunction_type` (string): Type of dysfunction (stick-slip, whirl, bit bounce) (inferred).
- `data.severity` (string): Dysfunction severity (inferred).
- `data.duration` (int): Dysfunction duration (inferred).
- `data.depth` (float): Depth at dysfunction (inferred).
- `data.parameters` (object): Drilling parameters at dysfunction (inferred).
- `data.recommendations` (string): Recommended actions (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.dysfunction_type": "string",
  "data.severity": "string",
  "data.duration": "int",
  "data.depth": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains drilling dysfunction detection events.

## Keywords

`dysfunctions`, `stick slip`, `whirl`, `bit bounce`, `drilling vibration`, `drilling dysfunction`, `vibration detection`
