# Metrics (Calculated Drilling KPIs)

Calculated drilling metrics and Key Performance Indicators (KPIs) for wells. This collection stores computed metrics at various aggregation levels (well, well section, BHA, etc.) including performance indicators like ROP averages, connection counts, and efficiency metrics. Metrics are typically calculated by background apps and used for dashboards, leaderboards, and performance comparisons.

## When to use this dataset

- You need pre-calculated KPIs for a well or well section.
- You want to compare performance metrics across multiple wells.
- You need aggregated statistics like average ROP, connection counts, or drilling efficiency.
- You want to populate dashboards or leaderboards with computed metrics.
- You need to filter metrics by segment (drilling, completion), well section, or other dimensions.

## Example queries

### Alerting
- Alert when a specific metric falls below a threshold value.
- Notify when connection count exceeds a target for a well section.

### Visualization
- Display KPI dashboard with key drilling metrics.
- Plot metric trends over well sections.
- Show leaderboard comparing metrics across rigs or wells.
- Chart metric comparisons by basin or mud type.

### Q&A
- What is the average ROP for this well section?
- How many connections were made in the Surface section?
- What is the drilling efficiency for this well compared to offset wells?
- Which rig has the best ROP performance this month?
- What metrics are available for the Production Lateral section?

## Frequency

`per_metric` (one record per metric key/type combination)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the metric was calculated (may be null for lifetime metrics).
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.key`: The metric identifier (e.g., "rop_avg", "drilling_connection_count").
- `data.type`: The aggregation level (e.g., "well", "well_section", "bha").

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the metric calculation (may be null).
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.value` (float): The calculated metric value.
- `data.key` (string): Metric identifier/name (e.g., "drilling_connection_count", "rop_avg").
- `data.type` (string): Aggregation level ("well", "well_section", "bha", etc.).
- `data.segment` (string): Operational segment ("drilling" or "completion").
- `data.company_id` (int): Company ID associated with the metric.
- `data.basin` (string): Basin name (may be null).
- `data.mud_type` (string): Mud type used (e.g., "Water-base", "Oil-base").
- `data.program_id` (int): Drilling program identifier.
- `data.rig_id` (int): Rig identifier.
- `data.asset_id` (int): Asset identifier (repeated in data for filtering).
- `data.well_section` (string): Well section name (e.g., "Surface", "Intermediate", "Production Lateral").

### `metadata` fields

- `metadata.timezone` (string): Timezone for the metric calculation (e.g., "America/Chicago").

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.value": "float",
  "data.key": "string",
  "data.type": "string",
  "data.segment": "string",
  "data.company_id": "int",
  "data.basin": "string",
  "data.mud_type": "string",
  "data.program_id": "int",
  "data.rig_id": "int",
  "data.asset_id": "int",
  "data.well_section": "string",
  "metadata": "object",
  "metadata.timezone": "string"
}
```

## Sample record

```json
{
  "_id": "example_metrics",
  "collection": "metrics",
  "timestamp": null,
  "company_id": 81,
  "data": {
    "value": 0,
    "key": "drilling_connection_count",
    "type": "well_section",
    "segment": "drilling",
    "company_id": 80,
    "basin": null,
    "mud_type": "Water-base",
    "program_id": 64736326,
    "rig_id": 46323758,
    "asset_id": 61191485,
    "well_section": "Surface"
  },
  "metadata": {
    "timezone": "America/Chicago"
  },
  "asset_id": 12345
}
```

## Keywords

`metrics`, `kpi`, `drilling metrics`, `performance indicators`, `drilling kpi`, `well metrics`, `leaderboard`, `dashboard metrics`
