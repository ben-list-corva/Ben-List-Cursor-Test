# Torque and Drag Overview (T&D Summary Data)

Torque and drag calculation overview providing summary metrics for weight transfer efficiency and drag severity. This collection contains high-level T&D indicators and trend data used for dashboards and quick status assessments of drilling string mechanics.

## When to use this dataset

- You need a quick overview of torque and drag status.
- You want to assess weight transfer efficiency.
- You need drag severity indicators.
- You want to monitor T&D trends during drilling.
- You need WOB comparison between model and actual.

## Example queries

### Alerting
- Alert when drag severity increases to high.
- Notify when weight transfer becomes poor.
- Alert on significant changes in T&D performance.

### Visualization
- Display T&D status dashboard.
- Show drag severity trend over time.
- Chart weight on bit model vs actual.
- Display weight transfer efficiency indicator.

### Q&A
- What is the current drag severity?
- Is weight transfer adequate?
- How does actual WOB compare to model?
- What is the trend in drag performance?
- Is there evidence of increasing friction?

## Frequency

`per_interval` (updated at regular intervals during drilling)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the overview record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.weight_transfer` (string): Weight transfer quality ("low", "medium", "high").
- `data.activity` (string): Current drilling activity.
- `data.weight_on_bit` (object): WOB comparison data.
  - `data.weight_on_bit.difference` (float): Difference between model and actual.
  - `data.weight_on_bit.model` (float): Modeled WOB.
  - `data.weight_on_bit.latch` (float): Latest measured value.
- `data.drag` (object): Drag severity assessment.
  - `data.drag.severity` (string): Drag severity level ("low", "medium", "high").
  - `data.drag.value` (float): Drag metric value (0-100).
  - `data.drag.points` (array): Historical drag data points with severity, value, and timestamp.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.weight_transfer": "string",
  "data.activity": "string",
  "data.weight_on_bit": "object",
  "data.weight_on_bit.difference": "float",
  "data.weight_on_bit.model": "float",
  "data.weight_on_bit.latch": "float",
  "data.drag": "object",
  "data.drag.severity": "string",
  "data.drag.value": "float",
  "data.drag.points": "array"
}
```

## Sample record

```json
{
  "_id": "example_torque-and-drag_overview",
  "version": 1,
  "provider": "corva",
  "collection": "torque-and-drag.overview",
  "timestamp": 1768920599,
  "data": {
    "weight_transfer": "low",
    "activity": "Rotary Drilling",
    "weight_on_bit": {
      "difference": 44.62,
      "model": 62.94,
      "latch": 18.32
    },
    "drag": {
      "severity": "high",
      "value": 100,
      "points": [
        {
          "severity": "high",
          "value": 100,
          "timestamp": 1768838958
        }
      ]
    }
  }
}
```

## Keywords

`torque and drag`, `t&d overview`, `weight transfer`, `drag severity`, `drilling mechanics`, `wob transfer`
