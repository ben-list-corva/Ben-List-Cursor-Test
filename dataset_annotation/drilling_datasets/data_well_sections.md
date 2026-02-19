# Well Sections (Drilling Section Definitions)

Well section definitions for drilling operations. This collection defines the major sections of the well (e.g., Surface, Intermediate, Production Lateral) with their depth intervals, hole sizes, and associated parameters. Essential for segmenting performance analysis and organizing drilling data by phase.

## When to use this dataset

- You need to identify the current well section being drilled.
- You want to analyze performance by well section.
- You need section boundaries for metrics calculation.
- You want to filter data by well section.
- You need hole size information at specific depths.
- You want to organize drilling reports by section.

## Example queries

### Alerting
- Alert when transitioning between well sections.
- Notify when approaching section TD.

### Visualization
- Display well sections on depth-based charts.
- Show performance comparison across sections.
- Chart footage drilled per section.
- Overlay sections on days vs depth.

### Q&A
- What well section are we currently drilling?
- What is the planned TD for this section?
- What is the hole size for each section?
- How does ROP compare across sections?
- How long did each section take to drill?

## Frequency

`per_section` (one record per well section definition)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the section was created or updated.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.name`: Name of the well section.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.name` (string): Section name (e.g., "Surface", "Intermediate", "Production Lateral").
- `data.top_depth` (float): Top measured depth of the section.
- `data.bottom_depth` (float): Bottom measured depth (section TD) of the section.
- `data.hole_size` (float): Hole size in inches for this section.
- `data.casing_size` (float): Associated casing size (inferred).
- `data.mud_weight_range` (object): Expected mud weight range (inferred).
- `data.sequence` (int): Section sequence number (inferred).
- `data.status` (string): Section status (planned, in-progress, complete) (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.name": "string",
  "data.top_depth": "float",
  "data.bottom_depth": "float",
  "data.hole_size": "float",
  "data.casing_size": "float",
  "data.sequence": "int",
  "data.status": "string"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains well section definitions with depth intervals.

## Keywords

`well sections`, `drilling sections`, `hole sections`, `section td`, `surface section`, `intermediate`, `production lateral`
