# Drillstring (BHA and Drill String Components)

Bottom hole assembly (BHA) and drillstring component data. This collection contains detailed information about the drill string configuration including all components from surface to bit - drill pipe, heavy weight, drill collars, stabilizers, motors, MWD/LWD tools, and bits. Essential for torque and drag calculations, hydraulics modeling, and operational planning.

## When to use this dataset

- You need the current BHA configuration for the well.
- You want to calculate torque and drag for the drillstring.
- You need component specifications for hydraulics calculations.
- You want to track BHA changes throughout the well.
- You need drillstring data for stuck pipe analysis.
- You want to analyze BHA performance across runs.

## Example queries

### Alerting
- Alert when BHA configuration changes.
- Notify when motor hours exceed service limits.
- Alert when approaching bit hours threshold.

### Visualization
- Display wellbore schematic with drillstring components.
- Show BHA component summary.
- Chart bit performance across different runs.
- Display motor specifications and operating limits.

### Q&A
- What is the current BHA configuration?
- What type of motor is in the hole?
- What are the bit specifications?
- How many hours are on the current motor?
- What is the total drillstring weight?

## Frequency

`per_bha` (one record per BHA configuration or drillstring change)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp when the drillstring was created or updated.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the record.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.name` (string): BHA or drillstring name/identifier.
- `data.bha_number` (int): BHA run number.
- `data.components` (array): Array of drillstring components.
- Component fields:
  - `family` (string): Component type (e.g., "Drill Pipe", "Motor", "Bit").
  - `type` (string): Specific component type.
  - `od` (float): Outer diameter in inches.
  - `id` (float): Inner diameter in inches.
  - `length` (float): Component length in feet.
  - `weight` (float): Component weight per foot.
  - `top_depth` (float): Top depth position in string.
  - `bottom_depth` (float): Bottom depth position in string.
  - `grade` (string): Material grade.
  - `connection` (string): Connection type.
- `data.bit` (object): Bit specifications.
  - `data.bit.size` (float): Bit diameter in inches.
  - `data.bit.type` (string): Bit type (PDC, roller cone, etc.).
  - `data.bit.manufacturer` (string): Bit manufacturer.
  - `data.bit.model` (string): Bit model number.
- `data.motor` (object): Motor specifications.
  - `data.motor.bend` (float): Motor bend angle.
  - `data.motor.od` (float): Motor outer diameter.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.name": "string",
  "data.bha_number": "int",
  "data.components": "array",
  "data.bit": "object",
  "data.motor": "object"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains drillstring configurations with component arrays.

## Keywords

`drillstring`, `bha`, `bottom hole assembly`, `drill pipe`, `motor`, `bit`, `drill collar`, `stabilizer`
