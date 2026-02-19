# Drilling Efficiency Optimization (Parameter Optimization Data)

Drilling efficiency optimization data containing analyzed drilling parameters and optimization recommendations. This dataset provides insights into optimal drilling parameter combinations for maximizing ROP and minimizing MSE.

## When to use this dataset

- You need drilling parameter optimization recommendations.
- You want to identify optimal WOB/RPM combinations.
- You need data to guide real-time parameter adjustments.
- You want to analyze historical optimization performance.

## Example queries

### Alerting
- Alert when current parameters deviate from optimal.
- Notify when optimization opportunity is identified.

### Visualization
- Display recommended vs actual parameters.
- Show optimization trends over depth.
- Chart efficiency improvement from optimization.

### Q&A
- What are the optimal drilling parameters?
- How much ROP improvement is possible?
- What parameter changes are recommended?
- How efficient is current drilling compared to potential?

## Frequency

`per_analysis` (calculated during drilling optimization analysis)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp of the optimization analysis.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the analysis.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields (inferred from domain knowledge)

- `data.recommended_wob` (float): Recommended weight on bit (inferred).
- `data.recommended_rpm` (float): Recommended RPM (inferred).
- `data.current_wob` (float): Current weight on bit (inferred).
- `data.current_rpm` (float): Current RPM (inferred).
- `data.expected_rop` (float): Expected ROP with recommendations (inferred).
- `data.current_rop` (float): Current ROP (inferred).
- `data.efficiency_gain` (float): Expected efficiency improvement (inferred).
- `data.hole_depth` (float): Depth of analysis.
- `data.formation` (string): Formation at analysis depth (inferred).

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.recommended_wob": "float",
  "data.recommended_rpm": "float",
  "data.current_wob": "float",
  "data.current_rpm": "float",
  "data.expected_rop": "float",
  "data.current_rop": "float",
  "data.efficiency_gain": "float",
  "data.hole_depth": "float"
}
```

## Sample record

Note: Sample record not available in source documentation. This dataset contains drilling optimization analysis results.

## Keywords

`drilling optimization`, `parameter optimization`, `rop optimization`, `drilling efficiency`, `optimal parameters`, `drilling performance`
