# Directional Slide Sheet (Slide/Rotate Tracking)

Slide sheet data tracking sliding and rotating drilling activities. This collection records details about each slide and rotate section during directional drilling, including toolface orientation, footage drilled, motor yields, and build/turn rates. It provides essential data for directional drilling performance analysis and motor yield calculations.

## When to use this dataset

- You need to track slide vs rotate drilling sections.
- You want to analyze motor yield and directional performance.
- You need toolface data for each drilling section.
- You want to calculate actual build and turn rates.
- You need to compare planned vs actual directional performance.
- You want to optimize slide sheet planning.

## Example queries

### Alerting
- Alert when motor yield differs significantly from expected.
- Notify when slide percentage exceeds target.
- Alert when toolface is inconsistent during slide.

### Visualization
- Display slide sheet timeline showing slide/rotate sections.
- Chart motor yield trends over the well.
- Plot toolface vs depth for each slide.
- Show build rate vs slide footage correlation.

### Q&A
- What was the average motor yield for the last 500 feet?
- How much footage was drilled in slide vs rotate mode?
- What toolface was used during the last slide?
- What is the current build rate trend?
- How does actual motor yield compare to predicted?

## Frequency

`per_section` (one record per slide or rotate drilling section)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the slide sheet entry.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.start_depth` (float): Starting measured depth of the section.
- `data.end_depth` (float): Ending measured depth of the section.
- `data.footage` (float): Footage drilled in this section.
- `data.mode` (string): Drilling mode ("slide" or "rotate").
- `data.toolface` (float): Average toolface orientation during slide.
- `data.toolface_type` (string): Type of toolface ("gravity" or "magnetic").
- `data.motor_yield` (float): Calculated motor yield (degrees per 100 feet).
- `data.build_rate` (float): Inclination build rate.
- `data.turn_rate` (float): Azimuth turn rate.
- `data.start_inclination` (float): Inclination at start of section.
- `data.end_inclination` (float): Inclination at end of section.
- `data.start_azimuth` (float): Azimuth at start of section.
- `data.end_azimuth` (float): Azimuth at end of section.
- `data.slide_percentage` (float): Percentage of section drilled in slide mode.
- `data.rop` (float): Rate of penetration during this section.
- `data.duration` (int): Duration in seconds.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.start_depth": "float",
  "data.end_depth": "float",
  "data.footage": "float",
  "data.mode": "string",
  "data.toolface": "float",
  "data.toolface_type": "string",
  "data.motor_yield": "float",
  "data.build_rate": "float",
  "data.turn_rate": "float",
  "data.start_inclination": "float",
  "data.end_inclination": "float",
  "data.start_azimuth": "float",
  "data.end_azimuth": "float",
  "data.slide_percentage": "float",
  "data.rop": "float",
  "data.duration": "int"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains slide sheet entries tracking slide and rotate drilling sections.

## Keywords

`slide sheet`, `directional drilling`, `slide rotate`, `motor yield`, `toolface`, `build rate`, `turn rate`, `directional performance`
