# Completion Pumps (Pump Equipment Data)

Completion pump equipment data. This collection contains information about the frac pumps used during completion operations including pump specifications, configuration, and operating parameters.

## When to use this dataset

- You need pump configuration information.
- You want to track pump fleet composition.
- You need pump specifications for calculations.
- You want to analyze pump utilization.

## Example queries

### Alerting
- Alert on pump configuration changes.
- Notify when pump count changes.

### Visualization
- Display pump fleet summary.
- Show pump specifications.
- Chart pump utilization.

### Q&A
- How many pumps are on location?
- What are the pump specifications?
- What is the total available hydraulic horsepower?
- What pump configuration is being used?

## Frequency

`per_configuration` (updated when pump configuration changes)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the pump record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.pump_count` (int): Number of pumps (inferred).
- `data.total_hhp` (float): Total hydraulic horsepower (inferred).
- `data.pump_type` (string): Type of pump (inferred).
- `data.pumps` (array): Array of individual pump details (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.pump_count": "int",
  "data.total_hhp": "float",
  "data.pump_type": "string",
  "data.pumps": "array"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains pump equipment configuration data.

## Keywords

`completion pumps`, `frac pumps`, `pump fleet`, `hydraulic horsepower`, `pump configuration`
