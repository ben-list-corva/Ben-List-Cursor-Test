# Directional Tortuosity (Wellbore Tortuosity Calculations)

Wellbore tortuosity calculations measuring the deviation of the actual wellbore path from a smooth trajectory. Tortuosity affects drilling efficiency, causes increased drag and torque, and impacts completion operations. This dataset provides tortuosity metrics calculated from survey data to assess wellbore quality.

## When to use this dataset

- You need to assess wellbore quality and smoothness.
- You want to analyze tortuosity impact on drilling performance.
- You need tortuosity data for torque and drag analysis.
- You want to compare wellbore quality across wells or sections.
- You need to identify high-tortuosity zones for intervention.

## Example queries

### Alerting
- Alert when tortuosity exceeds acceptable limits.
- Notify when dogleg severity causes excessive tortuosity.
- Alert on tortuosity trends indicating wellbore quality issues.

### Visualization
- Plot tortuosity index vs measured depth.
- Chart dogleg severity contributions to tortuosity.
- Display wellbore quality heatmap based on tortuosity.
- Show tortuosity comparison across well sections.

### Q&A
- What is the overall tortuosity index for this well?
- Which sections have the highest tortuosity?
- How does this well's tortuosity compare to offset wells?
- What is the maximum dogleg severity contributing to tortuosity?
- Is tortuosity affecting our torque and drag performance?

## Frequency

`per_survey` (calculated each time surveys are updated)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when tortuosity was calculated.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the calculation.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.measured_depth` (float): Measured depth for this calculation.
- `data.tortuosity_index` (float): Overall tortuosity index value.
- `data.cumulative_tortuosity` (float): Cumulative tortuosity from surface.
- `data.dogleg_severity` (float): Dogleg severity at this depth.
- `data.dogleg_severity_max` (float): Maximum dogleg severity encountered.
- `data.dogleg_severity_avg` (float): Average dogleg severity.
- `data.smoothness_index` (float): Wellbore smoothness metric (inferred).
- `data.micro_tortuosity` (float): Short-wavelength tortuosity component (inferred).
- `data.macro_tortuosity` (float): Long-wavelength tortuosity component (inferred).
- `data.well_section` (string): Well section for the calculation.
- `data.surveys` (array): Array of survey-by-survey tortuosity values.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.measured_depth": "float",
  "data.tortuosity_index": "float",
  "data.cumulative_tortuosity": "float",
  "data.dogleg_severity": "float",
  "data.dogleg_severity_max": "float",
  "data.dogleg_severity_avg": "float",
  "data.smoothness_index": "float",
  "data.micro_tortuosity": "float",
  "data.macro_tortuosity": "float",
  "data.well_section": "string",
  "data.surveys": "array"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains wellbore tortuosity calculations and quality metrics.

## Keywords

`tortuosity`, `wellbore tortuosity`, `dogleg severity`, `wellbore quality`, `trajectory smoothness`, `micro tortuosity`, `drilling quality`
