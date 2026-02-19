# Corva Platform – Datasets & Data Streams Reference

> **Source**: Compiled from Corva Dev Center documentation (dc-docs.corva.ai), API docs, and example code.
> **Note**: The complete, live list of datasets is available in the [Corva Dev Center Dataset Explorer](https://app.corva.ai/dev-center/datasets) (requires authentication). This document captures what is publicly documented.

---

## 1. How Data is Organized

| Concept | Description |
|---------|-------------|
| **Provider** | The entity that produces the data. Corva's built-in data uses provider `corva`. Custom apps use your company identifier (e.g. `big-data-energy`). |
| **Dataset / Collection** | A MongoDB collection storing records. Identified as `{provider}#{dataset}` (e.g. `corva#wits`). |
| **Data API Path** | `/api/v1/data/{provider}/{dataset}/` (e.g. `/api/v1/data/corva/wits/`) |

### Collection Types

| Type | Description | Example |
|------|-------------|---------|
| **Time-based** | Records created at a time interval (e.g. every 1 second) | `corva#wits` |
| **Depth-based** | Records created at a depth interval (e.g. every 1 ft) | `corva#drilling.wits.depth` |
| **Reference** | Non-time/depth records (metadata, config, notes) | `corva#data.well-sections`, `corva#data.drillstring` |

---

## 2. Core Real-Time Stream Datasets

These are the primary real-time streams that **Stream Apps** subscribe to.

### 2.1 `corva#wits` — Drilling Time-Based (1-second interval)

| Field | Type | Description |
|-------|------|-------------|
| `_id` | string | Unique document ID |
| `version` | int | Schema version |
| `provider` | string | `"corva"` |
| `collection` | string | `"wits"` |
| `timestamp` | int | Unix epoch (seconds) |
| `asset_id` | int | Well / asset identifier |
| `company_id` | int | Operator / company identifier |
| `app` | string | Source app key |
| **`metadata`** | object | References to related records (see below) |
| **`data`** | object | Telemetry payload (see below) |
| `data_raw` | object | Raw/unprocessed data |

#### `metadata` sub-fields

| Key | Type | Description |
|-----|------|-------------|
| `drillstring` | string (ID) | Reference to active drillstring document |
| `casing` | string (ID) | Reference to casing document |
| `mud` | string (ID) | Reference to active mud document |
| `cuttings` | string (ID) | Reference to cuttings document |
| `surface-equipment` | string (ID) | Reference to surface equipment document |
| `actual_survey` | string (ID) | Reference to actual survey document |
| `plan_survey` | string (ID) | Reference to plan survey document |

#### `data` sub-fields (commonly available channels)

| Channel Key | Unit (typical) | Description |
|-------------|----------------|-------------|
| `entry_at` | epoch (s) | Record entry timestamp |
| `bit_depth` | ft | Current bit depth |
| `hole_depth` | ft | Current hole depth |
| `block_height` | ft | Traveling block height |
| `hook_load` | klbs | Hook load |
| `weight_on_bit` | klbs | Weight on bit |
| `rop` | ft/hr | Rate of penetration |
| `rate_of_penetration` | ft/hr | Rate of penetration (alt key) |
| `time_of_penetration` | min/ft | Time of penetration |
| `rotary_rpm` | rpm | Surface rotary RPM |
| `rotary_torque` | ft-lbs | Rotary torque |
| `standpipe_pressure` | psi | Standpipe pressure |
| `diff_press` | psi | Differential pressure |
| `pump_spm_1` | spm | Pump 1 strokes per minute |
| `pump_spm_2` | spm | Pump 2 strokes per minute |
| `pump_spm_total` | spm | Total pump SPM |
| `strks_total` | strokes | Total strokes |
| `strks_pump_1` | strokes | Pump 1 total strokes |
| `strks_pump_2` | strokes | Pump 2 total strokes |
| `strks_pump_3` | strokes | Pump 3 total strokes |
| `mud_flow_in` | gpm | Mud flow rate in |
| `total mud volume` | bbl | Total mud volume |
| `trip tank mud volume` | bbl | Trip tank mud volume |
| `gamma_ray` | API | Gamma ray measurement |
| `inclination` | deg | MWD inclination |
| `azimuth` | deg | MWD azimuth |
| `true_vertical_depth` | ft | True vertical depth |
| `tool face` | deg | Tool face angle |
| `gravity_tool_face` | deg | Gravity tool face |
| `magnetic_tool_face` | deg | Magnetic tool face |
| `motor rpm` | rpm | Downhole motor RPM |
| `bit rpm` | rpm | Bit RPM |
| `mwd temperature` | °F | MWD temperature |
| `h2s` | ppm | H2S gas reading |
| `total gas return` | units | Total gas return |
| `on bottom hours` | hrs | Cumulative on-bottom hours |
| `circulating hours` | hrs | Cumulative circulating hours |
| `state` | string | Rig state (e.g. "In Slips", "Rotary Drilling") |
| `memos` | string | Operator memos / notes |
| `ad_rop_setpoint` | ft/hr | Autodriller ROP setpoint |
| `ad_wob_setpoint` | klbs | Autodriller WOB setpoint |
| `ad_diff_press_setpoint` | psi | Autodriller diff press setpoint |
| `autodriller status` | int | Autodriller on/off status |
| `over pull` | klbs | Overpull |
| `relative mse` | - | Relative mechanical specific energy |
| `surface stick slip index` | - | Surface stick-slip index |
| `line wear` | - | Line/cable wear counter |
| `trip speed` | ft/hr | Tripping speed |

> **Note**: Available channels vary well-to-well depending on the data provider (WITSML source). Not every channel will be populated for every asset.

---

### 2.2 `corva#drilling.wits.depth` — Drilling Depth-Based (per-foot interval)

| Field | Type | Description |
|-------|------|-------------|
| `_id` | string | Unique document ID |
| `version` | int | Schema version |
| `provider` | string | `"corva"` |
| `collection` | string | `"drilling.wits.depth"` |
| `asset_id` | int | Well / asset identifier |
| `company_id` | int | Operator / company identifier |
| `measured_depth` | float | Measured depth (ft) — **primary index** |
| `timestamp_read` | int | Timestamp when the depth record was read |
| `log_identifier` | string | Identifies the depth log source |
| `app` | string | Source app key (e.g. `"corva.witsml-depth-source"`) |

#### `data` sub-fields (depth-based channels)

| Channel Key | Description |
|-------------|-------------|
| `dep` | Depth (ft) |
| `tvd` | True vertical depth (ft) |
| `hdtv` | Hole depth TVD |
| `ctda` | Cumulative tortuosity / dogleg (azimuth) |
| `ctdi` | Cumulative tortuosity / dogleg (inclination) |
| `ropa` | Rate of penetration average (ft/hr) |
| `wobavg` | Weight on bit average (klbs) |
| `hkldav` | Hookload average (klbs) |
| `rpmsavg` | Surface RPM average |
| `tqabav` | Torque average (ft-lbs) |
| `sppavg` | Standpipe pressure average (psi) |
| `fliavg` | Flow in average (gpm) |
| `floavg` | Flow out average (gpm) |
| `tmiavg` | Mud temp in average (°F) |
| `tmoavg` | Mud temp out average (°F) |
| `dmiavg` | Mud density in average (ppg) |
| `dmoavg` | Mud density out average (ppg) |
| `lagdep` | Lag depth (ft) |
| `ghcavg` | Total gas (avg) |
| `ghcmax` | Total gas (max) |
| `gcc1av` | C1 methane average |
| `gcc2av` | C2 ethane average |
| `gcc3av` | C3 propane average |
| `gcc4na` | nC4 butane average |
| `gcc4ia` | iC4 isobutane average |
| `gcc5na` | nC5 pentane average |
| `gcc5ia` | iC5 isopentane average |
| `gcc5nea` | neoC5 neopentane average |
| `remarks` | String – remarks / notes |
| `hob` | Height of block? / Hole OB |
| `bitf` | Bit force |

---

### 2.3 `corva#completion.wits` — Completions (Frac/Pump)

| Field | Type | Description |
|-------|------|-------------|
| `_id` | string | Unique document ID |
| `version` | int | Schema version |
| `provider` | string | `"corva"` |
| `collection` | string | `"completion.wits"` |
| `timestamp` | int | Unix epoch (seconds) |
| `asset_id` | int | Well / asset identifier |
| `company_id` | int | Operator / company identifier |
| `stage_number` | int | **Frac stage number** |

#### `data` sub-fields (completions channels)

| Channel Key | Unit (typical) | Description |
|-------------|----------------|-------------|
| `timestamp` | epoch (s) | Data timestamp |
| `is_valid` | bool | Data validity flag |
| `elapsed_time` | s | Elapsed time in stage |
| `wellhead_pressure` | psi | Treating/wellhead pressure |
| `pumpside_pressure` | psi | Pumpside pressure |
| `backside_pressure` | psi | Annular/backside pressure |
| `slurry_flow_rate_in` | bpm | Slurry flow rate in |
| `clean_flow_rate_in` | bpm | Clean flow rate in |
| `total_clean_volume_in` | bbl | Total clean volume pumped |
| `total_slurry_volume_in` | bbl | Total slurry volume pumped |
| `total_proppant_concentration` | ppa | Surface proppant concentration |
| `bottomhole_proppant_concentration` | ppa | Bottomhole proppant concentration |
| `total_proppant_mass` | lbs | Cumulative proppant mass |
| `proppant_1_concentration` | ppa | Proppant type 1 concentration |
| `proppant_1_mass` | lbs | Proppant type 1 mass |
| `proppant_2_concentration` | ppa | Proppant type 2 concentration |
| `hydrostatic_pressure` | psi | Hydrostatic pressure |
| `inverse_hydrostatic_pressure` | 1/psi | Inverse hydrostatic pressure |
| `total_chemical_rate_in` | gpm | Total chemical rate |
| `total_friction_reducer` | gal | Total friction reducer |
| `friction_reducer` | gpt | Friction reducer concentration |
| `friction_reducer_extra` | gpt | Extra friction reducer |
| `cross_linker` | gpt | Crosslinker concentration |
| `gel` | ppt | Gel concentration |
| `acid` | gpt | Acid concentration |
| `surfactant` | gpt | Surfactant concentration |
| `scale_inhibitor` | gpt | Scale inhibitor |
| `enzyme_breaker` | gpt | Enzyme breaker |
| `liquid_breaker` | gpt | Liquid breaker |
| `powder_breaker` | ppt | Powder breaker |
| `clay_stabilizer` | gpt | Clay stabilizer |
| `corrosion_inhibitor` | gpt | Corrosion inhibitor |
| `biocide` | gpt | Biocide |
| `emulsifier` | gpt | Emulsifier |
| `non_emulsifier` | gpt | Non-emulsifier / demulsifier |
| `iron_control` | gpt | Iron control |
| `oxygen_scavenger` | gpt | Oxygen scavenger |
| `mutual_solvent` | gpt | Mutual solvent |
| `paraffin_control` | gpt | Paraffin control |
| `ph_adjusting_agent` | gpt | pH adjusting agent |
| `accelerator` | gpt | Accelerator |
| `fluid_loss` | gpt | Fluid loss additive |
| `acid_inhibitor` | gpt | Acid inhibitor |
| `acid_retarder` | gpt | Acid retarder |
| `anti_sludge` | gpt | Anti-sludge |
| `fines_suspender` | gpt | Fines suspender |
| `divertor` | gpt | Divertor |
| `instant_crosslinker` | gpt | Instant crosslinker |
| `delayed_crosslinker` | gpt | Delayed crosslinker |
| `polymer_plug` | - | Polymer plug |
| `powder_gel` | ppt | Powder gel |
| `powder_friction_reducer` | ppt | Powder friction reducer |
| `powder_enzyme_breaker` | ppt | Powder enzyme breaker |
| `extra_clean_fluid` | bbl | Extra clean fluid |
| `end_of_stage` | int (0/1) | End of stage flag |

---

### 2.4 `corva#wireline.wits` — Wireline

| Field | Type | Description |
|-------|------|-------------|
| `_id` | string | Unique document ID |
| `version` | int | Schema version |
| `provider` | string | `"corva"` |
| `collection` | string | `"wireline.wits"` |
| `timestamp` | int | Unix epoch (seconds) |
| `asset_id` | int | Well / asset identifier |
| `company_id` | int | Operator / company identifier |
| `stage_number` | int | Stage number |
| `app` | string | Source app key |

#### `data` sub-fields (wireline channels)

| Channel Key | Unit (typical) | Description |
|-------------|----------------|-------------|
| `measured_depth` | ft | Current wireline depth |
| `line_speed` | ft/min | Wireline speed |
| `line_tension` | lbs | Wireline tension |
| `elapsed_time` | s | Elapsed time |
| `current` | A | Electrical current |
| `voltage` | V | Voltage |
| `casing_collar_locator` | mV | CCL reading |
| `state` | string | Activity state (e.g. "Unclassified") |
| `wellbore_orientation` | string | "Vertical" / "Horizontal" |
| `c_006` | - | Custom channel 006 |
| `c_007` | - | Custom channel 007 |

---

## 3. Reference / Metadata Datasets

These are **non-streaming** collections that store well configuration and planning data. They are accessed via the Data API and are referenced by ID in stream event metadata.

| Dataset (API path) | Provider | Description |
|---------------------|----------|-------------|
| `data.well-sections` | corva | Well sections / hole sections (name, diameter, top_depth) |
| `data.drillstring` | corva | BHA / drillstring components |
| `data.casing` | corva | Casing string design |
| `data.mud` | corva | Mud / fluid properties |
| `data.actual-survey` | corva | Actual directional survey stations |
| `data.plan-survey` | corva | Planned survey / well plan |
| `data.bit` | corva | Bit records |
| `data.surface-equipment` | corva | Surface equipment configuration |
| `data.cuttings` | corva | Cuttings / geology records |
| `activities.summary-2tours` | corva | Daily activity summaries (day/night tours) |
| `completion.data.purged_stages` | corva | Records of reprocessed/purged frac stages |

### Example: `data.well-sections` document shape

```json
{
  "_id": "...",
  "asset_id": 12345,
  "company_id": 1,
  "provider": "corva",
  "collection": "data.well-sections",
  "data": {
    "name": "Surface Casing",
    "diameter": 9.625,
    "top_depth": 0
  }
}
```

### Example: `activities.summary-2tours` document shape

```json
{
  "_id": "5f75f5016c880105025879a6",
  "version": 1,
  "asset_id": 31659357,
  "company_id": 1,
  "provider": "corva",
  "collection": "activities.summary-2tours",
  "timestamp": 1545177600,
  "data": {
    "start_timestamp": 1545091200,
    "end_timestamp": 1545177600,
    "activities": [
      { "name": "In Slips", "day": 37935, "night": 43200 },
      { "name": "Run in Hole", "day": 80 },
      { "name": "Pull out of Hole", "day": 455 },
      { "name": "Static Off Bottom", "day": 4725 },
      { "name": "Dry Reaming Down", "day": 5 }
    ]
  }
}
```

---

## 4. Platform API Endpoints (v2)

These use the **Corva Platform API** (`api.corva.ai`) and return JSON:API formatted data.

| Endpoint | Description |
|----------|-------------|
| `GET /v2/wells` | List wells (supports filters: rig, company, fields, pagination) |
| `GET /v2/wells/{id}` | Get a specific well |
| `GET /v2/rigs/{id}` | Get a specific rig |
| `GET /v2/assets/{id}` | Get an asset |

---

## 5. How to Query Datasets

### Data API (recommended)

```
GET https://data.corva.ai/api/v1/data/{provider}/{dataset}/?query={...}&limit=N&sort={...}&fields=field1,field2&skip=N
```

**Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| `query` | JSON string | MongoDB-style query (e.g. `{"asset_id": 12345}`) |
| `sort` | JSON string | Sort order (e.g. `{"timestamp": -1}` for newest first) |
| `limit` | int | Max records to return |
| `skip` | int | Offset for pagination |
| `fields` | string | Comma-separated list of fields to return |

### Python SDK Example

```python
from corva import Api

response = api.get(
    '/api/v1/data/corva/wits/',
    params={
        'query': '{"asset_id": 12345}',
        'sort': '{"timestamp": -1}',
        'limit': 500,
        'fields': 'timestamp,data.hole_depth,data.weight_on_bit,data.hook_load'
    }
)
records = response.json()
```

### JavaScript (Frontend) Example

```javascript
import { corvaDataAPI } from '@corva/ui/clients';

const records = await corvaDataAPI.get('/api/v1/data/corva/wits/', {
  query: JSON.stringify({ asset_id: 12345 }),
  sort: JSON.stringify({ timestamp: -1 }),
  limit: 500,
  fields: 'timestamp,data.hole_depth,data.weight_on_bit'
});
```

---

## 6. Interactive Documentation & Tools

| Resource | URL |
|----------|-----|
| Dev Center Dataset Explorer | https://app.corva.ai/dev-center/datasets |
| Data API Swagger (test tool) | https://data.corva.ai/docs#/ |
| Data API Redoc (reference) | https://data.corva.ai/redoc |
| Platform API Swagger | https://api.corva.ai/documentation/index.html |
| Python SDK Docs | https://corva-ai.github.io/python-sdk/ |
| Node SDK (npm) | https://www.npmjs.com/package/@corva/node-sdk |
| UI Component Library | https://storybook.dev.corva.ai/ |
| Example Python Apps | https://github.com/corva-ai/corva-example-python-apps |
| Example Node Apps | https://github.com/corva-ai/corva-example-node-apps |

---

## 7. Notes

- **Channel availability varies**: Not every `data.*` key will appear for every well. It depends on the WITSML data source and what the data provider sends.
- **This list is not exhaustive**: Corva's Dataset Explorer (behind auth) contains the full catalog including company-specific and app-generated datasets.
- **Custom datasets**: Any Dev Center app can create its own datasets under its provider namespace (e.g. `my-company#my-custom-dataset`). These must be declared in the app's `manifest.json`.
- **Permissions**: Read/write permissions to datasets must be declared in `manifest.json`. Read-only access can be granted to `corva#*` datasets; read/write is available for your own company's datasets.
