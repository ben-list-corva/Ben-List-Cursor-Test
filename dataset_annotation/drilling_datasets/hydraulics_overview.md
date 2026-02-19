# Hydraulics Overview (Hydraulics Summary Data)

Hydraulics overview and summary data. This collection provides aggregated hydraulics information including PDM flowrate limits, recommended flowrates, and hole cleaning severity assessments. Used for dashboards and quick status checks of hydraulic conditions.

## When to use this dataset

- You need a quick overview of hydraulic status.
- You want to check hole cleaning severity.
- You need PDM flowrate limits.
- You want recommended minimum flowrates.
- You need summary hydraulics data for dashboards.

## Example queries

### Alerting
- Alert when hole cleaning severity increases.
- Notify when operating outside PDM flowrate limits.
- Alert on poor hole cleaning conditions.

### Visualization
- Display hydraulics status dashboard.
- Show hole cleaning trend.
- Chart flowrate recommendations.
- Display PDM operating window.

### Q&A
- What is the current hole cleaning severity?
- What are the PDM flowrate limits?
- What is the recommended minimum flowrate?
- Is hole cleaning adequate at current parameters?
- What is the trend in hole cleaning performance?

## Frequency

`per_interval` (updated at regular intervals)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the overview record.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.pdm_flowrate_limits` (object): PDM flowrate operating limits.
  - `data.pdm_flowrate_limits.min_standard_flowrate` (float): Minimum recommended flowrate for PDM.
  - `data.pdm_flowrate_limits.max_standard_flowrate` (float): Maximum recommended flowrate for PDM.
- `data.recommended_minimum_flowrate` (float): Recommended minimum flowrate for hole cleaning.
- `data.hole_cleaning` (object): Hole cleaning status.
  - `data.hole_cleaning.severity` (string): Severity level ("low", "medium", "high").
  - `data.hole_cleaning.value` (float): Hole cleaning metric value.
  - `data.hole_cleaning.points` (array): Historical hole cleaning data points with severity, value, and timestamp.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.pdm_flowrate_limits": "object",
  "data.pdm_flowrate_limits.min_standard_flowrate": "float",
  "data.pdm_flowrate_limits.max_standard_flowrate": "float",
  "data.recommended_minimum_flowrate": "float",
  "data.hole_cleaning": "object",
  "data.hole_cleaning.severity": "string",
  "data.hole_cleaning.value": "float",
  "data.hole_cleaning.points": "array"
}
```

## Sample record

```json
{
  "_id": "example_hydraulics_overview",
  "version": 1,
  "provider": "corva",
  "collection": "hydraulics.overview",
  "timestamp": 1768920599,
  "data": {
    "pdm_flowrate_limits": {
      "min_standard_flowrate": 350,
      "max_standard_flowrate": 700
    },
    "recommended_minimum_flowrate": 299.9,
    "hole_cleaning": {
      "severity": "low",
      "value": 0,
      "points": [
        {
          "severity": "low",
          "value": 0,
          "timestamp": 1768847084
        }
      ]
    }
  }
}
```

## Keywords

`hydraulics overview`, `hole cleaning`, `pdm flowrate`, `hydraulics summary`, `flowrate limits`, `hole cleaning severity`
