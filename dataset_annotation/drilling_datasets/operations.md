# Operations (High-Level Drilling Operations)

High-level drilling operations data categorizing rig activities into major operation types such as drilling, tripping, circulating, and other operational phases. This dataset provides aggregated operation periods with detailed performance metrics, depth tracking, and ROP (Rate of Penetration) analysis.

## When to use this dataset

- You need to analyze drilling operations at a high level (drilling vs tripping vs circulating).
- You want to calculate performance metrics for specific operation types.
- You need to track depth progress per operation.
- You want to analyze rotary vs slide drilling performance.
- You need to identify well sections and BHA configurations during operations.
- You want to compare operational efficiency across different time periods.

## Example queries

### Alerting
- Alert when tripping operations exceed expected duration.
- Notify when ROP drops below threshold during drilling operations.
- Alert when slide percentage exceeds a target value.

### Visualization
- Plot depth vs time colored by operation type.
- Chart ROP trends across drilling operations.
- Show rotary vs slide footage breakdown.
- Visualize operation duration by type over the well.

### Q&A
- What was the average ROP during the last drilling operation?
- How much time was spent tripping today?
- What percentage of drilling was rotary vs slide?
- What was the total footage drilled in the Production Lateral section?
- Which BHA configuration had the best ROP performance?

## Frequency

`per_operation` (one record per operation period)

## Primary keys and meaning

- `timestamp`: Unix/epoch timestamp marking the end of the operation.
- `asset_id`: Unique ID of the asset (well) for filtering a specific well.
- `data.operation`: Operation type code.
- `data.start_timestamp`: Start time of the operation (unique per asset and operation type).

## Available fields

### Top-level fields

- `timestamp` (long): Unix/epoch timestamp of the data point.
- `asset_id` (int): Unique asset ID.
- `company_id` (int): Company identifier.

### `data` fields

- `data.start_timestamp` (long): Unix/epoch timestamp when the operation started.
- `data.end_timestamp` (long): Unix/epoch timestamp when the operation ended.
- `data.shift` (string): Shift during which the operation occurred ("day" or "night").
- `data.operation` (string): Operation type code identifier.
- `data.operation_name` (string): Human-readable operation name (e.g., "Drilling(Drilling)").
- `data.operation_time` (int): Duration of the operation in seconds.
- `data.start_depth` (float): Hole depth at the start of the operation.
- `data.end_depth` (float): Hole depth at the end of the operation.
- `data.depth_change` (float): Total depth change during the operation.
- `data.start_bit_depth` (float): Bit depth at the start of the operation.
- `data.end_bit_depth` (float): Bit depth at the end of the operation.
- `data.bit_depth_change` (float): Total bit depth change during the operation.
- `data.start_block_height` (float): Block height at the start of the operation.
- `data.end_block_height` (float): Block height at the end of the operation.
- `data.block_height_change` (float): Total block height change during the operation.
- `data.well_section` (string): Well section name (e.g., "Surface", "Production Lateral").
- `data.hole_size` (float): Hole size in inches.
- `data.bha_id` (int): Bottom hole assembly identifier.

### `data.performance` fields

- `data.performance.total_rop` (float): Overall rate of penetration for the operation.
- `data.performance.rotary_rop` (float): ROP during rotary drilling.
- `data.performance.rotary_percentage` (float): Percentage of operation time spent in rotary mode.
- `data.performance.rotary_depth_change` (float): Footage drilled in rotary mode.
- `data.performance.slide_rop` (float): ROP during slide drilling.
- `data.performance.slide_percentage` (float): Percentage of operation time spent in slide mode.
- `data.performance.slide_depth_change` (float): Footage drilled in slide mode.

### `data.rop_variability` fields

- `data.rop_variability.ad_rop_sd` (float): Standard deviation of ROP (activity detection).
- `data.rop_variability.ad_rop_mean` (float): Mean ROP (activity detection).
- `data.rop_variability.edr_rop_sd` (float): Standard deviation of ROP (EDR-based).
- `data.rop_variability.edt_rop_mean` (float): Mean ROP (EDR-based).
- `data.rop_variability.start_hole_depth` (float): Starting hole depth for variability calculation.
- `data.rop_variability.end_hole_depth` (float): Ending hole depth for variability calculation.
- `data.rop_variability.pd_status` (boolean): Predictive drilling status flag.

## Collection schema

```json
{
  "timestamp": "long",
  "asset_id": "int",
  "company_id": "int",
  "data.start_timestamp": "long",
  "data.end_timestamp": "long",
  "data.shift": "string",
  "data.operation": "string",
  "data.operation_name": "string",
  "data.operation_time": "int",
  "data.start_depth": "float",
  "data.end_depth": "float",
  "data.depth_change": "float",
  "data.start_bit_depth": "float",
  "data.end_bit_depth": "float",
  "data.bit_depth_change": "float",
  "data.start_block_height": "float",
  "data.end_block_height": "float",
  "data.block_height_change": "float",
  "data.well_section": "string",
  "data.hole_size": "float",
  "data.bha_id": "int",
  "data.performance": "object",
  "data.performance.total_rop": "float",
  "data.performance.rotary_rop": "float",
  "data.performance.rotary_percentage": "float",
  "data.performance.rotary_depth_change": "float",
  "data.performance.slide_rop": "float",
  "data.performance.slide_percentage": "float",
  "data.performance.slide_depth_change": "float",
  "data.rop_variability": "object"
}
```

## Sample record

```json
{
  "_id": "example_operations",
  "version": 1,
  "provider": "corva",
  "collection": "operations",
  "timestamp": 1768399040,
  "company_id": 81,
  "asset_id": 12345,
  "data": {
    "start_timestamp": 1768397400,
    "end_timestamp": 1768399040,
    "shift": "day",
    "operation": "7",
    "operation_name": "Drilling(Drilling)",
    "operation_time": 1640,
    "start_depth": 14230.53,
    "end_depth": 14321.74,
    "depth_change": 91.21,
    "start_bit_depth": 14230.53,
    "end_bit_depth": 14321.71,
    "bit_depth_change": 91.18,
    "start_block_height": 93.21,
    "end_block_height": 2.06,
    "block_height_change": -91.15,
    "performance": {
      "total_rop": 200.22,
      "rotary_rop": 200.22,
      "rotary_percentage": 100,
      "rotary_depth_change": 91.21,
      "slide_rop": 0,
      "slide_percentage": 0,
      "slide_depth_change": 0
    },
    "well_section": "Production Lateral",
    "hole_size": 6.75,
    "bha_id": 1,
    "rop_variability": {
      "ad_rop_sd": 92.24287653380912,
      "ad_rop_mean": 174.9750531926707,
      "edr_rop_sd": 84.96031976987472,
      "edt_rop_mean": 183.601670294281,
      "start_hole_depth": 14230.5302,
      "end_hole_depth": 14321.7373,
      "pd_status": false
    }
  }
}
```

## Keywords

`operations`, `drilling operations`, `tripping`, `circulating`, `rop performance`, `rotary drilling`, `slide drilling`, `well section`
