# Corva Data Dictionary

> **Scope**: 102 datasets with known field schemas
> **Source**: Corva Dataset Explorer API + schema extraction
> **Editable CSV**: `corva_data_dictionary.csv` (edit in Excel, then run `rebuild_dictionary.py`)

---

## Quick Lookup Table

| Dataset | Category | Type | API Path | Fields | Description |
|---|---|---|---|---|---|
| `corva#activities.summary-2tours` | Activities / Operations | time | `/api/v1/data/corva/activities.summary-2tours/` | 14 | MongoDB document unique identifier |
| `corva#activities.summary-3m` | Activities / Operations | time | `/api/v1/data/corva/activities.summary-3m/` | 14 | MongoDB document unique identifier |
| `corva#activities.summary-continuous` | Activities / Operations | time | `/api/v1/data/corva/activities.summary-continuous/` | 14 | MongoDB document unique identifier |
| `corva#activity-groups` | Activities / Operations | time | `/api/v1/data/corva/activity-groups/` | 19 | MongoDB document unique identifier |
| `corva#anti-collision.metadata-edm` | Anti-Collision | reference | `/api/v1/data/corva/anti-collision.metadata-edm/` | 17 | MongoDB document unique identifier |
| `corva#anti-collision.metadata-well` | Anti-Collision | reference | `/api/v1/data/corva/anti-collision.metadata-well/` | 17 | MongoDB document unique identifier |
| `corva#askcorva.settings` | AskCorva / AI | reference | `/api/v1/data/corva/askcorva.settings/` | 16 | Name/label for kpi |
| `corva#assets` | Other | time | `/api/v1/data/corva/assets/` | 34 | MongoDB document unique identifier |
| `corva#circulation.lag-depth` | Circulation | time | `/api/v1/data/corva/circulation.lag-depth/` | 16 | MongoDB document unique identifier |
| `corva#circulation.volumetric` | Circulation | time | `/api/v1/data/corva/circulation.volumetric/` | 13 | MongoDB document unique identifier |
| `corva#completion.ccl-annotations` | Completions / Frac | time | `/api/v1/data/corva/completion.ccl-annotations/` | 17 | MongoDB document unique identifier |
| `corva#completion.ccl-anomalies` | Completions / Frac | reference | `/api/v1/data/corva/completion.ccl-anomalies/` | 17 | MongoDB document unique identifier |
| `corva#completion.ccl-settings` | Completions / Frac | time | `/api/v1/data/corva/completion.ccl-settings/` | 19 | MongoDB document unique identifier |
| `corva#completion.ccl-summary` | Completions / Frac | reference | `/api/v1/data/corva/completion.ccl-summary/` | 22 | MongoDB document unique identifier |
| `corva#completion.custom_metrics` | Completions / Frac | time | `/api/v1/data/corva/completion.custom_metrics/` | 13 | Hhp |
| `corva#completion.data.files` | Completions / Frac | time | `/api/v1/data/corva/completion.data.files/` | 11 | MongoDB document unique identifier |
| `corva#completion.data.job-settings` | Completions / Frac | time | `/api/v1/data/corva/completion.data.job-settings/` | 20 | MongoDB document unique identifier |
| `corva#completion.data.time-log` | Completions / Frac | time | `/api/v1/data/corva/completion.data.time-log/` | 17 | MongoDB document unique identifier |
| `corva#completion.offset.abra` | Completions / Frac | time | `/api/v1/data/corva/completion.offset.abra/` | 12 | MongoDB document unique identifier |
| `corva#completion.predictions` | Completions / Frac | time | `/api/v1/data/corva/completion.predictions/` | 201 | MongoDB document unique identifier |
| `corva#completion.stage-times` | Completions / Frac | time | `/api/v1/data/corva/completion.stage-times/` | 12 | MongoDB document unique identifier |
| `corva#completion.wits` | WITS (Other Phases) | time | `/api/v1/data/corva/completion.wits/` | 47 | Nested object containing default units data |
| `corva#completion.wits.raw` | WITS (Other Phases) | time | `/api/v1/data/corva/completion.wits.raw/` | 58 | MongoDB document unique identifier |
| `corva#completion.wits.summary-10s` | WITS (Other Phases) | time | `/api/v1/data/corva/completion.wits.summary-10s/` | 211 | MongoDB document unique identifier |
| `corva#completion.wits.summary-1m` | WITS (Other Phases) | time | `/api/v1/data/corva/completion.wits.summary-1m/` | 211 | MongoDB document unique identifier |
| `corva#config-response` | Other | time | `/api/v1/data/corva/config-response/` | 12 | MongoDB document unique identifier |
| `corva#data.actual_survey` | Well Data (data.*) | time | `/api/v1/data/corva/data.actual_survey/` | 28 | MongoDB document unique identifier |
| `corva#data.afe` | Well Data (data.*) | time | `/api/v1/data/corva/data.afe/` | 12 | MongoDB document unique identifier |
| `corva#data.casing` | Well Data (data.*) | time | `/api/v1/data/corva/data.casing/` | 22 | MongoDB document unique identifier |
| `corva#data.crews` | Well Data (data.*) | time | `/api/v1/data/corva/data.crews/` | 22 | MongoDB document unique identifier |
| `corva#data.diaries` | Well Data (data.*) | time | `/api/v1/data/corva/data.diaries/` | 10 | MongoDB document unique identifier |
| `corva#data.drillstring` | Well Data (data.*) | time | `/api/v1/data/corva/data.drillstring/` | 38 | MongoDB document unique identifier |
| `corva#data.files` | Well Data (data.*) | time | `/api/v1/data/corva/data.files/` | 11 | MongoDB document unique identifier |
| `corva#data.formations` | Well Data (data.*) | time | `/api/v1/data/corva/data.formations/` | 12 | MongoDB document unique identifier |
| `corva#data.lessons-learned` | Well Data (data.*) | time | `/api/v1/data/corva/data.lessons-learned/` | 21 | MongoDB document unique identifier |
| `corva#data.mud` | Well Data (data.*) | time | `/api/v1/data/corva/data.mud/` | 61 | MongoDB document unique identifier |
| `corva#data.npt-events` | Well Data (data.*) | time | `/api/v1/data/corva/data.npt-events/` | 15 | MongoDB document unique identifier |
| `corva#data.operation-summaries` | Well Data (data.*) | time | `/api/v1/data/corva/data.operation-summaries/` | 10 | MongoDB document unique identifier |
| `corva#data.plan_survey` | Well Data (data.*) | time | `/api/v1/data/corva/data.plan_survey/` | 22 | MongoDB document unique identifier |
| `corva#data.surface-equipment` | Well Data (data.*) | time | `/api/v1/data/corva/data.surface-equipment/` | 22 | MongoDB document unique identifier |
| `corva#data.well-sections` | Well Data (data.*) | time | `/api/v1/data/corva/data.well-sections/` | 14 | MongoDB document unique identifier |
| `corva#directional.accuracy` | Directional | time | `/api/v1/data/corva/directional.accuracy/` | 76 | MongoDB document unique identifier |
| `corva#directional.projection_to_bit` | Directional | time | `/api/v1/data/corva/directional.projection_to_bit/` | 13 | MongoDB document unique identifier |
| `corva#directional.rotational-tendency` | Directional | time | `/api/v1/data/corva/directional.rotational-tendency/` | 26 | MongoDB document unique identifier |
| `corva#directional.surveys` | Directional | time | `/api/v1/data/corva/directional.surveys/` | 29 | MongoDB document unique identifier |
| `corva#directional.tortuosity` | Directional | time | `/api/v1/data/corva/directional.tortuosity/` | 48 | MongoDB document unique identifier |
| `corva#directional.trend` | Directional | time | `/api/v1/data/corva/directional.trend/` | 32 | MongoDB document unique identifier |
| `corva#drilling-dysfunction` | Drilling | time | `/api/v1/data/corva/drilling-dysfunction/` | 14 | MongoDB document unique identifier |
| `corva#drilling-efficiency.mse` | Drilling | time | `/api/v1/data/corva/drilling-efficiency.mse/` | 14 | MongoDB document unique identifier |
| `corva#drilling-efficiency.mse-heatmap` | Drilling | time | `/api/v1/data/corva/drilling-efficiency.mse-heatmap/` | 52 | MongoDB document unique identifier |
| `corva#drilling-efficiency.optimization` | Drilling | time | `/api/v1/data/corva/drilling-efficiency.optimization/` | 19 | MongoDB document unique identifier |
| `corva#drilling-efficiency.predictions` | Drilling | time | `/api/v1/data/corva/drilling-efficiency.predictions/` | 58 | MongoDB document unique identifier |
| `corva#drilling-efficiency.rop-heatmap` | Drilling | time | `/api/v1/data/corva/drilling-efficiency.rop-heatmap/` | 52 | MongoDB document unique identifier |
| `corva#drilling.mud-ops` | Drilling | time | `/api/v1/data/corva/drilling.mud-ops/` | 66 | MongoDB document unique identifier |
| `corva#drillout.data.drillstring` | Drillout | time | `/api/v1/data/corva/drillout.data.drillstring/` | 42 | MongoDB document unique identifier |
| `corva#drillout.data.mud` | Drillout | time | `/api/v1/data/corva/drillout.data.mud/` | 17 | MongoDB document unique identifier |
| `corva#drillout.data.surface-equipment` | Drillout | time | `/api/v1/data/corva/drillout.data.surface-equipment/` | 22 | MongoDB document unique identifier |
| `corva#drillout.torque-and-drag.axial-load` | Drillout | time | `/api/v1/data/corva/drillout.torque-and-drag.axial-load/` | 19 | MongoDB document unique identifier |
| `corva#drillout.torque-and-drag.hookload-trend` | Drillout | time | `/api/v1/data/corva/drillout.torque-and-drag.hookload-trend/` | 58 | MongoDB document unique identifier |
| `corva#drillout.torque-and-drag.stress` | Drillout | time | `/api/v1/data/corva/drillout.torque-and-drag.stress/` | 20 | MongoDB document unique identifier |
| `corva#drillout.torque-and-drag.torque-trend` | Drillout | time | `/api/v1/data/corva/drillout.torque-and-drag.torque-trend/` | 38 | MongoDB document unique identifier |
| `corva#drillout.wits.summary-6h` | WITS (Other Phases) | time | `/api/v1/data/corva/drillout.wits.summary-6h/` | 49 | MongoDB document unique identifier |
| `corva#formation-evaluation.metadata` | Formation Evaluation | time | `/api/v1/data/corva/formation-evaluation.metadata/` | 39 | MongoDB document unique identifier |
| `corva#hydraulics.cuttings-transport` | Hydraulics | time | `/api/v1/data/corva/hydraulics.cuttings-transport/` | 25 | MongoDB document unique identifier |
| `corva#hydraulics.overview` | Hydraulics | time | `/api/v1/data/corva/hydraulics.overview/` | 21 | MongoDB document unique identifier |
| `corva#hydraulics.pressure-loss` | Hydraulics | time | `/api/v1/data/corva/hydraulics.pressure-loss/` | 54 | MongoDB document unique identifier |
| `corva#hydraulics.pressure-trend` | Hydraulics | time | `/api/v1/data/corva/hydraulics.pressure-trend/` | 23 | MongoDB document unique identifier |
| `corva#hydraulics.surge-and-swab` | Hydraulics | time | `/api/v1/data/corva/hydraulics.surge-and-swab/` | 34 | MongoDB document unique identifier |
| `corva#kick-detection` | Other | time | `/api/v1/data/corva/kick-detection/` | 21 | MongoDB document unique identifier |
| `corva#launchpad_witsml_recommendations` | Launchpad / Connectivity | reference | `/api/v1/data/corva/launchpad_witsml_recommendations/` | 36 | MongoDB document unique identifier |
| `corva#machine-learning.rop` | Predictive Drilling / ML | time | `/api/v1/data/corva/machine-learning.rop/` | 48 | MongoDB document unique identifier |
| `corva#metrics` | Metrics / KPIs | time | `/api/v1/data/corva/metrics/` | 17 | MongoDB document unique identifier |
| `corva#milling-console-real-time` | Other | time | `/api/v1/data/corva/milling-console-real-time/` | 14 | Container object for all measurement/computed data fields |
| `corva#operations` | Activities / Operations | time | `/api/v1/data/corva/operations/` | 40 | MongoDB document unique identifier |
| `corva#pdm.operating-condition` | PDM / Motor | time | `/api/v1/data/corva/pdm.operating-condition/` | 32 | MongoDB document unique identifier |
| `corva#pdm.overview` | PDM / Motor | time | `/api/v1/data/corva/pdm.overview/` | 19 | MongoDB document unique identifier |
| `corva#pdm.stall-detection` | PDM / Motor | time | `/api/v1/data/corva/pdm.stall-detection/` | 13 | MongoDB document unique identifier |
| `corva#procedural-compliance` | Other | time | `/api/v1/data/corva/procedural-compliance/` | 14 | MongoDB document unique identifier |
| `corva#production.wits` | Production (Enverus) | time | `/api/v1/data/corva/production.wits/` | 16 | MongoDB document unique identifier |
| `corva#pumpdown.wits` | WITS (Other Phases) | time | `/api/v1/data/corva/pumpdown.wits/` | 17 | MongoDB document unique identifier |
| `corva#torque-and-drag.axial-load` | Torque & Drag | time | `/api/v1/data/corva/torque-and-drag.axial-load/` | 19 | MongoDB document unique identifier |
| `corva#torque-and-drag.downhole-transfer` | Torque & Drag | time | `/api/v1/data/corva/torque-and-drag.downhole-transfer/` | 20 | MongoDB document unique identifier |
| `corva#torque-and-drag.friction-factor` | Torque & Drag | time | `/api/v1/data/corva/torque-and-drag.friction-factor/` | 22 | MongoDB document unique identifier |
| `corva#torque-and-drag.hookload-trend` | Torque & Drag | time | `/api/v1/data/corva/torque-and-drag.hookload-trend/` | 58 | MongoDB document unique identifier |
| `corva#torque-and-drag.overview` | Torque & Drag | time | `/api/v1/data/corva/torque-and-drag.overview/` | 23 | MongoDB document unique identifier |
| `corva#torque-and-drag.stress` | Torque & Drag | time | `/api/v1/data/corva/torque-and-drag.stress/` | 20 | MongoDB document unique identifier |
| `corva#torque-and-drag.torque` | Torque & Drag | time | `/api/v1/data/corva/torque-and-drag.torque/` | 16 | MongoDB document unique identifier |
| `corva#torque-and-drag.torque-trend` | Torque & Drag | time | `/api/v1/data/corva/torque-and-drag.torque-trend/` | 38 | MongoDB document unique identifier |
| `corva#traces.offsets` | Other | time | `/api/v1/data/corva/traces.offsets/` | 63 | MongoDB document unique identifier |
| `corva#trend-analysis` | Other | time | `/api/v1/data/corva/trend-analysis/` | 16 | MongoDB document unique identifier |
| `corva#trip-sheet` | Other | time | `/api/v1/data/corva/trip-sheet/` | 28 | MongoDB document unique identifier |
| `corva#well_cache` | Other | time | `/api/v1/data/corva/well_cache/` | 102 | MongoDB document unique identifier |
| `corva#wellness_rule_settings_history` | Wellness / Check-Up | reference | `/api/v1/data/corva/wellness_rule_settings_history/` | 22 | MongoDB document unique identifier |
| `corva#wireline.activity.summary-stage` | Wireline | time | `/api/v1/data/corva/wireline.activity.summary-stage/` | 72 | MongoDB document unique identifier |
| `corva#wireline.stage-times` | Wireline | time | `/api/v1/data/corva/wireline.stage-times/` | 17 | MongoDB document unique identifier |
| `corva#wireline.wits` | WITS (Other Phases) | time | `/api/v1/data/corva/wireline.wits/` | 21 | MongoDB document unique identifier |
| `corva#wireline.wits.summary-10s` | WITS (Other Phases) | time | `/api/v1/data/corva/wireline.wits.summary-10s/` | 15 | MongoDB document unique identifier |
| `corva#wits` | WITS / Real-Time Drilling | time | `/api/v1/data/corva/wits/` | 52 | Nested object containing default units data |
| `corva#wits.summary-1ft` | WITS / Real-Time Drilling | time | `/api/v1/data/corva/wits.summary-1ft/` | 59 | MongoDB document unique identifier |
| `corva#wits.summary-1m` | WITS / Real-Time Drilling | time | `/api/v1/data/corva/wits.summary-1m/` | 68 | MongoDB document unique identifier |
| `corva#wits.summary-30m` | WITS / Real-Time Drilling | time | `/api/v1/data/corva/wits.summary-30m/` | 70 | MongoDB document unique identifier |
| `corva#wits.summary-6h` | WITS / Real-Time Drilling | time | `/api/v1/data/corva/wits.summary-6h/` | 73 | MongoDB document unique identifier |

---

## Datasets by Category

### 1. WITS / Real-Time Drilling

#### `corva#wits`

- **Friendly Name**: wits
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wits/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `default_units` | object |  |  | Nested object containing default units data |  | wits, real-time, drilling, container, object |
| `default_units.rop` | str | ft/h |  | Rate of penetration - drilling speed (ft/hr) |  | wits, real-time, drilling, drilling, rop, real-time, key-metric, performance |
| `default_units.das_doc` | str | in/rev |  | Das doc |  | wits, real-time, drilling |
| `default_units.das_mse` | str | ksi |  | Das mse |  | wits, real-time, drilling |
| `default_units.das_rop` | str | ft/h |  | Das rop |  | wits, real-time, drilling |
| `default_units.das_time` | str | s |  | Timestamp for das |  | wits, real-time, drilling, metadata, time |
| `default_units.bit_depth` | str | ft |  | Current depth of the drill bit |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `default_units.gain_loss` | str | bbl |  | Gain loss |  | wits, real-time, drilling |
| `default_units.hook_load` | str | klbf |  | Hook load |  | wits, real-time, drilling |
| `default_units.total_gas` | str | %EMA |  | Total gas |  | wits, real-time, drilling |
| `default_units.diff_press` | str | psi |  | Differential pressure across the motor (psi) |  | wits, real-time, drilling, pdm, pressure, real-time |
| `default_units.hole_depth` | str | ft |  | Current hole depth (bottom of wellbore) |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `default_units.mud_volume` | str | bbl |  | Mud volume |  | wits, real-time, drilling |
| `default_units.mud_density` | str | ppg |  | Mud density |  | wits, real-time, drilling |
| `default_units.mud_flow_in` | str | gal/min |  | Mud flow in |  | wits, real-time, drilling |
| `default_units.block_height` | str | ft |  | Traveling block height (ft) |  | wits, real-time, drilling, drilling, rig, real-time |
| `default_units.mud_flow_out` | str | gal/min |  | Mud flow out |  | wits, real-time, drilling |
| `default_units.pit_volume_1` | str | bbl |  | Pit volume 1 |  | wits, real-time, drilling |
| `default_units.pit_volume_2` | str | bbl |  | Pit volume 2 |  | wits, real-time, drilling |
| `default_units.pit_volume_3` | str | bbl |  | Pit volume 3 |  | wits, real-time, drilling |
| `default_units.pit_volume_4` | str | bbl |  | Pit volume 4 |  | wits, real-time, drilling |
| `default_units.pit_volume_5` | str | bbl |  | Pit volume 5 |  | wits, real-time, drilling |
| `default_units.pit_volume_6` | str | bbl |  | Pit volume 6 |  | wits, real-time, drilling |
| `default_units.pit_volume_7` | str | bbl |  | Pit volume 7 |  | wits, real-time, drilling |
| `default_units.pit_volume_8` | str | bbl |  | Pit volume 8 |  | wits, real-time, drilling |
| `default_units.kill_pressure` | str | psi |  | Pressure: kill (psi) |  | wits, real-time, drilling, pressure, measurement |
| `default_units.rotary_torque` | str | ft-klbf |  | Rotary torque |  | wits, real-time, drilling |
| `default_units.weight_on_bit` | str | klbf |  | Weight applied to the drill bit (klbs) |  | wits, real-time, drilling, drilling, wob, real-time, key-metric |
| `default_units.choke_pressure` | str | psi |  | Pressure: choke (psi) |  | wits, real-time, drilling, pressure, measurement |
| `default_units.ad_torque_limit` | str | ft-klbf |  | Ad torque limit |  | wits, real-time, drilling |
| `default_units.ad_wob_setpoint` | str | klbf |  | Ad wob setpoint |  | wits, real-time, drilling |
| `default_units.mwd_annulus_ecd` | str | ppg |  | Mwd annulus ecd |  | wits, real-time, drilling |
| `default_units.das_downhole_mse` | str | ksi |  | Das downhole mse |  | wits, real-time, drilling |
| `default_units.total_pit_volume` | str | bbl |  | Total pit volume |  | wits, real-time, drilling |
| `default_units.active_pit_volume` | str | bbl |  | Active pit volume |  | wits, real-time, drilling |
| `default_units.wellhead_pressure` | str | psi |  | Pressure: wellhead (psi) |  | wits, real-time, drilling, pressure, measurement |
| `default_units.boost_pump_flow_in` | str | gal/min |  | Boost pump flow in |  | wits, real-time, drilling |
| `default_units.standpipe_pressure` | str | psi |  | Standpipe pressure - pump pressure at surface (psi) |  | wits, real-time, drilling, drilling, spp, pressure, real-time, key-metric |
| `default_units.trip_tank_volume_1` | str | bbl |  | Trip tank volume 1 |  | wits, real-time, drilling |
| `default_units.trip_tank_volume_2` | str | bbl |  | Trip tank volume 2 |  | wits, real-time, drilling |
| `default_units.trip_tank_volume_3` | str | bbl |  | Trip tank volume 3 |  | wits, real-time, drilling |
| `default_units.das_recommended_rop` | str | ft/h |  | Das recommended rop |  | wits, real-time, drilling |
| `default_units.das_recommended_wob` | str | klbf |  | Das recommended wob |  | wits, real-time, drilling |
| `default_units.das_rop_lower_limit` | str | ft/h |  | Das rop lower limit |  | wits, real-time, drilling |
| `default_units.das_rop_upper_limit` | str | ft/h |  | Das rop upper limit |  | wits, real-time, drilling |
| `default_units.das_wob_lower_limit` | str | klbf |  | Das wob lower limit |  | wits, real-time, drilling |
| `default_units.das_wob_upper_limit` | str | klbf |  | Das wob upper limit |  | wits, real-time, drilling |
| `default_units.das_recommended_flow` | str | gal/min |  | Das recommended flow |  | wits, real-time, drilling |
| `default_units.das_rop_limiting_max` | str | ft/h |  | Das rop limiting max |  | wits, real-time, drilling |
| `default_units.mwd_annulus_pressure` | str | psi |  | Pressure: mwd annulus (psi) |  | wits, real-time, drilling, pressure, measurement |
| `default_units.annular_back_pressure` | str | psi |  | Pressure: annular back (psi) |  | wits, real-time, drilling, pressure, measurement |
| `default_units.ad_diff_press_setpoint` | str | psi |  | Ad diff press setpoint |  | wits, real-time, drilling |

#### `corva#wits.summary-1ft`

- **Friendly Name**: wits.summary-1ft
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wits.summary-1ft/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760ab86c88011b6e589c74 |  | MongoDB document unique identifier |  | wits, real-time, drilling, metadata, internal, primary-key |
| `app` | str | wits-depth-summary |  | App |  | wits, real-time, drilling |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, drilling, metadata, container |
| `data.state_max` | str | Rotary Drilling |  | State max |  | wits, real-time, drilling |
| `data.hole_depth` | int | 7069 |  | Current hole depth (bottom of wellbore) |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `data.entry_at_max` | int | 1545575264 |  | Entry at max |  | wits, real-time, drilling |
| `data.entry_at_min` | int | 1545575229 |  | Entry at min |  | wits, real-time, drilling |
| `data.bit_depth_max` | float | 7069.01 |  | Maximum bit depth in the summary interval |  | wits, real-time, drilling, depth, drilling, aggregated |
| `data.bit_depth_min` | float | 7068.6 |  | Minimum bit depth in the summary interval |  | wits, real-time, drilling, depth, drilling, aggregated |
| `data.hook_load_max` | float | 741.25 |  | Hook load max |  | wits, real-time, drilling |
| `data.hook_load_min` | float | 738.74 |  | Hook load min |  | wits, real-time, drilling |
| `data.timestamp_max` | int | 1545575264 |  | Timestamp max |  | wits, real-time, drilling |
| `data.timestamp_min` | int | 1545575229 |  | Timestamp min |  | wits, real-time, drilling |
| `data.bit_depth_mean` | float | 7068.745 |  | Bit depth mean |  | wits, real-time, drilling |
| `data.hole_depth_max` | float | 7069.09 |  | Maximum hole depth in the summary interval |  | wits, real-time, drilling, depth, drilling, aggregated |
| `data.hole_depth_min` | float | 7068.86 |  | Minimum hole depth in the summary interval |  | wits, real-time, drilling, depth, drilling, aggregated |
| `data.hook_load_mean` | float | 740.575 |  | Hook load mean |  | wits, real-time, drilling |
| `data.pump_spm_3_max` | int | 17 |  | Pump spm 3 max |  | wits, real-time, drilling |
| `data.pump_spm_3_min` | int | 2 |  | Pump spm 3 min |  | wits, real-time, drilling |
| `data.hole_depth_mean` | float | 7068.889 |  | Hole depth mean |  | wits, real-time, drilling |
| `data.mud_flow_in_max` | float | 207.08 |  | Mud flow in max |  | wits, real-time, drilling |
| `data.mud_flow_in_min` | float | 34.25 |  | Mud flow in min |  | wits, real-time, drilling |
| `data.pump_spm_3_mean` | float | 8.75 |  | Pump spm 3 mean |  | wits, real-time, drilling |
| `data.bit_depth_median` | float | 7068.71 |  | Bit depth median |  | wits, real-time, drilling |
| `data.block_height_max` | int | 62 |  | Block height max |  | wits, real-time, drilling |
| `data.block_height_min` | float | 61.46 |  | Block height min |  | wits, real-time, drilling |
| `data.hook_load_median` | float | 740.795 |  | Hook load median |  | wits, real-time, drilling |
| `data.mud_flow_in_mean` | float | 120.704 |  | Mud flow in mean |  | wits, real-time, drilling |
| `data.block_height_mean` | float | 61.826 |  | Block height mean |  | wits, real-time, drilling |
| `data.hole_depth_median` | float | 7068.86 |  | Hole depth median |  | wits, real-time, drilling |
| `data.pump_spm_3_median` | int | 8 |  | Pump spm 3 median |  | wits, real-time, drilling |
| `data.mud_flow_in_median` | float | 130.705 |  | Mud flow in median |  | wits, real-time, drilling |
| `data.pump_spm_total_max` | int | 17 |  | Pump spm total max |  | wits, real-time, drilling |
| `data.pump_spm_total_min` | int | 2 |  | Pump spm total min |  | wits, real-time, drilling |
| `data.block_height_median` | float | 61.88 |  | Block height median |  | wits, real-time, drilling |
| `data.pump_spm_total_mean` | float | 8.75 |  | Pump spm total mean |  | wits, real-time, drilling |
| `data.pump_spm_total_median` | int | 8 |  | Pump spm total median |  | wits, real-time, drilling |
| `data.standpipe_pressure_max` | float | 67.04 |  | Standpipe pressure max |  | wits, real-time, drilling |
| `data.standpipe_pressure_min` | float | 57.43 |  | Standpipe pressure min |  | wits, real-time, drilling |
| `data.standpipe_pressure_mean` | float | 62.789 |  | Standpipe pressure mean |  | wits, real-time, drilling |
| `data.true_vertical_depth_max` | float | 7069.09 |  | True vertical depth max |  | wits, real-time, drilling |
| `data.true_vertical_depth_min` | float | 7068.86 |  | True vertical depth min |  | wits, real-time, drilling |
| `data.true_vertical_depth_mean` | float | 7068.889 |  | True vertical depth mean |  | wits, real-time, drilling |
| `data.standpipe_pressure_median` | float | 63.04 |  | Standpipe pressure median |  | wits, real-time, drilling |
| `data.true_vertical_depth_median` | float | 7068.86 |  | True vertical depth median |  | wits, real-time, drilling |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, drilling, metadata, well-id, filter-key, required |
| `metadata` | object |  |  | Nested object containing metadata data |  | wits, real-time, drilling, container, object |
| `metadata.mud` | str | 5f75f3786c88017f9358a561 |  | Mud |  | wits, real-time, drilling |
| `metadata.casing` | null |  |  | Casing |  | wits, real-time, drilling |
| `metadata.cuttings` | null |  |  | Cuttings |  | wits, real-time, drilling |
| `metadata.drillstring` | str | 5f75f3796c88017f9358a5ff |  | Drillstring |  | wits, real-time, drilling |
| `metadata.plan_survey` | str | 5f75f3786c88017f9358a5f7 |  | Plan survey |  | wits, real-time, drilling |
| `metadata.actual_survey` | str | 5f75f3796c88017f9358a663 |  | Actual survey |  | wits, real-time, drilling |
| `metadata.surface-equipment` | str | 5f75f3796c88017f9358a616 |  | Surface equipment |  | wits, real-time, drilling |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, drilling, metadata, internal |
| `timestamp` | int | 1545575264 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, drilling, metadata, time-index, filter-key, required |
| `collection` | str | wits.summary-1ft |  | MongoDB collection name this record belongs to |  | wits, real-time, drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, drilling, metadata, company, filter-key |

#### `corva#wits.summary-1m`

- **Friendly Name**: wits.summary-1m
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wits.summary-1m/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f380e9681d7bc92f84b5 |  | MongoDB document unique identifier |  | wits, real-time, drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, drilling, metadata, container |
| `data.h2s` | null |  |  | H2s |  | wits, real-time, drilling |
| `data.rop` | int | 0 |  | Rate of penetration - drilling speed (ft/hr) |  | wits, real-time, drilling, drilling, rop, real-time, key-metric, performance |
| `data.bvel` | int | 0 |  | Bvel |  | wits, real-time, drilling |
| `data.klpg` | float | 7.73 |  | Klpg |  | wits, real-time, drilling |
| `data.mtin` | float | 79.36 |  | Mtin |  | wits, real-time, drilling |
| `data.mwin` | float | 0.01 |  | Mwin |  | wits, real-time, drilling |
| `data.risr` | int | 0 |  | Risr |  | wits, real-time, drilling |
| `data.spm5` | int | 0 |  | Spm5 |  | wits, real-time, drilling |
| `data.time` | str | 2018-12-18T16:15:39.0000000Z |  | Time |  | wits, real-time, drilling |
| `data.cecdb` | null |  |  | Cecdb |  | wits, real-time, drilling |
| `data.mtout` | float | 74.01 |  | Mtout |  | wits, real-time, drilling |
| `data.mwout` | int | 0 |  | Mwout |  | wits, real-time, drilling |
| `data.state` | str | In Slips |  | State |  | wits, real-time, drilling |
| `data.depthv` | int | 7065 |  | Depthv |  | wits, real-time, drilling |
| `data.pitact` | float | 48.69 |  | Pitact |  | wits, real-time, drilling |
| `data.totgas` | int | 0 |  | Totgas |  | wits, real-time, drilling |
| `data.bitdepv` | float | 116.35 |  | Bitdepv |  | wits, real-time, drilling |
| `data.co2_avg` | int | 0 |  | Co2 avg |  | wits, real-time, drilling |
| `data.dep_rtn` | float | 0.07 |  | Dep rtn |  | wits, real-time, drilling |
| `data.flowout` | int | 0 |  | Flowout |  | wits, real-time, drilling |
| `data.rop_ins` | int | 0 |  | Rop ins |  | wits, real-time, drilling |
| `data.entry_at` | int | 1545149760 |  | Timestamp for entry |  | wits, real-time, drilling, metadata, time |
| `data.hkld_max` | int | 0 |  | Hkld max |  | wits, real-time, drilling |
| `data.totgasin` | int | 0 |  | Totgasin |  | wits, real-time, drilling |
| `data.bit_depth` | float | 116.35 |  | Current depth of the drill bit |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `data.flowoutpc` | float | -0.32 |  | Flowoutpc |  | wits, real-time, drilling |
| `data.gamma_ray` | int | 0 |  | Gamma ray measurement from MWD/LWD tool (API units) |  | wits, real-time, drilling, drilling, mwd, formation, real-time |
| `data.hook_load` | int | 184 |  | Hook load |  | wits, real-time, drilling |
| `data.strokesum` | int | 0 |  | Strokesum |  | wits, real-time, drilling |
| `data.diff_press` | int | 0 |  | Differential pressure across the motor (psi) |  | wits, real-time, drilling, pdm, pressure, real-time |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `data.pump_spm_1` | int | 0 |  | Pump spm 1 |  | wits, real-time, drilling |
| `data.pump_spm_2` | int | 0 |  | Pump spm 2 |  | wits, real-time, drilling |
| `data.pump_spm_3` | int | 0 |  | Pump spm 3 |  | wits, real-time, drilling |
| `data.pump_spm_4` | int | 0 |  | Pump spm 4 |  | wits, real-time, drilling |
| `data.rotary_rpm` | int | 0 |  | Surface rotary speed (RPM) |  | wits, real-time, drilling, drilling, rpm, real-time, key-metric |
| `data.strokectr1` | int | 0 |  | Strokectr1 |  | wits, real-time, drilling |
| `data.strokectr2` | int | 0 |  | Strokectr2 |  | wits, real-time, drilling |
| `data.strokectr3` | int | 0 |  | Strokectr3 |  | wits, real-time, drilling |
| `data.strokectr4` | int | 0 |  | Strokectr4 |  | wits, real-time, drilling |
| `data.strokectr5` | int | 0 |  | Strokectr5 |  | wits, real-time, drilling |
| `data.strokectr6` | null |  |  | Strokectr6 |  | wits, real-time, drilling |
| `data.torque_max` | int | 0 |  | Torque max |  | wits, real-time, drilling |
| `data.choke_press` | float | 13.65 |  | Choke press |  | wits, real-time, drilling |
| `data.gainlosstot` | float | 47.52 |  | Gainlosstot |  | wits, real-time, drilling |
| `data.mud_flow_in` | int | 0 |  | Mud flow in |  | wits, real-time, drilling |
| `data.block_height` | int | 19 |  | Traveling block height (ft) |  | wits, real-time, drilling, drilling, rig, real-time |
| `data.rotary_torque` | int | 0 |  | Rotary torque |  | wits, real-time, drilling |
| `data.weight_on_bit` | int | 0 |  | Weight applied to the drill bit (klbs) |  | wits, real-time, drilling, drilling, wob, real-time, key-metric |
| `data.depth_enhanced` | null |  |  | Depth enhanced |  | wits, real-time, drilling |
| `data.pump_spm_total` | int | 0 |  | Pump spm total |  | wits, real-time, drilling |
| `data.bitdep_enhanced` | null |  |  | Bitdep enhanced |  | wits, real-time, drilling |
| `data.depthv_enhanced` | null |  |  | Depthv enhanced |  | wits, real-time, drilling |
| `data.bitdepv_enhanced` | int | 0 |  | Bitdepv enhanced |  | wits, real-time, drilling |
| `data.depth_hydraulics` | null |  |  | Depth hydraulics |  | wits, real-time, drilling |
| `data.bitdep_hydraulics` | null |  |  | Bitdep hydraulics |  | wits, real-time, drilling |
| `data.depthv_hydraulics` | null |  |  | Depthv hydraulics |  | wits, real-time, drilling |
| `data.bitdepv_hydraulics` | null |  |  | Bitdepv hydraulics |  | wits, real-time, drilling |
| `data.standpipe_pressure` | float | 79.87 |  | Standpipe pressure - pump pressure at surface (psi) |  | wits, real-time, drilling, drilling, spp, pressure, real-time, key-metric |
| `data.true_vertical_depth` | int | 7065 |  | Depth value: true vertical (ft) |  | wits, real-time, drilling, depth, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, drilling, metadata, internal |
| `timestamp` | int | 1545149760 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, drilling, metadata, time-index, filter-key, required |
| `collection` | str | wits.summary-1m |  | MongoDB collection name this record belongs to |  | wits, real-time, drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, drilling, metadata, company, filter-key |

#### `corva#wits.summary-30m`

- **Friendly Name**: wits.summary-30m
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wits.summary-30m/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f38dce24b22b224dc1f9 |  | MongoDB document unique identifier |  | wits, real-time, drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, drilling, metadata, container |
| `data.h2s` | null |  |  | H2s |  | wits, real-time, drilling |
| `data.rop` | int | 0 |  | Rate of penetration - drilling speed (ft/hr) |  | wits, real-time, drilling, drilling, rop, real-time, key-metric, performance |
| `data.bvel` | int | 0 |  | Bvel |  | wits, real-time, drilling |
| `data.klpg` | float | 6.91 |  | Klpg |  | wits, real-time, drilling |
| `data.mtin` | float | 79.36 |  | Mtin |  | wits, real-time, drilling |
| `data.mwin` | float | 0.01 |  | Mwin |  | wits, real-time, drilling |
| `data.risr` | int | 0 |  | Risr |  | wits, real-time, drilling |
| `data.spm5` | int | 0 |  | Spm5 |  | wits, real-time, drilling |
| `data.time` | str | 2018-12-18T16:22:39.0000000Z |  | Time |  | wits, real-time, drilling |
| `data.cecdb` | null |  |  | Cecdb |  | wits, real-time, drilling |
| `data.mtout` | float | 74.04 |  | Mtout |  | wits, real-time, drilling |
| `data.mwout` | int | 0 |  | Mwout |  | wits, real-time, drilling |
| `data.state` | str | In Slips |  | State |  | wits, real-time, drilling |
| `data.depthv` | int | 7065 |  | Depthv |  | wits, real-time, drilling |
| `data.pitact` | float | 48.67 |  | Pitact |  | wits, real-time, drilling |
| `data.totgas` | int | 0 |  | Totgas |  | wits, real-time, drilling |
| `data.bitdepv` | float | 116.35 |  | Bitdepv |  | wits, real-time, drilling |
| `data.co2_avg` | int | 0 |  | Co2 avg |  | wits, real-time, drilling |
| `data.dep_rtn` | float | 0.07 |  | Dep rtn |  | wits, real-time, drilling |
| `data.flowout` | int | 0 |  | Flowout |  | wits, real-time, drilling |
| `data.rop_ins` | int | 0 |  | Rop ins |  | wits, real-time, drilling |
| `data.entry_at` | int | 1545150600 |  | Timestamp for entry |  | wits, real-time, drilling, metadata, time |
| `data.hkld_max` | int | 0 |  | Hkld max |  | wits, real-time, drilling |
| `data.totgasin` | int | 0 |  | Totgasin |  | wits, real-time, drilling |
| `data.bit_depth` | float | 116.35 |  | Current depth of the drill bit |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `data.flowoutpc` | float | -0.32 |  | Flowoutpc |  | wits, real-time, drilling |
| `data.gamma_ray` | int | 0 |  | Gamma ray measurement from MWD/LWD tool (API units) |  | wits, real-time, drilling, drilling, mwd, formation, real-time |
| `data.hook_load` | float | 183.78 |  | Hook load |  | wits, real-time, drilling |
| `data.strokesum` | int | 0 |  | Strokesum |  | wits, real-time, drilling |
| `data.diff_press` | int | 0 |  | Differential pressure across the motor (psi) |  | wits, real-time, drilling, pdm, pressure, real-time |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `data.pump_spm_1` | int | 0 |  | Pump spm 1 |  | wits, real-time, drilling |
| `data.pump_spm_2` | int | 0 |  | Pump spm 2 |  | wits, real-time, drilling |
| `data.pump_spm_3` | int | 0 |  | Pump spm 3 |  | wits, real-time, drilling |
| `data.pump_spm_4` | int | 0 |  | Pump spm 4 |  | wits, real-time, drilling |
| `data.rotary_rpm` | int | 0 |  | Surface rotary speed (RPM) |  | wits, real-time, drilling, drilling, rpm, real-time, key-metric |
| `data.strokectr1` | int | 0 |  | Strokectr1 |  | wits, real-time, drilling |
| `data.strokectr2` | int | 0 |  | Strokectr2 |  | wits, real-time, drilling |
| `data.strokectr3` | int | 0 |  | Strokectr3 |  | wits, real-time, drilling |
| `data.strokectr4` | int | 0 |  | Strokectr4 |  | wits, real-time, drilling |
| `data.strokectr5` | int | 0 |  | Strokectr5 |  | wits, real-time, drilling |
| `data.strokectr6` | null |  |  | Strokectr6 |  | wits, real-time, drilling |
| `data.torque_max` | int | 0 |  | Torque max |  | wits, real-time, drilling |
| `data.choke_press` | float | 8.82 |  | Choke press |  | wits, real-time, drilling |
| `data.gainlosstot` | float | 47.51 |  | Gainlosstot |  | wits, real-time, drilling |
| `data.mud_flow_in` | int | 0 |  | Mud flow in |  | wits, real-time, drilling |
| `data.block_height` | float | 18.88 |  | Traveling block height (ft) |  | wits, real-time, drilling, drilling, rig, real-time |
| `data.rotary_torque` | int | 0 |  | Rotary torque |  | wits, real-time, drilling |
| `data.weight_on_bit` | int | 0 |  | Weight applied to the drill bit (klbs) |  | wits, real-time, drilling, drilling, wob, real-time, key-metric |
| `data.activity_times` | object |  |  | Nested object containing activity times data |  | wits, real-time, drilling, container, object |
| `data.activity_times.in slips` | int | 885 |  | In slips |  | wits, real-time, drilling |
| `data.depth_enhanced` | null |  |  | Depth enhanced |  | wits, real-time, drilling |
| `data.pump_spm_total` | int | 0 |  | Pump spm total |  | wits, real-time, drilling |
| `data.bitdep_enhanced` | null |  |  | Bitdep enhanced |  | wits, real-time, drilling |
| `data.depthv_enhanced` | null |  |  | Depthv enhanced |  | wits, real-time, drilling |
| `data.bitdepv_enhanced` | int | 0 |  | Bitdepv enhanced |  | wits, real-time, drilling |
| `data.depth_hydraulics` | null |  |  | Depth hydraulics |  | wits, real-time, drilling |
| `data.bitdep_hydraulics` | null |  |  | Bitdep hydraulics |  | wits, real-time, drilling |
| `data.depthv_hydraulics` | null |  |  | Depthv hydraulics |  | wits, real-time, drilling |
| `data.bitdepv_hydraulics` | null |  |  | Bitdepv hydraulics |  | wits, real-time, drilling |
| `data.standpipe_pressure` | float | 79.47 |  | Standpipe pressure - pump pressure at surface (psi) |  | wits, real-time, drilling, drilling, spp, pressure, real-time, key-metric |
| `data.true_vertical_depth` | int | 7065 |  | Depth value: true vertical (ft) |  | wits, real-time, drilling, depth, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, drilling, metadata, internal |
| `timestamp` | int | 1545150600 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, drilling, metadata, time-index, filter-key, required |
| `collection` | str | wits.summary-30m |  | MongoDB collection name this record belongs to |  | wits, real-time, drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, drilling, metadata, company, filter-key |

#### `corva#wits.summary-6h`

- **Friendly Name**: wits.summary-6h
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wits.summary-6h/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3dc6c880174e0592862 |  | MongoDB document unique identifier |  | wits, real-time, drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, drilling, metadata, container |
| `data.h2s` | int | 0 |  | H2s |  | wits, real-time, drilling |
| `data.rop` | int | 0 |  | Rate of penetration - drilling speed (ft/hr) |  | wits, real-time, drilling, drilling, rop, real-time, key-metric, performance |
| `data.bvel` | int | 0 |  | Bvel |  | wits, real-time, drilling |
| `data.klpg` | float | 6.91 |  | Klpg |  | wits, real-time, drilling |
| `data.mtin` | float | 79.44 |  | Mtin |  | wits, real-time, drilling |
| `data.mwin` | float | 0.01 |  | Mwin |  | wits, real-time, drilling |
| `data.risr` | int | 0 |  | Risr |  | wits, real-time, drilling |
| `data.spm5` | int | 0 |  | Spm5 |  | wits, real-time, drilling |
| `data.time` | str | 2018-12-18T17:07:37.0000000Z |  | Time |  | wits, real-time, drilling |
| `data.cecdb` | int | 0 |  | Cecdb |  | wits, real-time, drilling |
| `data.mtout` | float | 74.27 |  | Mtout |  | wits, real-time, drilling |
| `data.mwout` | int | 0 |  | Mwout |  | wits, real-time, drilling |
| `data.state` | str | In Slips |  | State |  | wits, real-time, drilling |
| `data.depthv` | int | 7065 |  | Depthv |  | wits, real-time, drilling |
| `data.pitact` | float | 48.67 |  | Pitact |  | wits, real-time, drilling |
| `data.totgas` | int | 0 |  | Totgas |  | wits, real-time, drilling |
| `data.bitdepv` | float | 116.35 |  | Bitdepv |  | wits, real-time, drilling |
| `data.co2_avg` | int | 0 |  | Co2 avg |  | wits, real-time, drilling |
| `data.dep_rtn` | float | 0.07 |  | Dep rtn |  | wits, real-time, drilling |
| `data.flowout` | int | 0 |  | Flowout |  | wits, real-time, drilling |
| `data.rop_ins` | int | 0 |  | Rop ins |  | wits, real-time, drilling |
| `data.entry_at` | int | 1545156000 |  | Timestamp for entry |  | wits, real-time, drilling, metadata, time |
| `data.hkld_max` | int | 0 |  | Hkld max |  | wits, real-time, drilling |
| `data.totgasin` | int | 0 |  | Totgasin |  | wits, real-time, drilling |
| `data.bit_depth` | float | 116.35 |  | Current depth of the drill bit |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `data.flowoutpc` | float | -0.32 |  | Flowoutpc |  | wits, real-time, drilling |
| `data.gamma_ray` | int | 0 |  | Gamma ray measurement from MWD/LWD tool (API units) |  | wits, real-time, drilling, drilling, mwd, formation, real-time |
| `data.hook_load` | float | 184.02 |  | Hook load |  | wits, real-time, drilling |
| `data.strokesum` | int | 0 |  | Strokesum |  | wits, real-time, drilling |
| `data.diff_press` | int | 0 |  | Differential pressure across the motor (psi) |  | wits, real-time, drilling, pdm, pressure, real-time |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | wits, real-time, drilling, depth, drilling, real-time, key-metric |
| `data.pump_spm_1` | int | 0 |  | Pump spm 1 |  | wits, real-time, drilling |
| `data.pump_spm_2` | int | 0 |  | Pump spm 2 |  | wits, real-time, drilling |
| `data.pump_spm_3` | int | 0 |  | Pump spm 3 |  | wits, real-time, drilling |
| `data.pump_spm_4` | int | 0 |  | Pump spm 4 |  | wits, real-time, drilling |
| `data.rotary_rpm` | int | 0 |  | Surface rotary speed (RPM) |  | wits, real-time, drilling, drilling, rpm, real-time, key-metric |
| `data.strokectr1` | int | 0 |  | Strokectr1 |  | wits, real-time, drilling |
| `data.strokectr2` | int | 0 |  | Strokectr2 |  | wits, real-time, drilling |
| `data.strokectr3` | int | 0 |  | Strokectr3 |  | wits, real-time, drilling |
| `data.strokectr4` | int | 0 |  | Strokectr4 |  | wits, real-time, drilling |
| `data.strokectr5` | int | 0 |  | Strokectr5 |  | wits, real-time, drilling |
| `data.strokectr6` | int | 0 |  | Strokectr6 |  | wits, real-time, drilling |
| `data.torque_max` | int | 0 |  | Torque max |  | wits, real-time, drilling |
| `data.choke_press` | float | 8.02 |  | Choke press |  | wits, real-time, drilling |
| `data.gainlosstot` | float | 47.51 |  | Gainlosstot |  | wits, real-time, drilling |
| `data.mud_flow_in` | int | 0 |  | Mud flow in |  | wits, real-time, drilling |
| `data.block_height` | float | 18.8 |  | Traveling block height (ft) |  | wits, real-time, drilling, drilling, rig, real-time |
| `data.rotary_torque` | int | 0 |  | Rotary torque |  | wits, real-time, drilling |
| `data.weight_on_bit` | int | 0 |  | Weight applied to the drill bit (klbs) |  | wits, real-time, drilling, drilling, wob, real-time, key-metric |
| `data.activity_times` | object |  |  | Nested object containing activity times data |  | wits, real-time, drilling, container, object |
| `data.activity_times.in slips` | int | 4675 |  | In slips |  | wits, real-time, drilling |
| `data.activity_times.run in hole` | int | 25 |  | Run in hole |  | wits, real-time, drilling |
| `data.activity_times.pull out of hole` | int | 125 |  | Pull out of hole |  | wits, real-time, drilling |
| `data.activity_times.static off bottom` | int | 1485 |  | Static off bottom |  | wits, real-time, drilling |
| `data.depth_enhanced` | int | 0 |  | Depth enhanced |  | wits, real-time, drilling |
| `data.pump_spm_total` | int | 0 |  | Pump spm total |  | wits, real-time, drilling |
| `data.bitdep_enhanced` | int | 0 |  | Bitdep enhanced |  | wits, real-time, drilling |
| `data.depthv_enhanced` | int | 0 |  | Depthv enhanced |  | wits, real-time, drilling |
| `data.bitdepv_enhanced` | int | 0 |  | Bitdepv enhanced |  | wits, real-time, drilling |
| `data.depth_hydraulics` | int | 0 |  | Depth hydraulics |  | wits, real-time, drilling |
| `data.bitdep_hydraulics` | int | 0 |  | Bitdep hydraulics |  | wits, real-time, drilling |
| `data.depthv_hydraulics` | int | 0 |  | Depthv hydraulics |  | wits, real-time, drilling |
| `data.bitdepv_hydraulics` | int | 0 |  | Bitdepv hydraulics |  | wits, real-time, drilling |
| `data.standpipe_pressure` | float | 79.87 |  | Standpipe pressure - pump pressure at surface (psi) |  | wits, real-time, drilling, drilling, spp, pressure, real-time, key-metric |
| `data.true_vertical_depth` | int | 7065 |  | Depth value: true vertical (ft) |  | wits, real-time, drilling, depth, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, drilling, metadata, internal |
| `timestamp` | int | 1545156000 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, drilling, metadata, time-index, filter-key, required |
| `collection` | str | wits.summary-6h |  | MongoDB collection name this record belongs to |  | wits, real-time, drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, drilling, metadata, company, filter-key |

### 2. Drilling

#### `corva#drilling-dysfunction`

- **Friendly Name**: drilling-dysfunction
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drilling-dysfunction/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f63d7c6a264acca084ea |  | MongoDB document unique identifier |  | drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drilling, metadata, container |
| `data.activity` | str | In Slips |  | Activity code number |  | drilling, operations, activity, classification |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | drilling, depth, drilling, real-time, key-metric |
| `data.hole_depth_tvd` | int | 7065 |  | Hole depth tvd |  | drilling |
| `data.tsr_summary_value` | null |  |  | Tsr summary value |  | drilling |
| `data.tsr_summary_category` | null |  |  | Tsr summary category |  | drilling |
| `type` | str | tsr_1_min_summary |  | Type classifier for this record |  | drilling, metadata, classification |
| `version` | int | 1 |  | Schema version number for this record |  | drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drilling, metadata, internal |
| `timestamp` | int | 1545199919 |  | Unix epoch timestamp (seconds) of the record |  | drilling, metadata, time-index, filter-key, required |
| `collection` | str | drilling-dysfunction |  | MongoDB collection name this record belongs to |  | drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drilling, metadata, company, filter-key |

#### `corva#drilling-efficiency.mse`

- **Friendly Name**: drilling-efficiency.mse
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drilling-efficiency.mse/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75fc7fce24b23d534d5f3c |  | MongoDB document unique identifier |  | drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drilling, metadata, container |
| `data.rop` | array[unknown] |  |  | Rate of penetration - drilling speed (ft/hr) |  | drilling, drilling, rop, real-time, key-metric, performance |
| `data.ucs` | array[unknown] |  |  | Array of ucs records |  | drilling, container, array |
| `data.status` | int | 0 |  | Current status of the record/check |  | drilling, metadata, status |
| `data.downhole` | array[unknown] |  |  | Array of downhole records |  | drilling, container, array |
| `data.gamma_ray` | array[unknown] |  |  | Gamma ray measurement from MWD/LWD tool (API units) |  | drilling, drilling, mwd, formation, real-time |
| `data.casing_depth` | int | 7065 |  | Depth value: casing (ft) |  | drilling, depth, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drilling, metadata, internal |
| `timestamp` | int | 1545316207 |  | Unix epoch timestamp (seconds) of the record |  | drilling, metadata, time-index, filter-key, required |
| `collection` | str | drilling-efficiency.mse |  | MongoDB collection name this record belongs to |  | drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drilling, metadata, company, filter-key |

#### `corva#drilling-efficiency.mse-heatmap`

- **Friendly Name**: drilling-efficiency.mse-heatmap
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drilling-efficiency.mse-heatmap/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760d6f14483c400ef8e81c |  | MongoDB document unique identifier |  | drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drilling, metadata, container |
| `data.rotary` | array[dict] |  |  | Array of rotary records |  | drilling, container, array |
| `data.rotary[].heatmap` | array[list] |  |  | Array of heatmap records |  | drilling, container, array |
| `data.status` | int | 0 |  | Current status of the record/check |  | drilling, metadata, status |
| `data.x_axis` | object |  |  | Nested object containing x axis data |  | drilling, container, object |
| `data.x_axis.rows` | int | 25 |  | Rows |  | drilling |
| `data.x_axis.type` | str | rpm |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.x_axis.maximum` | int | 120 |  | Maximum |  | drilling |
| `data.x_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.y_axis` | object |  |  | Nested object containing y axis data |  | drilling, container, object |
| `data.y_axis.type` | str | wob |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.y_axis.columns` | int | 25 |  | Columns |  | drilling |
| `data.y_axis.maximum` | int | 60 |  | Maximum |  | drilling |
| `data.y_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.z_axis` | object |  |  | Nested object containing z axis data |  | drilling, container, object |
| `data.z_axis.type` | str | mse |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.z_axis.maximum` | float | 93.88 |  | Maximum |  | drilling |
| `data.z_axis.minimum` | float | 89.95 |  | Minimum |  | drilling |
| `data.warning` | object |  |  | Nested object containing warning data |  | drilling, container, object |
| `data.warning.code` | str | diff_pressure_rop_heatmap_not_available |  | Code |  | drilling |
| `data.warning.message` | str | The drillstring does not contain a PDM, therefo... |  | Message |  | drilling |
| `data.formation` | object |  |  | Nested object containing formation data |  | drilling, container, object |
| `data.formation.tvd_top` | int | 0 |  | Tvd top |  | drilling |
| `data.formation.lithology` | str |  |  | Lithology |  | drilling |
| `data.formation.tvd_bottom` | int | 8436 |  | Tvd bottom |  | drilling |
| `data.formation.formation_name` | str | Surface Formation |  | Name/label for formation |  | drilling, metadata, display, label |
| `data.formation.measured_depth_top` | int | 0 |  | Measured depth top |  | drilling |
| `data.is_lateral` | bool | False |  | Flag indicating whether is lateral |  | drilling, boolean, flag |
| `data.wob_histogram` | object |  |  | Nested object containing wob histogram data |  | drilling, container, object |
| `data.wob_histogram.maximum` | int | 60 |  | Maximum |  | drilling |
| `data.wob_histogram.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.wob_histogram.divisions` | int | 25 |  | Divisions |  | drilling |
| `data.wob_histogram.frequencies` | array[int] |  |  | Array of frequencies records |  | drilling, container, array |
| `data.wob_histogram.normalized_frequencies` | array[int] |  |  | Array of normalized frequencies records |  | drilling, container, array |
| `data.measured_depth` | object |  |  | Measured depth along the wellbore path |  | drilling, depth, survey, directional |
| `data.measured_depth.maximum` | float | 7539.84 |  | Maximum |  | drilling |
| `data.measured_depth.minimum` | float | 7401.34 |  | Minimum |  | drilling |
| `data.optimal_region` | object |  |  | Nested object containing optimal region data |  | drilling, container, object |
| `data.optimal_region.max_mse` | float | 93.88 |  | Max mse |  | drilling |
| `data.optimal_region.max_rpm` | int | 62 |  | Max rpm |  | drilling |
| `data.optimal_region.min_rpm` | int | 53 |  | Min rpm |  | drilling |
| `data.optimal_region.optimized_mse` | float | 91.77 |  | Optimized mse |  | drilling |
| `data.optimal_region.max_weight_on_bit` | float | 9.6 |  | Max weight on bit |  | drilling |
| `data.optimal_region.min_weight_on_bit` | float | 4.8 |  | Min weight on bit |  | drilling |
| `data.heatmap_wob_axis` | array[list] |  |  | Array of heatmap wob axis records |  | drilling, container, array |
| `version` | int | 1 |  | Schema version number for this record |  | drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drilling, metadata, internal |
| `timestamp` | int | 1545621414 |  | Unix epoch timestamp (seconds) of the record |  | drilling, metadata, time-index, filter-key, required |
| `collection` | str | drilling-efficiency.mse-heatmap |  | MongoDB collection name this record belongs to |  | drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drilling, metadata, company, filter-key |

#### `corva#drilling-efficiency.optimization`

- **Friendly Name**: drilling-efficiency.optimization
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drilling-efficiency.optimization/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760ac414483c31f2f98412 |  | MongoDB document unique identifier |  | drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drilling, metadata, container |
| `data.actual` | object |  |  | Nested object containing actual data |  | drilling, container, object |
| `data.actual.rop` | int | 5 |  | Rate of penetration - drilling speed (ft/hr) |  | drilling, drilling, rop, real-time, key-metric, performance |
| `data.actual.state` | str | Rotary Drilling |  | State |  | drilling |
| `data.actual.bit_size` | int | 26 |  | Bit size |  | drilling |
| `data.actual.rotary_rpm` | int | 0 |  | Surface rotary speed (RPM) |  | drilling, drilling, rpm, real-time, key-metric |
| `data.actual.inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | drilling, directional, survey, key-metric |
| `data.actual.mud_flow_in` | float | 80.3 |  | Mud flow in |  | drilling |
| `data.actual.weight_on_bit` | float | 4.88 |  | Weight applied to the drill bit (klbs) |  | drilling, drilling, wob, real-time, key-metric |
| `data.status` | int | 0 |  | Current status of the record/check |  | drilling, metadata, status |
| `data.recommended_mse` | dict | {} |  | Recommended mse |  | drilling |
| `data.recommended_rotary` | dict | {} |  | Recommended rotary |  | drilling |
| `version` | int | 1 |  | Schema version number for this record |  | drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drilling, metadata, internal |
| `timestamp` | int | 1545575935 |  | Unix epoch timestamp (seconds) of the record |  | drilling, metadata, time-index, filter-key, required |
| `collection` | str | drilling-efficiency.optimization |  | MongoDB collection name this record belongs to |  | drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drilling, metadata, company, filter-key |

#### `corva#drilling-efficiency.predictions`

- **Friendly Name**: drilling-efficiency.predictions
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drilling-efficiency.predictions/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75fa38e9681d141d2ec654 |  | MongoDB document unique identifier |  | drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drilling, metadata, container |
| `data.rotary` | array[dict] |  |  | Array of rotary records |  | drilling, container, array |
| `data.rotary[].heatmap` | array[list] |  |  | Array of heatmap records |  | drilling, container, array |
| `data.status` | int | 0 |  | Current status of the record/check |  | drilling, metadata, status |
| `data.x_axis` | object |  |  | Nested object containing x axis data |  | drilling, container, object |
| `data.x_axis.rows` | int | 25 |  | Rows |  | drilling |
| `data.x_axis.type` | str | rpm |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.x_axis.maximum` | int | 60 |  | Maximum |  | drilling |
| `data.x_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.y_axis` | object |  |  | Nested object containing y axis data |  | drilling, container, object |
| `data.y_axis.type` | str | wob |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.y_axis.columns` | int | 25 |  | Columns |  | drilling |
| `data.y_axis.maximum` | int | 60 |  | Maximum |  | drilling |
| `data.y_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.z_axis` | object |  |  | Nested object containing z axis data |  | drilling, container, object |
| `data.z_axis.type` | str | rop |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.z_axis.maximum` | int | 0 |  | Maximum |  | drilling |
| `data.z_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.formation` | object |  |  | Nested object containing formation data |  | drilling, container, object |
| `data.formation.tvd_top` | int | 0 |  | Tvd top |  | drilling |
| `data.formation.lithology` | str |  |  | Lithology |  | drilling |
| `data.formation.tvd_bottom` | int | 8436 |  | Tvd bottom |  | drilling |
| `data.formation.formation_name` | str | Surface Formation |  | Name/label for formation |  | drilling, metadata, display, label |
| `data.formation.measured_depth_top` | int | 0 |  | Measured depth top |  | drilling |
| `data.is_lateral` | bool | False |  | Flag indicating whether is lateral |  | drilling, boolean, flag |
| `data.wob_histogram` | object |  |  | Nested object containing wob histogram data |  | drilling, container, object |
| `data.wob_histogram.maximum` | int | 60 |  | Maximum |  | drilling |
| `data.wob_histogram.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.wob_histogram.divisions` | int | 25 |  | Divisions |  | drilling |
| `data.wob_histogram.frequencies` | array[int] |  |  | Array of frequencies records |  | drilling, container, array |
| `data.wob_histogram.normalized_frequencies` | array[int] |  |  | Array of normalized frequencies records |  | drilling, container, array |
| `data.measured_depth` | dict | {} |  | Measured depth along the wellbore path |  | drilling, depth, survey, directional |
| `data.optimal_region` | dict | {} |  | Optimal region |  | drilling |
| `data.heatmap_wob_axis` | array[list] |  |  | Array of heatmap wob axis records |  | drilling, container, array |
| `data.z_axis_diff_axis` | object |  |  | Nested object containing z axis diff axis data |  | drilling, container, object |
| `data.z_axis_diff_axis.type` | str | rop |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.z_axis_diff_axis.maximum` | int | 0 |  | Maximum |  | drilling |
| `data.z_axis_diff_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.y_axis_diff_press` | object |  |  | Nested object containing y axis diff press data |  | drilling, container, object |
| `data.y_axis_diff_press.type` | str | diff_press |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.y_axis_diff_press.columns` | int | 25 |  | Columns |  | drilling |
| `data.y_axis_diff_press.maximum` | int | 1150 |  | Maximum |  | drilling |
| `data.y_axis_diff_press.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.diff_press_histogram` | object |  |  | Nested object containing diff press histogram data |  | drilling, container, object |
| `data.diff_press_histogram.maximum` | int | 1150 |  | Maximum |  | drilling |
| `data.diff_press_histogram.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.diff_press_histogram.divisions` | int | 25 |  | Divisions |  | drilling |
| `data.diff_press_histogram.frequencies` | array[int] |  |  | Array of frequencies records |  | drilling, container, array |
| `data.diff_press_histogram.normalized_frequencies` | array[int] |  |  | Array of normalized frequencies records |  | drilling, container, array |
| `data.heatmap_diff_press_axis` | array[list] |  |  | Array of heatmap diff press axis records |  | drilling, container, array |
| `data.optimal_region_diff_axis` | dict | {} |  | Optimal region diff axis |  | drilling |
| `version` | int | 1 |  | Schema version number for this record |  | drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drilling, metadata, internal |
| `timestamp` | int | 1545275111 |  | Unix epoch timestamp (seconds) of the record |  | drilling, metadata, time-index, filter-key, required |
| `collection` | str | drilling-efficiency.rop-heatmap |  | MongoDB collection name this record belongs to |  | drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drilling, metadata, company, filter-key |

#### `corva#drilling-efficiency.rop-heatmap`

- **Friendly Name**: drilling-efficiency.rop-heatmap
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drilling-efficiency.rop-heatmap/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224debf2 |  | MongoDB document unique identifier |  | drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drilling, metadata, container |
| `data.rotary` | array[dict] |  |  | Array of rotary records |  | drilling, container, array |
| `data.rotary[].heatmap` | array[list] |  |  | Array of heatmap records |  | drilling, container, array |
| `data.status` | int | 0 |  | Current status of the record/check |  | drilling, metadata, status |
| `data.x_axis` | object |  |  | Nested object containing x axis data |  | drilling, container, object |
| `data.x_axis.rows` | int | 25 |  | Rows |  | drilling |
| `data.x_axis.type` | str | rpm |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.x_axis.maximum` | int | 60 |  | Maximum |  | drilling |
| `data.x_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.y_axis` | object |  |  | Nested object containing y axis data |  | drilling, container, object |
| `data.y_axis.type` | str | wob |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.y_axis.columns` | int | 25 |  | Columns |  | drilling |
| `data.y_axis.maximum` | int | 60 |  | Maximum |  | drilling |
| `data.y_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.z_axis` | object |  |  | Nested object containing z axis data |  | drilling, container, object |
| `data.z_axis.type` | str | rop |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.z_axis.maximum` | int | 0 |  | Maximum |  | drilling |
| `data.z_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.is_lateral` | bool | False |  | Flag indicating whether is lateral |  | drilling, boolean, flag |
| `data.wob_histogram` | object |  |  | Nested object containing wob histogram data |  | drilling, container, object |
| `data.wob_histogram.maximum` | int | 60 |  | Maximum |  | drilling |
| `data.wob_histogram.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.wob_histogram.divisions` | int | 25 |  | Divisions |  | drilling |
| `data.wob_histogram.frequencies` | array[int] |  |  | Array of frequencies records |  | drilling, container, array |
| `data.wob_histogram.normalized_frequencies` | array[int] |  |  | Array of normalized frequencies records |  | drilling, container, array |
| `data.measured_depth` | dict | {} |  | Measured depth along the wellbore path |  | drilling, depth, survey, directional |
| `data.optimal_region` | dict | {} |  | Optimal region |  | drilling |
| `data.heatmap_wob_axis` | array[list] |  |  | Array of heatmap wob axis records |  | drilling, container, array |
| `data.z_axis_diff_axis` | object |  |  | Nested object containing z axis diff axis data |  | drilling, container, object |
| `data.z_axis_diff_axis.type` | str | rop |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.z_axis_diff_axis.maximum` | int | 0 |  | Maximum |  | drilling |
| `data.z_axis_diff_axis.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.y_axis_diff_press` | object |  |  | Nested object containing y axis diff press data |  | drilling, container, object |
| `data.y_axis_diff_press.type` | str | diff_press |  | Type classifier for this record |  | drilling, metadata, classification |
| `data.y_axis_diff_press.columns` | int | 25 |  | Columns |  | drilling |
| `data.y_axis_diff_press.maximum` | int | 1150 |  | Maximum |  | drilling |
| `data.y_axis_diff_press.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.diff_press_histogram` | object |  |  | Nested object containing diff press histogram data |  | drilling, container, object |
| `data.diff_press_histogram.maximum` | int | 1150 |  | Maximum |  | drilling |
| `data.diff_press_histogram.minimum` | int | 0 |  | Minimum |  | drilling |
| `data.diff_press_histogram.divisions` | int | 25 |  | Divisions |  | drilling |
| `data.diff_press_histogram.frequencies` | array[int] |  |  | Array of frequencies records |  | drilling, container, array |
| `data.diff_press_histogram.normalized_frequencies` | array[int] |  |  | Array of normalized frequencies records |  | drilling, container, array |
| `data.heatmap_diff_press_axis` | array[list] |  |  | Array of heatmap diff press axis records |  | drilling, container, array |
| `data.optimal_region_diff_axis` | dict | {} |  | Optimal region diff axis |  | drilling |
| `version` | int | 1 |  | Schema version number for this record |  | drilling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drilling, metadata, internal |
| `timestamp` | int | 1545199574 |  | Unix epoch timestamp (seconds) of the record |  | drilling, metadata, time-index, filter-key, required |
| `collection` | str | drilling-efficiency.rop-heatmap |  | MongoDB collection name this record belongs to |  | drilling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drilling, metadata, company, filter-key |

#### `corva#drilling.mud-ops`

- **Friendly Name**: drilling.mud-ops
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drilling.mud-ops/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 665dc9ef46d3c905f59921df |  | MongoDB document unique identifier |  | drilling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drilling, metadata, container |
| `data.dTim` | int | 1717369200 |  | Dtim |  | drilling |
| `data.pumpOp` | array[dict] |  |  | Array of pumpOp records |  | drilling, container, array |
| `data.pumpOp[].pump` | int | 1 |  | Pump |  | drilling |
| `data.pumpOp[].idLiner` | object |  |  | Nested object containing idLiner data |  | drilling, container, object |
| `data.pumpOp[].idLiner.uom` | str | in |  | Uom |  | drilling |
| `data.pumpOp[].idLiner.value` | int | 6 |  | Value |  | drilling |
| `data.pumpOp[].pressure` | object |  |  | Nested object containing pressure data |  | drilling, container, object |
| `data.pumpOp[].pressure.uom` | str | psi |  | Uom |  | drilling |
| `data.pumpOp[].pressure.value` | int | 3950 |  | Value |  | drilling |
| `data.pumpOp[].lenStroke` | object |  |  | Nested object containing lenStroke data |  | drilling, container, object |
| `data.pumpOp[].lenStroke.uom` | str | in |  | Uom |  | drilling |
| `data.pumpOp[].lenStroke.value` | int | 12 |  | Value |  | drilling |
| `data.pumpOp[].rateStroke` | object |  |  | Nested object containing rateStroke data |  | drilling, container, object |
| `data.pumpOp[].rateStroke.uom` | str | rpm |  | Uom |  | drilling |
| `data.pumpOp[].rateStroke.value` | int | 110 |  | Value |  | drilling |
| `data.pumpOp[].pcEfficiency` | object |  |  | Nested object containing pcEfficiency data |  | drilling, container, object |
| `data.pumpOp[].pcEfficiency.uom` | str | % |  | Uom |  | drilling |
| `data.pumpOp[].pcEfficiency.value` | int | 95 |  | Value |  | drilling |
| `data.dayCost` | array[dict] |  |  | Array of dayCost records |  | drilling, container, array |
| `data.dayCost[].costCode` | str | mud product |  | Costcode |  | drilling |
| `data.dayCost[].costClass` | str | mud |  | Costclass |  | drilling |
| `data.dayCost[].costAmount` | float | 5057.19 |  | Costamount |  | drilling |
| `data.dayCost[].costItemDescription` | str | daily mud product cost |  | Costitemdescription |  | drilling |
| `data.sum24Hr` | str | Finish testing BOPs. Make up RSS BHA. TIH and t... |  | Sum24hr |  | drilling |
| `data.mudVolume` | object |  |  | Nested object containing mudVolume data |  | drilling, container, object |
| `data.mudVolume.mudLosses` | object |  |  | Nested object containing mudLosses data |  | drilling, container, object |
| `data.mudVolume.mudLosses.volLostShakerSurf` | int | 0 |  | Vollostshakersurf |  | drilling |
| `data.mudVolume.mudLosses.volTotMudLostHole` | int | 0 |  | Voltotmudlosthole |  | drilling |
| `data.mudVolume.mudLosses.volTotMudLostSurf` | int | 83 |  | Voltotmudlostsurf |  | drilling |
| `data.mudVolume.volMudBuilt` | int | 267 |  | Volmudbuilt |  | drilling |
| `data.mudVolume.volTotMudEnd` | int | 998 |  | Voltotmudend |  | drilling |
| `data.mudVolume.volMudReceived` | int | 0 |  | Volmudreceived |  | drilling |
| `data.mudVolume.volMudReturned` | int | 0 |  | Volmudreturned |  | drilling |
| `data.mudVolume.volTotMudStart` | int | 842 |  | Voltotmudstart |  | drilling |
| `data.pitVolume` | array[dict] |  |  | Array of pitVolume records |  | drilling, container, array |
| `data.pitVolume[].pit` | int | 1 |  | Pit |  | drilling |
| `data.pitVolume[].dTim` | int | 1717369059 |  | Dtim |  | drilling |
| `data.pitVolume[].volPit` | object |  |  | Nested object containing volPit data |  | drilling, container, object |
| `data.pitVolume[].volPit.uom` | str | bbl |  | Uom |  | drilling |
| `data.pitVolume[].volPit.value` | int | 0 |  | Value |  | drilling |
| `data.pitVolume[].densFluid` | object |  |  | Nested object containing densFluid data |  | drilling, container, object |
| `data.pitVolume[].densFluid.uom` | null |  |  | Uom |  | drilling |
| `data.pitVolume[].densFluid.value` | null |  |  | Value |  | drilling |
| `data.pitVolume[].descFluid` | null |  |  | Descfluid |  | drilling |
| `data.costDayMud` | float | 6573.95 |  | Costdaymud |  | drilling |
| `data.mudInventory` | array[dict] |  |  | Array of mudInventory records |  | drilling, container, array |
| `data.mudInventory[].name` | str | EZ-SQUEEZE |  | Display name of the component or record |  | drilling, metadata, display |
| `data.mudInventory[].qtyUsed` | int | 0 |  | Qtyused |  | drilling |
| `data.mudInventory[].costItem` | int | 0 |  | Costitem |  | drilling |
| `data.mudInventory[].qtyStart` | int | 250 |  | Qtystart |  | drilling |
| `data.mudInventory[].qtyReceived` | int | 0 |  | Qtyreceived |  | drilling |
| `data.mudInventory[].qtyReturned` | int | 0 |  | Qtyreturned |  | drilling |
| `data.mudInventory[].pricePerUnit` | int | 0 |  | Priceperunit |  | drilling |
| `data.mudInventory[].itemWtPerUnit` | object |  |  | Nested object containing itemWtPerUnit data |  | drilling, container, object |
| `data.mudInventory[].itemWtPerUnit.uom` | str | lbm |  | Uom |  | drilling |
| `data.mudInventory[].itemWtPerUnit.value` | int | 50 |  | Value |  | drilling |
| `data.mudInventory[].qtyAdjustment` | int | 0 |  | Qtyadjustment |  | drilling |
| `data.mudInventory[].qtyOnLocation` | int | 250 |  | Qtyonlocation |  | drilling |
| `version` | int | 1 |  | Schema version number for this record |  | drilling, metadata, internal, versioning |
| `asset_id` | int | 87177326 |  | Unique identifier for the well/asset this record belongs to |  | drilling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drilling, metadata, internal |
| `timestamp` | int | 1717422575 |  | Unix epoch timestamp (seconds) of the record |  | drilling, metadata, time-index, filter-key, required |
| `collection` | str | drilling.mud-ops |  | MongoDB collection name this record belongs to |  | drilling, metadata, internal |
| `company_id` | int | 135 |  | Unique identifier for the company/operator |  | drilling, metadata, company, filter-key |

### 3. Directional

#### `corva#directional.accuracy`

- **Friendly Name**: directional.accuracy
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/directional.accuracy/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224debf8 |  | MongoDB document unique identifier |  | directional, survey, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | directional, survey, metadata, container |
| `data.points` | array[dict] |  |  | Array of points records |  | directional, survey, container, array |
| `data.points[].severity` | str | low |  | Severity level of the alert/issue |  | directional, survey, wellness, alert, severity |
| `data.points[].timestamp` | int | 1545199574 |  | Timestamp |  | directional, survey |
| `data.points[].distance_to_plan` | int | 0 |  | Distance to plan |  | directional, survey |
| `data.status` | int | 0 |  | Current status of the record/check |  | directional, survey, metadata, status |
| `data.accuracy` | object |  |  | Nested object containing accuracy data |  | directional, survey, container, object |
| `data.accuracy.severity` | str | low |  | Severity level of the alert/issue |  | directional, survey, wellness, alert, severity |
| `data.accuracy.distance_to_plan` | float | 0.0003318786628541581 |  | Distance to plan |  | directional, survey |
| `data.plan_name` | str | WP AVP |  | Name/label for plan |  | directional, survey, metadata, display, label |
| `data.plan_point` | object |  |  | Nested object containing plan point data |  | directional, survey, container, object |
| `data.plan_point.tvd` | int | 7065 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.plan_point.azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.plan_point.easting` | int | 0 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.plan_point.northing` | int | 0 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.plan_point.inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.plan_point.measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.actual_name` | str |  |  | Name/label for actual |  | directional, survey, metadata, display, label |
| `data.actual_point` | object |  |  | Nested object containing actual point data |  | directional, survey, container, object |
| `data.actual_point.tvd` | int | 7065 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.actual_point.azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.actual_point.easting` | int | 0 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.actual_point.northing` | int | 0 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.actual_point.inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.actual_point.measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.actual_point.vertical_section` | int | 0 |  | Projected distance along planned azimuth (ft) |  | directional, survey, directional, survey, calculated |
| `data.recommendation` | object |  |  | Nested object containing recommendation data |  | directional, survey, container, object |
| `data.recommendation.high` | int | 0 |  | High |  | directional, survey |
| `data.recommendation.right` | int | 0 |  | Right |  | directional, survey |
| `data.vertical_plane` | object |  |  | Nested object containing vertical plane data |  | directional, survey, container, object |
| `data.vertical_plane.below` | float | -1438.33 |  | Below |  | directional, survey |
| `data.vertical_plane.right` | float | -8.41 |  | Right |  | directional, survey |
| `data.vertical_plane.distance` | float | 1438.36 |  | Distance |  | directional, survey |
| `data.vertical_plane.plan_point` | object |  |  | Nested object containing plan point data |  | directional, survey, container, object |
| `data.vertical_plane.plan_point.tvd` | float | 8503.33 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.vertical_plane.plan_point.azimuth` | float | 78.91 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.vertical_plane.plan_point.easting` | float | 1.62 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.vertical_plane.plan_point.northing` | float | -8.26 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.vertical_plane.plan_point.inclination` | float | 0.03 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.vertical_plane.plan_point.measured_depth` | float | 8503.4 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.vertical_plane.actual_point` | object |  |  | Nested object containing actual point data |  | directional, survey, container, object |
| `data.vertical_plane.actual_point.tvd` | int | 7065 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.vertical_plane.actual_point.azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.vertical_plane.actual_point.easting` | int | 0 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.vertical_plane.actual_point.northing` | int | 0 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.vertical_plane.actual_point.inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.vertical_plane.actual_point.measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.vertical_plane.actual_point.vertical_section` | int | 0 |  | Projected distance along planned azimuth (ft) |  | directional, survey, directional, survey, calculated |
| `data.vertical_plane.ahead_azimuth` | float | 78.91 |  | Ahead azimuth |  | directional, survey |
| `data.survey_measured_depth` | int | 7065 |  | Depth value: survey measured (ft) |  | directional, survey, depth, measurement |
| `data.minimum_distance_plane` | object |  |  | Nested object containing minimum distance plane data |  | directional, survey, container, object |
| `data.minimum_distance_plane.high` | int | 0 |  | High |  | directional, survey |
| `data.minimum_distance_plane.right` | int | 0 |  | Right |  | directional, survey |
| `data.minimum_distance_plane.distance` | int | 0 |  | Distance |  | directional, survey |
| `data.minimum_distance_plane.plan_point` | object |  |  | Nested object containing plan point data |  | directional, survey, container, object |
| `data.minimum_distance_plane.plan_point.tvd` | int | 7065 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.minimum_distance_plane.plan_point.azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.minimum_distance_plane.plan_point.easting` | int | 0 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.minimum_distance_plane.plan_point.northing` | int | 0 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.minimum_distance_plane.plan_point.inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.minimum_distance_plane.plan_point.measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.minimum_distance_plane.actual_point` | object |  |  | Nested object containing actual point data |  | directional, survey, container, object |
| `data.minimum_distance_plane.actual_point.tvd` | int | 7065 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.minimum_distance_plane.actual_point.azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.minimum_distance_plane.actual_point.easting` | int | 0 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.minimum_distance_plane.actual_point.northing` | int | 0 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.minimum_distance_plane.actual_point.inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.minimum_distance_plane.actual_point.measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.minimum_distance_plane.actual_point.vertical_section` | int | 0 |  | Projected distance along planned azimuth (ft) |  | directional, survey, directional, survey, calculated |
| `version` | int | 1 |  | Schema version number for this record |  | directional, survey, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | directional, survey, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | directional, survey, metadata, internal |
| `timestamp` | int | 1545199574 |  | Unix epoch timestamp (seconds) of the record |  | directional, survey, metadata, time-index, filter-key, required |
| `collection` | str | directional.accuracy |  | MongoDB collection name this record belongs to |  | directional, survey, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | directional, survey, metadata, company, filter-key |

#### `corva#directional.projection_to_bit`

- **Friendly Name**: directional.projection_to_bit
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/directional.projection_to_bit/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f63ace24b22b224dec4b |  | MongoDB document unique identifier |  | directional, survey, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | directional, survey, metadata, container |
| `data.error` | object |  |  | Nested object containing error data |  | directional, survey, container, object |
| `data.error.message` | str | Missing ['bend_angle', 'bit_to_bend'] in PDM in... |  | Message |  | directional, survey |
| `data.active_string_id` | str | 5f75f3796c88017f9358a5fe |  | Identifier for active string |  | directional, survey, metadata, identifier, reference |
| `data.active_string_type` | str | drillstring |  | Type of active string (drillstring, casing, etc.) |  | directional, survey, bha, classification |
| `data.drillstring_number` | int | 1 |  | Drillstring/BHA run number |  | directional, survey, bha, reference, run-number |
| `version` | int | 1 |  | Schema version number for this record |  | directional, survey, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | directional, survey, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | directional, survey, metadata, internal |
| `timestamp` | int | 1545199589 |  | Unix epoch timestamp (seconds) of the record |  | directional, survey, metadata, time-index, filter-key, required |
| `collection` | str | directional.projection_to_bit |  | MongoDB collection name this record belongs to |  | directional, survey, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | directional, survey, metadata, company, filter-key |

#### `corva#directional.rotational-tendency`

- **Friendly Name**: directional.rotational-tendency
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/directional.rotational-tendency/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760d497c6a265f2da0cea6 |  | MongoDB document unique identifier |  | directional, survey, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | directional, survey, metadata, container |
| `data.status` | int | 0 |  | Current status of the record/check |  | directional, survey, metadata, status |
| `data.start_depth` | int | 7065 |  | Starting measured depth for this interval/run |  | directional, survey, depth, interval, range |
| `data.rotational_tendency` | array[dict] |  |  | Array of rotational tendency records |  | directional, survey, container, array |
| `data.rotational_tendency[].dls` | float | 0.368 |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | directional, survey, directional, survey, calculated, key-metric |
| `data.rotational_tendency[].bit_rpm` | int | 0 |  | Bit rpm |  | directional, survey |
| `data.rotational_tendency[].gamma_ray` | int | 0 |  | Gamma ray measurement from MWD/LWD tool (API units) |  | directional, survey, drilling, mwd, formation, real-time |
| `data.rotational_tendency[].turn_rate` | int | 0 |  | Rate of azimuth change (deg/100ft) |  | directional, survey, directional, tendency, calculated |
| `data.rotational_tendency[].build_rate` | float | 0.368 |  | Rate of inclination change (deg/100ft) |  | directional, survey, directional, tendency, calculated |
| `data.rotational_tendency[].rotary_rpm` | float | 60.7 |  | Surface rotary speed (RPM) |  | directional, survey, drilling, rpm, real-time, key-metric |
| `data.rotational_tendency[].rotary_torque` | float | 0.06 |  | Rotary torque |  | directional, survey |
| `data.rotational_tendency[].weight_on_bit` | float | 22.7 |  | Weight applied to the drill bit (klbs) |  | directional, survey, drilling, wob, real-time, key-metric |
| `data.rotational_tendency[].downhole_torque` | float | 0.01 |  | Downhole torque |  | directional, survey |
| `data.rotational_tendency[].to_measured_depth` | int | 7413 |  | Depth value: to measured (ft) |  | directional, survey, depth, measurement |
| `data.rotational_tendency[].from_measured_depth` | int | 7065 |  | Depth value: from measured (ft) |  | directional, survey, depth, measurement |
| `data.rotational_tendency[].to_vertical_section` | float | 2.18 |  | To vertical section |  | directional, survey |
| `data.rotational_tendency[].from_vertical_section` | int | 0 |  | From vertical section |  | directional, survey |
| `data.rotational_tendency[].downhole_weight_on_bit` | int | 0 |  | Downhole weight on bit |  | directional, survey |
| `data.continuous_build_rate` | array[unknown] |  |  | Rate: continuous build |  | directional, survey, rate, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | directional, survey, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | directional, survey, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | directional, survey, metadata, internal |
| `timestamp` | int | 1545618451 |  | Unix epoch timestamp (seconds) of the record |  | directional, survey, metadata, time-index, filter-key, required |
| `collection` | str | directional.rotational-tendency |  | MongoDB collection name this record belongs to |  | directional, survey, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | directional, survey, metadata, company, filter-key |

#### `corva#directional.surveys`

- **Friendly Name**: directional.surveys
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/directional.surveys/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224debf7 |  | MongoDB document unique identifier |  | directional, survey, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | directional, survey, metadata, container |
| `data.plan` | array[dict] |  |  | Array of plan records |  | directional, survey, container, array |
| `data.plan[].dls` | int | 0 |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | directional, survey, directional, survey, calculated, key-metric |
| `data.plan[].tvd` | int | 0 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.plan[].azimuth` | int | 0 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.plan[].easting` | int | 0 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.plan[].northing` | int | 0 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.plan[].inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.plan[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.plan[].vertical_section` | int | 0 |  | Projected distance along planned azimuth (ft) |  | directional, survey, directional, survey, calculated |
| `data.actual` | array[dict] |  |  | Array of actual records |  | directional, survey, container, array |
| `data.actual[].dls` | int | 0 |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | directional, survey, directional, survey, calculated, key-metric |
| `data.actual[].tvd` | int | 7065 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.actual[].azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.actual[].easting` | int | 0 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.actual[].northing` | int | 0 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.actual[].inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.actual[].measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.actual[].vertical_section` | int | 0 |  | Projected distance along planned azimuth (ft) |  | directional, survey, directional, survey, calculated |
| `data.status` | int | 0 |  | Current status of the record/check |  | directional, survey, metadata, status |
| `data.plan_name` | str | WP AVP |  | Name/label for plan |  | directional, survey, metadata, display, label |
| `data.actual_name` | str |  |  | Name/label for actual |  | directional, survey, metadata, display, label |
| `version` | int | 1 |  | Schema version number for this record |  | directional, survey, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | directional, survey, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | directional, survey, metadata, internal |
| `timestamp` | int | 1545199574 |  | Unix epoch timestamp (seconds) of the record |  | directional, survey, metadata, time-index, filter-key, required |
| `collection` | str | directional.surveys |  | MongoDB collection name this record belongs to |  | directional, survey, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | directional, survey, metadata, company, filter-key |

#### `corva#directional.tortuosity`

- **Friendly Name**: directional.tortuosity
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/directional.tortuosity/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f63b3d168654756bc7cc |  | MongoDB document unique identifier |  | directional, survey, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | directional, survey, metadata, container |
| `data.stations` | array[dict] |  |  | Array of stations records |  | directional, survey, container, array |
| `data.stations[].ti` | int | 0 |  | Ti |  | directional, survey |
| `data.stations[].dls` | int | 0 |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | directional, survey, directional, survey, calculated, key-metric |
| `data.stations[].tvd` | int | 7065 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.stations[].azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.stations[].easting` | int | 0 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.stations[].northing` | int | 0 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.stations[].inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.stations[].is_inflection` | bool | True |  | Flag indicating whether is inflection |  | directional, survey, boolean, flag |
| `data.stations[].alpha_adjusted` | int | 0 |  | Alpha adjusted |  | directional, survey |
| `data.stations[].measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.stations[].normalized_dls` | int | 0 |  | Normalized dls |  | directional, survey |
| `data.stations[].tortuosity_index` | int | 0 |  | Tortuosity index |  | directional, survey |
| `data.stations[].vertical_section` | int | 0 |  | Projected distance along planned azimuth (ft) |  | directional, survey, directional, survey, calculated |
| `data.stations[].unwanted_curvature` | int | 0 |  | Unwanted curvature |  | directional, survey |
| `data.stations[].absolute_tortuosity` | int | 0 |  | Absolute tortuosity |  | directional, survey |
| `data.stations[].cumulative_curvature` | int | 0 |  | Cumulative curvature |  | directional, survey |
| `data.stations[].cumulative_alpha_adjusted` | int | 0 |  | Cumulative alpha adjusted |  | directional, survey |
| `data.stations[].cumulative_normalized_dls` | int | 0 |  | Cumulative normalized dls |  | directional, survey |
| `data.stations[].cumulative_tortuosity_index` | int | 0 |  | Cumulative tortuosity index |  | directional, survey |
| `data.last_station` | object |  |  | Nested object containing last station data |  | directional, survey, container, object |
| `data.last_station.ti` | float | 1.3533e-06 |  | Ti |  | directional, survey |
| `data.last_station.dls` | float | 0.2214 |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | directional, survey, directional, survey, calculated, key-metric |
| `data.last_station.tvd` | float | 28401.8647 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.last_station.azimuth` | float | 101.15 |  | Wellbore azimuth direction (degrees from north) |  | directional, survey, directional, survey, key-metric |
| `data.last_station.easting` | float | 7523.2675 |  | East-west position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.last_station.northing` | float | -2599.9018 |  | North-south position relative to surface location (ft) |  | directional, survey, directional, survey, coordinate |
| `data.last_station.inclination` | float | 26.22 |  | Wellbore inclination angle from vertical (degrees) |  | directional, survey, directional, survey, key-metric |
| `data.last_station.is_inflection` | bool | True |  | Flag indicating whether is inflection |  | directional, survey, boolean, flag |
| `data.last_station.alpha_adjusted` | float | 26.503 |  | Alpha adjusted |  | directional, survey |
| `data.last_station.measured_depth` | int | 30198 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.last_station.normalized_dls` | float | 0.486 |  | Normalized dls |  | directional, survey |
| `data.last_station.tortuosity_index` | float | 0.3827 |  | Tortuosity index |  | directional, survey |
| `data.last_station.vertical_section` | float | 7959.8342 |  | Projected distance along planned azimuth (ft) |  | directional, survey, directional, survey, calculated |
| `data.last_station.unwanted_curvature` | float | 22.3845 |  | Unwanted curvature |  | directional, survey |
| `data.last_station.absolute_tortuosity` | float | 0.1177 |  | Absolute tortuosity |  | directional, survey |
| `data.last_station.cumulative_curvature` | float | 80.8747 |  | Cumulative curvature |  | directional, survey |
| `data.last_station.cumulative_alpha_adjusted` | float | 3555.645 |  | Cumulative alpha adjusted |  | directional, survey |
| `data.last_station.cumulative_normalized_dls` | float | 135.0004 |  | Cumulative normalized dls |  | directional, survey |
| `data.last_station.cumulative_tortuosity_index` | float | 25.9709 |  | Cumulative tortuosity index |  | directional, survey |
| `version` | int | 1 |  | Schema version number for this record |  | directional, survey, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | directional, survey, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | directional, survey, metadata, internal |
| `timestamp` | int | 1545199619 |  | Unix epoch timestamp (seconds) of the record |  | directional, survey, metadata, time-index, filter-key, required |
| `collection` | str | directional.tortuosity |  | MongoDB collection name this record belongs to |  | directional, survey, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | directional, survey, metadata, company, filter-key |

#### `corva#directional.trend`

- **Friendly Name**: directional.trend
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/directional.trend/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224debf6 |  | MongoDB document unique identifier |  | directional, survey, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | directional, survey, metadata, container |
| `data.dls` | array[unknown] |  |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | directional, survey, directional, survey, calculated, key-metric |
| `data.tfo` | array[unknown] |  |  | Array of tfo records |  | directional, survey, container, array |
| `data.status` | int | 0 |  | Current status of the record/check |  | directional, survey, metadata, status |
| `data.last_dls` | object |  |  | Nested object containing last dls data |  | directional, survey, container, object |
| `data.last_dls.measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.tvd_plan` | array[dict] |  |  | Array of tvd plan records |  | directional, survey, container, array |
| `data.tvd_plan[].tvd` | int | 0 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.tvd_plan[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.plan_name` | str | WP AVP |  | Name/label for plan |  | directional, survey, metadata, display, label |
| `data.tvd_actual` | array[dict] |  |  | Array of tvd actual records |  | directional, survey, container, array |
| `data.tvd_actual[].tvd` | int | 7065 |  | True vertical depth from surface |  | directional, survey, depth, survey, directional, calculated |
| `data.tvd_actual[].measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | directional, survey, depth, survey, directional |
| `data.actual_name` | str |  |  | Name/label for actual |  | directional, survey, metadata, display, label |
| `data.motor_yield` | array[dict] |  |  | Array of motor yield records |  | directional, survey, container, array |
| `data.motor_yield[].dls` | int | 0 |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | directional, survey, directional, survey, calculated, key-metric |
| `data.motor_yield[].length` | int | 7065 |  | Length of the component (ft) |  | directional, survey, bha, component, dimension |
| `data.motor_yield[].motor_yield` | int | 0 |  | Motor yield |  | directional, survey |
| `data.motor_yield[].slide_length` | int | 0 |  | Slide length |  | directional, survey |
| `data.motor_yield[].to_measured_depth` | int | 7065 |  | Depth value: to measured (ft) |  | directional, survey, depth, measurement |
| `data.motor_yield[].from_measured_depth` | int | 0 |  | Depth value: from measured (ft) |  | directional, survey, depth, measurement |
| `data.effective_toolface` | array[dict] |  |  | Array of effective toolface records |  | directional, survey, container, array |
| `data.effective_toolface[].to_measured_depth` | int | 7065 |  | Depth value: to measured (ft) |  | directional, survey, depth, measurement |
| `data.effective_toolface[].effective_toolface` | int | 0 |  | Effective toolface |  | directional, survey |
| `data.effective_toolface[].from_measured_depth` | int | 0 |  | Depth value: from measured (ft) |  | directional, survey, depth, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | directional, survey, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | directional, survey, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | directional, survey, metadata, internal |
| `timestamp` | int | 1545199574 |  | Unix epoch timestamp (seconds) of the record |  | directional, survey, metadata, time-index, filter-key, required |
| `collection` | str | directional.trend |  | MongoDB collection name this record belongs to |  | directional, survey, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | directional, survey, metadata, company, filter-key |

### 4. Torque & Drag

#### `corva#torque-and-drag.axial-load`

- **Friendly Name**: torque-and-drag.axial-load
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/torque-and-drag.axial-load/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f737e9681d11fe2ebe69 |  | MongoDB document unique identifier |  | torque-drag, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | torque-drag, modeling, metadata, container |
| `data.points` | array[dict] |  |  | Array of points records |  | torque-drag, modeling, container, array |
| `data.points[].axial_load` | float | 65.17 |  | Axial force along the drill string (klbs) |  | torque-drag, modeling, torque-drag, calculated, modeling |
| `data.points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | torque-drag, modeling, depth, survey, directional |
| `data.points[].helical_buckling_force` | float | -84.81 |  | Helical buckling force |  | torque-drag, modeling |
| `data.points[].sinusoidal_buckling_force` | float | -29.98 |  | Sinusoidal buckling force |  | torque-drag, modeling |
| `data.status` | int | 0 |  | Current status of the record/check |  | torque-drag, modeling, metadata, status |
| `data.activity` | str | Run in Hole |  | Activity code number |  | torque-drag, modeling, operations, activity, classification |
| `data.buckling` | str |  |  | Buckling state/load of drill string |  | torque-drag, modeling, torque-drag, calculated, risk |
| `data.hookload` | float | 250.19 |  | Weight hanging from the hook (klbs) |  | torque-drag, modeling, drilling, hookload, real-time, torque-drag |
| `data.pipe_stretch` | float | 0.01 |  | Pipe stretch |  | torque-drag, modeling |
| `data.buckling_ranges` | array[unknown] |  |  | Array of buckling ranges records |  | torque-drag, modeling, container, array |
| `version` | int | 1 |  | Schema version number for this record |  | torque-drag, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | torque-drag, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | torque-drag, modeling, metadata, internal |
| `timestamp` | int | 1545221116 |  | Unix epoch timestamp (seconds) of the record |  | torque-drag, modeling, metadata, time-index, filter-key, required |
| `collection` | str | torque-and-drag.axial-load |  | MongoDB collection name this record belongs to |  | torque-drag, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | torque-drag, modeling, metadata, company, filter-key |

#### `corva#torque-and-drag.downhole-transfer`

- **Friendly Name**: torque-and-drag.downhole-transfer
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/torque-and-drag.downhole-transfer/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224debfb |  | MongoDB document unique identifier |  | torque-drag, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | torque-drag, modeling, metadata, container |
| `data.latch` | dict | {} |  | Latch |  | torque-drag, modeling |
| `data.status` | int | 0 |  | Current status of the record/check |  | torque-drag, modeling, metadata, status |
| `data.surface` | object |  |  | Nested object containing surface data |  | torque-drag, modeling, container, object |
| `data.surface.hook_load` | float | 188.79 |  | Hook load |  | torque-drag, modeling |
| `data.activity` | str | In Slips |  | Activity code number |  | torque-drag, modeling, operations, activity, classification |
| `data.downhole` | dict | {} |  | Downhole |  | torque-drag, modeling |
| `data.bit_depth` | float | 20.84 |  | Current depth of the drill bit |  | torque-drag, modeling, depth, drilling, real-time, key-metric |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | torque-drag, modeling, depth, drilling, real-time, key-metric |
| `data.bit_depth_tvd` | float | 20.84 |  | True vertical depth of the drill bit |  | torque-drag, modeling, depth, drilling, tvd, calculated |
| `data.downhole_model` | dict | {} |  | Downhole model |  | torque-drag, modeling |
| `data.hole_depth_tvd` | int | 7065 |  | Hole depth tvd |  | torque-drag, modeling |
| `data.weight_on_bit_efficiency` | str | high |  | Weight on bit efficiency |  | torque-drag, modeling |
| `version` | int | 1 |  | Schema version number for this record |  | torque-drag, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | torque-drag, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | torque-drag, modeling, metadata, internal |
| `timestamp` | int | 1545199579 |  | Unix epoch timestamp (seconds) of the record |  | torque-drag, modeling, metadata, time-index, filter-key, required |
| `collection` | str | torque-and-drag.downhole-transfer |  | MongoDB collection name this record belongs to |  | torque-drag, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | torque-drag, modeling, metadata, company, filter-key |

#### `corva#torque-and-drag.friction-factor`

- **Friendly Name**: torque-and-drag.friction-factor
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/torque-and-drag.friction-factor/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f7146c88010502589960 |  | MongoDB document unique identifier |  | torque-drag, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | torque-drag, modeling, metadata, container |
| `data.status` | int | 0 |  | Current status of the record/check |  | torque-drag, modeling, metadata, status |
| `data.predicted` | object |  |  | Nested object containing predicted data |  | torque-drag, modeling, container, object |
| `data.predicted.casing` | float | 0.15 |  | Casing |  | torque-drag, modeling |
| `data.predicted.open_hole_pickup` | float | 0.25 |  | Open hole pickup |  | torque-drag, modeling |
| `data.predicted.open_hole_rotating` | float | 0.25 |  | Open hole rotating |  | torque-drag, modeling |
| `data.predicted.open_hole_slackoff` | float | 0.25 |  | Open hole slackoff |  | torque-drag, modeling |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | torque-drag, modeling, depth, drilling, real-time, key-metric |
| `data.usage_type` | str | override |  | Type classification for usage |  | torque-drag, modeling, metadata, classification |
| `data.casing_depth` | int | 7065 |  | Depth value: casing (ft) |  | torque-drag, modeling, depth, measurement |
| `data.current_usage` | object |  |  | Nested object containing current usage data |  | torque-drag, modeling, container, object |
| `data.current_usage.casing` | float | 0.15 |  | Casing |  | torque-drag, modeling |
| `data.current_usage.open_hole_pickup` | float | 0.25 |  | Open hole pickup |  | torque-drag, modeling |
| `data.current_usage.open_hole_rotating` | float | 0.25 |  | Open hole rotating |  | torque-drag, modeling |
| `data.current_usage.open_hole_slackoff` | float | 0.25 |  | Open hole slackoff |  | torque-drag, modeling |
| `version` | int | 1 |  | Schema version number for this record |  | torque-drag, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | torque-drag, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | torque-drag, modeling, metadata, internal |
| `timestamp` | int | 1545218568 |  | Unix epoch timestamp (seconds) of the record |  | torque-drag, modeling, metadata, time-index, filter-key, required |
| `collection` | str | torque-and-drag.friction-factor |  | MongoDB collection name this record belongs to |  | torque-drag, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | torque-drag, modeling, metadata, company, filter-key |

#### `corva#torque-and-drag.hookload-trend`

- **Friendly Name**: torque-and-drag.hookload-trend
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/torque-and-drag.hookload-trend/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224debef |  | MongoDB document unique identifier |  | torque-drag, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | torque-drag, modeling, metadata, container |
| `data.actual` | object |  |  | Nested object containing actual data |  | torque-drag, modeling, container, object |
| `data.actual.pick_up` | array[unknown] |  |  | Array of pick up records |  | torque-drag, modeling, container, array |
| `data.actual.ream_in` | array[unknown] |  |  | Array of ream in records |  | torque-drag, modeling, container, array |
| `data.actual.wash_up` | array[unknown] |  |  | Array of wash up records |  | torque-drag, modeling, container, array |
| `data.actual.ream_out` | array[unknown] |  |  | Array of ream out records |  | torque-drag, modeling, container, array |
| `data.actual.slack_off` | array[unknown] |  |  | Array of slack off records |  | torque-drag, modeling, container, array |
| `data.actual.wash_down` | array[unknown] |  |  | Array of wash down records |  | torque-drag, modeling, container, array |
| `data.actual.rotary_off_bottom` | array[unknown] |  |  | Array of rotary off bottom records |  | torque-drag, modeling, container, array |
| `data.config` | object |  |  | Nested object containing config data |  | torque-drag, modeling, container, object |
| `data.config.id` | int | 1 |  | Numeric identifier for this record/run |  | torque-drag, modeling, metadata, identifier |
| `data.config._id` | str | 5f75f3796c88017f9358a5fe |  | Configuration parameter:  id |  | torque-drag, modeling, configuration, settings |
| `data.config.type` | str | DrillString |  | Type classifier for this record |  | torque-drag, modeling, metadata, classification |
| `data.config.hole_size` | int | 30 |  | Configuration parameter: hole size |  | torque-drag, modeling, configuration, settings |
| `data.curves` | object |  |  | Nested object containing curves data |  | torque-drag, modeling, container, object |
| `data.curves.pick_up` | array[dict] |  |  | Array of pick up records |  | torque-drag, modeling, container, array |
| `data.curves.pick_up[].points` | array[dict] |  |  | Array of points records |  | torque-drag, modeling, container, array |
| `data.curves.pick_up[].points[].hookload` | int | 189 |  | Weight hanging from the hook (klbs) |  | torque-drag, modeling, drilling, hookload, real-time, torque-drag |
| `data.curves.pick_up[].points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | torque-drag, modeling, depth, survey, directional |
| `data.curves.pick_up[].casing_friction_factor` | float | 0.15 |  | Casing friction factor |  | torque-drag, modeling |
| `data.curves.pick_up[].openhole_friction_factor` | float | 0.1 |  | Openhole friction factor |  | torque-drag, modeling |
| `data.curves.slack_off` | array[dict] |  |  | Array of slack off records |  | torque-drag, modeling, container, array |
| `data.curves.slack_off[].points` | array[dict] |  |  | Array of points records |  | torque-drag, modeling, container, array |
| `data.curves.slack_off[].points[].hookload` | int | 189 |  | Weight hanging from the hook (klbs) |  | torque-drag, modeling, drilling, hookload, real-time, torque-drag |
| `data.curves.slack_off[].points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | torque-drag, modeling, depth, survey, directional |
| `data.curves.slack_off[].casing_friction_factor` | float | 0.15 |  | Casing friction factor |  | torque-drag, modeling |
| `data.curves.slack_off[].openhole_friction_factor` | float | 0.1 |  | Openhole friction factor |  | torque-drag, modeling |
| `data.curves.rotary_off_bottom` | array[dict] |  |  | Array of rotary off bottom records |  | torque-drag, modeling, container, array |
| `data.curves.rotary_off_bottom[].points` | array[dict] |  |  | Array of points records |  | torque-drag, modeling, container, array |
| `data.curves.rotary_off_bottom[].points[].torque` | int | 0 |  | Rotary torque at surface (ft-lbs) |  | torque-drag, modeling, drilling, torque, real-time, torque-drag |
| `data.curves.rotary_off_bottom[].points[].hookload` | int | 189 |  | Weight hanging from the hook (klbs) |  | torque-drag, modeling, drilling, hookload, real-time, torque-drag |
| `data.curves.rotary_off_bottom[].points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | torque-drag, modeling, depth, survey, directional |
| `data.curves.rotary_off_bottom[].flow_rate` | int | 0 |  | Rate: flow |  | torque-drag, modeling, rate, measurement |
| `data.curves.rotary_off_bottom[].casing_friction_factor` | int | 0 |  | Casing friction factor |  | torque-drag, modeling |
| `data.curves.rotary_off_bottom[].openhole_friction_factor` | int | 0 |  | Openhole friction factor |  | torque-drag, modeling |
| `data.status` | int | 0 |  | Current status of the record/check |  | torque-drag, modeling, metadata, status |
| `data.activity` | str | In Slips |  | Activity code number |  | torque-drag, modeling, operations, activity, classification |
| `data.outliers` | object |  |  | Nested object containing outliers data |  | torque-drag, modeling, container, object |
| `data.outliers.pick_up` | array[unknown] |  |  | Array of pick up records |  | torque-drag, modeling, container, array |
| `data.outliers.ream_in` | array[unknown] |  |  | Array of ream in records |  | torque-drag, modeling, container, array |
| `data.outliers.wash_up` | array[unknown] |  |  | Array of wash up records |  | torque-drag, modeling, container, array |
| `data.outliers.ream_out` | array[unknown] |  |  | Array of ream out records |  | torque-drag, modeling, container, array |
| `data.outliers.slack_off` | array[unknown] |  |  | Array of slack off records |  | torque-drag, modeling, container, array |
| `data.outliers.wash_down` | array[unknown] |  |  | Array of wash down records |  | torque-drag, modeling, container, array |
| `data.outliers.rotary_off_bottom` | array[unknown] |  |  | Array of rotary off bottom records |  | torque-drag, modeling, container, array |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | torque-drag, modeling, depth, drilling, real-time, key-metric |
| `data.is_extended` | bool | False |  | Flag indicating whether is extended |  | torque-drag, modeling, boolean, flag |
| `data.has_confidence` | bool | True |  | Flag indicating whether has confidence |  | torque-drag, modeling, boolean, flag |
| `data.activity_groups` | object |  |  | Nested object containing activity groups data |  | torque-drag, modeling, container, object |
| `data.activity_groups.end_timestamp` | int | 1545199574 |  | End timestamp of the interval/run (Unix epoch) |  | torque-drag, modeling, time, interval, range |
| `data.activity_groups.start_timestamp` | int | 1545199574 |  | Start timestamp of the interval/run (Unix epoch) |  | torque-drag, modeling, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | torque-drag, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | torque-drag, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | torque-drag, modeling, metadata, internal |
| `timestamp` | int | 1545199574 |  | Unix epoch timestamp (seconds) of the record |  | torque-drag, modeling, metadata, time-index, filter-key, required |
| `collection` | str | torque-and-drag.hookload-trend |  | MongoDB collection name this record belongs to |  | torque-drag, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | torque-drag, modeling, metadata, company, filter-key |

#### `corva#torque-and-drag.overview`

- **Friendly Name**: torque-and-drag.overview
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/torque-and-drag.overview/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760adc62fd2f164883e065 |  | MongoDB document unique identifier |  | torque-drag, modeling, metadata, internal, primary-key |
| `app` | str | corva |  | App |  | torque-drag, modeling |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | torque-drag, modeling, metadata, container |
| `data.drag` | object |  |  | Nested object containing drag data |  | torque-drag, modeling, container, object |
| `data.drag.value` | int | 0 |  | Value |  | torque-drag, modeling |
| `data.drag.points` | array[dict] |  |  | Array of points records |  | torque-drag, modeling, container, array |
| `data.drag.points[].value` | int | 0 |  | Value |  | torque-drag, modeling |
| `data.drag.points[].severity` | str | low |  | Severity level of the alert/issue |  | torque-drag, modeling, wellness, alert, severity |
| `data.drag.points[].timestamp` | int | 1545575820 |  | Timestamp |  | torque-drag, modeling |
| `data.drag.severity` | str | low |  | Severity level of the alert/issue |  | torque-drag, modeling, wellness, alert, severity |
| `data.status` | int | 0 |  | Current status of the record/check |  | torque-drag, modeling, metadata, status |
| `data.activity` | str | Rotary Drilling |  | Activity code number |  | torque-drag, modeling, operations, activity, classification |
| `data.weight_on_bit` | object |  |  | Weight applied to the drill bit (klbs) |  | torque-drag, modeling, drilling, wob, real-time, key-metric |
| `data.weight_on_bit.latch` | int | 0 |  | Latch |  | torque-drag, modeling |
| `data.weight_on_bit.model` | int | 0 |  | Model |  | torque-drag, modeling |
| `data.weight_on_bit.difference` | int | 0 |  | Difference |  | torque-drag, modeling |
| `data.weight_transfer` | str | high |  | Weight transfer |  | torque-drag, modeling |
| `version` | int | 1 |  | Schema version number for this record |  | torque-drag, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | torque-drag, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | torque-drag, modeling, metadata, internal |
| `timestamp` | int | 1545577031 |  | Unix epoch timestamp (seconds) of the record |  | torque-drag, modeling, metadata, time-index, filter-key, required |
| `collection` | str | torque-and-drag.overview |  | MongoDB collection name this record belongs to |  | torque-drag, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | torque-drag, modeling, metadata, company, filter-key |

#### `corva#torque-and-drag.stress`

- **Friendly Name**: torque-and-drag.stress
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/torque-and-drag.stress/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f737e9681d11fe2ebe68 |  | MongoDB document unique identifier |  | torque-drag, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | torque-drag, modeling, metadata, container |
| `data.points` | array[dict] |  |  | Array of points records |  | torque-drag, modeling, container, array |
| `data.points[].axial_stress` | float | 3295.7 |  | Axial stress |  | torque-drag, modeling |
| `data.points[].twist_stress` | int | 0 |  | Twist stress |  | torque-drag, modeling |
| `data.points[].yield_stress` | int | 135000 |  | Yield stress |  | torque-drag, modeling |
| `data.points[].bending_stress` | int | 0 |  | Bending stress |  | torque-drag, modeling |
| `data.points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | torque-drag, modeling, depth, survey, directional |
| `data.points[].von_mises_stress` | float | 3295.7 |  | Von mises stress |  | torque-drag, modeling |
| `data.points[].yield_stress_60_percent` | int | 81000 |  | Yield stress 60 percent |  | torque-drag, modeling |
| `data.points[].yield_stress_80_percent` | int | 108000 |  | Yield stress 80 percent |  | torque-drag, modeling |
| `data.status` | int | 0 |  | Current status of the record/check |  | torque-drag, modeling, metadata, status |
| `data.activity` | str | Run in Hole |  | Activity code number |  | torque-drag, modeling, operations, activity, classification |
| `data.stress_yield_ranges` | str |  |  | Stress yield ranges |  | torque-drag, modeling |
| `version` | int | 1 |  | Schema version number for this record |  | torque-drag, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | torque-drag, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | torque-drag, modeling, metadata, internal |
| `timestamp` | int | 1545221116 |  | Unix epoch timestamp (seconds) of the record |  | torque-drag, modeling, metadata, time-index, filter-key, required |
| `collection` | str | torque-and-drag.stress |  | MongoDB collection name this record belongs to |  | torque-drag, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | torque-drag, modeling, metadata, company, filter-key |

#### `corva#torque-and-drag.torque`

- **Friendly Name**: torque-and-drag.torque
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/torque-and-drag.torque/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f737e9681d11fe2ebe67 |  | MongoDB document unique identifier |  | torque-drag, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | torque-drag, modeling, metadata, container |
| `data.points` | array[dict] |  |  | Array of points records |  | torque-drag, modeling, container, array |
| `data.points[].torque` | int | 0 |  | Rotary torque at surface (ft-lbs) |  | torque-drag, modeling, drilling, torque, real-time, torque-drag |
| `data.points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | torque-drag, modeling, depth, survey, directional |
| `data.points[].torsional_yield` | float | 291.72 |  | Torsional yield |  | torque-drag, modeling |
| `data.status` | int | 0 |  | Current status of the record/check |  | torque-drag, modeling, metadata, status |
| `data.activity` | str | Run in Hole |  | Activity code number |  | torque-drag, modeling, operations, activity, classification |
| `data.torsional_yield` | str |  |  | Torsional yield |  | torque-drag, modeling |
| `data.torsional_yield_ranges` | array[unknown] |  |  | Array of torsional yield ranges records |  | torque-drag, modeling, container, array |
| `version` | int | 1 |  | Schema version number for this record |  | torque-drag, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | torque-drag, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | torque-drag, modeling, metadata, internal |
| `timestamp` | int | 1545221116 |  | Unix epoch timestamp (seconds) of the record |  | torque-drag, modeling, metadata, time-index, filter-key, required |
| `collection` | str | torque-and-drag.torque |  | MongoDB collection name this record belongs to |  | torque-drag, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | torque-drag, modeling, metadata, company, filter-key |

#### `corva#torque-and-drag.torque-trend`

- **Friendly Name**: torque-and-drag.torque-trend
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/torque-and-drag.torque-trend/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224debf0 |  | MongoDB document unique identifier |  | torque-drag, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | torque-drag, modeling, metadata, container |
| `data.actual` | object |  |  | Nested object containing actual data |  | torque-drag, modeling, container, object |
| `data.actual.ream_in` | array[unknown] |  |  | Array of ream in records |  | torque-drag, modeling, container, array |
| `data.actual.ream_out` | array[unknown] |  |  | Array of ream out records |  | torque-drag, modeling, container, array |
| `data.actual.rotary_off_bottom` | array[unknown] |  |  | Array of rotary off bottom records |  | torque-drag, modeling, container, array |
| `data.config` | object |  |  | Nested object containing config data |  | torque-drag, modeling, container, object |
| `data.config.id` | int | 1 |  | Numeric identifier for this record/run |  | torque-drag, modeling, metadata, identifier |
| `data.config._id` | str | 5f75f3796c88017f9358a5fe |  | Configuration parameter:  id |  | torque-drag, modeling, configuration, settings |
| `data.config.type` | str | DrillString |  | Type classifier for this record |  | torque-drag, modeling, metadata, classification |
| `data.config.hole_size` | int | 30 |  | Configuration parameter: hole size |  | torque-drag, modeling, configuration, settings |
| `data.curves` | object |  |  | Nested object containing curves data |  | torque-drag, modeling, container, object |
| `data.curves.rotary_off_bottom` | array[dict] |  |  | Array of rotary off bottom records |  | torque-drag, modeling, container, array |
| `data.curves.rotary_off_bottom[].points` | array[dict] |  |  | Array of points records |  | torque-drag, modeling, container, array |
| `data.curves.rotary_off_bottom[].points[].torque` | int | 0 |  | Rotary torque at surface (ft-lbs) |  | torque-drag, modeling, drilling, torque, real-time, torque-drag |
| `data.curves.rotary_off_bottom[].points[].hookload` | int | 189 |  | Weight hanging from the hook (klbs) |  | torque-drag, modeling, drilling, hookload, real-time, torque-drag |
| `data.curves.rotary_off_bottom[].points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | torque-drag, modeling, depth, survey, directional |
| `data.curves.rotary_off_bottom[].casing_friction_factor` | float | 0.15 |  | Casing friction factor |  | torque-drag, modeling |
| `data.curves.rotary_off_bottom[].openhole_friction_factor` | float | 0.1 |  | Openhole friction factor |  | torque-drag, modeling |
| `data.status` | int | 0 |  | Current status of the record/check |  | torque-drag, modeling, metadata, status |
| `data.activity` | str | In Slips |  | Activity code number |  | torque-drag, modeling, operations, activity, classification |
| `data.outliers` | object |  |  | Nested object containing outliers data |  | torque-drag, modeling, container, object |
| `data.outliers.ream_in` | array[unknown] |  |  | Array of ream in records |  | torque-drag, modeling, container, array |
| `data.outliers.ream_out` | array[unknown] |  |  | Array of ream out records |  | torque-drag, modeling, container, array |
| `data.outliers.rotary_off_bottom` | array[unknown] |  |  | Array of rotary off bottom records |  | torque-drag, modeling, container, array |
| `data.flow_rate` | int | 0 |  | Rate: flow |  | torque-drag, modeling, rate, measurement |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | torque-drag, modeling, depth, drilling, real-time, key-metric |
| `data.is_extended` | bool | False |  | Flag indicating whether is extended |  | torque-drag, modeling, boolean, flag |
| `data.has_confidence` | bool | True |  | Flag indicating whether has confidence |  | torque-drag, modeling, boolean, flag |
| `data.activity_groups` | object |  |  | Nested object containing activity groups data |  | torque-drag, modeling, container, object |
| `data.activity_groups.end_timestamp` | int | 1545199574 |  | End timestamp of the interval/run (Unix epoch) |  | torque-drag, modeling, time, interval, range |
| `data.activity_groups.start_timestamp` | int | 1545199574 |  | Start timestamp of the interval/run (Unix epoch) |  | torque-drag, modeling, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | torque-drag, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | torque-drag, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | torque-drag, modeling, metadata, internal |
| `timestamp` | int | 1545199574 |  | Unix epoch timestamp (seconds) of the record |  | torque-drag, modeling, metadata, time-index, filter-key, required |
| `collection` | str | torque-and-drag.torque-trend |  | MongoDB collection name this record belongs to |  | torque-drag, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | torque-drag, modeling, metadata, company, filter-key |

### 5. Hydraulics

#### `corva#hydraulics.cuttings-transport`

- **Friendly Name**: hydraulics.cuttings-transport
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/hydraulics.cuttings-transport/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760adc62fd2f164883e092 |  | MongoDB document unique identifier |  | hydraulics, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | hydraulics, modeling, metadata, container |
| `data.rop` | float | 24.8 |  | Rate of penetration - drilling speed (ft/hr) |  | hydraulics, modeling, drilling, rop, real-time, key-metric, performance |
| `data.status` | int | 0 |  | Current status of the record/check |  | hydraulics, modeling, metadata, status |
| `data.sections` | array[dict] |  |  | Array of sections records |  | hydraulics, modeling, container, array |
| `data.sections[].method` | str | vertical |  | Method |  | hydraulics, modeling |
| `data.sections[].fluid_velocity` | float | 3.5 |  | Fluid velocity |  | hydraulics, modeling |
| `data.sections[].measured_depth` | float | 6275.53 |  | Measured depth along the wellbore path |  | hydraulics, modeling, depth, survey, directional |
| `data.sections[].transport_ratio` | float | 0.991 |  | Transport ratio |  | hydraulics, modeling |
| `data.sections[].cuttings_velocity` | float | 3.5 |  | Cuttings velocity |  | hydraulics, modeling |
| `data.sections[].cuttings_concentration` | float | 8.2 |  | Volume fraction of cuttings in annulus (%) |  | hydraulics, modeling, hydraulics, cuttings, calculated |
| `data.sections[].cuttings_layer_thickness` | int | 0 |  | Cuttings layer thickness |  | hydraulics, modeling |
| `data.sections[].recommended_minimum_flowrate` | float | 230.1 |  | Recommended minimum flowrate |  | hydraulics, modeling |
| `data.bit_depth` | float | 7090.94 |  | Current depth of the drill bit |  | hydraulics, modeling, depth, drilling, real-time, key-metric |
| `data.hole_depth` | float | 7090.94 |  | Current hole depth (bottom of wellbore) |  | hydraulics, modeling, depth, drilling, real-time, key-metric |
| `data.mud_flow_in` | float | 140.5 |  | Mud flow in |  | hydraulics, modeling |
| `data.bit_depth_tvd` | float | 7090.94 |  | True vertical depth of the drill bit |  | hydraulics, modeling, depth, drilling, tvd, calculated |
| `data.hole_depth_tvd` | float | 7090.94 |  | Hole depth tvd |  | hydraulics, modeling |
| `data.pdm_flowrate_limits` | dict | {} |  | Pdm flowrate limits |  | hydraulics, modeling |
| `version` | int | 1 |  | Schema version number for this record |  | hydraulics, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | hydraulics, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | hydraulics, modeling, metadata, internal |
| `timestamp` | int | 1545577206 |  | Unix epoch timestamp (seconds) of the record |  | hydraulics, modeling, metadata, time-index, filter-key, required |
| `collection` | str | hydraulics.cuttings-transport |  | MongoDB collection name this record belongs to |  | hydraulics, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | hydraulics, modeling, metadata, company, filter-key |

#### `corva#hydraulics.overview`

- **Friendly Name**: hydraulics.overview
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/hydraulics.overview/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760adc62fd2f164883e093 |  | MongoDB document unique identifier |  | hydraulics, modeling, metadata, internal, primary-key |
| `app` | str | corva |  | App |  | hydraulics, modeling |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | hydraulics, modeling, metadata, container |
| `data.status` | int | 0 |  | Current status of the record/check |  | hydraulics, modeling, metadata, status |
| `data.bit_depth_tvd` | float | 7090.94 |  | True vertical depth of the drill bit |  | hydraulics, modeling, depth, drilling, tvd, calculated |
| `data.hole_cleaning` | object |  |  | Nested object containing hole cleaning data |  | hydraulics, modeling, container, object |
| `data.hole_cleaning.value` | int | 38 |  | Value |  | hydraulics, modeling |
| `data.hole_cleaning.points` | array[dict] |  |  | Array of points records |  | hydraulics, modeling, container, array |
| `data.hole_cleaning.points[].value` | int | 38 |  | Value |  | hydraulics, modeling |
| `data.hole_cleaning.points[].severity` | str | high |  | Severity level of the alert/issue |  | hydraulics, modeling, wellness, alert, severity |
| `data.hole_cleaning.points[].timestamp` | int | 1545577206 |  | Timestamp |  | hydraulics, modeling |
| `data.hole_cleaning.severity` | str | high |  | Severity level of the alert/issue |  | hydraulics, modeling, wellness, alert, severity |
| `data.hole_depth_tvd` | float | 7090.94 |  | Hole depth tvd |  | hydraulics, modeling |
| `data.pdm_flowrate_limits` | dict | {} |  | Pdm flowrate limits |  | hydraulics, modeling |
| `data.recommended_minimum_flowrate` | float | 230.2 |  | Recommended minimum flowrate |  | hydraulics, modeling |
| `version` | int | 1 |  | Schema version number for this record |  | hydraulics, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | hydraulics, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | hydraulics, modeling, metadata, internal |
| `timestamp` | int | 1545577206 |  | Unix epoch timestamp (seconds) of the record |  | hydraulics, modeling, metadata, time-index, filter-key, required |
| `collection` | str | hydraulics.overview |  | MongoDB collection name this record belongs to |  | hydraulics, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | hydraulics, modeling, metadata, company, filter-key |

#### `corva#hydraulics.pressure-loss`

- **Friendly Name**: hydraulics.pressure-loss
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/hydraulics.pressure-loss/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224dec05 |  | MongoDB document unique identifier |  | hydraulics, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | hydraulics, modeling, metadata, container |
| `data.rop` | int | 0 |  | Rate of penetration - drilling speed (ft/hr) |  | hydraulics, modeling, drilling, rop, real-time, key-metric, performance |
| `data.rpm` | int | 0 |  | Rpm |  | hydraulics, modeling |
| `data.ecds` | array[dict] |  |  | Array of ecds records |  | hydraulics, modeling, container, array |
| `data.ecds[].ecd` | float | 8.8 |  | Equivalent circulating density (ppg) |  | hydraulics, modeling, drilling, hydraulics, calculated, key-metric |
| `data.ecds[].type` | str | annulus_cased |  | Type classifier for this record |  | hydraulics, modeling, metadata, classification |
| `data.ecds[].measured_depth` | float | 20.84 |  | Measured depth along the wellbore path |  | hydraulics, modeling, depth, survey, directional |
| `data.alerts` | object |  |  | Nested object containing alerts data |  | hydraulics, modeling, container, object |
| `data.alerts.flow` | array[unknown] |  |  | Array of flow records |  | hydraulics, modeling, container, array |
| `data.alerts.loss` | array[unknown] |  |  | Array of loss records |  | hydraulics, modeling, container, array |
| `data.alerts.collapse` | array[unknown] |  |  | Array of collapse records |  | hydraulics, modeling, container, array |
| `data.alerts.fracture` | array[unknown] |  |  | Array of fracture records |  | hydraulics, modeling, container, array |
| `data.alerts.main_alert` | str | none |  | Main alert |  | hydraulics, modeling |
| `data.alerts.flow_length` | int | 0 |  | Flow length |  | hydraulics, modeling |
| `data.alerts.loss_length` | int | 0 |  | Loss length |  | hydraulics, modeling |
| `data.alerts.collapse_length` | int | 0 |  | Collapse length |  | hydraulics, modeling |
| `data.alerts.fracture_length` | int | 0 |  | Fracture length |  | hydraulics, modeling |
| `data.points` | array[dict] |  |  | Array of points records |  | hydraulics, modeling, container, array |
| `data.points[].top` | int | 0 |  | Top |  | hydraulics, modeling |
| `data.points[].type` | str | surface_tools |  | Type classifier for this record |  | hydraulics, modeling, metadata, classification |
| `data.points[].bottom` | int | 0 |  | Bottom |  | hydraulics, modeling |
| `data.points[].flow_regime` | str | laminar |  | Flow regime |  | hydraulics, modeling |
| `data.points[].pressure_loss` | int | 0 |  | Pressure drop across a component or section (psi) |  | hydraulics, modeling, hydraulics, calculated, pressure |
| `data.points[].fluid_velocity` | int | 0 |  | Fluid velocity |  | hydraulics, modeling |
| `data.points[].reynolds_number` | int | 0 |  | Reynolds number |  | hydraulics, modeling |
| `data.points[].total_pressure_top` | int | 0 |  | Total pressure top |  | hydraulics, modeling |
| `data.points[].dynamic_pressure_top` | int | 0 |  | Dynamic pressure top |  | hydraulics, modeling |
| `data.points[].total_pressure_bottom` | int | 0 |  | Total pressure bottom |  | hydraulics, modeling |
| `data.points[].dynamic_pressure_bottom` | int | 0 |  | Dynamic pressure bottom |  | hydraulics, modeling |
| `data.status` | int | 0 |  | Current status of the record/check |  | hydraulics, modeling, metadata, status |
| `data.activity` | str | In Slips |  | Activity code number |  | hydraulics, modeling, operations, activity, classification |
| `data.flowrate` | int | 0 |  | Flowrate |  | hydraulics, modeling |
| `data.bit_depth` | float | 20.84 |  | Current depth of the drill bit |  | hydraulics, modeling, depth, drilling, real-time, key-metric |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | hydraulics, modeling, depth, drilling, real-time, key-metric |
| `data.mud_density` | float | 8.8 |  | Mud density |  | hydraulics, modeling |
| `data.percentages` | array[dict] |  |  | Array of percentages records |  | hydraulics, modeling, container, array |
| `data.percentages[].type` | str | surface_tools |  | Type classifier for this record |  | hydraulics, modeling, metadata, classification |
| `data.percentages[].pressure_loss` | int | 0 |  | Pressure drop across a component or section (psi) |  | hydraulics, modeling, hydraulics, calculated, pressure |
| `data.casing_depth` | int | 7065 |  | Depth value: casing (ft) |  | hydraulics, modeling, depth, measurement |
| `data.bit_depth_tvd` | float | 20.84 |  | True vertical depth of the drill bit |  | hydraulics, modeling, depth, drilling, tvd, calculated |
| `data.hole_depth_tvd` | int | 7065 |  | Hole depth tvd |  | hydraulics, modeling |
| `data.standpipe_pressure` | float | 80.5 |  | Standpipe pressure - pump pressure at surface (psi) |  | hydraulics, modeling, drilling, spp, pressure, real-time, key-metric |
| `data.predicted_ecd_at_bit` | float | 8.8 |  | Predicted ecd at bit |  | hydraulics, modeling |
| `data.predicted_ecd_at_casing` | float | 8.8 |  | Predicted ecd at casing |  | hydraulics, modeling |
| `data.predicted_standpipe_pressure` | int | 0 |  | Pressure: predicted standpipe (psi) |  | hydraulics, modeling, pressure, measurement |
| `data.predicted_annulus_pressure_loss` | int | 0 |  | Predicted annulus pressure loss |  | hydraulics, modeling |
| `data.predicted_annulus_total_pressure_at_bit` | float | 9.5 |  | Predicted annulus total pressure at bit |  | hydraulics, modeling |
| `version` | int | 1 |  | Schema version number for this record |  | hydraulics, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | hydraulics, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | hydraulics, modeling, metadata, internal |
| `timestamp` | int | 1545199629 |  | Unix epoch timestamp (seconds) of the record |  | hydraulics, modeling, metadata, time-index, filter-key, required |
| `collection` | str | hydraulics.pressure-loss |  | MongoDB collection name this record belongs to |  | hydraulics, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | hydraulics, modeling, metadata, company, filter-key |

#### `corva#hydraulics.pressure-trend`

- **Friendly Name**: hydraulics.pressure-trend
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/hydraulics.pressure-trend/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760d6f14483c400ef8e806 |  | MongoDB document unique identifier |  | hydraulics, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | hydraulics, modeling, metadata, container |
| `data.ecd` | array[dict] |  |  | Equivalent circulating density (ppg) |  | hydraulics, modeling, drilling, hydraulics, calculated, key-metric |
| `data.ecd[].ecd` | float | 9.103 |  | Equivalent circulating density (ppg) |  | hydraulics, modeling, drilling, hydraulics, calculated, key-metric |
| `data.ecd[].measured_depth` | float | 7072.82 |  | Measured depth along the wellbore path |  | hydraulics, modeling, depth, survey, directional |
| `data.status` | int | 0 |  | Current status of the record/check |  | hydraulics, modeling, metadata, status |
| `data.mud_weight` | array[dict] |  |  | Mud weight/density (ppg) |  | hydraulics, modeling, mud, property, key-metric |
| `data.mud_weight[].mud_weight` | float | 12.5 |  | Mud weight/density (ppg) |  | hydraulics, modeling, mud, property, key-metric |
| `data.mud_weight[].measured_depth` | int | 7377 |  | Measured depth along the wellbore path |  | hydraulics, modeling, depth, survey, directional |
| `data.mud_flow_in` | array[dict] |  |  | Array of mud flow in records |  | hydraulics, modeling, container, array |
| `data.mud_flow_in[].mud_flow_in` | float | 77.131 |  | Mud flow in |  | hydraulics, modeling |
| `data.mud_flow_in[].measured_depth` | float | 7072.82 |  | Measured depth along the wellbore path |  | hydraulics, modeling, depth, survey, directional |
| `data.mwd_annulus_ecd` | array[unknown] |  |  | Array of mwd annulus ecd records |  | hydraulics, modeling, container, array |
| `data.standpipe_pressure` | array[dict] |  |  | Standpipe pressure - pump pressure at surface (psi) |  | hydraulics, modeling, drilling, spp, pressure, real-time, key-metric |
| `data.standpipe_pressure[].measured_depth` | float | 7072.82 |  | Measured depth along the wellbore path |  | hydraulics, modeling, depth, survey, directional |
| `data.standpipe_pressure[].standpipe_pressure` | float | 64.08 |  | Standpipe pressure - pump pressure at surface (psi) |  | hydraulics, modeling, drilling, spp, pressure, real-time, key-metric |
| `data.mwd_annulus_pressure` | array[unknown] |  |  | Pressure: mwd annulus (psi) |  | hydraulics, modeling, pressure, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | hydraulics, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | hydraulics, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | hydraulics, modeling, metadata, internal |
| `timestamp` | int | 1545621414 |  | Unix epoch timestamp (seconds) of the record |  | hydraulics, modeling, metadata, time-index, filter-key, required |
| `collection` | str | hydraulics.pressure-trend |  | MongoDB collection name this record belongs to |  | hydraulics, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | hydraulics, modeling, metadata, company, filter-key |

#### `corva#hydraulics.surge-and-swab`

- **Friendly Name**: hydraulics.surge-and-swab
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/hydraulics.surge-and-swab/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224debee |  | MongoDB document unique identifier |  | hydraulics, modeling, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | hydraulics, modeling, metadata, container |
| `data.actual` | object |  |  | Nested object containing actual data |  | hydraulics, modeling, container, object |
| `data.actual.pick_up` | array[unknown] |  |  | Array of pick up records |  | hydraulics, modeling, container, array |
| `data.actual.ream_in` | array[unknown] |  |  | Array of ream in records |  | hydraulics, modeling, container, array |
| `data.actual.wash_up` | array[unknown] |  |  | Array of wash up records |  | hydraulics, modeling, container, array |
| `data.actual.ream_out` | array[unknown] |  |  | Array of ream out records |  | hydraulics, modeling, container, array |
| `data.actual.slack_off` | array[unknown] |  |  | Array of slack off records |  | hydraulics, modeling, container, array |
| `data.actual.wash_down` | array[unknown] |  |  | Array of wash down records |  | hydraulics, modeling, container, array |
| `data.curves` | object |  |  | Nested object containing curves data |  | hydraulics, modeling, container, object |
| `data.curves.swab` | array[dict] |  |  | Array of swab records |  | hydraulics, modeling, container, array |
| `data.curves.swab[].type` | str | swab |  | Type classifier for this record |  | hydraulics, modeling, metadata, classification |
| `data.curves.swab[].points` | array[dict] |  |  | Array of points records |  | hydraulics, modeling, container, array |
| `data.curves.swab[].points[].ecd` | float | 8.69 |  | Equivalent circulating density (ppg) |  | hydraulics, modeling, drilling, hydraulics, calculated, key-metric |
| `data.curves.swab[].points[].measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | hydraulics, modeling, depth, survey, directional |
| `data.curves.swab[].end_type` | str | open_ended |  | Type classification for end |  | hydraulics, modeling, metadata, classification |
| `data.curves.swab[].string_velocity` | int | 50 |  | String velocity |  | hydraulics, modeling |
| `data.curves.surge` | array[dict] |  |  | Array of surge records |  | hydraulics, modeling, container, array |
| `data.curves.surge[].type` | str | surge |  | Type classifier for this record |  | hydraulics, modeling, metadata, classification |
| `data.curves.surge[].points` | array[dict] |  |  | Array of points records |  | hydraulics, modeling, container, array |
| `data.curves.surge[].points[].ecd` | float | 8.91 |  | Equivalent circulating density (ppg) |  | hydraulics, modeling, drilling, hydraulics, calculated, key-metric |
| `data.curves.surge[].points[].measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | hydraulics, modeling, depth, survey, directional |
| `data.curves.surge[].end_type` | str | close_ended |  | Type classification for end |  | hydraulics, modeling, metadata, classification |
| `data.curves.surge[].string_velocity` | int | 50 |  | String velocity |  | hydraulics, modeling |
| `data.status` | int | 0 |  | Current status of the record/check |  | hydraulics, modeling, metadata, status |
| `data.bit_depth` | float | 20.84 |  | Current depth of the drill bit |  | hydraulics, modeling, depth, drilling, real-time, key-metric |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | hydraulics, modeling, depth, drilling, real-time, key-metric |
| `data.mud_density` | float | 8.8 |  | Mud density |  | hydraulics, modeling |
| `version` | int | 1 |  | Schema version number for this record |  | hydraulics, modeling, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | hydraulics, modeling, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | hydraulics, modeling, metadata, internal |
| `timestamp` | int | 1545199574 |  | Unix epoch timestamp (seconds) of the record |  | hydraulics, modeling, metadata, time-index, filter-key, required |
| `collection` | str | hydraulics.surge-and-swab |  | MongoDB collection name this record belongs to |  | hydraulics, modeling, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | hydraulics, modeling, metadata, company, filter-key |

### 6. PDM / Motor

#### `corva#pdm.operating-condition`

- **Friendly Name**: pdm.operating-condition
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/pdm.operating-condition/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224dec09 |  | MongoDB document unique identifier |  | pdm, motor, downhole, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | pdm, motor, downhole, metadata, container |
| `data.rpm` | int | 0 |  | Rpm |  | pdm, motor, downhole |
| `data.stall` | str | low |  | Motor stall detected |  | pdm, motor, downhole, pdm, stall, boolean, alert |
| `data.limits` | object |  |  | Nested object containing limits data |  | pdm, motor, downhole, container, object |
| `data.limits.max_rpm` | int | 135 |  | Max rpm |  | pdm, motor, downhole |
| `data.limits.min_rpm` | float | 57.15 |  | Min rpm |  | pdm, motor, downhole |
| `data.limits.max_standard_flowrate` | int | 1500 |  | Max standard flowrate |  | pdm, motor, downhole |
| `data.limits.min_standard_flowrate` | int | 635 |  | Min standard flowrate |  | pdm, motor, downhole |
| `data.limits.max_differential_pressure` | int | 1150 |  | Pressure: max differential (psi) |  | pdm, motor, downhole, pressure, measurement |
| `data.limits.transitional_differential_pressure_limit` | int | 1035 |  | Transitional differential pressure limit |  | pdm, motor, downhole |
| `data.status` | int | 0 |  | Current status of the record/check |  | pdm, motor, downhole, metadata, status |
| `data.torque` | int | 0 |  | Rotary torque at surface (ft-lbs) |  | pdm, motor, downhole, drilling, torque, real-time, torque-drag |
| `data.bit_depth` | float | 20.84 |  | Current depth of the drill bit |  | pdm, motor, downhole, depth, drilling, real-time, key-metric |
| `data.flow_rate` | int | 0 |  | Rate: flow |  | pdm, motor, downhole, rate, measurement |
| `data.pdm_power` | int | 0 |  | Pdm power |  | pdm, motor, downhole |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | pdm, motor, downhole, depth, drilling, real-time, key-metric |
| `data.torque_line` | array[dict] |  |  | Array of torque line records |  | pdm, motor, downhole, container, array |
| `data.torque_line[].torque` | int | 0 |  | Rotary torque at surface (ft-lbs) |  | pdm, motor, downhole, drilling, torque, real-time, torque-drag |
| `data.torque_line[].differential_pressure` | int | 0 |  | Differential pressure across downhole motor (psi) |  | pdm, motor, downhole, drilling, pressure, pdm, real-time |
| `data.bit_depth_tvd` | float | 20.84 |  | True vertical depth of the drill bit |  | pdm, motor, downhole, depth, drilling, tvd, calculated |
| `data.total_bit_rpm` | int | 0 |  | Total bit rpm |  | pdm, motor, downhole |
| `data.hole_depth_tvd` | int | 7065 |  | Hole depth tvd |  | pdm, motor, downhole |
| `data.flow_rate_lines` | array[unknown] |  |  | Array of flow rate lines records |  | pdm, motor, downhole, container, array |
| `data.total_bit_torque` | int | 0 |  | Total bit torque |  | pdm, motor, downhole |
| `data.differential_pressure` | int | 0 |  | Differential pressure across downhole motor (psi) |  | pdm, motor, downhole, drilling, pressure, pdm, real-time |
| `version` | int | 1 |  | Schema version number for this record |  | pdm, motor, downhole, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | pdm, motor, downhole, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | pdm, motor, downhole, metadata, internal |
| `timestamp` | int | 1545199629 |  | Unix epoch timestamp (seconds) of the record |  | pdm, motor, downhole, metadata, time-index, filter-key, required |
| `collection` | str | pdm.operating-condition |  | MongoDB collection name this record belongs to |  | pdm, motor, downhole, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | pdm, motor, downhole, metadata, company, filter-key |

#### `corva#pdm.overview`

- **Friendly Name**: pdm.overview
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/pdm.overview/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f637ce24b22b224dec08 |  | MongoDB document unique identifier |  | pdm, motor, downhole, metadata, internal, primary-key |
| `app` | str | corva |  | App |  | pdm, motor, downhole |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | pdm, motor, downhole, metadata, container |
| `data.status` | int | 0 |  | Current status of the record/check |  | pdm, motor, downhole, metadata, status |
| `data.differential_pressure` | object |  |  | Differential pressure across downhole motor (psi) |  | pdm, motor, downhole, drilling, pressure, pdm, real-time |
| `data.differential_pressure.value` | int | 0 |  | Value |  | pdm, motor, downhole |
| `data.differential_pressure.points` | array[dict] |  |  | Array of points records |  | pdm, motor, downhole, container, array |
| `data.differential_pressure.points[].value` | int | 0 |  | Value |  | pdm, motor, downhole |
| `data.differential_pressure.points[].severity` | str | low |  | Severity level of the alert/issue |  | pdm, motor, downhole, wellness, alert, severity |
| `data.differential_pressure.points[].timestamp` | int | 1545199629 |  | Timestamp |  | pdm, motor, downhole |
| `data.differential_pressure.points[].percentage` | int | 0 |  | Percentage |  | pdm, motor, downhole |
| `data.differential_pressure.severity` | str | low |  | Severity level of the alert/issue |  | pdm, motor, downhole, wellness, alert, severity |
| `data.differential_pressure.percentage` | int | 0 |  | Percentage |  | pdm, motor, downhole |
| `version` | int | 1 |  | Schema version number for this record |  | pdm, motor, downhole, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | pdm, motor, downhole, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | pdm, motor, downhole, metadata, internal |
| `timestamp` | int | 1545199629 |  | Unix epoch timestamp (seconds) of the record |  | pdm, motor, downhole, metadata, time-index, filter-key, required |
| `collection` | str | pdm.overview |  | MongoDB collection name this record belongs to |  | pdm, motor, downhole, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | pdm, motor, downhole, metadata, company, filter-key |

#### `corva#pdm.stall-detection`

- **Friendly Name**: pdm.stall-detection
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/pdm.stall-detection/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f7712de62fd2f466c8362da |  | MongoDB document unique identifier |  | pdm, motor, downhole, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | pdm, motor, downhole, metadata, container |
| `data.status` | int | 1 |  | Current status of the record/check |  | pdm, motor, downhole, metadata, status |
| `data.warning` | object |  |  | Nested object containing warning data |  | pdm, motor, downhole, container, object |
| `data.warning.code` | str | not_available_during_running_casing |  | Code |  | pdm, motor, downhole |
| `data.warning.stale` | bool | True |  | Flag indicating whether stale |  | pdm, motor, downhole, boolean, flag |
| `data.warning.message` | str | The current status is running casing/liner, at ... |  | Message |  | pdm, motor, downhole |
| `version` | int | 1 |  | Schema version number for this record |  | pdm, motor, downhole, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | pdm, motor, downhole, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | pdm, motor, downhole, metadata, internal |
| `timestamp` | int | 1548180245 |  | Unix epoch timestamp (seconds) of the record |  | pdm, motor, downhole, metadata, time-index, filter-key, required |
| `collection` | str | pdm.stall-detection |  | MongoDB collection name this record belongs to |  | pdm, motor, downhole, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | pdm, motor, downhole, metadata, company, filter-key |

### 7. Circulation

#### `corva#circulation.lag-depth`

- **Friendly Name**: circulation.lag-depth
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/circulation.lag-depth/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f760c2498fd15638925124a |  | MongoDB document unique identifier |  | circulation, hydraulics, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | circulation, hydraulics, metadata, container |
| `data.bit_depth` | float | 7343.12 |  | Current depth of the drill bit |  | circulation, hydraulics, depth, drilling, real-time, key-metric |
| `data.lag_depth` | float | 7079.94 |  | Depth value: lag (ft) |  | circulation, hydraulics, depth, measurement |
| `data.timestamp` | int | 1545598715 |  | Timestamp |  | circulation, hydraulics |
| `data.hole_depth` | float | 7343.12 |  | Current hole depth (bottom of wellbore) |  | circulation, hydraulics, depth, drilling, real-time, key-metric |
| `data.mud_flow_in` | float | 1254.96 |  | Mud flow in |  | circulation, hydraulics |
| `data.time_passed` | int | 23326 |  | Time passed |  | circulation, hydraulics |
| `data.pump_spm_total` | int | 100 |  | Pump spm total |  | circulation, hydraulics |
| `data.bit_to_surface_strokes` | int | 23202 |  | Bit to surface strokes |  | circulation, hydraulics |
| `version` | int | 1 |  | Schema version number for this record |  | circulation, hydraulics, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | circulation, hydraulics, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | circulation, hydraulics, metadata, internal |
| `timestamp` | int | 1545598715 |  | Unix epoch timestamp (seconds) of the record |  | circulation, hydraulics, metadata, time-index, filter-key, required |
| `collection` | str | circulation.lag-depth |  | MongoDB collection name this record belongs to |  | circulation, hydraulics, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | circulation, hydraulics, metadata, company, filter-key |

#### `corva#circulation.volumetric`

- **Friendly Name**: circulation.volumetric
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/circulation.volumetric/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f66c16a4233fd4e3fcde |  | MongoDB document unique identifier |  | circulation, hydraulics, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | circulation, hydraulics, metadata, container |
| `data.status` | int | 1 |  | Current status of the record/check |  | circulation, hydraulics, metadata, status |
| `data.warning` | object |  |  | Nested object containing warning data |  | circulation, hydraulics, container, object |
| `data.warning.code` | str | data_missing_error |  | Code |  | circulation, hydraulics |
| `data.warning.stale` | bool | True |  | Flag indicating whether stale |  | circulation, hydraulics, boolean, flag |
| `data.warning.message` | str | The data appears to have the following missing ... |  | Message |  | circulation, hydraulics |
| `version` | int | 1 |  | Schema version number for this record |  | circulation, hydraulics, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | circulation, hydraulics, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | circulation, hydraulics, metadata, internal |
| `timestamp` | int | 1545203779 |  | Unix epoch timestamp (seconds) of the record |  | circulation, hydraulics, metadata, time-index, filter-key, required |
| `collection` | str | circulation.volumetric |  | MongoDB collection name this record belongs to |  | circulation, hydraulics, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | circulation, hydraulics, metadata, company, filter-key |

### 8. Activities / Operations

#### `corva#activities.summary-2tours`

- **Friendly Name**: activities.summary-2tours
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/activities.summary-2tours/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 62067e095562de56f22116c0 |  | MongoDB document unique identifier |  | operations, activity, rig-state, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | operations, activity, rig-state, metadata, container |
| `data.activities` | array[dict] |  |  | Array of activities records |  | operations, activity, rig-state, container, array |
| `data.activities[].day` | int | 43200 |  | Duration during day shift (seconds) |  | operations, activity, rig-state, operations, time, shift |
| `data.activities[].name` | str | Static Off Bottom |  | Display name of the component or record |  | operations, activity, rig-state, metadata, display |
| `data.activities[].night` | int | 33264 |  | Duration during night shift (seconds) |  | operations, activity, rig-state, operations, time, shift |
| `data.end_timestamp` | int | 1644580800 |  | End timestamp of the interval/run (Unix epoch) |  | operations, activity, rig-state, time, interval, range |
| `data.start_timestamp` | int | 1644494400 |  | Start timestamp of the interval/run (Unix epoch) |  | operations, activity, rig-state, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | operations, activity, rig-state, metadata, internal, versioning |
| `asset_id` | int | 123456 |  | Unique identifier for the well/asset this record belongs to |  | operations, activity, rig-state, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | operations, activity, rig-state, metadata, internal |
| `timestamp` | int | 1644580800 |  | Unix epoch timestamp (seconds) of the record |  | operations, activity, rig-state, metadata, time-index, filter-key, required |
| `collection` | str | activities.summary-2tours |  | MongoDB collection name this record belongs to |  | operations, activity, rig-state, metadata, internal |
| `company_id` | int | 3 |  | Unique identifier for the company/operator |  | operations, activity, rig-state, metadata, company, filter-key |

#### `corva#activities.summary-3m`

- **Friendly Name**: activities.summary-3m
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/activities.summary-3m/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 62067e095562de56f22116c0 |  | MongoDB document unique identifier |  | operations, activity, rig-state, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | operations, activity, rig-state, metadata, container |
| `data.activities` | array[dict] |  |  | Array of activities records |  | operations, activity, rig-state, container, array |
| `data.activities[].day` | int | 43200 |  | Duration during day shift (seconds) |  | operations, activity, rig-state, operations, time, shift |
| `data.activities[].name` | str | Static Off Bottom |  | Display name of the component or record |  | operations, activity, rig-state, metadata, display |
| `data.activities[].night` | int | 33264 |  | Duration during night shift (seconds) |  | operations, activity, rig-state, operations, time, shift |
| `data.end_timestamp` | int | 1644580800 |  | End timestamp of the interval/run (Unix epoch) |  | operations, activity, rig-state, time, interval, range |
| `data.start_timestamp` | int | 1644494400 |  | Start timestamp of the interval/run (Unix epoch) |  | operations, activity, rig-state, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | operations, activity, rig-state, metadata, internal, versioning |
| `asset_id` | int | 123456 |  | Unique identifier for the well/asset this record belongs to |  | operations, activity, rig-state, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | operations, activity, rig-state, metadata, internal |
| `timestamp` | int | 1644580800 |  | Unix epoch timestamp (seconds) of the record |  | operations, activity, rig-state, metadata, time-index, filter-key, required |
| `collection` | str | activities.summary-3m |  | MongoDB collection name this record belongs to |  | operations, activity, rig-state, metadata, internal |
| `company_id` | int | 3 |  | Unique identifier for the company/operator |  | operations, activity, rig-state, metadata, company, filter-key |

#### `corva#activities.summary-continuous`

- **Friendly Name**: activities.summary-continuous
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/activities.summary-continuous/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3d53d168654756ba8ef |  | MongoDB document unique identifier |  | operations, activity, rig-state, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | operations, activity, rig-state, metadata, container |
| `data.activities` | array[dict] |  |  | Array of activities records |  | operations, activity, rig-state, container, array |
| `data.activities[].day` | int | 42169 |  | Duration during day shift (seconds) |  | operations, activity, rig-state, operations, time, shift |
| `data.activities[].name` | str | In Slips |  | Display name of the component or record |  | operations, activity, rig-state, metadata, display |
| `data.activities[].night` | int | 43200 |  | Duration during night shift (seconds) |  | operations, activity, rig-state, operations, time, shift |
| `data.end_timestamp` | int | 1545155400 |  | End timestamp of the interval/run (Unix epoch) |  | operations, activity, rig-state, time, interval, range |
| `data.start_timestamp` | int | 1545069000 |  | Start timestamp of the interval/run (Unix epoch) |  | operations, activity, rig-state, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | operations, activity, rig-state, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | operations, activity, rig-state, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | operations, activity, rig-state, metadata, internal |
| `timestamp` | int | 1545155400 |  | Unix epoch timestamp (seconds) of the record |  | operations, activity, rig-state, metadata, time-index, filter-key, required |
| `collection` | str | activities.summary-continuous |  | MongoDB collection name this record belongs to |  | operations, activity, rig-state, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | operations, activity, rig-state, metadata, company, filter-key |

#### `corva#activity-groups`

- **Friendly Name**: activity-groups
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/activity-groups/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f8de98fd15520124e1c3 |  | MongoDB document unique identifier |  | operations, activity, rig-state, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | operations, activity, rig-state, metadata, container |
| `data.activity` | int | 1 |  | Activity code number |  | operations, activity, rig-state, operations, activity, classification |
| `data.end_time` | int | 1545262752 |  | End time of the activity/operation (Unix epoch) |  | operations, activity, rig-state, operations, time, interval |
| `data.start_time` | int | 1545249823 |  | Start time of the activity/operation (Unix epoch) |  | operations, activity, rig-state, operations, time, interval |
| `data.activity_name` | str | Tripping in |  | Name of the rig activity (e.g., Drilling, Tripping) |  | operations, activity, rig-state, operations, activity, classification |
| `data.end_bit_depth` | float | 6472.6 |  | Bit depth at end of operation (ft) |  | operations, activity, rig-state, operations, depth, interval |
| `data.end_hole_depth` | int | 7065 |  | Hole depth at end of operation (ft) |  | operations, activity, rig-state, operations, depth, interval |
| `data.operation_time` | int | 12929 |  | Duration of the operation (seconds) |  | operations, activity, rig-state, operations, time, duration |
| `data.start_bit_depth` | int | 1240 |  | Bit depth at start of operation (ft) |  | operations, activity, rig-state, operations, depth, interval |
| `data.bit_depth_change` | null |  |  | Change in bit depth during operation (ft) |  | operations, activity, rig-state, operations, depth, calculated |
| `data.start_hole_depth` | int | 7065 |  | Hole depth at start of operation (ft) |  | operations, activity, rig-state, operations, depth, interval |
| `data.hole_depth_change` | null |  |  | Change in hole depth during operation (ft) |  | operations, activity, rig-state, operations, depth, calculated |
| `version` | int | 1 |  | Schema version number for this record |  | operations, activity, rig-state, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | operations, activity, rig-state, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | operations, activity, rig-state, metadata, internal |
| `timestamp` | int | 1545262752 |  | Unix epoch timestamp (seconds) of the record |  | operations, activity, rig-state, metadata, time-index, filter-key, required |
| `collection` | str | activity-groups |  | MongoDB collection name this record belongs to |  | operations, activity, rig-state, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | operations, activity, rig-state, metadata, company, filter-key |

#### `corva#operations`

- **Friendly Name**: operations
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/operations/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | string |  | MongoDB document unique identifier |  | operations, activity, rig-state, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | operations, activity, rig-state, metadata, container |
| `data.cased` | str | boolean |  | Cased |  | operations, activity, rig-state |
| `data.liner` | str | boolean |  | Liner |  | operations, activity, rig-state |
| `data.shift` | str | string |  | Shift |  | operations, activity, rig-state |
| `data.bha_id` | str | integer or float |  | BHA/drillstring run number identifier |  | operations, activity, rig-state, bha, reference, link |
| `data.casing_id` | str | integer |  | Casing inner diameter (in) |  | operations, activity, rig-state, casing, dimension |
| `data.end_depth` | str | float |  | Ending measured depth for this interval/run |  | operations, activity, rig-state, depth, interval, range |
| `data.hole_size` | str | float |  | Hole size |  | operations, activity, rig-state |
| `data.operation` | str | string |  | Operation |  | operations, activity, rig-state |
| `data.activities` | array[dict] |  |  | Array of activities records |  | operations, activity, rig-state, container, array |
| `data.activities[].operation` | str | string |  | Operation |  | operations, activity, rig-state |
| `data.activities[].activity_name` | str | string |  | Name of the rig activity (e.g., Drilling, Tripping) |  | operations, activity, rig-state, operations, activity, classification |
| `data.activities[].operation_time` | str | integer |  | Duration of the operation (seconds) |  | operations, activity, rig-state, operations, time, duration |
| `data.performance` | object |  |  | Nested object containing performance data |  | operations, activity, rig-state, container, object |
| `data.performance.slide_rop` | str | float |  | Slide rop |  | operations, activity, rig-state |
| `data.performance.total_rop` | str | float |  | Total rop |  | operations, activity, rig-state |
| `data.performance.rotary_rop` | str | float |  | Rotary rop |  | operations, activity, rig-state |
| `data.performance.tripping_speed` | str | float |  | Tripping speed |  | operations, activity, rig-state |
| `data.performance.slide_percentage` | str | float |  | Slide percentage |  | operations, activity, rig-state |
| `data.performance.rotary_percentage` | str | float |  | Rotary percentage |  | operations, activity, rig-state |
| `data.performance.rotary_depth_chage` | str | float |  | Rotary depth chage |  | operations, activity, rig-state |
| `data.performance.slide_depth_change` | str | float |  | Slide depth change |  | operations, activity, rig-state |
| `data.start_depth` | str | float |  | Starting measured depth for this interval/run |  | operations, activity, rig-state, depth, interval, range |
| `data.depth_change` | str | float |  | Depth change |  | operations, activity, rig-state |
| `data.well_section` | str | string |  | Well section |  | operations, activity, rig-state |
| `data.end_bit_depth` | str | float |  | Bit depth at end of operation (ft) |  | operations, activity, rig-state, operations, depth, interval |
| `data.end_timestamp` | str | integer |  | End timestamp of the interval/run (Unix epoch) |  | operations, activity, rig-state, time, interval, range |
| `data.landing_string` | str | string |  | Landing string |  | operations, activity, rig-state |
| `data.operation_name` | str | string |  | Name/label for operation |  | operations, activity, rig-state, metadata, display, label |
| `data.operation_time` | str | integer |  | Duration of the operation (seconds) |  | operations, activity, rig-state, operations, time, duration |
| `data.start_bit_depth` | str | float |  | Bit depth at start of operation (ft) |  | operations, activity, rig-state, operations, depth, interval |
| `data.start_timestamp` | str | integer |  | Start timestamp of the interval/run (Unix epoch) |  | operations, activity, rig-state, time, interval, range |
| `data.bit_depth_change` | str | float |  | Change in bit depth during operation (ft) |  | operations, activity, rig-state, operations, depth, calculated |
| `version` | str | integer |  | Schema version number for this record |  | operations, activity, rig-state, metadata, internal, versioning |
| `asset_id` | str | integer |  | Unique identifier for the well/asset this record belongs to |  | operations, activity, rig-state, metadata, well-id, filter-key, required |
| `provider` | str | string |  | Data provider name (typically "corva") |  | operations, activity, rig-state, metadata, internal |
| `timestamp` | str | integer |  | Unix epoch timestamp (seconds) of the record |  | operations, activity, rig-state, metadata, time-index, filter-key, required |
| `collection` | str | string |  | MongoDB collection name this record belongs to |  | operations, activity, rig-state, metadata, internal |
| `company_id` | str | integer |  | Unique identifier for the company/operator |  | operations, activity, rig-state, metadata, company, filter-key |

### 9. Well Data (data.*)

#### `corva#data.actual_survey`

- **Friendly Name**: data.actual_survey
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.actual_survey/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3796c88017f9358a663 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.stations` | array[dict] |  |  | Array of stations records |  | well-data, reference, container, array |
| `data.stations[].dls` | int | 0 |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | well-data, reference, directional, survey, calculated, key-metric |
| `data.stations[].tvd` | int | 7065 |  | True vertical depth from surface |  | well-data, reference, depth, survey, directional, calculated |
| `data.stations[].azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | well-data, reference, directional, survey, key-metric |
| `data.stations[].easting` | int | 0 |  | East-west position relative to surface location (ft) |  | well-data, reference, directional, survey, coordinate |
| `data.stations[].northing` | int | 0 |  | North-south position relative to surface location (ft) |  | well-data, reference, directional, survey, coordinate |
| `data.stations[].inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | well-data, reference, directional, survey, key-metric |
| `data.stations[].measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | well-data, reference, depth, survey, directional |
| `data.stations[].vertical_section` | int | 0 |  | Projected distance along planned azimuth (ft) |  | well-data, reference, directional, survey, calculated |
| `data.has_tie_in` | bool | True |  | Flag indicating whether has tie in |  | well-data, reference, boolean, flag |
| `data.target_changes` | array[unknown] |  |  | Array of target changes records |  | well-data, reference, container, array |
| `data.tie_in_station` | object |  |  | Nested object containing tie in station data |  | well-data, reference, container, object |
| `data.tie_in_station.tvd` | int | 7065 |  | True vertical depth from surface |  | well-data, reference, depth, survey, directional, calculated |
| `data.tie_in_station.azimuth` | float | 165.06 |  | Wellbore azimuth direction (degrees from north) |  | well-data, reference, directional, survey, key-metric |
| `data.tie_in_station.easting` | int | 0 |  | East-west position relative to surface location (ft) |  | well-data, reference, directional, survey, coordinate |
| `data.tie_in_station.northing` | int | 0 |  | North-south position relative to surface location (ft) |  | well-data, reference, directional, survey, coordinate |
| `data.tie_in_station.inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | well-data, reference, directional, survey, key-metric |
| `data.tie_in_station.measured_depth` | int | 7065 |  | Measured depth along the wellbore path |  | well-data, reference, depth, survey, directional |
| `data.has_target_change` | bool | False |  | Flag indicating whether has target change |  | well-data, reference, boolean, flag |
| `data.vertical_section_azimuth` | float | 109.13 |  | Vertical section azimuth |  | well-data, reference |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1585152180 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.actual_survey |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 56 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.afe`

- **Friendly Name**: data.afe
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.afe/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e99cff3398f8f4eb76c84c5 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.cost` | int | 3000000 |  | Cost |  | well-data, reference |
| `data.days` | int | 10 |  | Days |  | well-data, reference |
| `data.depth` | int | 1 |  | Depth |  | well-data, reference |
| `_pre_id` | int | 1587138535778 |  | Identifier for  pre |  | well-data, reference, metadata, identifier, reference |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1587138547 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.afe |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.casing`

- **Friendly Name**: data.casing
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.casing/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3796c88017f9358a67b |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.grade` | str | X80Q |  | Steel grade of the component (e.g., S135, P110) |  | well-data, reference, bha, component, material |
| `data.length` | int | 3548 |  | Length of the component (ft) |  | well-data, reference, bha, component, dimension |
| `data.end_depth` | int | 10600 |  | Ending measured depth for this interval/run |  | well-data, reference, depth, interval, range |
| `data.top_depth` | int | 7052 |  | Top depth of casing string (ft MD) |  | well-data, reference, casing, depth, range |
| `data.components` | array[unknown] |  |  | Array of components records |  | well-data, reference, container, array |
| `data.start_depth` | int | 10600 |  | Starting measured depth for this interval/run |  | well-data, reference, depth, interval, range |
| `data.bottom_depth` | int | 10600 |  | Bottom depth of casing string (ft MD) |  | well-data, reference, casing, depth, range |
| `data.end_timestamp` | int | 1546151613 |  | End timestamp of the interval/run (Unix epoch) |  | well-data, reference, time, interval, range |
| `data.is_exact_time` | bool | True |  | Whether the timestamp is exact (vs estimated) |  | well-data, reference, metadata, time, quality, boolean |
| `data.linear_weight` | float | 453.04 |  | Weight per unit length (lbs/ft or ppf) |  | well-data, reference, bha, component, dimension |
| `data.inner_diameter` | float | 19.19 |  | Inner diameter of the component (in) |  | well-data, reference, bha, component, dimension, hydraulics |
| `data.outer_diameter` | int | 23 |  | Outer diameter of the component (in) |  | well-data, reference, bha, component, dimension |
| `data.start_timestamp` | int | 1545816600 |  | Start timestamp of the interval/run (Unix epoch) |  | well-data, reference, time, interval, range |
| `data.setting_timestamp` | int | 1545817079 |  | Timestamp when the drillstring was set/configured |  | well-data, reference, bha, time, configuration |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1584994984 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.casing |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 56 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.crews`

- **Friendly Name**: data.crews
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.crews/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 6022b8cbed61c00065af70f1 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.crews` | array[dict] |  |  | Array of crews records |  | well-data, reference, container, array |
| `data.crews[].id` | str | 2edcaa30-6af4-11eb-987d-910d9bb6c3fa |  | Numeric identifier for this record/run |  | well-data, reference, metadata, identifier |
| `data.crews[].name` | str | Crew A |  | Display name of the component or record |  | well-data, reference, metadata, display |
| `data.rotations` | array[dict] |  |  | Array of rotations records |  | well-data, reference, container, array |
| `data.rotations[].id` | str | 411b6150-6af4-11eb-987d-910d9bb6c3fa |  | Numeric identifier for this record/run |  | well-data, reference, metadata, identifier |
| `data.rotations[].order` | int | 0 |  | Position order of component in the BHA (0 = top) |  | well-data, reference, bha, component, ordering |
| `data.rotations[].shift` | str | day |  | Shift |  | well-data, reference |
| `data.rotations[].crew_id` | str | 2edcaa30-6af4-11eb-987d-910d9bb6c3fa |  | Identifier for crew |  | well-data, reference, metadata, identifier, reference |
| `data.rotations[].end_date` | int | 1547099999 |  | End date |  | well-data, reference |
| `data.rotations[].start_date` | int | 1544594400 |  | Start date |  | well-data, reference |
| `data.rotation_days` | int | 28 |  | Rotation days |  | well-data, reference |
| `data.day_shift_start` | int | 21600 |  | Day shift start |  | well-data, reference |
| `data.night_shift_start` | int | 64800 |  | Night shift start |  | well-data, reference |
| `data.is_third_shift_enabled` | bool | False |  | Flag indicating whether is third shift enabled |  | well-data, reference, boolean, flag |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1612888267 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.crews |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.diaries`

- **Friendly Name**: data.diaries
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.diaries/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 615d822a30c9341b3e63b934 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.summary` | str | Spud information updated by automatic spud chec... |  | Summary |  | well-data, reference |
| `data.date_time` | int | 1633518122 |  | Timestamp for date |  | well-data, reference, metadata, time |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1633518122 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.diaries |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.drillstring`

- **Friendly Name**: data.drillstring
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.drillstring/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 601c679bf37f1f1f5139dd71 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.id` | int | 1 |  | Numeric identifier for this record/run |  | well-data, reference, metadata, identifier |
| `data.end_depth` | float | 1021.65 |  | Ending measured depth for this interval/run |  | well-data, reference, depth, interval, range |
| `data.calibrated` | bool | True |  | Whether the drillstring has been calibrated for T&D |  | well-data, reference, bha, torque-drag, calibration, boolean |
| `data.components` | array[dict] |  |  | Array of components records |  | well-data, reference, container, array |
| `data.components[].id` | str | ba6fdde0-a235-11e8-b181-59931cd96497 |  | Numeric identifier for this record/run |  | well-data, reference, metadata, identifier |
| `data.components[].name` | str | 5''DP(4.5" IF) |  | Display name of the component or record |  | well-data, reference, metadata, display |
| `data.components[].class` | str | Premium |  | Classification/condition of the component (e.g., Premium, Class 2) |  | well-data, reference, bha, component, condition |
| `data.components[].grade` | str | S135 |  | Steel grade of the component (e.g., S135, P110) |  | well-data, reference, bha, component, material |
| `data.components[].order` | int | 0 |  | Position order of component in the BHA (0 = top) |  | well-data, reference, bha, component, ordering |
| `data.components[].family` | str | dp |  | Component type family (dp, hwdp, dc, bit, mwd, pdm, etc.) |  | well-data, reference, bha, component, classification |
| `data.components[].length` | int | 31 |  | Length of the component (ft) |  | well-data, reference, bha, component, dimension |
| `data.components[].weight` | float | 747.41 |  | Total weight of the component (lbs) |  | well-data, reference, bha, component, dimension |
| `data.components[].expanded` | bool | True |  | Whether UI component is expanded (display state) |  | well-data, reference, ui, display, boolean |
| `data.components[].material` | str | Steel |  | Material type (e.g., Steel, Non-Magnetic) |  | well-data, reference, bha, component, material |
| `data.components[].linear_weight` | float | 24.11 |  | Weight per unit length (lbs/ft or ppf) |  | well-data, reference, bha, component, dimension |
| `data.components[].inner_diameter` | float | 4.276 |  | Inner diameter of the component (in) |  | well-data, reference, bha, component, dimension, hydraulics |
| `data.components[].outer_diameter` | int | 5 |  | Outer diameter of the component (in) |  | well-data, reference, bha, component, dimension |
| `data.components[].connection_type` | str | 4.5" IF |  | Thread connection type (e.g., 4.5" IF, NC50) |  | well-data, reference, bha, component, connection |
| `data.components[].component_length` | int | 31 |  | Length of the component (ft) |  | well-data, reference, bha, component, dimension |
| `data.components[].length_tooljoint` | float | 1.75 |  | Length of the tool joint (ft) |  | well-data, reference, bha, component, tooljoint |
| `data.components[].inner_diameter_tooljoint` | float | 3.25 |  | ID of the tool joint (in) |  | well-data, reference, bha, component, tooljoint |
| `data.components[].outer_diameter_tooljoint` | float | 6.625 |  | OD of the tool joint (in) |  | well-data, reference, bha, component, tooljoint |
| `data.components[].gamma_sensor_to_bit_distance` | null |  |  | Distance from gamma sensor to bit (ft) |  | well-data, reference, bha, mwd, offset |
| `data.start_depth` | int | 472 |  | Starting measured depth for this interval/run |  | well-data, reference, depth, interval, range |
| `data.calibrated_by` | int | 3388 |  | User ID who calibrated the drillstring |  | well-data, reference, bha, torque-drag, calibration, metadata |
| `data.calibrated_on` | int | 1596693378 |  | Timestamp when drillstring was calibrated |  | well-data, reference, bha, torque-drag, calibration, metadata |
| `data.end_timestamp` | int | 1596699496 |  | End timestamp of the interval/run (Unix epoch) |  | well-data, reference, time, interval, range |
| `data.is_exact_time` | bool | True |  | Whether the timestamp is exact (vs estimated) |  | well-data, reference, metadata, time, quality, boolean |
| `data.start_timestamp` | int | 1596668460 |  | Start timestamp of the interval/run (Unix epoch) |  | well-data, reference, time, interval, range |
| `data.setting_timestamp` | int | 1596668926 |  | Timestamp when the drillstring was set/configured |  | well-data, reference, bha, time, configuration |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 20902927 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1596230718 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.drillstring |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 41 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.files`

- **Friendly Name**: data.files
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.files/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3796c88017f9358a665 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.pid` | str | 5b125500-6d2f-11ea-b9ec-874abd779d92 |  | Pid |  | well-data, reference |
| `data.file_name` | str | demo/1601565563/Run_1_Drill_Out_Spacout.xlsx |  | Original filename of the uploaded file |  | well-data, reference, metadata, file |
| `data.display_name` | str | Run_1_Drill_Out_Spacout.xlsx |  | Name/label for display |  | well-data, reference, metadata, display, label |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1584986152 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.files |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 56 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.formations`

- **Friendly Name**: data.formations
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.formations/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3796c88017f9358a67f |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.md` | float | 8436.07 |  | Md |  | well-data, reference |
| `data.td` | int | 8436 |  | Td |  | well-data, reference |
| `data.lithology` | str |  |  | Lithology |  | well-data, reference |
| `data.formation_name` | str | Top of Salt |  | Name/label for formation |  | well-data, reference, metadata, display, label |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1551361310 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.formations |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.lessons-learned`

- **Friendly Name**: data.lessons-learned
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.lessons-learned/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str |  |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.cause` | str | Third Party |  | Cause |  | well-data, reference |
| `data.phase` | str | Drilling |  | Phase |  | well-data, reference |
| `data.topic` | str | Well Control |  | Topic |  | well-data, reference |
| `data.md_end` | float | 7691.47 |  | Md end |  | well-data, reference |
| `data.section` | str | Intermediate |  | Section |  | well-data, reference |
| `data.tvd_end` | float | 7691.2104 |  | Tvd end |  | well-data, reference |
| `data.activity` | str | Operating |  | Activity code number |  | well-data, reference, operations, activity, classification |
| `data.end_time` | int | 1631181600 |  | End time of the activity/operation (Unix epoch) |  | well-data, reference, operations, time, interval |
| `data.md_start` | float | 7440.912 |  | Md start |  | well-data, reference |
| `data.severity` | str | Minor |  | Severity level of the alert/issue |  | well-data, reference, wellness, alert, severity |
| `data.tvd_start` | float | 7440.6684 |  | Tvd start |  | well-data, reference |
| `data.start_time` | int | 1631156400 |  | Start time of the activity/operation (Unix epoch) |  | well-data, reference, operations, time, interval |
| `data.description` | str |  |  | Description |  | well-data, reference |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 56196474 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1635276722 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.lessons-learned |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 1 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.mud`

- **Friendly Name**: data.mud
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.mud/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 64e8dca460b012716082b15a |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.ph` | int | 1 |  | pH of the mud system |  | well-data, reference, mud, property, chemistry |
| `data.tvd` | int | 100 |  | True vertical depth from surface |  | well-data, reference, depth, survey, directional, calculated |
| `data.date` | int | 1692982336 |  | Date |  | well-data, reference |
| `data.depth` | int | 100 |  | Depth |  | well-data, reference |
| `data.tau_0` | int | 1 |  | Tau 0 |  | well-data, reference |
| `data.ph_temp` | int | 1 |  | Ph temp |  | well-data, reference |
| `data.date_str` | null |  |  | Date str |  | well-data, reference |
| `data.hardness` | object |  |  | Nested object containing hardness data |  | well-data, reference, container, object |
| `data.hardness.ca` | int | 1 |  | Ca |  | well-data, reference |
| `data.hardness.total` | int | 1 |  | Total |  | well-data, reference |
| `data.mud_type` | str | Water-base |  | Type classification for mud |  | well-data, reference, metadata, classification |
| `data.salinity` | object |  |  | Nested object containing salinity data |  | well-data, reference, container, object |
| `data.salinity.chlorides` | int | 1 |  | Chloride content in mud (ppm) |  | well-data, reference, mud, property, chemistry |
| `data.salinity.sodium_chloride` | int | 1 |  | Sodium chloride |  | well-data, reference |
| `data.salinity.calcium_chloride` | int | 1 |  | Calcium chloride |  | well-data, reference |
| `data.salinity.water_phase_salinity` | int | 1 |  | Water phase salinity |  | well-data, reference |
| `data.viscosity` | object |  |  | Nested object containing viscosity data |  | well-data, reference, container, object |
| `data.viscosity.pv` | int | 1 |  | Pv |  | well-data, reference |
| `data.viscosity.yp` | int | 1 |  | Yp |  | well-data, reference |
| `data.viscosity.funnel` | object |  |  | Nested object containing funnel data |  | well-data, reference, container, object |
| `data.viscosity.funnel.measurement` | int | 1 |  | Measurement |  | well-data, reference |
| `data.viscosity.funnel.temperature` | int | 98 |  | Temperature |  | well-data, reference |
| `data.viscosity.gel_strength` | object |  |  | Nested object containing gel strength data |  | well-data, reference, container, object |
| `data.viscosity.gel_strength.10_min` | int | 1 |  | 10 min |  | well-data, reference |
| `data.viscosity.gel_strength.10_sec` | int | 1 |  | 10 sec |  | well-data, reference |
| `data.viscosity.gel_strength.30_min` | int | 1 |  | 30 min |  | well-data, reference |
| `data.viscosity.rpm_readings` | array[dict] |  |  | Array of rpm readings records |  | well-data, reference, container, array |
| `data.viscosity.rpm_readings[].id` | str | e5cf3ac1-4367-11ee-afda-4b87a654401d |  | Numeric identifier for this record/run |  | well-data, reference, metadata, identifier |
| `data.viscosity.rpm_readings[].rpm` | int | 600 |  | Rpm |  | well-data, reference |
| `data.viscosity.rpm_readings[].dial_reading` | int | 1 |  | Dial reading |  | well-data, reference |
| `data.mud_density` | int | 8 |  | Mud density |  | well-data, reference |
| `data.api_filtrate` | object |  |  | Nested object containing api filtrate data |  | well-data, reference, container, object |
| `data.api_filtrate.filtrate` | int | 1 |  | API filtrate (ml/30min) |  | well-data, reference, mud, property, filtration |
| `data.api_filtrate.cake_thickness` | int | 1 |  | Cake thickness |  | well-data, reference |
| `data.lime_content` | int | 1 |  | Lime content |  | well-data, reference |
| `data.hthp_filtrate` | object |  |  | Nested object containing hthp filtrate data |  | well-data, reference, container, object |
| `data.hthp_filtrate.temp` | int | 1 |  | Temp |  | well-data, reference |
| `data.hthp_filtrate.filtrate` | int | 1 |  | API filtrate (ml/30min) |  | well-data, reference, mud, property, filtration |
| `data.hthp_filtrate.cake_thickness` | int | 1 |  | Cake thickness |  | well-data, reference |
| `data.sample_location` | str | 1 |  | Sample location |  | well-data, reference |
| `data.oil_content_percent` | int | 98 |  | Oil content percent |  | well-data, reference |
| `data.total_solid_percent` | int | 1 |  | Total solid percent |  | well-data, reference |
| `data.electrical_stability` | int | 1 |  | Electrical stability |  | well-data, reference |
| `data.sand_content_percent` | int | 1 |  | Sand content percent |  | well-data, reference |
| `data.water_content_percent` | int | 2 |  | Water content percent |  | well-data, reference |
| `data.corrected_solid_percent` | int | 1 |  | Corrected solid percent |  | well-data, reference |
| `data.average_specific_gravity` | int | 0 |  | Average specific gravity |  | well-data, reference |
| `data.low_gravity_solids_volume` | int | 1 |  | Low gravity solids volume |  | well-data, reference |
| `data.high_gravity_solids_volume` | int | 1 |  | High gravity solids volume |  | well-data, reference |
| `data.low_gravity_solids_percent` | int | 1 |  | Low gravity solids percent |  | well-data, reference |
| `data.phenolphthalein_alkalinity` | int | 1 |  | Phenolphthalein alkalinity |  | well-data, reference |
| `data.high_gravity_solids_percent` | int | 1 |  | High gravity solids percent |  | well-data, reference |
| `data.phenolphthalein_alkalinity_filtrate` | int | 1 |  | Phenolphthalein alkalinity filtrate |  | well-data, reference |
| `version` | int | 2 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 13915897 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1692982436 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.mud |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.npt-events`

- **Friendly Name**: data.npt-events
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.npt-events/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 61045ada92ca6540e49046f9 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.type` | str | fishing |  | Type classifier for this record |  | well-data, reference, metadata, classification |
| `data.depth` | int | 20000 |  | Depth |  | well-data, reference |
| `data.comment` | str |  |  | Comment |  | well-data, reference |
| `data.end_time` | int | 1545184920 |  | End time of the activity/operation (Unix epoch) |  | well-data, reference, operations, time, interval |
| `data.is_impact` | bool | False |  | Flag indicating whether is impact |  | well-data, reference, boolean, flag |
| `data.start_time` | int | 1545130920 |  | Start time of the activity/operation (Unix epoch) |  | well-data, reference, operations, time, interval |
| `_pre_id` | int | 1627675334503 |  | Identifier for  pre |  | well-data, reference, metadata, identifier, reference |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1627675354 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.npt-events |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.operation-summaries`

- **Friendly Name**: data.operation-summaries
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.operation-summaries/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3796c88017f9358a617 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.summary` | str | Perform Between Well Work Scope. |  | Summary |  | well-data, reference |
| `data.date_time` | int | 1544508000 |  | Timestamp for date |  | well-data, reference, metadata, time |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1585242601 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.operation-summaries |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 56 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.plan_survey`

- **Friendly Name**: data.plan_survey
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.plan_survey/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3786c88017f9358a5f7 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.stations` | array[dict] |  |  | Array of stations records |  | well-data, reference, container, array |
| `data.stations[].dls` | int | 0 |  | Dog leg severity - rate of wellbore curvature (deg/100ft) |  | well-data, reference, directional, survey, calculated, key-metric |
| `data.stations[].tvd` | int | 0 |  | True vertical depth from surface |  | well-data, reference, depth, survey, directional, calculated |
| `data.stations[].azimuth` | int | 0 |  | Wellbore azimuth direction (degrees from north) |  | well-data, reference, directional, survey, key-metric |
| `data.stations[].easting` | int | 0 |  | East-west position relative to surface location (ft) |  | well-data, reference, directional, survey, coordinate |
| `data.stations[].northing` | int | 0 |  | North-south position relative to surface location (ft) |  | well-data, reference, directional, survey, coordinate |
| `data.stations[].inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | well-data, reference, directional, survey, key-metric |
| `data.stations[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | well-data, reference, depth, survey, directional |
| `data.stations[].vertical_section` | int | 0 |  | Projected distance along planned azimuth (ft) |  | well-data, reference, directional, survey, calculated |
| `data.plan_name` | str | WP AVP |  | Name/label for plan |  | well-data, reference, metadata, display, label |
| `data.target_changes` | array[unknown] |  |  | Array of target changes records |  | well-data, reference, container, array |
| `data.tie_in_station` | dict | {} |  | Tie in station |  | well-data, reference |
| `data.has_target_change` | bool | False |  | Flag indicating whether has target change |  | well-data, reference, boolean, flag |
| `data.vertical_section_azimuth` | float | 109.13 |  | Vertical section azimuth |  | well-data, reference |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1585152138 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.plan_survey |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 56 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.surface-equipment`

- **Friendly Name**: data.surface-equipment
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.surface-equipment/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3796c88017f9358a616 |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.block_weight` | int | 189 |  | Block weight |  | well-data, reference |
| `data.wob_threshold` | int | 60 |  | Wob threshold |  | well-data, reference |
| `data.drilling_phase` | str | drilling |  | Drilling phase |  | well-data, reference |
| `data.toolface_threshold` | int | 5 |  | Toolface threshold |  | well-data, reference |
| `data.flow_rate_threshold` | int | 1500 |  | Flow rate threshold |  | well-data, reference |
| `data.maximum_spp_capacity` | int | 7500 |  | Maximum spp capacity |  | well-data, reference |
| `data.rotary_rpm_threshold` | int | 200 |  | Rotary rpm threshold |  | well-data, reference |
| `data.lateral_footage_limit` | int | 1000 |  | Lateral footage limit |  | well-data, reference |
| `data.surface_back_pressure` | int | 1 |  | Pressure: surface back (psi) |  | well-data, reference, pressure, measurement |
| `data.maximum_hosting_capacity` | int | 750 |  | Maximum hosting capacity |  | well-data, reference |
| `data.toolface_accuracy_window` | int | 30 |  | Toolface accuracy window |  | well-data, reference |
| `data.maximum_td_torque_capacity` | int | 40 |  | Maximum td torque capacity |  | well-data, reference |
| `data.rocking_system_setting_rpm` | null |  |  | Rocking system setting rpm |  | well-data, reference |
| `data.surface_circulation_system` | str | type1 |  | Surface circulation system |  | well-data, reference |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1587071042 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.surface-equipment |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 56 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

#### `corva#data.well-sections`

- **Friendly Name**: data.well-sections
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/data.well-sections/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3796c88017f9358a5fc |  | MongoDB document unique identifier |  | well-data, reference, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | well-data, reference, metadata, container |
| `data.name` | str | 36" JET |  | Display name of the component or record |  | well-data, reference, metadata, display |
| `data.pre_set` | bool | True |  | Flag indicating whether pre set |  | well-data, reference, boolean, flag |
| `data.diameter` | int | 36 |  | Diameter |  | well-data, reference |
| `data.top_depth` | int | 0 |  | Top depth of casing string (ft MD) |  | well-data, reference, casing, depth, range |
| `data.ur_diameter` | null |  |  | Ur diameter |  | well-data, reference |
| `data.bottom_depth` | int | 7065 |  | Bottom depth of casing string (ft MD) |  | well-data, reference, casing, depth, range |
| `version` | int | 1 |  | Schema version number for this record |  | well-data, reference, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | well-data, reference, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | well-data, reference, metadata, internal |
| `timestamp` | int | 1584989953 |  | Unix epoch timestamp (seconds) of the record |  | well-data, reference, metadata, time-index, filter-key, required |
| `collection` | str | data.well-sections |  | MongoDB collection name this record belongs to |  | well-data, reference, metadata, internal |
| `company_id` | int | 56 |  | Unique identifier for the company/operator |  | well-data, reference, metadata, company, filter-key |

### 10. Completions / Frac

#### `corva#completion.ccl-annotations`

- **Friendly Name**: completion.ccl-annotations
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.ccl-annotations/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 67db439dac7ada8ce8f02956 |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.state` | str | Run in Hole |  | State |  | completions, frac |
| `data.comment` | str | I see an anomaly |  | Comment |  | completions, frac |
| `data.user_email` | str | ryan.dawson@corva.ai |  | User email |  | completions, frac |
| `data.casing_joint` | null |  |  | Casing joint |  | completions, frac |
| `data.measured_depth` | int | 801 |  | Measured depth along the wellbore path |  | completions, frac, depth, survey, directional |
| `data.user_last_name` | str | Dawson |  | Name/label for user last |  | completions, frac, metadata, display, label |
| `data.current_user_id` | int | 15624 |  | Identifier for current user |  | completions, frac, metadata, identifier, reference |
| `data.user_first_name` | str | Ryan |  | Name/label for user first |  | completions, frac, metadata, display, label |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 123456 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 1725148859 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `collection` | str | completion.ccl-annotations |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 346 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |
| `stage_number` | int | 26 |  | Frac stage number |  | completions, frac, completions, frac, stage, index |

#### `corva#completion.ccl-anomalies`

- **Friendly Name**: completion.ccl-anomalies
- **Data Type**: reference
- **API Path**: `/api/v1/data/corva/completion.ccl-anomalies/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 681b8609df38c12e794f655a |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.state` | str | Run in Hole |  | State |  | completions, frac |
| `data.end_depth` | float | 13182.30935231508 |  | Ending measured depth for this interval/run |  | completions, frac, depth, interval, range |
| `data.start_depth` | float | 13178.009352315084 |  | Starting measured depth for this interval/run |  | completions, frac, depth, interval, range |
| `data.casing_joint` | null |  |  | Casing joint |  | completions, frac |
| `data.anomaly_score` | float | 0.8212986482895198 |  | Anomaly score |  | completions, frac |
| `data.classification` | null |  |  | Classification |  | completions, frac |
| `data.classification_updated_at` | null |  |  | Timestamp for classification updated |  | completions, frac, metadata, time |
| `data.classification_updated_by_user_id` | null |  |  | Identifier for classification updated by user |  | completions, frac, metadata, identifier, reference |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 123456 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 1746143883 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `collection` | str | completion.ccl-anomalies |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |
| `stage_number` | int | 26 |  | Frac stage number |  | completions, frac, completions, frac, stage, index |

#### `corva#completion.ccl-settings`

- **Friendly Name**: completion.ccl-settings
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.ccl-settings/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 67db46fee8cf5dcbc1b131be |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.user_email` | str | ryan.dawson@corva.ai |  | User email |  | completions, frac |
| `data.user_last_name` | str | Dawson |  | Name/label for user last |  | completions, frac, metadata, display, label |
| `data.current_user_id` | int | 15624 |  | Identifier for current user |  | completions, frac, metadata, identifier, reference |
| `data.user_first_name` | str | Ryan |  | Name/label for user first |  | completions, frac, metadata, display, label |
| `data.depth_shift_run_in_hole` | int | 0 |  | Depth shift run in hole |  | completions, frac |
| `data.depth_shift_pull_out_of_hole` | int | 0 |  | Depth shift pull out of hole |  | completions, frac |
| `data.anomaly_depth_overlap_threshold` | float | 65.62 |  | Anomaly depth overlap threshold |  | completions, frac |
| `data.anomaly_score_threshold_minor_to` | float | 0.6 |  | Anomaly score threshold minor to |  | completions, frac |
| `data.anomaly_score_threshold_minor_from` | int | 0 |  | Anomaly score threshold minor from |  | completions, frac |
| `data.anomaly_score_threshold_significant_to` | int | 1 |  | Anomaly score threshold significant to |  | completions, frac |
| `data.anomaly_score_threshold_significant_from` | float | 0.6 |  | Anomaly score threshold significant from |  | completions, frac |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 123456 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 1742423674 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `collection` | str | completion.ccl-settings |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |

#### `corva#completion.ccl-summary`

- **Friendly Name**: completion.ccl-summary
- **Data Type**: reference
- **API Path**: `/api/v1/data/corva/completion.ccl-summary/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 6813a8e10ba350389dcc3989 |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.state` | str | Run in Hole |  | State |  | completions, frac |
| `data.max_ccl` | float | 0.059356197065784266 |  | Max ccl |  | completions, frac |
| `data.min_ccl` | float | 0.026986904071739252 |  | Min ccl |  | completions, frac |
| `data.filtered` | array[dict] |  |  | Array of filtered records |  | completions, frac, container, array |
| `data.filtered[].ccl` | float | 0.028087487478160974 |  | Ccl |  | completions, frac |
| `data.filtered[].timestamp` | float | 1746117473.957198 |  | Timestamp |  | completions, frac |
| `data.filtered[].line_speed` | float | 69.23 |  | Line speed |  | completions, frac |
| `data.filtered[].line_tension` | float | 527.86 |  | Line tension |  | completions, frac |
| `data.filtered[].interpolated_depth` | float | 3296.013493872833 |  | Depth value: interpolated (ft) |  | completions, frac, depth, measurement |
| `data.mean_ccl` | float | 0.030301255351879674 |  | Mean ccl |  | completions, frac |
| `data.casing_joint` | null |  |  | Casing joint |  | completions, frac |
| `data.measured_depth` | int | 3296 |  | Measured depth along the wellbore path |  | completions, frac, depth, survey, directional |
| `data.delta_min_max_ccl` | float | 0.032369292994045014 |  | Delta min max ccl |  | completions, frac |
| `app_key` | str | corva.ccl_anomaly_summary_tool |  | App key |  | completions, frac |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 123456 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `collection` | str | completion.ccl-summary |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |
| `stage_number` | int | 50 |  | Frac stage number |  | completions, frac, completions, frac, stage, index |

#### `corva#completion.custom_metrics`

- **Friendly Name**: completion.custom_metrics
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.custom_metrics/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `hhp` | str | HHP |  | Hhp |  | completions, frac |
| `HVFRS` | object |  |  | Nested object containing HVFRS data |  | completions, frac, container, object |
| `HVFRS.HVFRS#` | str | bbl |  | Hvfrs# |  | completions, frac |
| `HVRFL` | object |  |  | Nested object containing HVRFL data |  | completions, frac, container, object |
| `HVRFL.HVRFL#` | str | bbl |  | Hvrfl# |  | completions, frac |
| `hhp_zone` | str | zone# |  | Hhp zone |  | completions, frac |
| `fluid_system` | str | system# |  | Fluid system |  | completions, frac |
| `pumping_hours` | str | segs |  | Pumping hours |  | completions, frac |
| `average_slurry_rate` | str | bbl/min |  | Rate: average slurry |  | completions, frac, rate, measurement |
| `stage_end_timestamp` | str | timestamp |  | Timestamp for stage end |  | completions, frac, metadata, time |
| `summary_start_timestamp` | str | timestamp |  | Timestamp for summary start |  | completions, frac, metadata, time |
| `average_wellhead_pressure` | str | psi |  | Pressure: average wellhead (psi) |  | completions, frac, pressure, measurement |
| `pumping_hours_start_timestamp` | str | timestamp |  | Timestamp for pumping hours start |  | completions, frac, metadata, time |

#### `corva#completion.data.files`

- **Friendly Name**: completion.data.files
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.data.files/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3776c88017f9358a51a |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.id` | str | 310a9340-4797-43a4-ac7d-0332bdd9c586 |  | Numeric identifier for this record/run |  | completions, frac, metadata, identifier |
| `data.is_folder` | bool | True |  | Flag indicating whether is folder |  | completions, frac, boolean, flag |
| `data.display_name` | str | Post Stage Reports |  | Name/label for display |  | completions, frac, metadata, display, label |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | demo |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 1601565559 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `collection` | str | corva#completion.data.files |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |

#### `corva#completion.data.job-settings`

- **Friendly Name**: completion.data.job-settings
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.data.job-settings/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 61536afb49c1cc1ddf276cc0 |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.goal_rate` | int | 50 |  | Rate: goal |  | completions, frac, rate, measurement |
| `data.maximum_hhp` | int | 1 |  | Maximum hhp |  | completions, frac |
| `data.max_goal_pressure` | int | 6500 |  | Pressure: max goal (psi) |  | completions, frac, pressure, measurement |
| `data.min_goal_pressure` | int | 5000 |  | Pressure: min goal (psi) |  | completions, frac, pressure, measurement |
| `data.maximum_pumping_capacity` | int | 60 |  | Maximum pumping capacity |  | completions, frac |
| `data.wellhead_pressure_rating` | int | 1 |  | Wellhead pressure rating |  | completions, frac |
| `data.packer_plug_pressure_rating` | int | 1 |  | Packer plug pressure rating |  | completions, frac |
| `data.maximum_casing_hanger_pressure` | int | 1 |  | Pressure: maximum casing hanger (psi) |  | completions, frac, pressure, measurement |
| `data.surface_fluid_storage_capacity` | int | 1 |  | Surface fluid storage capacity |  | completions, frac |
| `data.maximum_casing_internal_pressure` | int | 1 |  | Pressure: maximum casing internal (psi) |  | completions, frac, pressure, measurement |
| `data.equivalent_length_of_surface_equipment` | int | 1 |  | Equivalent length of surface equipment |  | completions, frac |
| `data.maximum_allowable_surface_treating_pressure` | int | 1 |  | Pressure: maximum allowable surface treating (psi) |  | completions, frac, pressure, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 1632856827 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `collection` | str | completion.data.job-settings |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |

#### `corva#completion.data.time-log`

- **Friendly Name**: completion.data.time-log
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.data.time-log/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 636c689904606001b3a9c61c |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.comment` | str | fracing this well |  | Comment |  | completions, frac |
| `data.duration` | float | 116.25 |  | Duration |  | completions, frac |
| `data.end_time` | int | 1668029951 |  | End time of the activity/operation (Unix epoch) |  | completions, frac, operations, time, interval |
| `data.operation` | str | fracturing |  | Operation |  | completions, frac |
| `data.start_time` | int | 1668021776 |  | Start time of the activity/operation (Unix epoch) |  | completions, frac, operations, time, interval |
| `data.stage_number` | int | 1 |  | Frac stage number |  | completions, frac, completions, frac, stage, index |
| `data.duration_pressure` | float | 146.87 |  | Pressure: duration (psi) |  | completions, frac, pressure, measurement |
| `data.end_time_pressure` | int | 1668029951 |  | Pressure: end time (psi) |  | completions, frac, pressure, measurement |
| `data.start_time_pressure` | int | 1668021139 |  | Pressure: start time (psi) |  | completions, frac, pressure, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 123456 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 1668021776 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `collection` | str | completion.data.time-log |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 1 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |

#### `corva#completion.offset.abra`

- **Friendly Name**: completion.offset.abra
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.offset.abra/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | xxxx |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.is_valid` | bool | True |  | Flag indicating whether is valid |  | completions, frac, boolean, flag |
| `data.pressure` | str | pressure from abra |  | Pressure |  | completions, frac |
| `data.timestamp` | str | timestamp from abra |  | Timestamp |  | completions, frac |
| `data.temperature` | str | temperature from abra |  | Temperature |  | completions, frac |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 24556316 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 123456472 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `company_id` | int | 15 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |
| `stage_number` | int | 13 |  | Frac stage number |  | completions, frac, completions, frac, stage, index |

#### `corva#completion.predictions`

- **Friendly Name**: completion.predictions
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.predictions/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e1d5cb9c547da4e9bd70afe |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.isip` | array[dict] |  |  | Instantaneous shut-in pressure (psi) |  | completions, frac, completions, frac, pressure, key-metric |
| `data.isip[].gel` | int | 0 |  | Gel |  | completions, frac |
| `data.isip[].acid` | int | 0 |  | Acid |  | completions, frac |
| `data.isip[].biocide` | int | 0 |  | Biocide |  | completions, frac |
| `data.isip[].divertor` | int | 0 |  | Divertor |  | completions, frac |
| `data.isip[].timestamp` | int | 1536949365 |  | Timestamp |  | completions, frac |
| `data.isip[].emulsifier` | int | 0 |  | Emulsifier |  | completions, frac |
| `data.isip[].fluid_loss` | int | 0 |  | Fluid loss |  | completions, frac |
| `data.isip[].powder_gel` | int | 0 |  | Powder gel |  | completions, frac |
| `data.isip[].surfactant` | int | 0 |  | Surfactant |  | completions, frac |
| `data.isip[].accelerator` | int | 0 |  | Accelerator |  | completions, frac |
| `data.isip[].anti_sludge` | int | 0 |  | Anti sludge |  | completions, frac |
| `data.isip[].cross_linker` | int | 0 |  | Cross linker |  | completions, frac |
| `data.isip[].elapsed_time` | int | 5157 |  | Timestamp for elapsed |  | completions, frac, metadata, time |
| `data.isip[].iron_control` | int | 0 |  | Iron control |  | completions, frac |
| `data.isip[].ploymer_plug` | int | 0 |  | Ploymer plug |  | completions, frac |
| `data.isip[].acid_retarder` | int | 0 |  | Acid retarder |  | completions, frac |
| `data.isip[].acid_inhibitor` | int | 0 |  | Acid inhibitor |  | completions, frac |
| `data.isip[].enzyme_breaker` | int | 0 |  | Enzyme breaker |  | completions, frac |
| `data.isip[].liquid_breaker` | int | 0 |  | Liquid breaker |  | completions, frac |
| `data.isip[].mutual_solvent` | int | 0 |  | Mutual solvent |  | completions, frac |
| `data.isip[].non_emulsifier` | int | 0 |  | Non emulsifier |  | completions, frac |
| `data.isip[].powder_breaker` | int | 0 |  | Powder breaker |  | completions, frac |
| `data.isip[].clay_stabilizer` | int | 0 |  | Clay stabilizer |  | completions, frac |
| `data.isip[].fines_suspender` | int | 0 |  | Fines suspender |  | completions, frac |
| `data.isip[].proppant_1_mass` | int | 0 |  | Proppant 1 mass |  | completions, frac |
| `data.isip[].proppant_2_mass` | int | 0 |  | Proppant 2 mass |  | completions, frac |
| `data.isip[].scale_inhibitor` | int | 0 |  | Scale inhibitor |  | completions, frac |
| `data.isip[].friction_reducer` | int | 0 |  | Friction reducer |  | completions, frac |
| `data.isip[].oxygen_scavenger` | int | 0 |  | Oxygen scavenger |  | completions, frac |
| `data.isip[].paraffin_control` | int | 0 |  | Paraffin control |  | completions, frac |
| `data.isip[].wellhead_pressure` | float | 2316.552830696106 |  | Pressure: wellhead (psi) |  | completions, frac, pressure, measurement |
| `data.isip[].clean_flow_rate_in` | int | 0 |  | Clean flow rate in |  | completions, frac |
| `data.isip[].ph_adjusting_agent` | int | 0 |  | Ph adjusting agent |  | completions, frac |
| `data.isip[].corrosion_inhibitor` | int | 0 |  | Corrosion inhibitor |  | completions, frac |
| `data.isip[].delayed_crosslinker` | int | 0 |  | Delayed crosslinker |  | completions, frac |
| `data.isip[].instant_crosslinker` | int | 0 |  | Instant crosslinker |  | completions, frac |
| `data.isip[].slurry_flow_rate_in` | float | 4.37 |  | Slurry flow rate in |  | completions, frac |
| `data.isip[].total_proppant_mass` | int | 0 |  | Total proppant mass |  | completions, frac |
| `data.isip[].hydrostatic_pressure` | int | 0 |  | Pressure: hydrostatic (psi) |  | completions, frac, pressure, measurement |
| `data.isip[].powder_enzyme_breaker` | int | 0 |  | Powder enzyme breaker |  | completions, frac |
| `data.isip[].total_clean_volume_in` | int | 0 |  | Total clean volume in |  | completions, frac |
| `data.isip[].total_chemical_rate_in` | int | 0 |  | Total chemical rate in |  | completions, frac |
| `data.isip[].total_slurry_volume_in` | int | 0 |  | Total slurry volume in |  | completions, frac |
| `data.isip[].powder_friction_reducer` | int | 0 |  | Powder friction reducer |  | completions, frac |
| `data.isip[].proppant_1_concentration` | int | 0 |  | Proppant 1 concentration |  | completions, frac |
| `data.isip[].proppant_2_concentration` | int | 0 |  | Proppant 2 concentration |  | completions, frac |
| `data.isip[].inverse_hydrostatic_pressure` | int | 0 |  | Pressure: inverse hydrostatic (psi) |  | completions, frac, pressure, measurement |
| `data.isip[].total_proppant_concentration` | int | 0 |  | Total proppant concentration |  | completions, frac |
| `data.isip[].bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | completions, frac, completions, frac, proppant, calculated |
| `data.ave_isip` | int | 2317 |  | Ave isip |  | completions, frac |
| `data.breakdown` | array[dict] |  |  | Array of breakdown records |  | completions, frac, container, array |
| `data.breakdown[].gel` | int | 0 |  | Gel |  | completions, frac |
| `data.breakdown[].acid` | int | 0 |  | Acid |  | completions, frac |
| `data.breakdown[].biocide` | int | 0 |  | Biocide |  | completions, frac |
| `data.breakdown[].divertor` | int | 0 |  | Divertor |  | completions, frac |
| `data.breakdown[].timestamp` | int | 1536944740 |  | Timestamp |  | completions, frac |
| `data.breakdown[].emulsifier` | int | 0 |  | Emulsifier |  | completions, frac |
| `data.breakdown[].fluid_loss` | int | 0 |  | Fluid loss |  | completions, frac |
| `data.breakdown[].powder_gel` | int | 0 |  | Powder gel |  | completions, frac |
| `data.breakdown[].surfactant` | int | 0 |  | Surfactant |  | completions, frac |
| `data.breakdown[].accelerator` | int | 0 |  | Accelerator |  | completions, frac |
| `data.breakdown[].anti_sludge` | int | 0 |  | Anti sludge |  | completions, frac |
| `data.breakdown[].cross_linker` | int | 0 |  | Cross linker |  | completions, frac |
| `data.breakdown[].elapsed_time` | int | 532 |  | Timestamp for elapsed |  | completions, frac, metadata, time |
| `data.breakdown[].iron_control` | int | 0 |  | Iron control |  | completions, frac |
| `data.breakdown[].ploymer_plug` | int | 0 |  | Ploymer plug |  | completions, frac |
| `data.breakdown[].acid_retarder` | int | 0 |  | Acid retarder |  | completions, frac |
| `data.breakdown[].acid_inhibitor` | int | 0 |  | Acid inhibitor |  | completions, frac |
| `data.breakdown[].enzyme_breaker` | int | 0 |  | Enzyme breaker |  | completions, frac |
| `data.breakdown[].liquid_breaker` | int | 0 |  | Liquid breaker |  | completions, frac |
| `data.breakdown[].mutual_solvent` | int | 0 |  | Mutual solvent |  | completions, frac |
| `data.breakdown[].non_emulsifier` | int | 0 |  | Non emulsifier |  | completions, frac |
| `data.breakdown[].powder_breaker` | int | 0 |  | Powder breaker |  | completions, frac |
| `data.breakdown[].clay_stabilizer` | int | 0 |  | Clay stabilizer |  | completions, frac |
| `data.breakdown[].fines_suspender` | int | 0 |  | Fines suspender |  | completions, frac |
| `data.breakdown[].proppant_1_mass` | int | 0 |  | Proppant 1 mass |  | completions, frac |
| `data.breakdown[].proppant_2_mass` | int | 0 |  | Proppant 2 mass |  | completions, frac |
| `data.breakdown[].scale_inhibitor` | int | 0 |  | Scale inhibitor |  | completions, frac |
| `data.breakdown[].friction_reducer` | int | 0 |  | Friction reducer |  | completions, frac |
| `data.breakdown[].oxygen_scavenger` | int | 0 |  | Oxygen scavenger |  | completions, frac |
| `data.breakdown[].paraffin_control` | int | 0 |  | Paraffin control |  | completions, frac |
| `data.breakdown[].wellhead_pressure` | float | 9180.28 |  | Pressure: wellhead (psi) |  | completions, frac, pressure, measurement |
| `data.breakdown[].clean_flow_rate_in` | int | 0 |  | Clean flow rate in |  | completions, frac |
| `data.breakdown[].ph_adjusting_agent` | int | 0 |  | Ph adjusting agent |  | completions, frac |
| `data.breakdown[].corrosion_inhibitor` | int | 0 |  | Corrosion inhibitor |  | completions, frac |
| `data.breakdown[].delayed_crosslinker` | int | 0 |  | Delayed crosslinker |  | completions, frac |
| `data.breakdown[].instant_crosslinker` | int | 0 |  | Instant crosslinker |  | completions, frac |
| `data.breakdown[].slurry_flow_rate_in` | float | 59.24 |  | Slurry flow rate in |  | completions, frac |
| `data.breakdown[].total_proppant_mass` | int | 0 |  | Total proppant mass |  | completions, frac |
| `data.breakdown[].hydrostatic_pressure` | int | 0 |  | Pressure: hydrostatic (psi) |  | completions, frac, pressure, measurement |
| `data.breakdown[].powder_enzyme_breaker` | int | 0 |  | Powder enzyme breaker |  | completions, frac |
| `data.breakdown[].total_clean_volume_in` | int | 0 |  | Total clean volume in |  | completions, frac |
| `data.breakdown[].total_chemical_rate_in` | int | 0 |  | Total chemical rate in |  | completions, frac |
| `data.breakdown[].total_slurry_volume_in` | int | 0 |  | Total slurry volume in |  | completions, frac |
| `data.breakdown[].powder_friction_reducer` | int | 0 |  | Powder friction reducer |  | completions, frac |
| `data.breakdown[].proppant_1_concentration` | int | 0 |  | Proppant 1 concentration |  | completions, frac |
| `data.breakdown[].proppant_2_concentration` | int | 0 |  | Proppant 2 concentration |  | completions, frac |
| `data.breakdown[].inverse_hydrostatic_pressure` | int | 0 |  | Pressure: inverse hydrostatic (psi) |  | completions, frac, pressure, measurement |
| `data.breakdown[].total_proppant_concentration` | int | 0 |  | Total proppant concentration |  | completions, frac |
| `data.breakdown[].bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | completions, frac, completions, frac, proppant, calculated |
| `data.flush_volume` | float | 367.49 |  | Flush volume |  | completions, frac |
| `data.ave_breakdown` | int | 9180 |  | Ave breakdown |  | completions, frac |
| `data.ave_chemicals` | object |  |  | Nested object containing ave chemicals data |  | completions, frac, container, object |
| `data.ave_chemicals.gel` | float | 3.42 |  | Gel |  | completions, frac |
| `data.ave_chemicals.acid` | int | 0 |  | Acid |  | completions, frac |
| `data.ave_chemicals.biocide` | int | 0 |  | Biocide |  | completions, frac |
| `data.ave_chemicals.divertor` | int | 0 |  | Divertor |  | completions, frac |
| `data.ave_chemicals.emulsifier` | int | 0 |  | Emulsifier |  | completions, frac |
| `data.ave_chemicals.fluid_loss` | int | 0 |  | Fluid loss |  | completions, frac |
| `data.ave_chemicals.powder_gel` | int | 0 |  | Powder gel |  | completions, frac |
| `data.ave_chemicals.surfactant` | int | 0 |  | Surfactant |  | completions, frac |
| `data.ave_chemicals.accelerator` | int | 0 |  | Accelerator |  | completions, frac |
| `data.ave_chemicals.anti_sludge` | int | 0 |  | Anti sludge |  | completions, frac |
| `data.ave_chemicals.cross_linker` | int | 0 |  | Cross linker |  | completions, frac |
| `data.ave_chemicals.iron_control` | int | 0 |  | Iron control |  | completions, frac |
| `data.ave_chemicals.ploymer_plug` | int | 0 |  | Ploymer plug |  | completions, frac |
| `data.ave_chemicals.acid_retarder` | int | 0 |  | Acid retarder |  | completions, frac |
| `data.ave_chemicals.acid_inhibitor` | int | 0 |  | Acid inhibitor |  | completions, frac |
| `data.ave_chemicals.enzyme_breaker` | int | 0 |  | Enzyme breaker |  | completions, frac |
| `data.ave_chemicals.liquid_breaker` | int | 0 |  | Liquid breaker |  | completions, frac |
| `data.ave_chemicals.mutual_solvent` | int | 0 |  | Mutual solvent |  | completions, frac |
| `data.ave_chemicals.non_emulsifier` | int | 0 |  | Non emulsifier |  | completions, frac |
| `data.ave_chemicals.powder_breaker` | int | 0 |  | Powder breaker |  | completions, frac |
| `data.ave_chemicals.clay_stabilizer` | int | 0 |  | Clay stabilizer |  | completions, frac |
| `data.ave_chemicals.fines_suspender` | int | 0 |  | Fines suspender |  | completions, frac |
| `data.ave_chemicals.scale_inhibitor` | float | 0.01 |  | Scale inhibitor |  | completions, frac |
| `data.ave_chemicals.friction_reducer` | float | 0.63 |  | Friction reducer |  | completions, frac |
| `data.ave_chemicals.oxygen_scavenger` | int | 0 |  | Oxygen scavenger |  | completions, frac |
| `data.ave_chemicals.paraffin_control` | int | 0 |  | Paraffin control |  | completions, frac |
| `data.ave_chemicals.ph_adjusting_agent` | int | 0 |  | Ph adjusting agent |  | completions, frac |
| `data.ave_chemicals.corrosion_inhibitor` | int | 0 |  | Corrosion inhibitor |  | completions, frac |
| `data.ave_chemicals.delayed_crosslinker` | int | 0 |  | Delayed crosslinker |  | completions, frac |
| `data.ave_chemicals.instant_crosslinker` | int | 0 |  | Instant crosslinker |  | completions, frac |
| `data.ave_chemicals.powder_enzyme_breaker` | int | 0 |  | Powder enzyme breaker |  | completions, frac |
| `data.ave_chemicals.powder_friction_reducer` | int | 0 |  | Powder friction reducer |  | completions, frac |
| `data.max_flow_rate` | float | 90.75 |  | Rate: max flow |  | completions, frac, rate, measurement |
| `data.delta_pressure` | null |  |  | Pressure: delta (psi) |  | completions, frac, pressure, measurement |
| `data.ave_pumping_rate` | float | 89.9 |  | Rate: ave pumping |  | completions, frac, rate, measurement |
| `data.pumping_duration` | int | 4680 |  | Pumping duration |  | completions, frac |
| `data.fracture_gradient` | float | 0.6824 |  | Fracture gradient |  | completions, frac |
| `data.total_clean_volume` | int | 6119 |  | Total clean volume |  | completions, frac |
| `data.total_proppant_mass` | int | 349337 |  | Total proppant mass |  | completions, frac |
| `data.total_slurry_volume` | int | 6495 |  | Total slurry volume |  | completions, frac |
| `data.cumulative_chemicals` | object |  |  | Nested object containing cumulative chemicals data |  | completions, frac, container, object |
| `data.cumulative_chemicals.gel` | float | 879.58 |  | Gel |  | completions, frac |
| `data.cumulative_chemicals.acid` | int | 0 |  | Acid |  | completions, frac |
| `data.cumulative_chemicals.biocide` | int | 0 |  | Biocide |  | completions, frac |
| `data.cumulative_chemicals.divertor` | int | 0 |  | Divertor |  | completions, frac |
| `data.cumulative_chemicals.emulsifier` | int | 0 |  | Emulsifier |  | completions, frac |
| `data.cumulative_chemicals.fluid_loss` | int | 0 |  | Fluid loss |  | completions, frac |
| `data.cumulative_chemicals.powder_gel` | int | 0 |  | Powder gel |  | completions, frac |
| `data.cumulative_chemicals.surfactant` | int | 0 |  | Surfactant |  | completions, frac |
| `data.cumulative_chemicals.accelerator` | int | 0 |  | Accelerator |  | completions, frac |
| `data.cumulative_chemicals.anti_sludge` | int | 0 |  | Anti sludge |  | completions, frac |
| `data.cumulative_chemicals.cross_linker` | int | 0 |  | Cross linker |  | completions, frac |
| `data.cumulative_chemicals.iron_control` | int | 0 |  | Iron control |  | completions, frac |
| `data.cumulative_chemicals.ploymer_plug` | int | 0 |  | Ploymer plug |  | completions, frac |
| `data.cumulative_chemicals.acid_retarder` | int | 0 |  | Acid retarder |  | completions, frac |
| `data.cumulative_chemicals.acid_inhibitor` | int | 0 |  | Acid inhibitor |  | completions, frac |
| `data.cumulative_chemicals.enzyme_breaker` | int | 0 |  | Enzyme breaker |  | completions, frac |
| `data.cumulative_chemicals.liquid_breaker` | int | 0 |  | Liquid breaker |  | completions, frac |
| `data.cumulative_chemicals.mutual_solvent` | int | 0 |  | Mutual solvent |  | completions, frac |
| `data.cumulative_chemicals.non_emulsifier` | int | 0 |  | Non emulsifier |  | completions, frac |
| `data.cumulative_chemicals.powder_breaker` | int | 0 |  | Powder breaker |  | completions, frac |
| `data.cumulative_chemicals.clay_stabilizer` | int | 0 |  | Clay stabilizer |  | completions, frac |
| `data.cumulative_chemicals.fines_suspender` | int | 0 |  | Fines suspender |  | completions, frac |
| `data.cumulative_chemicals.scale_inhibitor` | float | 3.26 |  | Scale inhibitor |  | completions, frac |
| `data.cumulative_chemicals.friction_reducer` | float | 161.48 |  | Friction reducer |  | completions, frac |
| `data.cumulative_chemicals.oxygen_scavenger` | int | 0 |  | Oxygen scavenger |  | completions, frac |
| `data.cumulative_chemicals.paraffin_control` | int | 0 |  | Paraffin control |  | completions, frac |
| `data.cumulative_chemicals.ph_adjusting_agent` | int | 0 |  | Ph adjusting agent |  | completions, frac |
| `data.cumulative_chemicals.corrosion_inhibitor` | int | 0 |  | Corrosion inhibitor |  | completions, frac |
| `data.cumulative_chemicals.delayed_crosslinker` | int | 0 |  | Delayed crosslinker |  | completions, frac |
| `data.cumulative_chemicals.instant_crosslinker` | int | 0 |  | Instant crosslinker |  | completions, frac |
| `data.cumulative_chemicals.powder_enzyme_breaker` | int | 0 |  | Powder enzyme breaker |  | completions, frac |
| `data.cumulative_chemicals.powder_friction_reducer` | int | 0 |  | Powder friction reducer |  | completions, frac |
| `data.duration_to_max_rate` | int | 589 |  | Rate: duration to max |  | completions, frac, rate, measurement |
| `data.ave_treating_pressure` | int | 6976 |  | Pressure: ave treating (psi) |  | completions, frac, pressure, measurement |
| `data.hydraulic_horse_power` | int | 15363 |  | Hydraulic horse power |  | completions, frac |
| `data.max_treating_pressure` | int | 9074 |  | Pressure: max treating (psi) |  | completions, frac, pressure, measurement |
| `data.ave_proppant_concentration` | float | 1.359 |  | Ave proppant concentration |  | completions, frac |
| `data.main_pumping_start_timestamp` | int | 1536944682 |  | Timestamp for main pumping start |  | completions, frac, metadata, time |
| `data.fracturing_operation_interval` | object |  |  | Nested object containing fracturing operation interval data |  | completions, frac, container, object |
| `data.fracturing_operation_interval.end_timestamp` | int | 1536949365 |  | End timestamp of the interval/run (Unix epoch) |  | completions, frac, time, interval, range |
| `data.fracturing_operation_interval.start_timestamp` | int | 1536944682 |  | Start timestamp of the interval/run (Unix epoch) |  | completions, frac, time, interval, range |
| `data.proppant_injection_start_timestamp` | int | 1536945453 |  | Timestamp for proppant injection start |  | completions, frac, metadata, time |
| `data.fracturing_operation_interval_pressure` | object |  |  | Pressure: fracturing operation interval (psi) |  | completions, frac, pressure, measurement |
| `data.fracturing_operation_interval_pressure.end_timestamp` | int | 1536949417 |  | End timestamp of the interval/run (Unix epoch) |  | completions, frac, time, interval, range |
| `data.fracturing_operation_interval_pressure.start_timestamp` | int | 1536944678 |  | Start timestamp of the interval/run (Unix epoch) |  | completions, frac, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 1536945667 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `collection` | str | completion.predictions |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |
| `created_at` | int | 1536945667 |  | Timestamp for created |  | completions, frac, metadata, time |
| `updated_at` | int | 1536959208 |  | Timestamp for updated |  | completions, frac, metadata, time |
| `stage_number` | int | 2 |  | Frac stage number |  | completions, frac, completions, frac, stage, index |

#### `corva#completion.stage-times`

- **Friendly Name**: completion.stage-times
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.stage-times/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5ee7ca7d01e557092b980b76 |  | MongoDB document unique identifier |  | completions, frac, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | completions, frac, metadata, container |
| `data.stage_end` | null |  |  | Stage end |  | completions, frac |
| `data.stage_start` | int | 1537045649 |  | Stage start |  | completions, frac |
| `data.stage_duration` | null |  |  | Duration of the frac stage (seconds) |  | completions, frac, completions, frac, stage, duration |
| `version` | int | 1 |  | Schema version number for this record |  | completions, frac, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | completions, frac, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | completions, frac, metadata, internal |
| `timestamp` | int | 1537045649 |  | Unix epoch timestamp (seconds) of the record |  | completions, frac, metadata, time-index, filter-key, required |
| `collection` | str | completion.stage-times |  | MongoDB collection name this record belongs to |  | completions, frac, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | completions, frac, metadata, company, filter-key |
| `stage_number` | int | 7 |  | Frac stage number |  | completions, frac, completions, frac, stage, index |

### 11. Wireline

#### `corva#wireline.activity.summary-stage`

- **Friendly Name**: wireline.activity.summary-stage
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wireline.activity.summary-stage/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f161d23de7b935e2fe8e1f2 |  | MongoDB document unique identifier |  | wireline, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wireline, completions, metadata, container |
| `data.static` | int | 197 |  | Static |  | wireline, completions |
| `data.durations` | object |  |  | Nested object containing durations data |  | wireline, completions, container, object |
| `data.durations.activities` | object |  |  | Nested object containing activities data |  | wireline, completions, container, object |
| `data.durations.activities.static` | int | 197 |  | Static |  | wireline, completions |
| `data.durations.activities.out of hole` | int | 845 |  | Out of hole |  | wireline, completions |
| `data.durations.activities.run in hole` | int | 2441 |  | Run in hole |  | wireline, completions |
| `data.durations.activities.plug and perf` | int | 5 |  | Plug and perf |  | wireline, completions |
| `data.durations.activities.pull out of hole` | int | 2452 |  | Pull out of hole |  | wireline, completions |
| `data.durations.orientations` | object |  |  | Nested object containing orientations data |  | wireline, completions, container, object |
| `data.durations.orientations.vertical` | int | 2360 |  | Vertical |  | wireline, completions |
| `data.durations.orientations.horizontal` | int | 2735 |  | Horizontal |  | wireline, completions |
| `data.durations.orientations.unclassified` | int | 845 |  | Unclassified |  | wireline, completions |
| `data.durations.activity_breakdown` | object |  |  | Nested object containing activity breakdown data |  | wireline, completions, container, object |
| `data.durations.activity_breakdown.static` | object |  |  | Nested object containing static data |  | wireline, completions, container, object |
| `data.durations.activity_breakdown.static.vertical` | int | 135 |  | Vertical |  | wireline, completions |
| `data.durations.activity_breakdown.static.horizontal` | int | 62 |  | Horizontal |  | wireline, completions |
| `data.durations.activity_breakdown.static.unclassified` | int | 0 |  | Unclassified |  | wireline, completions |
| `data.durations.activity_breakdown.out of hole` | object |  |  | Nested object containing out of hole data |  | wireline, completions, container, object |
| `data.durations.activity_breakdown.out of hole.vertical` | int | 0 |  | Vertical |  | wireline, completions |
| `data.durations.activity_breakdown.out of hole.horizontal` | int | 0 |  | Horizontal |  | wireline, completions |
| `data.durations.activity_breakdown.out of hole.unclassified` | int | 845 |  | Unclassified |  | wireline, completions |
| `data.durations.activity_breakdown.run in hole` | object |  |  | Nested object containing run in hole data |  | wireline, completions, container, object |
| `data.durations.activity_breakdown.run in hole.vertical` | int | 1240 |  | Vertical |  | wireline, completions |
| `data.durations.activity_breakdown.run in hole.horizontal` | int | 1201 |  | Horizontal |  | wireline, completions |
| `data.durations.activity_breakdown.run in hole.unclassified` | int | 0 |  | Unclassified |  | wireline, completions |
| `data.durations.activity_breakdown.unclassified` | object |  |  | Nested object containing unclassified data |  | wireline, completions, container, object |
| `data.durations.activity_breakdown.unclassified.vertical` | int | 0 |  | Vertical |  | wireline, completions |
| `data.durations.activity_breakdown.unclassified.horizontal` | int | 0 |  | Horizontal |  | wireline, completions |
| `data.durations.activity_breakdown.unclassified.unclassified` | int | 0 |  | Unclassified |  | wireline, completions |
| `data.durations.activity_breakdown.plug and perf` | object |  |  | Nested object containing plug and perf data |  | wireline, completions, container, object |
| `data.durations.activity_breakdown.plug and perf.vertical` | int | 0 |  | Vertical |  | wireline, completions |
| `data.durations.activity_breakdown.plug and perf.horizontal` | int | 5 |  | Horizontal |  | wireline, completions |
| `data.durations.activity_breakdown.plug and perf.unclassified` | int | 0 |  | Unclassified |  | wireline, completions |
| `data.durations.activity_breakdown.pull out of hole` | object |  |  | Nested object containing pull out of hole data |  | wireline, completions, container, object |
| `data.durations.activity_breakdown.pull out of hole.vertical` | int | 985 |  | Vertical |  | wireline, completions |
| `data.durations.activity_breakdown.pull out of hole.horizontal` | int | 1467 |  | Horizontal |  | wireline, completions |
| `data.durations.activity_breakdown.pull out of hole.unclassified` | int | 0 |  | Unclassified |  | wireline, completions |
| `data.durations.orientation_breakdown` | object |  |  | Nested object containing orientation breakdown data |  | wireline, completions, container, object |
| `data.durations.orientation_breakdown.vertical` | object |  |  | Nested object containing vertical data |  | wireline, completions, container, object |
| `data.durations.orientation_breakdown.vertical.static` | int | 135 |  | Static |  | wireline, completions |
| `data.durations.orientation_breakdown.vertical.out of hole` | int | 0 |  | Out of hole |  | wireline, completions |
| `data.durations.orientation_breakdown.vertical.run in hole` | int | 1240 |  | Run in hole |  | wireline, completions |
| `data.durations.orientation_breakdown.vertical.unclassified` | int | 0 |  | Unclassified |  | wireline, completions |
| `data.durations.orientation_breakdown.vertical.plug and perf` | int | 0 |  | Plug and perf |  | wireline, completions |
| `data.durations.orientation_breakdown.vertical.pull out of hole` | int | 985 |  | Pull out of hole |  | wireline, completions |
| `data.durations.orientation_breakdown.horizontal` | object |  |  | Nested object containing horizontal data |  | wireline, completions, container, object |
| `data.durations.orientation_breakdown.horizontal.static` | int | 62 |  | Static |  | wireline, completions |
| `data.durations.orientation_breakdown.horizontal.out of hole` | int | 0 |  | Out of hole |  | wireline, completions |
| `data.durations.orientation_breakdown.horizontal.run in hole` | int | 1201 |  | Run in hole |  | wireline, completions |
| `data.durations.orientation_breakdown.horizontal.unclassified` | int | 0 |  | Unclassified |  | wireline, completions |
| `data.durations.orientation_breakdown.horizontal.plug and perf` | int | 5 |  | Plug and perf |  | wireline, completions |
| `data.durations.orientation_breakdown.horizontal.pull out of hole` | int | 1467 |  | Pull out of hole |  | wireline, completions |
| `data.durations.orientation_breakdown.unclassified` | object |  |  | Nested object containing unclassified data |  | wireline, completions, container, object |
| `data.durations.orientation_breakdown.unclassified.static` | int | 0 |  | Static |  | wireline, completions |
| `data.durations.orientation_breakdown.unclassified.out of hole` | int | 845 |  | Out of hole |  | wireline, completions |
| `data.durations.orientation_breakdown.unclassified.run in hole` | int | 0 |  | Run in hole |  | wireline, completions |
| `data.durations.orientation_breakdown.unclassified.unclassified` | int | 0 |  | Unclassified |  | wireline, completions |
| `data.durations.orientation_breakdown.unclassified.plug and perf` | int | 0 |  | Plug and perf |  | wireline, completions |
| `data.durations.orientation_breakdown.unclassified.pull out of hole` | int | 0 |  | Pull out of hole |  | wireline, completions |
| `data.out of hole` | int | 845 |  | Out of hole |  | wireline, completions |
| `data.run in hole` | int | 2441 |  | Run in hole |  | wireline, completions |
| `data.plug and perf` | int | 5 |  | Plug and perf |  | wireline, completions |
| `data.pull out of hole` | int | 2452 |  | Pull out of hole |  | wireline, completions |
| `version` | int | 1 |  | Schema version number for this record |  | wireline, completions, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | wireline, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wireline, completions, metadata, internal |
| `timestamp` | int | 1574316069 |  | Unix epoch timestamp (seconds) of the record |  | wireline, completions, metadata, time-index, filter-key, required |
| `collection` | str | wireline.activity.summary-stage |  | MongoDB collection name this record belongs to |  | wireline, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wireline, completions, metadata, company, filter-key |
| `stage_number` | int | 3 |  | Frac stage number |  | wireline, completions, completions, frac, stage, index |

#### `corva#wireline.stage-times`

- **Friendly Name**: wireline.stage-times
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wireline.stage-times/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f161dbb7d913e5def2b5058 |  | MongoDB document unique identifier |  | wireline, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wireline, completions, metadata, container |
| `data.recorded` | object |  |  | Nested object containing recorded data |  | wireline, completions, container, object |
| `data.recorded.stage_end` | int | 1574322016 |  | Stage end |  | wireline, completions |
| `data.recorded.stage_start` | int | 1574307957 |  | Stage start |  | wireline, completions |
| `data.recorded.stage_duration` | int | 14059 |  | Duration of the frac stage (seconds) |  | wireline, completions, completions, frac, stage, duration |
| `data.stage_end` | int | 1574321567 |  | Stage end |  | wireline, completions |
| `data.stage_start` | int | 1574316488 |  | Stage start |  | wireline, completions |
| `data.stage_number` | int | 4 |  | Frac stage number |  | wireline, completions, completions, frac, stage, index |
| `data.stage_duration` | int | 5079 |  | Duration of the frac stage (seconds) |  | wireline, completions, completions, frac, stage, duration |
| `version` | int | 1 |  | Schema version number for this record |  | wireline, completions, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | wireline, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wireline, completions, metadata, internal |
| `timestamp` | int | 1574322016 |  | Unix epoch timestamp (seconds) of the record |  | wireline, completions, metadata, time-index, filter-key, required |
| `collection` | str | wireline.stage-times |  | MongoDB collection name this record belongs to |  | wireline, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wireline, completions, metadata, company, filter-key |
| `stage_number` | int | 4 |  | Frac stage number |  | wireline, completions, completions, frac, stage, index |

### 12. Drillout

#### `corva#drillout.data.drillstring`

- **Friendly Name**: drillout.data.drillstring
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drillout.data.drillstring/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e9623524dbf264e2a2b3f2a |  | MongoDB document unique identifier |  | drillout, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drillout, completions, metadata, container |
| `data.id` | int | 1 |  | Numeric identifier for this record/run |  | drillout, completions, metadata, identifier |
| `data.dumb-iron` | bool | True |  | Whether BHA is dumb-iron (no motors/MWD) |  | drillout, completions, bha, classification, boolean |
| `data.calibrated` | bool | True |  | Whether the drillstring has been calibrated for T&D |  | drillout, completions, bha, torque-drag, calibration, boolean |
| `data.components` | array[dict] |  |  | Array of components records |  | drillout, completions, container, array |
| `data.components[].id` | str | dc9c8500-1a93-11e8-ad72-851e724da1d5 |  | Numeric identifier for this record/run |  | drillout, completions, metadata, identifier |
| `data.components[].tfa` | null |  |  | Total flow area of bit nozzles (sq in) |  | drillout, completions, bha, bit, hydraulics |
| `data.components[].name` | str | 2 7/8" P-110 |  | Display name of the component or record |  | drillout, completions, metadata, display |
| `data.components[].size` | null |  |  | Size in bytes |  | drillout, completions, metadata, storage |
| `data.components[].class` | str | Premium |  | Classification/condition of the component (e.g., Premium, Class 2) |  | drillout, completions, bha, component, condition |
| `data.components[].grade` | str | P110 |  | Steel grade of the component (e.g., S135, P110) |  | drillout, completions, bha, component, material |
| `data.components[].order` | int | 0 |  | Position order of component in the BHA (0 = top) |  | drillout, completions, bha, component, ordering |
| `data.components[].family` | str | dp |  | Component type family (dp, hwdp, dc, bit, mwd, pdm, etc.) |  | drillout, completions, bha, component, classification |
| `data.components[].length` | int | 31 |  | Length of the component (ft) |  | drillout, completions, bha, component, dimension |
| `data.components[].weight` | float | 192.2 |  | Total weight of the component (lbs) |  | drillout, completions, bha, component, dimension |
| `data.components[].expanded` | bool | False |  | Whether UI component is expanded (display state) |  | drillout, completions, ui, display, boolean |
| `data.components[].gauge_od` | null |  |  | Gauge outer diameter (in) |  | drillout, completions, bha, stabilizer, dimension |
| `data.components[].material` | str | Steel |  | Material type (e.g., Steel, Non-Magnetic) |  | drillout, completions, bha, component, material |
| `data.components[].blade_width` | null |  |  | Width of stabilizer/reamer blade (in) |  | drillout, completions, bha, stabilizer, dimension |
| `data.components[].gauge_length` | null |  |  | Gauge length (in) |  | drillout, completions, bha, stabilizer, dimension |
| `data.components[].linear_weight` | float | 6.2 |  | Weight per unit length (lbs/ft or ppf) |  | drillout, completions, bha, component, dimension |
| `data.components[].inner_diameter` | float | 2.32 |  | Inner diameter of the component (in) |  | drillout, completions, bha, component, dimension, hydraulics |
| `data.components[].outer_diameter` | float | 2.88 |  | Outer diameter of the component (in) |  | drillout, completions, bha, component, dimension |
| `data.components[].connection_type` | str | PH-6 |  | Thread connection type (e.g., 4.5" IF, NC50) |  | drillout, completions, bha, component, connection |
| `data.components[].component_length` | int | 31 |  | Length of the component (ft) |  | drillout, completions, bha, component, dimension |
| `data.components[].length_tooljoint` | float | 1.5 |  | Length of the tool joint (ft) |  | drillout, completions, bha, component, tooljoint |
| `data.components[].inner_diameter_tooljoint` | float | 2.27 |  | ID of the tool joint (in) |  | drillout, completions, bha, component, tooljoint |
| `data.components[].outer_diameter_tooljoint` | float | 3.44 |  | OD of the tool joint (in) |  | drillout, completions, bha, component, tooljoint |
| `data.start_depth` | int | 2 |  | Starting measured depth for this interval/run |  | drillout, completions, depth, interval, range |
| `data.viscous_drag` | bool | False |  | Whether viscous drag is enabled in T&D model |  | drillout, completions, bha, torque-drag, modeling, boolean |
| `data.calibrated_by` | int | 4523 |  | User ID who calibrated the drillstring |  | drillout, completions, bha, torque-drag, calibration, metadata |
| `data.calibrated_on` | int | 1584818616 |  | Timestamp when drillstring was calibrated |  | drillout, completions, bha, torque-drag, calibration, metadata |
| `data.is_exact_time` | bool | True |  | Whether the timestamp is exact (vs estimated) |  | drillout, completions, metadata, time, quality, boolean |
| `data.start_timestamp` | int | 1584797400 |  | Start timestamp of the interval/run (Unix epoch) |  | drillout, completions, time, interval, range |
| `data.setting_timestamp` | int | 1585503725 |  | Timestamp when the drillstring was set/configured |  | drillout, completions, bha, time, configuration |
| `version` | int | 1 |  | Schema version number for this record |  | drillout, completions, metadata, internal, versioning |
| `asset_id` | int | 39888507 |  | Unique identifier for the well/asset this record belongs to |  | drillout, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drillout, completions, metadata, internal |
| `timestamp` | int | 1584815620 |  | Unix epoch timestamp (seconds) of the record |  | drillout, completions, metadata, time-index, filter-key, required |
| `collection` | str | drillout.data.drillstring |  | MongoDB collection name this record belongs to |  | drillout, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drillout, completions, metadata, company, filter-key |

#### `corva#drillout.data.mud`

- **Friendly Name**: drillout.data.mud
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drillout.data.mud/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e9623524dbf264e2a2b3f2b |  | MongoDB document unique identifier |  | drillout, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drillout, completions, metadata, container |
| `data.date` | int | 1585590878 |  | Date |  | drillout, completions |
| `data.depth` | int | 1 |  | Depth |  | drillout, completions |
| `data.mud_type` | str | Water-base |  | Type classification for mud |  | drillout, completions, metadata, classification |
| `data.viscosity` | object |  |  | Nested object containing viscosity data |  | drillout, completions, container, object |
| `data.viscosity.pv` | int | 2 |  | Pv |  | drillout, completions |
| `data.viscosity.yp` | int | 2 |  | Yp |  | drillout, completions |
| `data.viscosity.rpm_readings` | array[unknown] |  |  | Array of rpm readings records |  | drillout, completions, container, array |
| `data.mud_density` | int | 9 |  | Mud density |  | drillout, completions |
| `data.setting_timestamp` | int | 1585515600 |  | Timestamp when the drillstring was set/configured |  | drillout, completions, bha, time, configuration |
| `version` | int | 1 |  | Schema version number for this record |  | drillout, completions, metadata, internal, versioning |
| `asset_id` | int | 39888507 |  | Unique identifier for the well/asset this record belongs to |  | drillout, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drillout, completions, metadata, internal |
| `timestamp` | int | 1585590889 |  | Unix epoch timestamp (seconds) of the record |  | drillout, completions, metadata, time-index, filter-key, required |
| `collection` | str | drillout.data.mud |  | MongoDB collection name this record belongs to |  | drillout, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drillout, completions, metadata, company, filter-key |

#### `corva#drillout.data.surface-equipment`

- **Friendly Name**: drillout.data.surface-equipment
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drillout.data.surface-equipment/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e9623524dbf264e2a2b3f2c |  | MongoDB document unique identifier |  | drillout, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drillout, completions, metadata, container |
| `data.block_weight` | int | 12 |  | Block weight |  | drillout, completions |
| `data.wob_threshold` | int | 60 |  | Wob threshold |  | drillout, completions |
| `data.drilling_phase` | str | drillout |  | Drilling phase |  | drillout, completions |
| `data.toolface_threshold` | int | 5 |  | Toolface threshold |  | drillout, completions |
| `data.flow_rate_threshold` | int | 1500 |  | Flow rate threshold |  | drillout, completions |
| `data.maximum_spp_capacity` | int | 7500 |  | Maximum spp capacity |  | drillout, completions |
| `data.rotary_rpm_threshold` | int | 200 |  | Rotary rpm threshold |  | drillout, completions |
| `data.lateral_footage_limit` | int | 1000 |  | Lateral footage limit |  | drillout, completions |
| `data.surface_back_pressure` | int | 1 |  | Pressure: surface back (psi) |  | drillout, completions, pressure, measurement |
| `data.maximum_hosting_capacity` | int | 750 |  | Maximum hosting capacity |  | drillout, completions |
| `data.toolface_accuracy_window` | int | 30 |  | Toolface accuracy window |  | drillout, completions |
| `data.maximum_td_torque_capacity` | int | 40 |  | Maximum td torque capacity |  | drillout, completions |
| `data.rocking_system_setting_rpm` | null |  |  | Rocking system setting rpm |  | drillout, completions |
| `data.surface_circulation_system` | str | type1 |  | Surface circulation system |  | drillout, completions |
| `version` | int | 1 |  | Schema version number for this record |  | drillout, completions, metadata, internal, versioning |
| `asset_id` | int | 39888507 |  | Unique identifier for the well/asset this record belongs to |  | drillout, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drillout, completions, metadata, internal |
| `timestamp` | int | 1585593602 |  | Unix epoch timestamp (seconds) of the record |  | drillout, completions, metadata, time-index, filter-key, required |
| `collection` | str | drillout.data.surface-equipment |  | MongoDB collection name this record belongs to |  | drillout, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drillout, completions, metadata, company, filter-key |

#### `corva#drillout.torque-and-drag.axial-load`

- **Friendly Name**: drillout.torque-and-drag.axial-load
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drillout.torque-and-drag.axial-load/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e962c4f4dbf264ebd2b82cb |  | MongoDB document unique identifier |  | drillout, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drillout, completions, metadata, container |
| `data.points` | array[dict] |  |  | Array of points records |  | drillout, completions, container, array |
| `data.points[].axial_load` | float | 25.73 |  | Axial force along the drill string (klbs) |  | drillout, completions, torque-drag, calculated, modeling |
| `data.points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | drillout, completions, depth, survey, directional |
| `data.points[].helical_buckling_force` | float | -4.66 |  | Helical buckling force |  | drillout, completions |
| `data.points[].sinusoidal_buckling_force` | float | -1.65 |  | Sinusoidal buckling force |  | drillout, completions |
| `data.status` | int | 0 |  | Current status of the record/check |  | drillout, completions, metadata, status |
| `data.activity` | str | Run in Hole |  | Activity code number |  | drillout, completions, operations, activity, classification |
| `data.buckling` | str |  |  | Buckling state/load of drill string |  | drillout, completions, torque-drag, calculated, risk |
| `data.hookload` | float | 39.92 |  | Weight hanging from the hook (klbs) |  | drillout, completions, drilling, hookload, real-time, torque-drag |
| `data.pipe_stretch` | float | 0.95 |  | Pipe stretch |  | drillout, completions |
| `data.buckling_ranges` | array[unknown] |  |  | Array of buckling ranges records |  | drillout, completions, container, array |
| `version` | int | 1 |  | Schema version number for this record |  | drillout, completions, metadata, internal, versioning |
| `asset_id` | int | 39888507 |  | Unique identifier for the well/asset this record belongs to |  | drillout, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drillout, completions, metadata, internal |
| `timestamp` | int | 1585507218 |  | Unix epoch timestamp (seconds) of the record |  | drillout, completions, metadata, time-index, filter-key, required |
| `collection` | str | drillout.torque-and-drag.axial-load |  | MongoDB collection name this record belongs to |  | drillout, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drillout, completions, metadata, company, filter-key |

#### `corva#drillout.torque-and-drag.hookload-trend`

- **Friendly Name**: drillout.torque-and-drag.hookload-trend
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drillout.torque-and-drag.hookload-trend/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e962c0ba1213d513142a754 |  | MongoDB document unique identifier |  | drillout, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drillout, completions, metadata, container |
| `data.actual` | object |  |  | Nested object containing actual data |  | drillout, completions, container, object |
| `data.actual.pick_up` | array[unknown] |  |  | Array of pick up records |  | drillout, completions, container, array |
| `data.actual.ream_in` | array[unknown] |  |  | Array of ream in records |  | drillout, completions, container, array |
| `data.actual.wash_up` | array[unknown] |  |  | Array of wash up records |  | drillout, completions, container, array |
| `data.actual.ream_out` | array[unknown] |  |  | Array of ream out records |  | drillout, completions, container, array |
| `data.actual.slack_off` | array[unknown] |  |  | Array of slack off records |  | drillout, completions, container, array |
| `data.actual.wash_down` | array[unknown] |  |  | Array of wash down records |  | drillout, completions, container, array |
| `data.actual.rotary_off_bottom` | array[unknown] |  |  | Array of rotary off bottom records |  | drillout, completions, container, array |
| `data.config` | object |  |  | Nested object containing config data |  | drillout, completions, container, object |
| `data.config.id` | int | 1 |  | Numeric identifier for this record/run |  | drillout, completions, metadata, identifier |
| `data.config._id` | str | 5e9623524dbf264e2a2b3f2a |  | Configuration parameter:  id |  | drillout, completions, configuration, settings |
| `data.config.type` | str | DrillString |  | Type classifier for this record |  | drillout, completions, metadata, classification |
| `data.config.hole_size` | float | 4.63 |  | Configuration parameter: hole size |  | drillout, completions, configuration, settings |
| `data.curves` | object |  |  | Nested object containing curves data |  | drillout, completions, container, object |
| `data.curves.pick_up` | array[dict] |  |  | Array of pick up records |  | drillout, completions, container, array |
| `data.curves.pick_up[].points` | array[dict] |  |  | Array of points records |  | drillout, completions, container, array |
| `data.curves.pick_up[].points[].hookload` | int | 12 |  | Weight hanging from the hook (klbs) |  | drillout, completions, drilling, hookload, real-time, torque-drag |
| `data.curves.pick_up[].points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | drillout, completions, depth, survey, directional |
| `data.curves.pick_up[].casing_friction_factor` | float | 0.15 |  | Casing friction factor |  | drillout, completions |
| `data.curves.pick_up[].openhole_friction_factor` | float | 0.1 |  | Openhole friction factor |  | drillout, completions |
| `data.curves.slack_off` | array[dict] |  |  | Array of slack off records |  | drillout, completions, container, array |
| `data.curves.slack_off[].points` | array[dict] |  |  | Array of points records |  | drillout, completions, container, array |
| `data.curves.slack_off[].points[].hookload` | int | 12 |  | Weight hanging from the hook (klbs) |  | drillout, completions, drilling, hookload, real-time, torque-drag |
| `data.curves.slack_off[].points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | drillout, completions, depth, survey, directional |
| `data.curves.slack_off[].casing_friction_factor` | float | 0.15 |  | Casing friction factor |  | drillout, completions |
| `data.curves.slack_off[].openhole_friction_factor` | float | 0.1 |  | Openhole friction factor |  | drillout, completions |
| `data.curves.rotary_off_bottom` | array[dict] |  |  | Array of rotary off bottom records |  | drillout, completions, container, array |
| `data.curves.rotary_off_bottom[].points` | array[dict] |  |  | Array of points records |  | drillout, completions, container, array |
| `data.curves.rotary_off_bottom[].points[].torque` | int | 0 |  | Rotary torque at surface (ft-lbs) |  | drillout, completions, drilling, torque, real-time, torque-drag |
| `data.curves.rotary_off_bottom[].points[].hookload` | int | 12 |  | Weight hanging from the hook (klbs) |  | drillout, completions, drilling, hookload, real-time, torque-drag |
| `data.curves.rotary_off_bottom[].points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | drillout, completions, depth, survey, directional |
| `data.curves.rotary_off_bottom[].flow_rate` | int | 0 |  | Rate: flow |  | drillout, completions, rate, measurement |
| `data.curves.rotary_off_bottom[].casing_friction_factor` | int | 0 |  | Casing friction factor |  | drillout, completions |
| `data.curves.rotary_off_bottom[].openhole_friction_factor` | int | 0 |  | Openhole friction factor |  | drillout, completions |
| `data.status` | int | 0 |  | Current status of the record/check |  | drillout, completions, metadata, status |
| `data.activity` | str | Run in Hole |  | Activity code number |  | drillout, completions, operations, activity, classification |
| `data.outliers` | object |  |  | Nested object containing outliers data |  | drillout, completions, container, object |
| `data.outliers.pick_up` | array[unknown] |  |  | Array of pick up records |  | drillout, completions, container, array |
| `data.outliers.ream_in` | array[unknown] |  |  | Array of ream in records |  | drillout, completions, container, array |
| `data.outliers.wash_up` | array[unknown] |  |  | Array of wash up records |  | drillout, completions, container, array |
| `data.outliers.ream_out` | array[unknown] |  |  | Array of ream out records |  | drillout, completions, container, array |
| `data.outliers.slack_off` | array[unknown] |  |  | Array of slack off records |  | drillout, completions, container, array |
| `data.outliers.wash_down` | array[unknown] |  |  | Array of wash down records |  | drillout, completions, container, array |
| `data.outliers.rotary_off_bottom` | array[unknown] |  |  | Array of rotary off bottom records |  | drillout, completions, container, array |
| `data.hole_depth` | float | 2908.69 |  | Current hole depth (bottom of wellbore) |  | drillout, completions, depth, drilling, real-time, key-metric |
| `data.is_extended` | bool | False |  | Flag indicating whether is extended |  | drillout, completions, boolean, flag |
| `data.has_confidence` | bool | True |  | Flag indicating whether has confidence |  | drillout, completions, boolean, flag |
| `data.activity_groups` | object |  |  | Nested object containing activity groups data |  | drillout, completions, container, object |
| `data.activity_groups.end_timestamp` | int | 1585505003 |  | End timestamp of the interval/run (Unix epoch) |  | drillout, completions, time, interval, range |
| `data.activity_groups.start_timestamp` | int | 1585505003 |  | Start timestamp of the interval/run (Unix epoch) |  | drillout, completions, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | drillout, completions, metadata, internal, versioning |
| `asset_id` | int | 39888507 |  | Unique identifier for the well/asset this record belongs to |  | drillout, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drillout, completions, metadata, internal |
| `timestamp` | int | 1585505003 |  | Unix epoch timestamp (seconds) of the record |  | drillout, completions, metadata, time-index, filter-key, required |
| `collection` | str | drillout.torque-and-drag.hookload-trend |  | MongoDB collection name this record belongs to |  | drillout, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drillout, completions, metadata, company, filter-key |

#### `corva#drillout.torque-and-drag.stress`

- **Friendly Name**: drillout.torque-and-drag.stress
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drillout.torque-and-drag.stress/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e962c4f4dbf264ebd2b82ca |  | MongoDB document unique identifier |  | drillout, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drillout, completions, metadata, container |
| `data.points` | array[dict] |  |  | Array of points records |  | drillout, completions, container, array |
| `data.points[].axial_stress` | float | 12209.9 |  | Axial stress |  | drillout, completions |
| `data.points[].twist_stress` | float | 4090.6 |  | Twist stress |  | drillout, completions |
| `data.points[].yield_stress` | int | 110000 |  | Yield stress |  | drillout, completions |
| `data.points[].bending_stress` | int | 0 |  | Bending stress |  | drillout, completions |
| `data.points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | drillout, completions, depth, survey, directional |
| `data.points[].von_mises_stress` | float | 14116.6 |  | Von mises stress |  | drillout, completions |
| `data.points[].yield_stress_60_percent` | int | 66000 |  | Yield stress 60 percent |  | drillout, completions |
| `data.points[].yield_stress_80_percent` | int | 88000 |  | Yield stress 80 percent |  | drillout, completions |
| `data.status` | int | 0 |  | Current status of the record/check |  | drillout, completions, metadata, status |
| `data.activity` | str | Run in Hole |  | Activity code number |  | drillout, completions, operations, activity, classification |
| `data.stress_yield_ranges` | str |  |  | Stress yield ranges |  | drillout, completions |
| `version` | int | 1 |  | Schema version number for this record |  | drillout, completions, metadata, internal, versioning |
| `asset_id` | int | 39888507 |  | Unique identifier for the well/asset this record belongs to |  | drillout, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drillout, completions, metadata, internal |
| `timestamp` | int | 1585507218 |  | Unix epoch timestamp (seconds) of the record |  | drillout, completions, metadata, time-index, filter-key, required |
| `collection` | str | drillout.torque-and-drag.stress |  | MongoDB collection name this record belongs to |  | drillout, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drillout, completions, metadata, company, filter-key |

#### `corva#drillout.torque-and-drag.torque-trend`

- **Friendly Name**: drillout.torque-and-drag.torque-trend
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drillout.torque-and-drag.torque-trend/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e962c0ba1213d513142a755 |  | MongoDB document unique identifier |  | drillout, completions, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | drillout, completions, metadata, container |
| `data.actual` | object |  |  | Nested object containing actual data |  | drillout, completions, container, object |
| `data.actual.ream_in` | array[unknown] |  |  | Array of ream in records |  | drillout, completions, container, array |
| `data.actual.ream_out` | array[unknown] |  |  | Array of ream out records |  | drillout, completions, container, array |
| `data.actual.rotary_off_bottom` | array[unknown] |  |  | Array of rotary off bottom records |  | drillout, completions, container, array |
| `data.config` | object |  |  | Nested object containing config data |  | drillout, completions, container, object |
| `data.config.id` | int | 1 |  | Numeric identifier for this record/run |  | drillout, completions, metadata, identifier |
| `data.config._id` | str | 5e9623524dbf264e2a2b3f2a |  | Configuration parameter:  id |  | drillout, completions, configuration, settings |
| `data.config.type` | str | DrillString |  | Type classifier for this record |  | drillout, completions, metadata, classification |
| `data.config.hole_size` | float | 4.63 |  | Configuration parameter: hole size |  | drillout, completions, configuration, settings |
| `data.curves` | object |  |  | Nested object containing curves data |  | drillout, completions, container, object |
| `data.curves.rotary_off_bottom` | array[dict] |  |  | Array of rotary off bottom records |  | drillout, completions, container, array |
| `data.curves.rotary_off_bottom[].points` | array[dict] |  |  | Array of points records |  | drillout, completions, container, array |
| `data.curves.rotary_off_bottom[].points[].torque` | int | 0 |  | Rotary torque at surface (ft-lbs) |  | drillout, completions, drilling, torque, real-time, torque-drag |
| `data.curves.rotary_off_bottom[].points[].hookload` | int | 12 |  | Weight hanging from the hook (klbs) |  | drillout, completions, drilling, hookload, real-time, torque-drag |
| `data.curves.rotary_off_bottom[].points[].measured_depth` | int | 0 |  | Measured depth along the wellbore path |  | drillout, completions, depth, survey, directional |
| `data.curves.rotary_off_bottom[].casing_friction_factor` | float | 0.15 |  | Casing friction factor |  | drillout, completions |
| `data.curves.rotary_off_bottom[].openhole_friction_factor` | float | 0.1 |  | Openhole friction factor |  | drillout, completions |
| `data.status` | int | 0 |  | Current status of the record/check |  | drillout, completions, metadata, status |
| `data.activity` | str | Run in Hole |  | Activity code number |  | drillout, completions, operations, activity, classification |
| `data.outliers` | object |  |  | Nested object containing outliers data |  | drillout, completions, container, object |
| `data.outliers.ream_in` | array[unknown] |  |  | Array of ream in records |  | drillout, completions, container, array |
| `data.outliers.ream_out` | array[unknown] |  |  | Array of ream out records |  | drillout, completions, container, array |
| `data.outliers.rotary_off_bottom` | array[unknown] |  |  | Array of rotary off bottom records |  | drillout, completions, container, array |
| `data.flow_rate` | int | 0 |  | Rate: flow |  | drillout, completions, rate, measurement |
| `data.hole_depth` | float | 2908.69 |  | Current hole depth (bottom of wellbore) |  | drillout, completions, depth, drilling, real-time, key-metric |
| `data.is_extended` | bool | False |  | Flag indicating whether is extended |  | drillout, completions, boolean, flag |
| `data.has_confidence` | bool | True |  | Flag indicating whether has confidence |  | drillout, completions, boolean, flag |
| `data.activity_groups` | object |  |  | Nested object containing activity groups data |  | drillout, completions, container, object |
| `data.activity_groups.end_timestamp` | int | 1585505003 |  | End timestamp of the interval/run (Unix epoch) |  | drillout, completions, time, interval, range |
| `data.activity_groups.start_timestamp` | int | 1585505003 |  | Start timestamp of the interval/run (Unix epoch) |  | drillout, completions, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | drillout, completions, metadata, internal, versioning |
| `asset_id` | int | 39888507 |  | Unique identifier for the well/asset this record belongs to |  | drillout, completions, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | drillout, completions, metadata, internal |
| `timestamp` | int | 1585505003 |  | Unix epoch timestamp (seconds) of the record |  | drillout, completions, metadata, time-index, filter-key, required |
| `collection` | str | drillout.torque-and-drag.torque-trend |  | MongoDB collection name this record belongs to |  | drillout, completions, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | drillout, completions, metadata, company, filter-key |

### 13. Anti-Collision

#### `corva#anti-collision.metadata-edm`

- **Friendly Name**: anti-collision.metadata-edm
- **Data Type**: reference
- **API Path**: `/api/v1/data/corva/anti-collision.metadata-edm/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 67940b3ab08f74f18468f016 |  | MongoDB document unique identifier |  | anti-collision, directional, safety, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | anti-collision, directional, safety, metadata, container |
| `data.wells` | array[dict] |  |  | Array of wells records |  | anti-collision, directional, safety, container, array |
| `data.wells[].api_number` | int | 4246142919 |  | API well number (unique well identifier) |  | anti-collision, directional, safety, well-info, identifier, regulatory |
| `data.wells[].latitude_deg` | float | 31.49318565189394 |  | Well latitude in decimal degrees |  | anti-collision, directional, safety, well-info, coordinate, location |
| `data.wells[].longitude_deg` | float | -102.0585495249621 |  | Well longitude in decimal degrees |  | anti-collision, directional, safety, well-info, coordinate, location |
| `data.wells[].well_common_name` | str | EAGLE PASS C5 5411BH |  | Common/display name of the well |  | anti-collision, directional, safety, well-info, identifier, display |
| `data.file_hash` | str | f5f7dad8a8820bd1b930dfb275810518 |  | Hash of the uploaded file for deduplication |  | anti-collision, directional, safety, metadata, file, internal |
| `data.file_link` | str | anti-collision-edm/80/67940b267ae07be936140798/... |  | Storage path/URL of the uploaded file |  | anti-collision, directional, safety, metadata, file, storage |
| `data.file_name` | str | EAGLE_PASS_PROJECT_01092025replaced.edm.xml |  | Original filename of the uploaded file |  | anti-collision, directional, safety, metadata, file |
| `data.export_level` | str | Site |  | Export/scope level (Site, Well, etc.) |  | anti-collision, directional, safety, metadata, scope |
| `data.last_updated_at` | int | 1736446771 |  | Timestamp of last update |  | anti-collision, directional, safety, metadata, time, audit |
| `version` | int | 1 |  | Schema version number for this record |  | anti-collision, directional, safety, metadata, internal, versioning |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | anti-collision, directional, safety, metadata, internal |
| `timestamp` | int | 1737755450 |  | Unix epoch timestamp (seconds) of the record |  | anti-collision, directional, safety, metadata, time-index, filter-key, required |
| `collection` | str | anti-collision.metadata-edm |  | MongoDB collection name this record belongs to |  | anti-collision, directional, safety, metadata, internal |
| `company_id` | int | 80 |  | Unique identifier for the company/operator |  | anti-collision, directional, safety, metadata, company, filter-key |

#### `corva#anti-collision.metadata-well`

- **Friendly Name**: anti-collision.metadata-well
- **Data Type**: reference
- **API Path**: `/api/v1/data/corva/anti-collision.metadata-well/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 67940b3ac8732cabc46592a2 |  | MongoDB document unique identifier |  | anti-collision, directional, safety, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | anti-collision, directional, safety, metadata, container |
| `data.files` | array[dict] |  |  | Array of files records |  | anti-collision, directional, safety, container, array |
| `data.files[].file_hash` | str | f5f7dad8a8820bd1b930dfb275810518 |  | Hash of the uploaded file for deduplication |  | anti-collision, directional, safety, metadata, file, internal |
| `data.files[].file_link` | str | anti-collision-edm/80/67940b267ae07be936140798/... |  | Storage path/URL of the uploaded file |  | anti-collision, directional, safety, metadata, file, storage |
| `data.files[].file_name` | str | EAGLE_PASS_PROJECT_01092025replaced.edm.xml |  | Original filename of the uploaded file |  | anti-collision, directional, safety, metadata, file |
| `data.files[].export_level` | str | Site |  | Export/scope level (Site, Well, etc.) |  | anti-collision, directional, safety, metadata, scope |
| `data.files[].latest_updated_at` | int | 1736446771 |  | Timestamp for latest updated |  | anti-collision, directional, safety, metadata, time |
| `data.api_number` | int | 4246140000 |  | API well number (unique well identifier) |  | anti-collision, directional, safety, well-info, identifier, regulatory |
| `data.latitude_deg` | float | 31.49086178639833 |  | Well latitude in decimal degrees |  | anti-collision, directional, safety, well-info, coordinate, location |
| `data.longitude_deg` | float | -102.0658076204951 |  | Well longitude in decimal degrees |  | anti-collision, directional, safety, well-info, coordinate, location |
| `data.well_common_name` | str | EAGLE PASS B6 5913BH |  | Common/display name of the well |  | anti-collision, directional, safety, well-info, identifier, display |
| `version` | int | 1 |  | Schema version number for this record |  | anti-collision, directional, safety, metadata, internal, versioning |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | anti-collision, directional, safety, metadata, internal |
| `timestamp` | int | 1737755450 |  | Unix epoch timestamp (seconds) of the record |  | anti-collision, directional, safety, metadata, time-index, filter-key, required |
| `collection` | str | anti-collision.metadata-well |  | MongoDB collection name this record belongs to |  | anti-collision, directional, safety, metadata, internal |
| `company_id` | int | 80 |  | Unique identifier for the company/operator |  | anti-collision, directional, safety, metadata, company, filter-key |

### 14. Formation Evaluation

#### `corva#formation-evaluation.metadata`

- **Friendly Name**: formation-evaluation.metadata
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/formation-evaluation.metadata/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 611fb39d71603b61983e731e |  | MongoDB document unique identifier |  | formation, evaluation, geology, metadata, internal, primary-key |
| `app` | str | tasks.formation-evaluation-importer-task |  | App |  | formation, evaluation, geology |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | formation, evaluation, geology, metadata, container |
| `data.well` | object |  |  | Nested object containing well data |  | formation, evaluation, geology, container, object |
| `data.well.data` | array[dict] |  |  | Array of data records |  | formation, evaluation, geology, container, array |
| `data.well.data[].data` | object |  |  | Nested object containing data data |  | formation, evaluation, geology, container, object |
| `data.well.data[].data.unit` | str | FT |  | Unit |  | formation, evaluation, geology |
| `data.well.data[].data.value` | str | 6685.0000 |  | Value |  | formation, evaluation, geology |
| `data.well.data[].data.mnemonic` | str | STRT |  | Mnemonic |  | formation, evaluation, geology |
| `data.well.data[].data.description` | str | FIRST INDEX VALUE |  | Description |  | formation, evaluation, geology |
| `data.well.data[].mapping` | object |  |  | Nested object containing mapping data |  | formation, evaluation, geology, container, object |
| `data.well.data[].mapping.unit` | str | ft |  | Unit |  | formation, evaluation, geology |
| `data.well.data[].mapping.bucket` | str | Length |  | Bucket |  | formation, evaluation, geology |
| `data.well.data[].mapping.mnemonic` | str | STRT |  | Mnemonic |  | formation, evaluation, geology |
| `data.curve` | object |  |  | Nested object containing curve data |  | formation, evaluation, geology, container, object |
| `data.curve.data` | array[dict] |  |  | Array of data records |  | formation, evaluation, geology, container, array |
| `data.curve.data[].data` | object |  |  | Nested object containing data data |  | formation, evaluation, geology, container, object |
| `data.curve.data[].data.unit` | str | FT |  | Unit |  | formation, evaluation, geology |
| `data.curve.data[].data.value` | str | 0 000 00 00 |  | Value |  | formation, evaluation, geology |
| `data.curve.data[].data.mnemonic` | str | DEPT |  | Mnemonic |  | formation, evaluation, geology |
| `data.curve.data[].data.description` | str | Depth |  | Description |  | formation, evaluation, geology |
| `data.curve.data[].mapping` | object |  |  | Nested object containing mapping data |  | formation, evaluation, geology, container, object |
| `data.curve.data[].mapping.unit` | str | ft |  | Unit |  | formation, evaluation, geology |
| `data.curve.data[].mapping.bucket` | str | Length |  | Bucket |  | formation, evaluation, geology |
| `data.curve.data[].mapping.mnemonic` | str | md |  | Mnemonic |  | formation, evaluation, geology |
| `data.other` | object |  |  | Nested object containing other data |  | formation, evaluation, geology, container, object |
| `data.other.data` | str |  |  | Data |  | formation, evaluation, geology |
| `data.params` | object |  |  | Nested object containing params data |  | formation, evaluation, geology, container, object |
| `data.params.error` | object |  |  | Nested object containing error data |  | formation, evaluation, geology, container, object |
| `data.params.error.name` | str | PropertyError |  | Display name of the component or record |  | formation, evaluation, geology, metadata, display |
| `data.params.error.message` | str | Property param doesn't exist |  | Message |  | formation, evaluation, geology |
| `file` | str | _4H_RCBL.las |  | File |  | formation, evaluation, geology |
| `version` | int | 1 |  | Schema version number for this record |  | formation, evaluation, geology, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | formation, evaluation, geology, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | formation, evaluation, geology, metadata, internal |
| `timestamp` | int | 1629467549 |  | Unix epoch timestamp (seconds) of the record |  | formation, evaluation, geology, metadata, time-index, filter-key, required |
| `collection` | str | formation-evaluation.metadata |  | MongoDB collection name this record belongs to |  | formation, evaluation, geology, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | formation, evaluation, geology, metadata, company, filter-key |
| `records_count` | int | 13327 |  | Count of records |  | formation, evaluation, geology, aggregation, count |

### 15. Predictive Drilling / ML

#### `corva#machine-learning.rop`

- **Friendly Name**: machine-learning.rop
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/machine-learning.rop/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3856c880170905957da |  | MongoDB document unique identifier |  | machine-learning, prediction, optimization, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | machine-learning, prediction, optimization, metadata, container |
| `data.state` | str | In Slips |  | State |  | machine-learning, prediction, optimization |
| `data.rop_limit` | null |  |  | Rop limit |  | machine-learning, prediction, optimization |
| `data.wob_limit` | null |  |  | Wob limit |  | machine-learning, prediction, optimization |
| `data.actual_rpm` | null |  |  | Actual rpm |  | machine-learning, prediction, optimization |
| `data.actual_wob` | int | 0 |  | Actual wob |  | machine-learning, prediction, optimization |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | machine-learning, prediction, optimization, depth, drilling, real-time, key-metric |
| `data.rpm_limits` | null |  |  | Rpm limits |  | machine-learning, prediction, optimization |
| `data.updated_at` | null |  |  | Timestamp for updated |  | machine-learning, prediction, optimization, metadata, time |
| `data.actual_diff` | null |  |  | Actual diff |  | machine-learning, prediction, optimization |
| `data.current_rop` | null |  |  | Current rop |  | machine-learning, prediction, optimization |
| `data.current_rpm` | null |  |  | Current rpm |  | machine-learning, prediction, optimization |
| `data.diff_limits` | null |  |  | Diff limits |  | machine-learning, prediction, optimization |
| `data.inclination` | int | 0 |  | Wellbore inclination angle from vertical (degrees) |  | machine-learning, prediction, optimization, directional, survey, key-metric |
| `data.lower_bound` | null |  |  | Lower bound |  | machine-learning, prediction, optimization |
| `data.optimum_rpm` | null |  |  | Optimum rpm |  | machine-learning, prediction, optimization |
| `data.rpm_per_min` | null |  |  | Rpm per min |  | machine-learning, prediction, optimization |
| `data.ssi_per_min` | null |  |  | Ssi per min |  | machine-learning, prediction, optimization |
| `data.upper_bound` | null |  |  | Upper bound |  | machine-learning, prediction, optimization |
| `data.var_per_min` | null |  |  | Var per min |  | machine-learning, prediction, optimization |
| `data.actual_value` | null |  |  | Actual value |  | machine-learning, prediction, optimization |
| `data.current_diff` | null |  |  | Current diff |  | machine-learning, prediction, optimization |
| `data.diff_per_min` | null |  |  | Diff per min |  | machine-learning, prediction, optimization |
| `data.optimum_diff` | null |  |  | Optimum diff |  | machine-learning, prediction, optimization |
| `data.torque_limit` | null |  |  | Torque limit |  | machine-learning, prediction, optimization |
| `data.actual_torque` | int | 0 |  | Actual torque |  | machine-learning, prediction, optimization |
| `data.optimized_mse` | null |  |  | Optimized mse |  | machine-learning, prediction, optimization |
| `data.optimized_rop` | null |  |  | Optimized rop |  | machine-learning, prediction, optimization |
| `data.recommendation` | null |  |  | Recommendation |  | machine-learning, prediction, optimization |
| `data.timestamp_mean` | null |  |  | Timestamp mean |  | machine-learning, prediction, optimization |
| `data.hole_depth_mean` | null |  |  | Hole depth mean |  | machine-learning, prediction, optimization |
| `data.predicted_value` | null |  |  | Predicted value |  | machine-learning, prediction, optimization |
| `data.confidence_level` | null |  |  | Confidence level |  | machine-learning, prediction, optimization |
| `data.current_flowrate` | null |  |  | Current flowrate |  | machine-learning, prediction, optimization |
| `data.error_prediction` | null |  |  | Error prediction |  | machine-learning, prediction, optimization |
| `data.ssi_per_min_category` | null |  |  | Ssi per min category |  | machine-learning, prediction, optimization |
| `data.var_per_min_category` | null |  |  | Var per min category |  | machine-learning, prediction, optimization |
| `data.wob_expected_optimal` | null |  |  | Wob expected optimal |  | machine-learning, prediction, optimization |
| `data.recommendation_source` | null |  |  | Recommendation source |  | machine-learning, prediction, optimization |
| `data.torque_expected_optimal` | null |  |  | Torque expected optimal |  | machine-learning, prediction, optimization |
| `data.optimization_params_result` | null |  |  | Optimization params result |  | machine-learning, prediction, optimization |
| `version` | int | 1 |  | Schema version number for this record |  | machine-learning, prediction, optimization, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | machine-learning, prediction, optimization, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | machine-learning, prediction, optimization, metadata, internal |
| `timestamp` | int | 1545149819 |  | Unix epoch timestamp (seconds) of the record |  | machine-learning, prediction, optimization, metadata, time-index, filter-key, required |
| `collection` | str | machine-learning.rop |  | MongoDB collection name this record belongs to |  | machine-learning, prediction, optimization, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | machine-learning, prediction, optimization, metadata, company, filter-key |

### 16. Metrics / KPIs

#### `corva#metrics`

- **Friendly Name**: metrics
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/metrics/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f63013aed6000924133a |  | MongoDB document unique identifier |  | metrics, kpi, performance, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | metrics, kpi, performance, metadata, container |
| `data.key` | str | hole_depth_change |  | Key |  | metrics, kpi, performance |
| `data.type` | str | bha |  | Type classifier for this record |  | metrics, kpi, performance, metadata, classification |
| `data.value` | int | 0 |  | Value |  | metrics, kpi, performance |
| `data.bha_id` | int | 1 |  | BHA/drillstring run number identifier |  | metrics, kpi, performance, bha, reference, link |
| `data.rig_id` | int | 43 |  | Identifier for rig |  | metrics, kpi, performance, metadata, identifier, reference |
| `data.asset_id` | int | 31659357 |  | Identifier for asset |  | metrics, kpi, performance, metadata, identifier, reference |
| `data.company_id` | int | 5 |  | Identifier for company |  | metrics, kpi, performance, metadata, identifier, reference |
| `data.program_id` | int | 38 |  | Identifier for program |  | metrics, kpi, performance, metadata, identifier, reference |
| `data.well_sections` | array[unknown] |  |  | Array of well sections records |  | metrics, kpi, performance, container, array |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | metrics, kpi, performance, metadata, well-id, filter-key, required |
| `metadata` | object |  |  | Nested object containing metadata data |  | metrics, kpi, performance, container, object |
| `metadata.timezone` | str | America/Chicago |  | Timezone |  | metrics, kpi, performance |
| `timestamp` | int | 1545485398 |  | Unix epoch timestamp (seconds) of the record |  | metrics, kpi, performance, metadata, time-index, filter-key, required |
| `collection` | str | metrics |  | MongoDB collection name this record belongs to |  | metrics, kpi, performance, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | metrics, kpi, performance, metadata, company, filter-key |

### 17. Production (Enverus)

#### `corva#production.wits`

- **Friendly Name**: production.wits
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/production.wits/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 63ff1bd50a113b5684d9a06b |  | MongoDB document unique identifier |  | production, enverus, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | production, enverus, metadata, container |
| `data.is_valid` | bool | True |  | Flag indicating whether is valid |  | production, enverus, boolean, flag |
| `data.timestamp` | int | 1677562537 |  | Timestamp |  | production, enverus |
| `data.casing_pressure` | float | 47.557 |  | Pressure: casing (psi) |  | production, enverus, pressure, measurement |
| `data.tubing_pressure` | int | 0 |  | Pressure: tubing (psi) |  | production, enverus, pressure, measurement |
| `data.downhole_pressure` | int | 24318 |  | Pressure: downhole (psi) |  | production, enverus, pressure, measurement |
| `data.flowline_pressure` | float | 14847.72103666666 |  | Pressure: flowline (psi) |  | production, enverus, pressure, measurement |
| `data.surface_casing_pressure` | int | 0 |  | Pressure: surface casing (psi) |  | production, enverus, pressure, measurement |
| `data.intermediate_casing_pressure` | float | 14354.90934952312 |  | Pressure: intermediate casing (psi) |  | production, enverus, pressure, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | production, enverus, metadata, internal, versioning |
| `asset_id` | int | 50806874 |  | Unique identifier for the well/asset this record belongs to |  | production, enverus, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | production, enverus, metadata, internal |
| `timestamp` | int | 1677562537 |  | Unix epoch timestamp (seconds) of the record |  | production, enverus, metadata, time-index, filter-key, required |
| `collection` | str | production.wits |  | MongoDB collection name this record belongs to |  | production, enverus, metadata, internal |
| `company_id` | int | 25 |  | Unique identifier for the company/operator |  | production, enverus, metadata, company, filter-key |

### 18. Wellness / Check-Up

#### `corva#wellness_rule_settings_history`

- **Friendly Name**: wellness_rule_settings_history
- **Data Type**: reference
- **API Path**: `/api/v1/data/corva/wellness_rule_settings_history/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 6514536163f24e923604a6e2 |  | MongoDB document unique identifier |  | wellness, data-quality, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wellness, data-quality, metadata, container |
| `data.name` | str | Add Placeholder BHA |  | Display name of the component or record |  | wellness, data-quality, metadata, display |
| `data.package` | str | bha.add_placeholder_bha |  | Package |  | wellness, data-quality |
| `data.rule_id` | str | 6514536163f24e923604a6e2 |  | Identifier for rule |  | wellness, data-quality, metadata, identifier, reference |
| `data.version` | int | 1 |  | Version |  | wellness, data-quality |
| `data.category` | str | BHA |  | Category |  | wellness, data-quality |
| `data.internal` | bool | True |  | Flag indicating whether internal |  | wellness, data-quality, boolean, flag |
| `data.interval` | object |  |  | Nested object containing interval data |  | wellness, data-quality, container, object |
| `data.interval.type` | str | time |  | Type classifier for this record |  | wellness, data-quality, metadata, classification |
| `data.interval.cache_key` | str | check_placeholder_bha |  | Cache key |  | wellness, data-quality |
| `data.interval.interval_seconds` | int | 600 |  | Interval seconds |  | wellness, data-quality |
| `data.file_name` | str | check_placeholder_bha |  | Original filename of the uploaded file |  | wellness, data-quality, metadata, file |
| `data.life_cycle` | array[unknown] |  |  | Array of life cycle records |  | wellness, data-quality, container, array |
| `data.entry_point` | str | check_placeholder_bha |  | Entry point |  | wellness, data-quality |
| `data.environment` | str | drilling |  | Environment |  | wellness, data-quality |
| `data.point_allocation` | int | 10 |  | Point allocation |  | wellness, data-quality |
| `version` | int | 1 |  | Schema version number for this record |  | wellness, data-quality, metadata, internal, versioning |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wellness, data-quality, metadata, internal |
| `timestamp` | int | 1695830839 |  | Unix epoch timestamp (seconds) of the record |  | wellness, data-quality, metadata, time-index, filter-key, required |
| `collection` | str | wellness_rule_settings |  | MongoDB collection name this record belongs to |  | wellness, data-quality, metadata, internal |
| `company_id` | int | 3 |  | Unique identifier for the company/operator |  | wellness, data-quality, metadata, company, filter-key |

### 19. Launchpad / Connectivity

#### `corva#launchpad_witsml_recommendations`

- **Friendly Name**: launchpad_witsml_recommendations
- **Data Type**: reference
- **API Path**: `/api/v1/data/corva/launchpad_witsml_recommendations/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 6786b8044eb1ebf0d2e9cdab |  | MongoDB document unique identifier |  | connectivity, witsml, launchpad, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | connectivity, witsml, launchpad, metadata, container |
| `data.log_id` | null |  |  | Identifier for log |  | connectivity, witsml, launchpad, metadata, identifier, reference |
| `data.rig_id` | int | 2238 |  | Identifier for rig |  | connectivity, witsml, launchpad, metadata, identifier, reference |
| `data.status` | str | archived |  | Current status of the record/check |  | connectivity, witsml, launchpad, metadata, status |
| `data.rig_name` | str | Akita 14 |  | Name/label for rig |  | connectivity, witsml, launchpad, metadata, display, label |
| `data.bit_depth` | null |  |  | Current depth of the drill bit |  | connectivity, witsml, launchpad, depth, drilling, real-time, key-metric |
| `data.team_name` | str | Texas Tea |  | Name/label for team |  | connectivity, witsml, launchpad, metadata, display, label |
| `data.company_id` | int | 81 |  | Identifier for company |  | connectivity, witsml, launchpad, metadata, identifier, reference |
| `data.hole_depth` | null |  |  | Current hole depth (bottom of wellbore) |  | connectivity, witsml, launchpad, depth, drilling, real-time, key-metric |
| `data.company_name` | str | Shell |  | Name/label for company |  | connectivity, witsml, launchpad, metadata, display, label |
| `data.edr_provider` | null |  |  | Edr provider |  | connectivity, witsml, launchpad |
| `data.available_logs` | array[unknown] |  |  | Array of available logs records |  | connectivity, witsml, launchpad, container, array |
| `data.witsml_well_id` | null |  |  | Identifier for witsml well |  | connectivity, witsml, launchpad, metadata, identifier, reference |
| `data.corva_well_name` | str | SHELL ET AL HZ GROUNDBIRCH C04-36-080-20 |  | Name/label for corva well |  | connectivity, witsml, launchpad, metadata, display, label |
| `data.depth_paused_at` | null |  |  | Timestamp for depth paused |  | connectivity, witsml, launchpad, metadata, time |
| `data.witsml_well_name` | null |  |  | Name/label for witsml well |  | connectivity, witsml, launchpad, metadata, display, label |
| `data.potential_matches` | array[dict] |  |  | Array of potential matches records |  | connectivity, witsml, launchpad, container, array |
| `data.potential_matches[].well_uid` | str | ca_29344149 |  | Well uid |  | connectivity, witsml, launchpad |
| `data.potential_matches[].well_name` | str | SHELL ET AL HZ GROUNDBIRCH C04-36-080-20 |  | Name/label for well |  | connectivity, witsml, launchpad, metadata, display, label |
| `data.potential_matches[].edr_provider` | str | General - Pason - Canada |  | Edr provider |  | connectivity, witsml, launchpad |
| `data.potential_matches[].wellbore_uid` | str | ca_29344149_wb1 |  | Wellbore uid |  | connectivity, witsml, launchpad |
| `data.potential_matches[].similarity_ratio` | int | 1 |  | Similarity ratio |  | connectivity, witsml, launchpad |
| `data.bit_depth_mnemonic` | null |  |  | Bit depth mnemonic |  | connectivity, witsml, launchpad |
| `data.witsml_wellbore_id` | null |  |  | Identifier for witsml wellbore |  | connectivity, witsml, launchpad, metadata, identifier, reference |
| `data.data_first_received` | null |  |  | Data first received |  | connectivity, witsml, launchpad |
| `data.hole_depth_mnemonic` | null |  |  | Hole depth mnemonic |  | connectivity, witsml, launchpad |
| `data.last_check_timestamp` | null |  |  | Timestamp for last check |  | connectivity, witsml, launchpad, metadata, time |
| `data.depth_traces_record_id` | null |  |  | Identifier for depth traces record |  | connectivity, witsml, launchpad, metadata, identifier, reference |
| `app_key` | str | corva.launchpad |  | App key |  | connectivity, witsml, launchpad |
| `version` | int | 1 |  | Schema version number for this record |  | connectivity, witsml, launchpad, metadata, internal, versioning |
| `asset_id` | int | 82398980 |  | Unique identifier for the well/asset this record belongs to |  | connectivity, witsml, launchpad, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | connectivity, witsml, launchpad, metadata, internal |
| `timestamp` | int | 1736882153 |  | Unix epoch timestamp (seconds) of the record |  | connectivity, witsml, launchpad, metadata, time-index, filter-key, required |
| `collection` | str | launchpad_witsml_recommendations |  | MongoDB collection name this record belongs to |  | connectivity, witsml, launchpad, metadata, internal |
| `company_id` | int | 3 |  | Unique identifier for the company/operator |  | connectivity, witsml, launchpad, metadata, company, filter-key |

### 20. AskCorva / AI

#### `corva#askcorva.settings`

- **Friendly Name**: askcorva.settings
- **Data Type**: reference
- **API Path**: `/api/v1/data/corva/askcorva.settings/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `kpi_name` | str | test |  | Name/label for kpi |  | ai, askcorva, metadata, display, label |
| `pipeline` | array[dict] |  |  | Array of pipeline records |  | ai, askcorva, container, array |
| `pipeline[].$match` | object |  |  | Nested object containing $match data |  | ai, askcorva, container, object |
| `pipeline[].$match.$expr` | object |  |  | Nested object containing $expr data |  | ai, askcorva, container, object |
| `pipeline[].$match.$expr.$and` | array[dict] |  |  | Array of $and records |  | ai, askcorva, container, array |
| `pipeline[].$match.$expr.$and[].$ne` | array[dict] |  |  | Array of $ne records |  | ai, askcorva, container, array |
| `pipeline[].$match.$expr.$and[].$ne[].$toString` | str | $data.value |  | $tostring |  | ai, askcorva |
| `pipeline[].$match.data.key` | str | rop |  | Key |  | ai, askcorva |
| `pipeline[].$match.data.type` | str | hour |  | Type classifier for this record |  | ai, askcorva, metadata, classification |
| `pipeline[].$match.data.year` | int | 2024 |  | Year |  | ai, askcorva |
| `pipeline[].$match.data.value` | object |  |  | Nested object containing value data |  | ai, askcorva, container, object |
| `pipeline[].$match.data.value.$ne` | str | null |  | $ne |  | ai, askcorva |
| `pipeline[].$match.data.value.$type` | str | number |  | $type |  | ai, askcorva |
| `pipeline[].$match.data.value.$exists` | str | true |  | $exists |  | ai, askcorva |
| `company_id` | int | 3 |  | Unique identifier for the company/operator |  | ai, askcorva, metadata, company, filter-key |
| `kpi_segment` | str | Drilling |  | Kpi segment |  | ai, askcorva |

### 21. WITS (Other Phases)

#### `corva#completion.wits`

- **Friendly Name**: completion.wits
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.wits/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `default_units` | object |  |  | Nested object containing default units data |  | wits, real-time, container, object |
| `default_units.gel` | str | gal/Mgal |  | Gel |  | wits, real-time |
| `default_units.acid` | str | gal/Mgal |  | Acid |  | wits, real-time |
| `default_units.biocide` | str | gal/Mgal |  | Biocide |  | wits, real-time |
| `default_units.divertor` | str | lb/Mgal |  | Divertor |  | wits, real-time |
| `default_units.emulsifier` | str | gal/Mgal |  | Emulsifier |  | wits, real-time |
| `default_units.fluid_loss` | str | lb/Mgal |  | Fluid loss |  | wits, real-time |
| `default_units.powder_gel` | str | lb/Mgal |  | Powder gel |  | wits, real-time |
| `default_units.surfactant` | str | gal/Mgal |  | Surfactant |  | wits, real-time |
| `default_units.accelerator` | str | gal/Mgal |  | Accelerator |  | wits, real-time |
| `default_units.anti_sludge` | str | gal/Mgal |  | Anti sludge |  | wits, real-time |
| `default_units.cross_linker` | str | gal/Mgal |  | Cross linker |  | wits, real-time |
| `default_units.iron_control` | str | gal/Mgal |  | Iron control |  | wits, real-time |
| `default_units.ploymer_plug` | str | lb/Mgal |  | Ploymer plug |  | wits, real-time |
| `default_units.acid_retarder` | str | gal/Mgal |  | Acid retarder |  | wits, real-time |
| `default_units.acid_inhibitor` | str | gal/Mgal |  | Acid inhibitor |  | wits, real-time |
| `default_units.enzyme_breaker` | str | gal/Mgal |  | Enzyme breaker |  | wits, real-time |
| `default_units.liquid_breaker` | str | gal/Mgal |  | Liquid breaker |  | wits, real-time |
| `default_units.mutual_solvent` | str | gal/Mgal |  | Mutual solvent |  | wits, real-time |
| `default_units.non_emulsifier` | str | gal/Mgal |  | Non emulsifier |  | wits, real-time |
| `default_units.powder_breaker` | str | lb/Mgal |  | Powder breaker |  | wits, real-time |
| `default_units.slurry_density` | str | lb/gal |  | Slurry density |  | wits, real-time |
| `default_units.total_pump_spm` | str | bbl/min |  | Total pump spm |  | wits, real-time |
| `default_units.clay_stabilizer` | str | gal/Mgal |  | Clay stabilizer |  | wits, real-time |
| `default_units.fines_suspender` | str | gal/Mgal |  | Fines suspender |  | wits, real-time |
| `default_units.proppant_1_mass` | str | lb |  | Proppant 1 mass |  | wits, real-time |
| `default_units.proppant_2_mass` | str | lb |  | Proppant 2 mass |  | wits, real-time |
| `default_units.scale_inhibitor` | str | gal/Mgal |  | Scale inhibitor |  | wits, real-time |
| `default_units.friction_reducer` | str | gal/Mgal |  | Friction reducer |  | wits, real-time |
| `default_units.oxygen_scavenger` | str | gal/Mgal |  | Oxygen scavenger |  | wits, real-time |
| `default_units.paraffin_control` | str | gal/Mgal |  | Paraffin control |  | wits, real-time |
| `default_units.backside_pressure` | str | psi |  | Annular/backside pressure (psi) |  | wits, real-time, completions, frac, pressure |
| `default_units.pumpside_pressure` | str | psi |  | Pressure: pumpside (psi) |  | wits, real-time, pressure, measurement |
| `default_units.wellhead_pressure` | str | psi |  | Pressure: wellhead (psi) |  | wits, real-time, pressure, measurement |
| `default_units.clean_flow_rate_in` | str | bbl/min |  | Clean flow rate in |  | wits, real-time |
| `default_units.ph_adjusting_agent` | str | gal/Mgal |  | Ph adjusting agent |  | wits, real-time |
| `default_units.corrosion_inhibitor` | str | gal/Mgal |  | Corrosion inhibitor |  | wits, real-time |
| `default_units.delayed_crosslinker` | str | gal/Mgal |  | Delayed crosslinker |  | wits, real-time |
| `default_units.instant_crosslinker` | str | gal/Mgal |  | Instant crosslinker |  | wits, real-time |
| `default_units.slurry_flow_rate_in` | str | bbl/min |  | Slurry flow rate in |  | wits, real-time |
| `default_units.powder_enzyme_breaker` | str | lb/Mgal |  | Powder enzyme breaker |  | wits, real-time |
| `default_units.total_clean_volume_in` | str | bbl |  | Total clean volume in |  | wits, real-time |
| `default_units.friction_reducer_extra` | str | gal/Mgal |  | Friction reducer extra |  | wits, real-time |
| `default_units.total_slurry_volume_in` | str | bbl |  | Total slurry volume in |  | wits, real-time |
| `default_units.powder_friction_reducer` | str | lb/Mgal |  | Powder friction reducer |  | wits, real-time |
| `default_units.proppant_1_concentration` | str | lb/gal |  | Proppant 1 concentration |  | wits, real-time |
| `default_units.proppant_2_concentration` | str | lb/gal |  | Proppant 2 concentration |  | wits, real-time |

#### `corva#completion.wits.raw`

- **Friendly Name**: completion.wits.raw
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.wits.raw/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e1d5c807eac484db30d3ec9 |  | MongoDB document unique identifier |  | wits, real-time, metadata, internal, primary-key |
| `app` | str | corva.completion-column-mapper |  | App |  | wits, real-time |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, metadata, container |
| `data.gel` | int | 0 |  | Gel |  | wits, real-time |
| `data.uwi` | int | 40719 |  | Uwi |  | wits, real-time |
| `data.time` | int | 0 |  | Time |  | wits, real-time |
| `data.date_time` | null |  |  | Timestamp for date |  | wits, real-time, metadata, time |
| `data.well name` | str | EPLEY-SALE 39C 3H |  | Well name |  | wits, real-time |
| `data.chem van 8` | int | 0 |  | Chem van 8 |  | wits, real-time |
| `data.chem van 9` | int | 0 |  | Chem van 9 |  | wits, real-time |
| `data.fluid type` | str | HVFR-Low |  | Fluid type |  | wits, real-time |
| `data.prop total` | int | 0 |  | Prop total |  | wits, real-time |
| `data.tn density` | int | 0 |  | Tn density |  | wits, real-time |
| `data.chem van 10` | int | 0 |  | Chem van 10 |  | wits, real-time |
| `data.tn prop con` | int | 0 |  | Tn prop con |  | wits, real-time |
| `data.well api no` | str | 42-317-40719 |  | Well api no |  | wits, real-time |
| `data.blender 1 si` | int | 0 |  | Blender 1 si |  | wits, real-time |
| `data.stage number` | int | 1 |  | Stage number |  | wits, real-time |
| `data.blender 2 bio` | int | 0 |  | Blender 2 bio |  | wits, real-time |
| `data.proppant conc` | int | 0 |  | Proppant conc |  | wits, real-time |
| `data.proppant type` | str | 100 mesh |  | Proppant type |  | wits, real-time |
| `data.tn prop total` | int | 0 |  | Tn prop total |  | wits, real-time |
| `data.analog input 4` | float | -50.25 |  | Analog input 4 |  | wits, real-time |
| `data.analaog input 5` | float | -55.24 |  | Analaog input 5 |  | wits, real-time |
| `data.analaog input 6` | float | -3869.14 |  | Analaog input 6 |  | wits, real-time |
| `data.analaog input 7` | float | -3862.69 |  | Analaog input 7 |  | wits, real-time |
| `data.analaog input 8` | float | -3863.18 |  | Analaog input 8 |  | wits, real-time |
| `data.chem van 2 hvfr` | int | 0 |  | Chem van 2 hvfr |  | wits, real-time |
| `data.proppant_1_mass` | int | 0 |  | Proppant 1 mass |  | wits, real-time |
| `data.scale_inhibitor` | int | 0 |  | Scale inhibitor |  | wits, real-time |
| `data.chem van 6 accel` | int | 0 |  | Chem van 6 accel |  | wits, real-time |
| `data.friction_reducer` | int | 0 |  | Friction reducer |  | wits, real-time |
| `data.surf press [ann]` | float | -8.05 |  | Surf press [ann] |  | wits, real-time |
| `data.surf press [csg]` | float | -3849.84 |  | Surf press [csg] |  | wits, real-time |
| `data.blender dry add 1` | int | 0 |  | Blender dry add 1 |  | wits, real-time |
| `data.blender dry add 2` | int | 0 |  | Blender dry add 2 |  | wits, real-time |
| `data.chem van 3 xl 201` | int | 0 |  | Chem van 3 xl 201 |  | wits, real-time |
| `data.chem van 4 xl 201` | int | 0 |  | Chem van 4 xl 201 |  | wits, real-time |
| `data.chem van 5 buffer` | int | 0 |  | Chem van 5 buffer |  | wits, real-time |
| `data.chem van 7 buffer` | int | 0 |  | Chem van 7 buffer |  | wits, real-time |
| `data.hydration 1 gel 1` | float | 2.37 |  | Hydration 1 gel 1 |  | wits, real-time |
| `data.hydration 1 gel 2` | float | 2.92 |  | Hydration 1 gel 2 |  | wits, real-time |
| `data.hydration 2 gel 1` | int | 0 |  | Hydration 2 gel 1 |  | wits, real-time |
| `data.hydration 2 gel 2` | int | 0 |  | Hydration 2 gel 2 |  | wits, real-time |
| `data.pump strokes rate` | int | 0 |  | Pump strokes rate |  | wits, real-time |
| `data.wellhead_pressure` | float | -12.6 |  | Pressure: wellhead (psi) |  | wits, real-time, pressure, measurement |
| `data.clean_flow_rate_in` | int | 0 |  | Clean flow rate in |  | wits, real-time |
| `data.slurry_flow_rate_in` | int | 0 |  | Slurry flow rate in |  | wits, real-time |
| `data.total_clean_volume_in` | int | 0 |  | Total clean volume in |  | wits, real-time |
| `data.total_slurry_volume_in` | int | 0 |  | Total slurry volume in |  | wits, real-time |
| `data.proppant_1_concentration` | int | 0 |  | Proppant 1 concentration |  | wits, real-time |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, metadata, internal |
| `timestamp` | int | 1536944208 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, metadata, time-index, filter-key, required |
| `collection` | str | completion.wits.raw |  | MongoDB collection name this record belongs to |  | wits, real-time, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, metadata, company, filter-key |
| `stage_number` | int | 2 |  | Frac stage number |  | wits, real-time, completions, frac, stage, index |

#### `corva#completion.wits.summary-10s`

- **Friendly Name**: completion.wits.summary-10s
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.wits.summary-10s/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e1d5c82ca06904e95fa1b68 |  | MongoDB document unique identifier |  | wits, real-time, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, metadata, container |
| `data.max` | object |  |  | Nested object containing max data |  | wits, real-time, container, object |
| `data.max.gel` | int | 0 |  | Maximum value of gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.acid` | int | 0 |  | Maximum value of acid in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.biocide` | int | 0 |  | Maximum value of biocide in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.divertor` | int | 0 |  | Maximum value of divertor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.timestamp` | int | 1536944217 |  | Maximum value of timestamp in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.emulsifier` | int | 0 |  | Maximum value of emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.fluid_loss` | int | 0 |  | Maximum value of fluid loss in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.powder_gel` | int | 0 |  | Maximum value of powder gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.surfactant` | int | 0 |  | Maximum value of surfactant in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.accelerator` | int | 0 |  | Maximum value of accelerator in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.anti_sludge` | int | 0 |  | Maximum value of anti sludge in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.cross_linker` | int | 0 |  | Maximum value of cross linker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.elapsed_time` | int | 9 |  | Maximum value of elapsed time in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.iron_control` | int | 0 |  | Maximum value of iron control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.ploymer_plug` | int | 0 |  | Maximum value of ploymer plug in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.acid_retarder` | int | 0 |  | Maximum value of acid retarder in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.acid_inhibitor` | int | 0 |  | Maximum value of acid inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.enzyme_breaker` | int | 0 |  | Maximum value of enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.liquid_breaker` | int | 0 |  | Maximum value of liquid breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.mutual_solvent` | int | 0 |  | Maximum value of mutual solvent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.non_emulsifier` | int | 0 |  | Maximum value of non emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.powder_breaker` | int | 0 |  | Maximum value of powder breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.clay_stabilizer` | int | 0 |  | Maximum value of clay stabilizer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.fines_suspender` | int | 0 |  | Maximum value of fines suspender in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.proppant_1_mass` | int | 0 |  | Maximum value of proppant 1 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.proppant_2_mass` | int | 0 |  | Maximum value of proppant 2 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.scale_inhibitor` | int | 0 |  | Maximum value of scale inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.friction_reducer` | int | 0 |  | Maximum value of friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.oxygen_scavenger` | int | 0 |  | Maximum value of oxygen scavenger in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.paraffin_control` | int | 0 |  | Maximum value of paraffin control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.wellhead_pressure` | int | 0 |  | Maximum value of wellhead pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.clean_flow_rate_in` | int | 0 |  | Maximum value of clean flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.ph_adjusting_agent` | int | 0 |  | Maximum value of ph adjusting agent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.corrosion_inhibitor` | int | 0 |  | Maximum value of corrosion inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.delayed_crosslinker` | int | 0 |  | Maximum value of delayed crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.instant_crosslinker` | int | 0 |  | Maximum value of instant crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.slurry_flow_rate_in` | int | 0 |  | Maximum value of slurry flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_proppant_mass` | int | 0 |  | Maximum value of total proppant mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.hydrostatic_pressure` | float | 3992.064281011832 |  | Maximum value of hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.powder_enzyme_breaker` | int | 0 |  | Maximum value of powder enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_clean_volume_in` | int | 0 |  | Maximum value of total clean volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_chemical_rate_in` | int | 0 |  | Maximum value of total chemical rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_slurry_volume_in` | int | 0 |  | Maximum value of total slurry volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.powder_friction_reducer` | int | 0 |  | Maximum value of powder friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.proppant_1_concentration` | int | 0 |  | Maximum value of proppant 1 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.proppant_2_concentration` | int | 0 |  | Maximum value of proppant 2 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.inverse_hydrostatic_pressure` | float | 0.00025049696838712706 |  | Maximum value of inverse hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_proppant_concentration` | int | 0 |  | Maximum value of total proppant concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | wits, real-time, completions, frac, proppant, calculated |
| `data.min` | object |  |  | Nested object containing min data |  | wits, real-time, container, object |
| `data.min.gel` | int | 0 |  | Minimum value of gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.acid` | int | 0 |  | Minimum value of acid in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.biocide` | int | 0 |  | Minimum value of biocide in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.divertor` | int | 0 |  | Minimum value of divertor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.timestamp` | int | 1536944208 |  | Minimum value of timestamp in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.emulsifier` | int | 0 |  | Minimum value of emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.fluid_loss` | int | 0 |  | Minimum value of fluid loss in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.powder_gel` | int | 0 |  | Minimum value of powder gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.surfactant` | int | 0 |  | Minimum value of surfactant in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.accelerator` | int | 0 |  | Minimum value of accelerator in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.anti_sludge` | int | 0 |  | Minimum value of anti sludge in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.cross_linker` | int | 0 |  | Minimum value of cross linker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.elapsed_time` | int | 0 |  | Minimum value of elapsed time in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.iron_control` | int | 0 |  | Minimum value of iron control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.ploymer_plug` | int | 0 |  | Minimum value of ploymer plug in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.acid_retarder` | int | 0 |  | Minimum value of acid retarder in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.acid_inhibitor` | int | 0 |  | Minimum value of acid inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.enzyme_breaker` | int | 0 |  | Minimum value of enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.liquid_breaker` | int | 0 |  | Minimum value of liquid breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.mutual_solvent` | int | 0 |  | Minimum value of mutual solvent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.non_emulsifier` | int | 0 |  | Minimum value of non emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.powder_breaker` | int | 0 |  | Minimum value of powder breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.clay_stabilizer` | int | 0 |  | Minimum value of clay stabilizer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.fines_suspender` | int | 0 |  | Minimum value of fines suspender in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.proppant_1_mass` | int | 0 |  | Minimum value of proppant 1 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.proppant_2_mass` | int | 0 |  | Minimum value of proppant 2 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.scale_inhibitor` | int | 0 |  | Minimum value of scale inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.friction_reducer` | int | 0 |  | Minimum value of friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.oxygen_scavenger` | int | 0 |  | Minimum value of oxygen scavenger in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.paraffin_control` | int | 0 |  | Minimum value of paraffin control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.wellhead_pressure` | int | 0 |  | Minimum value of wellhead pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.clean_flow_rate_in` | int | 0 |  | Minimum value of clean flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.ph_adjusting_agent` | int | 0 |  | Minimum value of ph adjusting agent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.corrosion_inhibitor` | int | 0 |  | Minimum value of corrosion inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.delayed_crosslinker` | int | 0 |  | Minimum value of delayed crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.instant_crosslinker` | int | 0 |  | Minimum value of instant crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.slurry_flow_rate_in` | int | 0 |  | Minimum value of slurry flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_proppant_mass` | int | 0 |  | Minimum value of total proppant mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.hydrostatic_pressure` | float | 3992.064281011832 |  | Minimum value of hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.powder_enzyme_breaker` | int | 0 |  | Minimum value of powder enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_clean_volume_in` | int | 0 |  | Minimum value of total clean volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_chemical_rate_in` | int | 0 |  | Minimum value of total chemical rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_slurry_volume_in` | int | 0 |  | Minimum value of total slurry volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.powder_friction_reducer` | int | 0 |  | Minimum value of powder friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.proppant_1_concentration` | int | 0 |  | Minimum value of proppant 1 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.proppant_2_concentration` | int | 0 |  | Minimum value of proppant 2 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.inverse_hydrostatic_pressure` | float | 0.00025049696838712706 |  | Minimum value of inverse hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_proppant_concentration` | int | 0 |  | Minimum value of total proppant concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | wits, real-time, completions, frac, proppant, calculated |
| `data.mean` | object |  |  | Nested object containing mean data |  | wits, real-time, container, object |
| `data.mean.gel` | int | 0 |  | Average value of gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.acid` | int | 0 |  | Average value of acid in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.biocide` | int | 0 |  | Average value of biocide in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.divertor` | int | 0 |  | Average value of divertor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.timestamp` | float | 1536944212.5 |  | Average value of timestamp in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.emulsifier` | int | 0 |  | Average value of emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.fluid_loss` | int | 0 |  | Average value of fluid loss in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.powder_gel` | int | 0 |  | Average value of powder gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.surfactant` | int | 0 |  | Average value of surfactant in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.accelerator` | int | 0 |  | Average value of accelerator in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.anti_sludge` | int | 0 |  | Average value of anti sludge in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.cross_linker` | int | 0 |  | Average value of cross linker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.elapsed_time` | float | 4.5 |  | Average value of elapsed time in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.iron_control` | int | 0 |  | Average value of iron control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.ploymer_plug` | int | 0 |  | Average value of ploymer plug in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.acid_retarder` | int | 0 |  | Average value of acid retarder in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.acid_inhibitor` | int | 0 |  | Average value of acid inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.enzyme_breaker` | int | 0 |  | Average value of enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.liquid_breaker` | int | 0 |  | Average value of liquid breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.mutual_solvent` | int | 0 |  | Average value of mutual solvent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.non_emulsifier` | int | 0 |  | Average value of non emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.powder_breaker` | int | 0 |  | Average value of powder breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.clay_stabilizer` | int | 0 |  | Average value of clay stabilizer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.fines_suspender` | int | 0 |  | Average value of fines suspender in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.proppant_1_mass` | int | 0 |  | Average value of proppant 1 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.proppant_2_mass` | int | 0 |  | Average value of proppant 2 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.scale_inhibitor` | int | 0 |  | Average value of scale inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.friction_reducer` | int | 0 |  | Average value of friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.oxygen_scavenger` | int | 0 |  | Average value of oxygen scavenger in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.paraffin_control` | int | 0 |  | Average value of paraffin control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.wellhead_pressure` | int | 0 |  | Average value of wellhead pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.clean_flow_rate_in` | int | 0 |  | Average value of clean flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.ph_adjusting_agent` | int | 0 |  | Average value of ph adjusting agent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.corrosion_inhibitor` | int | 0 |  | Average value of corrosion inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.delayed_crosslinker` | int | 0 |  | Average value of delayed crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.instant_crosslinker` | int | 0 |  | Average value of instant crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.slurry_flow_rate_in` | int | 0 |  | Average value of slurry flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_proppant_mass` | int | 0 |  | Average value of total proppant mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.hydrostatic_pressure` | float | 3992.064281011832 |  | Average value of hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.powder_enzyme_breaker` | int | 0 |  | Average value of powder enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_clean_volume_in` | int | 0 |  | Average value of total clean volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_chemical_rate_in` | int | 0 |  | Average value of total chemical rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_slurry_volume_in` | int | 0 |  | Average value of total slurry volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.powder_friction_reducer` | int | 0 |  | Average value of powder friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.proppant_1_concentration` | int | 0 |  | Average value of proppant 1 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.proppant_2_concentration` | int | 0 |  | Average value of proppant 2 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.inverse_hydrostatic_pressure` | float | 0.0002504969683871271 |  | Average value of inverse hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_proppant_concentration` | int | 0 |  | Average value of total proppant concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | wits, real-time, completions, frac, proppant, calculated |
| `data.median` | object |  |  | Nested object containing median data |  | wits, real-time, container, object |
| `data.median.gel` | int | 0 |  | Median value of gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.acid` | int | 0 |  | Median value of acid in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.biocide` | int | 0 |  | Median value of biocide in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.divertor` | int | 0 |  | Median value of divertor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.timestamp` | float | 1536944212.5 |  | Median value of timestamp in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.emulsifier` | int | 0 |  | Median value of emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.fluid_loss` | int | 0 |  | Median value of fluid loss in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.powder_gel` | int | 0 |  | Median value of powder gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.surfactant` | int | 0 |  | Median value of surfactant in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.accelerator` | int | 0 |  | Median value of accelerator in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.anti_sludge` | int | 0 |  | Median value of anti sludge in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.cross_linker` | int | 0 |  | Median value of cross linker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.elapsed_time` | float | 4.5 |  | Median value of elapsed time in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.iron_control` | int | 0 |  | Median value of iron control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.ploymer_plug` | int | 0 |  | Median value of ploymer plug in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.acid_retarder` | int | 0 |  | Median value of acid retarder in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.acid_inhibitor` | int | 0 |  | Median value of acid inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.enzyme_breaker` | int | 0 |  | Median value of enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.liquid_breaker` | int | 0 |  | Median value of liquid breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.mutual_solvent` | int | 0 |  | Median value of mutual solvent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.non_emulsifier` | int | 0 |  | Median value of non emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.powder_breaker` | int | 0 |  | Median value of powder breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.clay_stabilizer` | int | 0 |  | Median value of clay stabilizer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.fines_suspender` | int | 0 |  | Median value of fines suspender in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.proppant_1_mass` | int | 0 |  | Median value of proppant 1 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.proppant_2_mass` | int | 0 |  | Median value of proppant 2 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.scale_inhibitor` | int | 0 |  | Median value of scale inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.friction_reducer` | int | 0 |  | Median value of friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.oxygen_scavenger` | int | 0 |  | Median value of oxygen scavenger in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.paraffin_control` | int | 0 |  | Median value of paraffin control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.wellhead_pressure` | int | 0 |  | Median value of wellhead pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.clean_flow_rate_in` | int | 0 |  | Median value of clean flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.ph_adjusting_agent` | int | 0 |  | Median value of ph adjusting agent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.corrosion_inhibitor` | int | 0 |  | Median value of corrosion inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.delayed_crosslinker` | int | 0 |  | Median value of delayed crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.instant_crosslinker` | int | 0 |  | Median value of instant crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.slurry_flow_rate_in` | int | 0 |  | Median value of slurry flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_proppant_mass` | int | 0 |  | Median value of total proppant mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.hydrostatic_pressure` | float | 3992.064281011832 |  | Median value of hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.powder_enzyme_breaker` | int | 0 |  | Median value of powder enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_clean_volume_in` | int | 0 |  | Median value of total clean volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_chemical_rate_in` | int | 0 |  | Median value of total chemical rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_slurry_volume_in` | int | 0 |  | Median value of total slurry volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.powder_friction_reducer` | int | 0 |  | Median value of powder friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.proppant_1_concentration` | int | 0 |  | Median value of proppant 1 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.proppant_2_concentration` | int | 0 |  | Median value of proppant 2 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.inverse_hydrostatic_pressure` | float | 0.00025049696838712706 |  | Median value of inverse hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_proppant_concentration` | int | 0 |  | Median value of total proppant concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | wits, real-time, completions, frac, proppant, calculated |
| `data.end_timestamp` | int | 1536944217 |  | End timestamp of the interval/run (Unix epoch) |  | wits, real-time, time, interval, range |
| `data.start_timestamp` | int | 1536944208 |  | Start timestamp of the interval/run (Unix epoch) |  | wits, real-time, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, metadata, internal |
| `timestamp` | int | 1536944217 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, metadata, time-index, filter-key, required |
| `collection` | str | completion.wits.summary-10s |  | MongoDB collection name this record belongs to |  | wits, real-time, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, metadata, company, filter-key |
| `stage_number` | int | 2 |  | Frac stage number |  | wits, real-time, completions, frac, stage, index |

#### `corva#completion.wits.summary-1m`

- **Friendly Name**: completion.wits.summary-1m
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/completion.wits.summary-1m/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e1d5c837eac484f4a0d34d5 |  | MongoDB document unique identifier |  | wits, real-time, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, metadata, container |
| `data.max` | object |  |  | Nested object containing max data |  | wits, real-time, container, object |
| `data.max.gel` | int | 0 |  | Maximum value of gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.acid` | int | 0 |  | Maximum value of acid in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.biocide` | int | 0 |  | Maximum value of biocide in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.divertor` | int | 0 |  | Maximum value of divertor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.timestamp` | int | 1536944267 |  | Maximum value of timestamp in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.emulsifier` | int | 0 |  | Maximum value of emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.fluid_loss` | int | 0 |  | Maximum value of fluid loss in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.powder_gel` | int | 0 |  | Maximum value of powder gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.surfactant` | int | 0 |  | Maximum value of surfactant in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.accelerator` | int | 0 |  | Maximum value of accelerator in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.anti_sludge` | int | 0 |  | Maximum value of anti sludge in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.cross_linker` | int | 0 |  | Maximum value of cross linker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.elapsed_time` | int | 59 |  | Maximum value of elapsed time in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.iron_control` | int | 0 |  | Maximum value of iron control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.ploymer_plug` | int | 0 |  | Maximum value of ploymer plug in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.acid_retarder` | int | 0 |  | Maximum value of acid retarder in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.acid_inhibitor` | int | 0 |  | Maximum value of acid inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.enzyme_breaker` | int | 0 |  | Maximum value of enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.liquid_breaker` | int | 0 |  | Maximum value of liquid breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.mutual_solvent` | int | 0 |  | Maximum value of mutual solvent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.non_emulsifier` | int | 0 |  | Maximum value of non emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.powder_breaker` | int | 0 |  | Maximum value of powder breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.clay_stabilizer` | int | 0 |  | Maximum value of clay stabilizer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.fines_suspender` | int | 0 |  | Maximum value of fines suspender in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.proppant_1_mass` | int | 0 |  | Maximum value of proppant 1 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.proppant_2_mass` | int | 0 |  | Maximum value of proppant 2 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.scale_inhibitor` | float | 7.63 |  | Maximum value of scale inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.friction_reducer` | int | 0 |  | Maximum value of friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.oxygen_scavenger` | int | 0 |  | Maximum value of oxygen scavenger in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.paraffin_control` | int | 0 |  | Maximum value of paraffin control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.wellhead_pressure` | float | 1461.12 |  | Maximum value of wellhead pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.clean_flow_rate_in` | int | 0 |  | Maximum value of clean flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.ph_adjusting_agent` | int | 0 |  | Maximum value of ph adjusting agent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.corrosion_inhibitor` | int | 0 |  | Maximum value of corrosion inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.delayed_crosslinker` | int | 0 |  | Maximum value of delayed crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.instant_crosslinker` | int | 0 |  | Maximum value of instant crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.slurry_flow_rate_in` | int | 0 |  | Maximum value of slurry flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_proppant_mass` | int | 0 |  | Maximum value of total proppant mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.hydrostatic_pressure` | float | 3992.064281011832 |  | Maximum value of hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.powder_enzyme_breaker` | int | 0 |  | Maximum value of powder enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_clean_volume_in` | int | 0 |  | Maximum value of total clean volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_chemical_rate_in` | float | 7.63 |  | Maximum value of total chemical rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_slurry_volume_in` | int | 0 |  | Maximum value of total slurry volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.powder_friction_reducer` | int | 0 |  | Maximum value of powder friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.proppant_1_concentration` | int | 0 |  | Maximum value of proppant 1 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.proppant_2_concentration` | int | 0 |  | Maximum value of proppant 2 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.inverse_hydrostatic_pressure` | float | 0.00025049696838712706 |  | Maximum value of inverse hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.total_proppant_concentration` | int | 0 |  | Maximum value of total proppant concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.max.bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | wits, real-time, completions, frac, proppant, calculated |
| `data.min` | object |  |  | Nested object containing min data |  | wits, real-time, container, object |
| `data.min.gel` | int | 0 |  | Minimum value of gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.acid` | int | 0 |  | Minimum value of acid in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.biocide` | int | 0 |  | Minimum value of biocide in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.divertor` | int | 0 |  | Minimum value of divertor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.timestamp` | int | 1536944208 |  | Minimum value of timestamp in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.emulsifier` | int | 0 |  | Minimum value of emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.fluid_loss` | int | 0 |  | Minimum value of fluid loss in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.powder_gel` | int | 0 |  | Minimum value of powder gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.surfactant` | int | 0 |  | Minimum value of surfactant in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.accelerator` | int | 0 |  | Minimum value of accelerator in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.anti_sludge` | int | 0 |  | Minimum value of anti sludge in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.cross_linker` | int | 0 |  | Minimum value of cross linker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.elapsed_time` | int | 0 |  | Minimum value of elapsed time in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.iron_control` | int | 0 |  | Minimum value of iron control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.ploymer_plug` | int | 0 |  | Minimum value of ploymer plug in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.acid_retarder` | int | 0 |  | Minimum value of acid retarder in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.acid_inhibitor` | int | 0 |  | Minimum value of acid inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.enzyme_breaker` | int | 0 |  | Minimum value of enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.liquid_breaker` | int | 0 |  | Minimum value of liquid breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.mutual_solvent` | int | 0 |  | Minimum value of mutual solvent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.non_emulsifier` | int | 0 |  | Minimum value of non emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.powder_breaker` | int | 0 |  | Minimum value of powder breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.clay_stabilizer` | int | 0 |  | Minimum value of clay stabilizer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.fines_suspender` | int | 0 |  | Minimum value of fines suspender in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.proppant_1_mass` | int | 0 |  | Minimum value of proppant 1 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.proppant_2_mass` | int | 0 |  | Minimum value of proppant 2 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.scale_inhibitor` | int | 0 |  | Minimum value of scale inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.friction_reducer` | int | 0 |  | Minimum value of friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.oxygen_scavenger` | int | 0 |  | Minimum value of oxygen scavenger in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.paraffin_control` | int | 0 |  | Minimum value of paraffin control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.wellhead_pressure` | int | 0 |  | Minimum value of wellhead pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.clean_flow_rate_in` | int | 0 |  | Minimum value of clean flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.ph_adjusting_agent` | int | 0 |  | Minimum value of ph adjusting agent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.corrosion_inhibitor` | int | 0 |  | Minimum value of corrosion inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.delayed_crosslinker` | int | 0 |  | Minimum value of delayed crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.instant_crosslinker` | int | 0 |  | Minimum value of instant crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.slurry_flow_rate_in` | int | 0 |  | Minimum value of slurry flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_proppant_mass` | int | 0 |  | Minimum value of total proppant mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.hydrostatic_pressure` | float | 3992.064281011832 |  | Minimum value of hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.powder_enzyme_breaker` | int | 0 |  | Minimum value of powder enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_clean_volume_in` | int | 0 |  | Minimum value of total clean volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_chemical_rate_in` | int | 0 |  | Minimum value of total chemical rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_slurry_volume_in` | int | 0 |  | Minimum value of total slurry volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.powder_friction_reducer` | int | 0 |  | Minimum value of powder friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.proppant_1_concentration` | int | 0 |  | Minimum value of proppant 1 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.proppant_2_concentration` | int | 0 |  | Minimum value of proppant 2 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.inverse_hydrostatic_pressure` | float | 0.00025049696838712706 |  | Minimum value of inverse hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.total_proppant_concentration` | int | 0 |  | Minimum value of total proppant concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.min.bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | wits, real-time, completions, frac, proppant, calculated |
| `data.mean` | object |  |  | Nested object containing mean data |  | wits, real-time, container, object |
| `data.mean.gel` | int | 0 |  | Average value of gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.acid` | int | 0 |  | Average value of acid in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.biocide` | int | 0 |  | Average value of biocide in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.divertor` | int | 0 |  | Average value of divertor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.timestamp` | float | 1536944237.5 |  | Average value of timestamp in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.emulsifier` | int | 0 |  | Average value of emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.fluid_loss` | int | 0 |  | Average value of fluid loss in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.powder_gel` | int | 0 |  | Average value of powder gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.surfactant` | int | 0 |  | Average value of surfactant in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.accelerator` | int | 0 |  | Average value of accelerator in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.anti_sludge` | int | 0 |  | Average value of anti sludge in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.cross_linker` | int | 0 |  | Average value of cross linker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.elapsed_time` | float | 29.5 |  | Average value of elapsed time in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.iron_control` | int | 0 |  | Average value of iron control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.ploymer_plug` | int | 0 |  | Average value of ploymer plug in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.acid_retarder` | int | 0 |  | Average value of acid retarder in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.acid_inhibitor` | int | 0 |  | Average value of acid inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.enzyme_breaker` | int | 0 |  | Average value of enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.liquid_breaker` | int | 0 |  | Average value of liquid breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.mutual_solvent` | int | 0 |  | Average value of mutual solvent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.non_emulsifier` | int | 0 |  | Average value of non emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.powder_breaker` | int | 0 |  | Average value of powder breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.clay_stabilizer` | int | 0 |  | Average value of clay stabilizer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.fines_suspender` | int | 0 |  | Average value of fines suspender in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.proppant_1_mass` | int | 0 |  | Average value of proppant 1 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.proppant_2_mass` | int | 0 |  | Average value of proppant 2 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.scale_inhibitor` | float | 1.1418333333333335 |  | Average value of scale inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.friction_reducer` | int | 0 |  | Average value of friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.oxygen_scavenger` | int | 0 |  | Average value of oxygen scavenger in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.paraffin_control` | int | 0 |  | Average value of paraffin control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.wellhead_pressure` | float | 220.19516666666667 |  | Average value of wellhead pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.clean_flow_rate_in` | int | 0 |  | Average value of clean flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.ph_adjusting_agent` | int | 0 |  | Average value of ph adjusting agent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.corrosion_inhibitor` | int | 0 |  | Average value of corrosion inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.delayed_crosslinker` | int | 0 |  | Average value of delayed crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.instant_crosslinker` | int | 0 |  | Average value of instant crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.slurry_flow_rate_in` | int | 0 |  | Average value of slurry flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_proppant_mass` | int | 0 |  | Average value of total proppant mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.hydrostatic_pressure` | float | 3992.064281011833 |  | Average value of hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.powder_enzyme_breaker` | int | 0 |  | Average value of powder enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_clean_volume_in` | int | 0 |  | Average value of total clean volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_chemical_rate_in` | float | 1.1418333333333335 |  | Average value of total chemical rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_slurry_volume_in` | int | 0 |  | Average value of total slurry volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.powder_friction_reducer` | int | 0 |  | Average value of powder friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.proppant_1_concentration` | int | 0 |  | Average value of proppant 1 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.proppant_2_concentration` | int | 0 |  | Average value of proppant 2 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.inverse_hydrostatic_pressure` | float | 0.000250496968387127 |  | Average value of inverse hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.total_proppant_concentration` | int | 0 |  | Average value of total proppant concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.mean.bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | wits, real-time, completions, frac, proppant, calculated |
| `data.median` | object |  |  | Nested object containing median data |  | wits, real-time, container, object |
| `data.median.gel` | int | 0 |  | Median value of gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.acid` | int | 0 |  | Median value of acid in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.biocide` | int | 0 |  | Median value of biocide in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.divertor` | int | 0 |  | Median value of divertor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.timestamp` | float | 1536944237.5 |  | Median value of timestamp in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.emulsifier` | int | 0 |  | Median value of emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.fluid_loss` | int | 0 |  | Median value of fluid loss in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.powder_gel` | int | 0 |  | Median value of powder gel in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.surfactant` | int | 0 |  | Median value of surfactant in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.accelerator` | int | 0 |  | Median value of accelerator in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.anti_sludge` | int | 0 |  | Median value of anti sludge in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.cross_linker` | int | 0 |  | Median value of cross linker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.elapsed_time` | float | 29.5 |  | Median value of elapsed time in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.iron_control` | int | 0 |  | Median value of iron control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.ploymer_plug` | int | 0 |  | Median value of ploymer plug in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.acid_retarder` | int | 0 |  | Median value of acid retarder in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.acid_inhibitor` | int | 0 |  | Median value of acid inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.enzyme_breaker` | int | 0 |  | Median value of enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.liquid_breaker` | int | 0 |  | Median value of liquid breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.mutual_solvent` | int | 0 |  | Median value of mutual solvent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.non_emulsifier` | int | 0 |  | Median value of non emulsifier in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.powder_breaker` | int | 0 |  | Median value of powder breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.clay_stabilizer` | int | 0 |  | Median value of clay stabilizer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.fines_suspender` | int | 0 |  | Median value of fines suspender in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.proppant_1_mass` | int | 0 |  | Median value of proppant 1 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.proppant_2_mass` | int | 0 |  | Median value of proppant 2 mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.scale_inhibitor` | int | 0 |  | Median value of scale inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.friction_reducer` | int | 0 |  | Median value of friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.oxygen_scavenger` | int | 0 |  | Median value of oxygen scavenger in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.paraffin_control` | int | 0 |  | Median value of paraffin control in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.wellhead_pressure` | int | 0 |  | Median value of wellhead pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.clean_flow_rate_in` | int | 0 |  | Median value of clean flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.ph_adjusting_agent` | int | 0 |  | Median value of ph adjusting agent in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.corrosion_inhibitor` | int | 0 |  | Median value of corrosion inhibitor in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.delayed_crosslinker` | int | 0 |  | Median value of delayed crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.instant_crosslinker` | int | 0 |  | Median value of instant crosslinker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.slurry_flow_rate_in` | int | 0 |  | Median value of slurry flow rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_proppant_mass` | int | 0 |  | Median value of total proppant mass in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.hydrostatic_pressure` | float | 3992.064281011832 |  | Median value of hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.powder_enzyme_breaker` | int | 0 |  | Median value of powder enzyme breaker in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_clean_volume_in` | int | 0 |  | Median value of total clean volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_chemical_rate_in` | int | 0 |  | Median value of total chemical rate in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_slurry_volume_in` | int | 0 |  | Median value of total slurry volume in in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.powder_friction_reducer` | int | 0 |  | Median value of powder friction reducer in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.proppant_1_concentration` | int | 0 |  | Median value of proppant 1 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.proppant_2_concentration` | int | 0 |  | Median value of proppant 2 concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.inverse_hydrostatic_pressure` | float | 0.00025049696838712706 |  | Median value of inverse hydrostatic pressure in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.total_proppant_concentration` | int | 0 |  | Median value of total proppant concentration in the summary interval |  | wits, real-time, aggregated, summary |
| `data.median.bottomhole_proppant_concentration` | int | 0 |  | Estimated proppant concentration at perforations (ppa) |  | wits, real-time, completions, frac, proppant, calculated |
| `data.end_timestamp` | int | 1536944267 |  | End timestamp of the interval/run (Unix epoch) |  | wits, real-time, time, interval, range |
| `data.start_timestamp` | int | 1536944208 |  | Start timestamp of the interval/run (Unix epoch) |  | wits, real-time, time, interval, range |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, metadata, internal |
| `timestamp` | int | 1536944267 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, metadata, time-index, filter-key, required |
| `collection` | str | completion.wits.summary-1m |  | MongoDB collection name this record belongs to |  | wits, real-time, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, metadata, company, filter-key |
| `stage_number` | int | 2 |  | Frac stage number |  | wits, real-time, completions, frac, stage, index |

#### `corva#drillout.wits.summary-6h`

- **Friendly Name**: drillout.wits.summary-6h
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/drillout.wits.summary-6h/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5e962f171403154eee3711ce |  | MongoDB document unique identifier |  | wits, real-time, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, metadata, container |
| `data.rop` | int | 0 |  | Rate of penetration - drilling speed (ft/hr) |  | wits, real-time, drilling, rop, real-time, key-metric, performance |
| `data.state` | str | Run in Hole |  | State |  | wits, real-time |
| `data.entry_at` | int | 1585522800 |  | Timestamp for entry |  | wits, real-time, metadata, time |
| `data.pipe rpm` | int | 0 |  | Pipe rpm |  | wits, real-time |
| `data.bit_depth` | float | 5963.76 |  | Current depth of the drill bit |  | wits, real-time, depth, drilling, real-time, key-metric |
| `data.gamma_ray` | int | 0 |  | Gamma ray measurement from MWD/LWD tool (API units) |  | wits, real-time, drilling, mwd, formation, real-time |
| `data.hook_load` | float | 37.8 |  | Hook load |  | wits, real-time |
| `data.wc torque` | int | 766 |  | Wc torque |  | wits, real-time |
| `data.diff_press` | float | 1027.55 |  | Differential pressure across the motor (psi) |  | wits, real-time, pdm, pressure, real-time |
| `data.hole_depth` | float | 5966.09 |  | Current hole depth (bottom of wellbore) |  | wits, real-time, depth, drilling, real-time, key-metric |
| `data.pump_spm_1` | int | 0 |  | Pump spm 1 |  | wits, real-time |
| `data.pump_spm_2` | int | 0 |  | Pump spm 2 |  | wits, real-time |
| `data.pump_spm_3` | int | 0 |  | Pump spm 3 |  | wits, real-time |
| `data.rop - fast` | int | 12 |  | Rop   fast |  | wits, real-time |
| `data.rotary_rpm` | int | 0 |  | Surface rotary speed (RPM) |  | wits, real-time, drilling, rpm, real-time, key-metric |
| `data.mud_flow_in` | int | 0 |  | Mud flow in |  | wits, real-time |
| `data.pipe torque` | int | 0 |  | Pipe torque |  | wits, real-time |
| `data.block_height` | float | 18.24 |  | Traveling block height (ft) |  | wits, real-time, drilling, rig, real-time |
| `data.rotary torque` | int | 0 |  | Rotary torque |  | wits, real-time |
| `data.rotary_torque` | float | 0.766 |  | Rotary torque |  | wits, real-time |
| `data.string torque` | int | 0 |  | String torque |  | wits, real-time |
| `data.top drive rpm` | int | 0 |  | Top drive rpm |  | wits, real-time |
| `data.weight_on_bit` | float | 1.4 |  | Weight applied to the drill bit (klbs) |  | wits, real-time, drilling, wob, real-time, key-metric |
| `data.activity_times` | object |  |  | Nested object containing activity times data |  | wits, real-time, container, object |
| `data.activity_times.in slips` | int | 289 |  | In slips |  | wits, real-time |
| `data.activity_times.run in hole` | int | 321 |  | Run in hole |  | wits, real-time |
| `data.activity_times.pull out of hole` | int | 91 |  | Pull out of hole |  | wits, real-time |
| `data.activity_times.static off bottom` | int | 1299 |  | Static off bottom |  | wits, real-time |
| `data.pump_spm_total` | int | 0 |  | Pump spm total |  | wits, real-time |
| `data.ds - dim torque` | int | 0 |  | Ds   dim torque |  | wits, real-time |
| `data.wc target torque` | int | 2500 |  | Wc target torque |  | wits, real-time |
| `data.wc torque enable` | int | 0 |  | Wc torque enable |  | wits, real-time |
| `data.rotary torque raw` | int | 0 |  | Rotary torque raw |  | wits, real-time |
| `data.display rot torque` | int | 0 |  | Display rot torque |  | wits, real-time |
| `data.ds - mud motor rpm` | int | 0 |  | Ds   mud motor rpm |  | wits, real-time |
| `data.standpipe_pressure` | int | 0 |  | Standpipe pressure - pump pressure at surface (psi) |  | wits, real-time, drilling, spp, pressure, real-time, key-metric |
| `data.mud_flow_out_percent` | int | 0 |  | Mud flow out percent |  | wits, real-time |
| `data.standpipe pressure 1` | int | 0 |  | Standpipe pressure 1 |  | wits, real-time |
| `data.standpipe pressure 2` | int | 0 |  | Standpipe pressure 2 |  | wits, real-time |
| `data.wpda - mud motor rpm` | int | 0 |  | Wpda   mud motor rpm |  | wits, real-time |
| `data.top drv torque - converted` | int | 0 |  | Top drv torque   converted |  | wits, real-time |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, metadata, internal, versioning |
| `asset_id` | int | 39888507 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, metadata, internal |
| `timestamp` | int | 1585522800 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, metadata, time-index, filter-key, required |
| `collection` | str | drillout.wits.summary-6h |  | MongoDB collection name this record belongs to |  | wits, real-time, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, metadata, company, filter-key |

#### `corva#pumpdown.wits`

- **Friendly Name**: pumpdown.wits
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/pumpdown.wits/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | str - MongoDB id |  | MongoDB document unique identifier |  | wits, real-time, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, metadata, container |
| `data.state` | str | str - indicating the state of activty |  | State |  | wits, real-time |
| `data.pumpdown_rate` | str | float - Required Parameter: flow rate measured ... |  | Rate: pumpdown |  | wits, real-time, rate, measurement |
| `data.pumpdown_volume` | str | float - Optional Parameter: total streamed clea... |  | Pumpdown volume |  | wits, real-time |
| `data.pumpdown_pressure` | str | float - Required Parameter: measured pressure a... |  | Pressure: pumpdown (psi) |  | wits, real-time, pressure, measurement |
| `data.pumpdown_volume_calc` | str | float - Optional Parameter: total calculated cl... |  | Pumpdown volume calc |  | wits, real-time |
| `app_key` | str | str - 'corva.pumpdown_engineering' |  | App key |  | wits, real-time |
| `version` | str | int - currently it is 1 |  | Schema version number for this record |  | wits, real-time, metadata, internal, versioning |
| `asset_id` | str | int - id specific to an asset |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, metadata, well-id, filter-key, required |
| `metadata` | object |  |  | Nested object containing metadata data |  | wits, real-time, container, object |
| `metadata.datasource` | str | str - showing the streambox id |  | Datasource |  | wits, real-time |
| `provider` | str | str - 'corva' |  | Data provider name (typically "corva") |  | wits, real-time, metadata, internal |
| `timestamp` | str | int - unix timestamp |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, metadata, time-index, filter-key, required |
| `collection` | str | str - 'pumpdown.wits' |  | MongoDB collection name this record belongs to |  | wits, real-time, metadata, internal |
| `company_id` | str | int - id specific to a company |  | Unique identifier for the company/operator |  | wits, real-time, metadata, company, filter-key |
| `stage_number` | str | int - frac stage number |  | Frac stage number |  | wits, real-time, completions, frac, stage, index |

#### `corva#wireline.wits`

- **Friendly Name**: wireline.wits
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wireline.wits/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f161be7de7b936052e8bd60 |  | MongoDB document unique identifier |  | wits, real-time, metadata, internal, primary-key |
| `app` | str | corva.wireline-enrichment-wrapper |  | App |  | wits, real-time |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, metadata, container |
| `data.c_006` | float | -0.5522 |  | C 006 |  | wits, real-time |
| `data.c_007` | float | -999.25 |  | C 007 |  | wits, real-time |
| `data.state` | str | Static |  | State |  | wits, real-time |
| `data.current` | int | 0 |  | Current |  | wits, real-time |
| `data.voltage` | int | 0 |  | Voltage |  | wits, real-time |
| `data.line_speed` | float | 0.05 |  | Line speed |  | wits, real-time |
| `data.elapsed_time` | float | 1119.9359 |  | Timestamp for elapsed |  | wits, real-time, metadata, time |
| `data.line_tension` | float | 320.5558 |  | Line tension |  | wits, real-time |
| `data.measured_depth` | float | 274.7967 |  | Measured depth along the wellbore path |  | wits, real-time, depth, survey, directional |
| `data.wellbore_orientation` | str | Vertical |  | Wellbore orientation |  | wits, real-time |
| `data.casing_collar_locator` | float | -0.08 |  | Casing collar locator |  | wits, real-time |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, metadata, internal |
| `timestamp` | int | 1574279324 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, metadata, time-index, filter-key, required |
| `collection` | str | wireline.wits |  | MongoDB collection name this record belongs to |  | wits, real-time, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, metadata, company, filter-key |
| `stage_number` | int | 2 |  | Frac stage number |  | wits, real-time, completions, frac, stage, index |

#### `corva#wireline.wits.summary-10s`

- **Friendly Name**: wireline.wits.summary-10s
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/wireline.wits.summary-10s/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f161c37cc363f53af7cc37e |  | MongoDB document unique identifier |  | wits, real-time, metadata, internal, primary-key |
| `app` | str | wireline-wits-summary |  | App |  | wits, real-time |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | wits, real-time, metadata, container |
| `data.state` | str | Pull out of Hole |  | State |  | wits, real-time |
| `data.elapsed_time_median` | int | 13218755584 |  | Elapsed time median |  | wits, real-time |
| `data.line_tension_median` | float | 12.934 |  | Line tension median |  | wits, real-time |
| `data.measured_depth_median` | int | 1000 |  | Measured depth median |  | wits, real-time |
| `data.casing_collar_locator_median` | float | -0.077 |  | Casing collar locator median |  | wits, real-time |
| `version` | int | 1 |  | Schema version number for this record |  | wits, real-time, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | wits, real-time, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | wits, real-time, metadata, internal |
| `timestamp` | int | 1574282520 |  | Unix epoch timestamp (seconds) of the record |  | wits, real-time, metadata, time-index, filter-key, required |
| `collection` | str | wireline.wits.summary-10s |  | MongoDB collection name this record belongs to |  | wits, real-time, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | wits, real-time, metadata, company, filter-key |
| `stage_number` | int | 2 |  | Frac stage number |  | wits, real-time, completions, frac, stage, index |

### 22. Other

#### `corva#assets`

- **Friendly Name**: assets
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/assets/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f378bb0c099b4c3f4ea1 |  | MongoDB document unique identifier |  | other, metadata, internal, primary-key |
| `rig` | object |  |  | Nested object containing rig data |  | other, container, object |
| `rig.id` | int | 43 |  | Numeric identifier for this record/run |  | other, metadata, identifier |
| `rig.name` | str | Rig #6 |  | Display name of the component or record |  | other, metadata, display |
| `name` | str | Deepwater A Well |  | Display name of the component or record |  | other, metadata, display |
| `type` | str | Asset::Well |  | Type classifier for this record |  | other, metadata, classification |
| `basin` | str | Deep Water |  | Basin |  | other |
| `stats` | object |  |  | Nested object containing stats data |  | other, container, object |
| `stats.total_time` | int | 6220800 |  | Timestamp for total |  | other, metadata, time |
| `stats.total_depth` | int | 30360 |  | Total depth of the well |  | other, depth, well-info |
| `county` | null |  |  | County |  | other |
| `status` | str | complete |  | Current status of the record/check |  | other, metadata, status |
| `program` | object |  |  | Nested object containing program data |  | other, container, object |
| `program.id` | int | 38 |  | Numeric identifier for this record/run |  | other, metadata, identifier |
| `program.name` | str | PROGRAM 2 |  | Display name of the component or record |  | other, metadata, display |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `timezone` | str | America/Chicago |  | Timezone |  | other |
| `top_hole` | object |  |  | Nested object containing top hole data |  | other, container, object |
| `top_hole.raw` | str | 25.3043° N, 90.0659° W |  | Raw |  | other |
| `top_hole.coordinates` | array[float] |  |  | Array of coordinates records |  | other, container, array |
| `api_number` | str | 60-812-40125 |  | API well number (unique well identifier) |  | other, well-info, identifier, regulatory |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |
| `created_at` | str | 2020-10-01T15:19:19.955000 |  | Timestamp for created |  | other, metadata, time |
| `bottom_hole` | dict | {} |  | Bottom hole |  | other |
| `mud_company` | str |  |  | Mud company |  | other |
| `string_design` | str | 4 |  | String design |  | other |
| `last_active_at` | str | 2019-03-20T06:50:45 |  | Timestamp for last active |  | other, metadata, time |
| `contractor_name` | str | Nomac |  | Name/label for contractor |  | other, metadata, display, label |
| `target_formation` | str | Wilcox |  | Target formation |  | other |
| `custom_properties` | object |  |  | Nested object containing custom properties data |  | other, container, object |
| `custom_properties.rig_type` | str | floating |  | Type classification for rig |  | other, metadata, classification |
| `custom_properties.off_bottom_tolerance` | str | 1.0 |  | Off bottom tolerance |  | other |
| `directional_driller` | str | Baker Hughes |  | Directional driller |  | other |
| `day_shift_start_time` | str | 06:00 |  | Timestamp for day shift start |  | other, metadata, time |

#### `corva#config-response`

- **Friendly Name**: config-response
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/config-response/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5db867c3b8e2ea4e39789e29 |  | MongoDB document unique identifier |  | other, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | other, metadata, container |
| `data.status` | int | 0 |  | Current status of the record/check |  | other, metadata, status |
| `data.message` | str | New Casing is set. |  | Message |  | other |
| `data.bit_depth` | int | 0 |  | Current depth of the drill bit |  | other, depth, drilling, real-time, key-metric |
| `data.hole_depth` | int | 0 |  | Current hole depth (bottom of wellbore) |  | other, depth, drilling, real-time, key-metric |
| `version` | int | 1 |  | Schema version number for this record |  | other, metadata, internal, versioning |
| `asset_id` | int | 15236 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | other, metadata, internal |
| `timestamp` | int | 1529938970 |  | Unix epoch timestamp (seconds) of the record |  | other, metadata, time-index, filter-key, required |
| `collection` | str | config-response |  | MongoDB collection name this record belongs to |  | other, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |

#### `corva#kick-detection`

- **Friendly Name**: kick-detection
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/kick-detection/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3936c88017090595899 |  | MongoDB document unique identifier |  | other, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | other, metadata, container |
| `data.activity` | str | In Slips |  | Activity code number |  | other, operations, activity, classification |
| `data.bit_depth` | float | 116.35 |  | Current depth of the drill bit |  | other, depth, drilling, real-time, key-metric |
| `data.occurrence` | bool | False |  | Flag indicating whether occurrence |  | other, boolean, flag |
| `data.block_height` | float | 18.8 |  | Traveling block height (ft) |  | other, drilling, rig, real-time |
| `data.is_filter_true` | bool | False |  | Flag indicating whether is filter true |  | other, boolean, flag |
| `data.ttk_transfer_status` | bool | False |  | Flag indicating whether ttk transfer status |  | other, boolean, flag |
| `data.pipe_movement_status` | bool | False |  | Flag indicating whether pipe movement status |  | other, boolean, flag |
| `data.stable_reference_volume` | null |  |  | Stable reference volume |  | other |
| `data.trip_tank_lineup_status` | bool | False |  | Flag indicating whether trip tank lineup status |  | other, boolean, flag |
| `data.ttk_pump_off_flag_status` | bool | False |  | Flag indicating whether ttk pump off flag status |  | other, boolean, flag |
| `data.stable_reference_timestamp` | null |  |  | Timestamp for stable reference |  | other, metadata, time |
| `data.standpipe_pressure_bleed_off_status` | bool | False |  | Flag indicating whether standpipe pressure bleed off status |  | other, boolean, flag |
| `type` | str | gain_in_trip_tank |  | Type classifier for this record |  | other, metadata, classification |
| `version` | int | 1 |  | Schema version number for this record |  | other, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | other, metadata, internal |
| `timestamp` | int | 1545150920 |  | Unix epoch timestamp (seconds) of the record |  | other, metadata, time-index, filter-key, required |
| `collection` | str | kick-detection |  | MongoDB collection name this record belongs to |  | other, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |

#### `corva#milling-console-real-time`

- **Friendly Name**: milling-console-real-time
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/milling-console-real-time/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `data` | object |  |  | Container object for all measurement/computed data fields |  | other, metadata, container |
| `data.bha_id` | str | 12345 |  | BHA/drillstring run number identifier |  | other, bha, reference, link |
| `data.casing_id` | str | 12345 |  | Casing inner diameter (in) |  | other, casing, dimension |
| `data.properties` | object |  |  | Nested object containing properties data |  | other, container, object |
| `data.properties.rop` | int | 0 |  | Rate of penetration - drilling speed (ft/hr) |  | other, drilling, rop, real-time, key-metric, performance |
| `data.properties.wob` | int | 0 |  | Wob |  | other |
| `data.properties.torque` | int | 0 |  | Rotary torque at surface (ft-lbs) |  | other, drilling, torque, real-time, torque-drag |
| `data.properties.wits_timestamp` | str | 2024-07-11 00:00:00 |  | Timestamp for wits |  | other, metadata, time |
| `data.properties.current_depth_md` | int | 0 |  | Current depth md |  | other |
| `data.properties.current_depth_tvd` | int | 0 |  | Current depth tvd |  | other |
| `data.properties.on_bottom_percent` | float | 0.75 |  | On bottom percent |  | other |
| `asset_id` | int | 0 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `timestamp` | int | 123456 |  | Unix epoch timestamp (seconds) of the record |  | other, metadata, time-index, filter-key, required |
| `company_id` | int | 0 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |

#### `corva#procedural-compliance`

- **Friendly Name**: procedural-compliance
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/procedural-compliance/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f3867c6a2644eca090fd |  | MongoDB document unique identifier |  | other, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | other, metadata, container |
| `data.warning` | object |  |  | Nested object containing warning data |  | other, container, object |
| `data.warning.code` | str | invalid_time_step |  | Code |  | other |
| `data.warning.message` | str | Can not run for time-steps greater than 1 secon... |  | Message |  | other |
| `data.procedure` | str | back_to_bottom |  | Procedure |  | other |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | other, depth, drilling, real-time, key-metric |
| `version` | int | 1 |  | Schema version number for this record |  | other, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | other, metadata, internal |
| `procedure` | str | back_to_bottom |  | Procedure |  | other |
| `timestamp` | int | 1545150239 |  | Unix epoch timestamp (seconds) of the record |  | other, metadata, time-index, filter-key, required |
| `collection` | str | procedural-compliance |  | MongoDB collection name this record belongs to |  | other, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |

#### `corva#traces.offsets`

- **Friendly Name**: traces.offsets
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/traces.offsets/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 60a3c418c910d416495c270f |  | MongoDB document unique identifier |  | other, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | other, metadata, container |
| `data.app_id` | int | 333 |  | Identifier for app |  | other, metadata, identifier, reference |
| `data.offsets` | object |  |  | Nested object containing offsets data |  | other, container, object |
| `data.offsets.column` | object |  |  | Nested object containing column data |  | other, container, object |
| `data.offsets.column.1` | object |  |  | Nested object containing 1 data |  | other, container, object |
| `data.offsets.column.1.0` | object |  |  | Nested object containing 0 data |  | other, container, object |
| `data.offsets.column.1.0.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.1.0.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.column.1.1` | object |  |  | Nested object containing 1 data |  | other, container, object |
| `data.offsets.column.1.1.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.1.1.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.column.1.2` | object |  |  | Nested object containing 2 data |  | other, container, object |
| `data.offsets.column.1.2.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.1.2.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.column.2` | object |  |  | Nested object containing 2 data |  | other, container, object |
| `data.offsets.column.2.0` | object |  |  | Nested object containing 0 data |  | other, container, object |
| `data.offsets.column.2.0.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.2.0.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.column.2.1` | object |  |  | Nested object containing 1 data |  | other, container, object |
| `data.offsets.column.2.1.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.2.1.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.column.2.2` | object |  |  | Nested object containing 2 data |  | other, container, object |
| `data.offsets.column.2.2.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.2.2.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.column.3` | object |  |  | Nested object containing 3 data |  | other, container, object |
| `data.offsets.column.3.0` | object |  |  | Nested object containing 0 data |  | other, container, object |
| `data.offsets.column.3.0.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.3.0.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.column.3.2` | object |  |  | Nested object containing 2 data |  | other, container, object |
| `data.offsets.column.3.2.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.3.2.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.column.4` | object |  |  | Nested object containing 4 data |  | other, container, object |
| `data.offsets.column.4.0` | object |  |  | Nested object containing 0 data |  | other, container, object |
| `data.offsets.column.4.0.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.column.4.0.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.side_bar` | object |  |  | Nested object containing side bar data |  | other, container, object |
| `data.offsets.side_bar.0` | object |  |  | Nested object containing 0 data |  | other, container, object |
| `data.offsets.side_bar.0.3` | object |  |  | Nested object containing 3 data |  | other, container, object |
| `data.offsets.side_bar.0.3.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.3.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.4` | object |  |  | Nested object containing 4 data |  | other, container, object |
| `data.offsets.side_bar.0.4.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.4.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.6` | object |  |  | Nested object containing 6 data |  | other, container, object |
| `data.offsets.side_bar.0.6.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.6.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.7` | object |  |  | Nested object containing 7 data |  | other, container, object |
| `data.offsets.side_bar.0.7.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.7.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.8` | object |  |  | Nested object containing 8 data |  | other, container, object |
| `data.offsets.side_bar.0.8.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.8.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.9` | object |  |  | Nested object containing 9 data |  | other, container, object |
| `data.offsets.side_bar.0.9.rig_id` | null |  |  | Identifier for rig |  | other, metadata, identifier, reference |
| `data.offsets.side_bar.0.9.well_id` | null |  |  | Identifier for well |  | other, metadata, identifier, reference |
| `data.user_id` | int | 262 |  | Identifier for user |  | other, metadata, identifier, reference |
| `version` | int | 1 |  | Schema version number for this record |  | other, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | other, metadata, internal |
| `timestamp` | int | 1621345304 |  | Unix epoch timestamp (seconds) of the record |  | other, metadata, time-index, filter-key, required |
| `collection` | str | traces.offsets |  | MongoDB collection name this record belongs to |  | other, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |

#### `corva#trend-analysis`

- **Friendly Name**: trend-analysis
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/trend-analysis/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f42b14483c1fd0f90270 |  | MongoDB document unique identifier |  | other, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | other, metadata, container |
| `data.analysis` | str | over_pull |  | Analysis |  | other |
| `data.bit_depth` | float | 80.94 |  | Current depth of the drill bit |  | other, depth, drilling, real-time, key-metric |
| `data.hook_load` | float | 208.44 |  | Hook load |  | other |
| `data.hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | other, depth, drilling, real-time, key-metric |
| `data.occurrence` | bool | False |  | Flag indicating whether occurrence |  | other, boolean, flag |
| `data.baseline_hookload` | float | 208.5 |  | Baseline hookload |  | other |
| `data.baseline_bit_depth` | float | 73.55 |  | Depth value: baseline bit (ft) |  | other, depth, measurement |
| `data.baseline_hole_depth` | int | 7065 |  | Depth value: baseline hole (ft) |  | other, depth, measurement |
| `version` | int | 1 |  | Schema version number for this record |  | other, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | other, metadata, internal |
| `timestamp` | int | 1545159154 |  | Unix epoch timestamp (seconds) of the record |  | other, metadata, time-index, filter-key, required |
| `collection` | str | trend-analysis |  | MongoDB collection name this record belongs to |  | other, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |

#### `corva#trip-sheet`

- **Friendly Name**: trip-sheet
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/trip-sheet/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 5f75f850469b802512454267 |  | MongoDB document unique identifier |  | other, metadata, internal, primary-key |
| `data` | object |  |  | Container object for all measurement/computed data fields |  | other, metadata, container |
| `data.config_data` | object |  |  | Nested object containing config data data |  | other, container, object |
| `data.config_data.bha_length` | int | 1000 |  | Bha length |  | other |
| `data.config_data.active_string_id` | str | 5f75f3796c88017f9358a5fe |  | Identifier for active string |  | other, metadata, identifier, reference |
| `data.config_data.active_string_type` | str | drillstring |  | Type of active string (drillstring, casing, etc.) |  | other, bha, classification |
| `data.config_data.drillstring_number` | int | 1 |  | Drillstring/BHA run number |  | other, bha, reference, run-number |
| `data.connection_records` | array[dict] |  |  | Array of connection records records |  | other, container, array |
| `data.connection_records[].stand_id` | str | Stand |  | Identifier for stand |  | other, metadata, identifier, reference |
| `data.connection_records[].timestamp` | int | 1545452762 |  | Timestamp |  | other |
| `data.connection_records[].hole_depth` | int | 7065 |  | Current hole depth (bottom of wellbore) |  | other, depth, drilling, real-time, key-metric |
| `data.connection_records[].bit_depth_end` | float | 1007.11 |  | Bit depth end |  | other |
| `data.connection_records[].stand_counter` | int | 31 |  | Stand counter |  | other |
| `data.connection_records[].tripped_depth` | float | 132.99 |  | Depth value: tripped (ft) |  | other, depth, measurement |
| `data.connection_records[].trip_direction` | str | Trip out |  | Trip direction |  | other |
| `data.connection_records[].bit_depth_start` | float | 1141.32 |  | Bit depth start |  | other |
| `data.connection_records[].block_height_max` | float | 135.13 |  | Block height max |  | other |
| `data.connection_records[].block_height_min` | float | 2.14 |  | Block height min |  | other |
| `data.connection_records[].start_volume_ttk1` | null |  |  | Start volume ttk1 |  | other |
| `data.connection_records[].start_volume_ttk2` | null |  |  | Start volume ttk2 |  | other |
| `data.connection_records[].start_volume_active` | null |  |  | Start volume active |  | other |
| `version` | int | 1 |  | Schema version number for this record |  | other, metadata, internal, versioning |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `provider` | str | corva |  | Data provider name (typically "corva") |  | other, metadata, internal |
| `timestamp` | int | 1545241679 |  | Unix epoch timestamp (seconds) of the record |  | other, metadata, time-index, filter-key, required |
| `collection` | str | trip-sheet |  | MongoDB collection name this record belongs to |  | other, metadata, internal |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |
| `updated_at` | int | 1545452762 |  | Timestamp for updated |  | other, metadata, time |

#### `corva#well_cache`

- **Friendly Name**: well_cache
- **Data Type**: time
- **API Path**: `/api/v1/data/corva/well_cache/`

| Field Path | Type | Example | Unit | Description | Notes | Tags |
|---|---|---|---|---|---|---|
| `_id` | str | 61045ada44e8f4f4270f7aa2 |  | MongoDB document unique identifier |  | other, metadata, internal, primary-key |
| `rig` | object |  |  | Nested object containing rig data |  | other, container, object |
| `rig.id` | int | 181 |  | Numeric identifier for this record/run |  | other, metadata, identifier |
| `rig.name` | str | Rig #6 |  | Display name of the component or record |  | other, metadata, display |
| `alert` | dict | {} |  | Alert |  | other |
| `asset` | object |  |  | Nested object containing asset data |  | other, container, object |
| `asset.name` | str | Deepwater A Well |  | Display name of the component or record |  | other, metadata, display |
| `asset.state` | str | planned |  | State |  | other |
| `asset.stats` | object |  |  | Nested object containing stats data |  | other, container, object |
| `asset.stats.drilling` | object |  |  | Nested object containing drilling data |  | other, container, object |
| `asset.stats.drilling.end` | int | 1551355200 |  | End |  | other |
| `asset.stats.drilling.start` | int | 1545156000 |  | Start |  | other |
| `asset.stats.drilling.total_npt` | int | 2070000 |  | Total npt |  | other |
| `asset.stats.drilling.total_cost` | int | 0 |  | Total cost |  | other |
| `asset.stats.completions` | object |  |  | Nested object containing completions data |  | other, container, object |
| `asset.stats.completions.end` | null |  |  | End |  | other |
| `asset.stats.completions.start` | null |  |  | Start |  | other |
| `asset.stats.completions.frac_total_minutes` | int | 0 |  | Frac total minutes |  | other |
| `asset.stats.completions.wireline_total_minutes` | int | 0 |  | Wireline total minutes |  | other |
| `asset.string_design` | str | 4 |  | String design |  | other |
| `asset.target_formation` | str | Wilcox |  | Target formation |  | other |
| `company` | object |  |  | Nested object containing company data |  | other, container, object |
| `company.id` | int | 5 |  | Numeric identifier for this record/run |  | other, metadata, identifier |
| `company.name` | str | Demo |  | Display name of the component or record |  | other, metadata, display |
| `program` | object |  |  | Nested object containing program data |  | other, container, object |
| `program.id` | int | 8 |  | Numeric identifier for this record/run |  | other, metadata, identifier |
| `program.name` | str | PROGRAM 2 |  | Display name of the component or record |  | other, metadata, display |
| `asset_id` | int | 31659357 |  | Unique identifier for the well/asset this record belongs to |  | other, metadata, well-id, filter-key, required |
| `location` | object |  |  | Nested object containing location data |  | other, container, object |
| `location.type` | str | Point |  | Type classifier for this record |  | other, metadata, classification |
| `location.coordinates` | array[int] |  |  | Array of coordinates records |  | other, container, array |
| `timestamp` | int | 1629302042 |  | Unix epoch timestamp (seconds) of the record |  | other, metadata, time-index, filter-key, required |
| `company_id` | int | 5 |  | Unique identifier for the company/operator |  | other, metadata, company, filter-key |
| `corva#wits` | object |  |  | Nested object containing corva#wits data |  | other, container, object |
| `corva#wits.data` | object |  |  | Nested object containing data data |  | other, container, object |
| `corva#wits.data.state` | str | In Slips |  | State |  | other |
| `corva#wits.data.bit_depth` | float | 38.14 |  | Current depth of the drill bit |  | other, depth, drilling, real-time, key-metric |
| `corva#wits.data.hole_depth` | int | 30360 |  | Current hole depth (bottom of wellbore) |  | other, depth, drilling, real-time, key-metric |
| `corva#wits.timestamp` | int | 1553064645 |  | Timestamp |  | other |
| `frac_fleet` | dict | {} |  | Frac fleet |  | other |
| `drillout_unit` | dict | {} |  | Drillout unit |  | other |
| `app_annotation` | dict | {} |  | App annotation |  | other |
| `corva#data-mud` | object |  |  | Nested object containing corva#data mud data |  | other, container, object |
| `corva#data-mud.data` | object |  |  | Nested object containing data data |  | other, container, object |
| `corva#data-mud.data.mud_type` | str | Oil-base |  | Type classification for mud |  | other, metadata, classification |
| `corva#data-mud.data.mud_density` | float | 16.5 |  | Mud density |  | other |
| `last_active_at` | int | 1553064645 |  | Timestamp for last active |  | other, metadata, time |
| `corva#data-casing` | object |  |  | Nested object containing corva#data casing data |  | other, container, object |
| `corva#data-casing.data` | object |  |  | Nested object containing data data |  | other, container, object |
| `corva#data-casing.data.inner_diameter` | float | 9.156 |  | Inner diameter of the component (in) |  | other, bha, component, dimension, hydraulics |
| `corva#data-casing.data.outer_diameter` | float | 10.75 |  | Outer diameter of the component (in) |  | other, bha, component, dimension |
| `corva#data-casing.data.setting_timestamp` | int | 1550685391 |  | Timestamp when the drillstring was set/configured |  | other, bha, time, configuration |
| `corva#data-casing.timestamp` | int | 1585065966 |  | Timestamp |  | other |
| `corva#wireline-wits` | dict | {} |  | Corva#wireline wits |  | other |
| `corva#completion-wits` | dict | {} |  | Corva#completion wits |  | other |
| `corva#data-npt-events` | object |  |  | Nested object containing corva#data npt events data |  | other, container, object |
| `corva#data-npt-events.data` | object |  |  | Nested object containing data data |  | other, container, object |
| `corva#data-npt-events.data.type` | str | rig service |  | Type classifier for this record |  | other, metadata, classification |
| `corva#data-npt-events.data.depth` | int | 1000 |  | Depth |  | other |
| `corva#data-npt-events.data.comment` | str |  |  | Comment |  | other |
| `corva#data-npt-events.data.end_time` | int | 1545310920 |  | End time of the activity/operation (Unix epoch) |  | other, operations, time, interval |
| `corva#data-npt-events.data.is_impact` | bool | False |  | Flag indicating whether is impact |  | other, boolean, flag |
| `corva#data-npt-events.data.start_time` | int | 1545130920 |  | Start time of the activity/operation (Unix epoch) |  | other, operations, time, interval |
| `corva#data-drillstring` | object |  |  | Nested object containing corva#data drillstring data |  | other, container, object |
| `corva#data-drillstring.data` | object |  |  | Nested object containing data data |  | other, container, object |
| `corva#data-drillstring.data.id` | float | 6.93 |  | Numeric identifier for this record/run |  | other, metadata, identifier |
| `corva#data-drillstring.data.components` | array[dict] |  |  | Array of components records |  | other, container, array |
| `corva#data-drillstring.data.components[].family` | str | dp |  | Component type family (dp, hwdp, dc, bit, mwd, pdm, etc.) |  | other, bha, component, classification |
| `corva#data-drillstring.data.components[].material` | str | Steel |  | Material type (e.g., Steel, Non-Magnetic) |  | other, bha, component, material |
| `corva#data-drillstring.data.setting_timestamp` | int | 1552415528 |  | Timestamp when the drillstring was set/configured |  | other, bha, time, configuration |
| `corva#data-drillstring.timestamp` | int | 1586706777 |  | Timestamp |  | other |
| `corva#data-well-sections` | object |  |  | Nested object containing corva#data well sections data |  | other, container, object |
| `corva#data-well-sections.data` | object |  |  | Nested object containing data data |  | other, container, object |
| `corva#data-well-sections.data.name` | str | Intermediate Vertical |  | Display name of the component or record |  | other, metadata, display |
| `corva#data-well-sections.data.pre_set` | bool | False |  | Flag indicating whether pre set |  | other, boolean, flag |
| `corva#data-well-sections.data.diameter` | float | 14.5 |  | Diameter |  | other |
| `corva#data-well-sections.data.top_depth` | int | 27781 |  | Top depth of casing string (ft MD) |  | other, casing, depth, range |
| `corva#data-well-sections.data.bottom_depth` | int | 27951 |  | Bottom depth of casing string (ft MD) |  | other, casing, depth, range |
| `corva#directional-accuracy` | object |  |  | Nested object containing corva#directional accuracy data |  | other, container, object |
| `corva#directional-accuracy.data` | object |  |  | Nested object containing data data |  | other, container, object |
| `corva#directional-accuracy.data.points` | array[dict] |  |  | Array of points records |  | other, container, array |
| `corva#directional-accuracy.data.points[].severity` | str | low |  | Severity level of the alert/issue |  | other, wellness, alert, severity |
| `corva#directional-accuracy.data.points[].timestamp` | int | 1549594169 |  | Timestamp |  | other |
| `corva#directional-accuracy.data.points[].distance_to_plan` | float | 0.01 |  | Distance to plan |  | other |
| `corva#directional-accuracy.data.vertical_plane` | null |  |  | Vertical plane |  | other |
| `corva#directional-accuracy.data.horizontal_plane` | object |  |  | Nested object containing horizontal plane data |  | other, container, object |
| `corva#directional-accuracy.data.horizontal_plane.ahead` | float | 0.06 |  | Ahead |  | other |
| `corva#directional-accuracy.data.horizontal_plane.right` | float | -0.02 |  | Right |  | other |
| `corva#directional-accuracy.data.horizontal_plane.distance` | float | 0.06 |  | Distance |  | other |
| `corva#directional-accuracy.data.minimum_distance_plane` | object |  |  | Nested object containing minimum distance plane data |  | other, container, object |
| `corva#directional-accuracy.data.minimum_distance_plane.high` | int | 0 |  | High |  | other |
| `corva#directional-accuracy.data.minimum_distance_plane.right` | int | 0 |  | Right |  | other |
| `corva#directional-accuracy.data.minimum_distance_plane.distance` | float | 0.06 |  | Distance |  | other |
| `corva#completion-data-stages` | dict | {} |  | Corva#completion data stages |  | other |
| `corva#data-operation-summaries` | object |  |  | Nested object containing corva#data operation summaries data |  | other, container, object |
| `corva#data-operation-summaries.data` | object |  |  | Nested object containing data data |  | other, container, object |
| `corva#data-operation-summaries.data.summary` | str | Continued to TOH with BOP test assy from 2,550'... |  | Summary |  | other |
| `corva#data-operation-summaries.data.date_time` | int | 1551074400 |  | Timestamp for date |  | other, metadata, time |
| `corva#data-well-sections-phases` | dict | {} |  | Corva#data well sections phases |  | other |
| `corva#completion-data-ntp-events` | dict | {} |  | Corva#completion data ntp events |  | other |
| `corva#completion-data-actual-stages` | dict | {} |  | Corva#completion data actual stages |  | other |
| `corva#completion-data-operation-summaries` | dict | {} |  | Corva#completion data operation summaries |  | other |

---

## API Access Patterns

### Data API Endpoint

```
GET /api/v1/data/{provider}/{dataset}/
```

### Common Query Parameters

| Parameter | Description | Example |
|---|---|---|
| `query` | MongoDB-style query (JSON string) | `{"asset_id": 12345}` |
| `sort` | Sort order (JSON string) | `{"timestamp": -1}` |
| `limit` | Max records to return | `500` |
| `skip` | Records to skip (pagination) | `0` |
| `fields` | Comma-separated field list | `timestamp,data.hole_depth` |

### Python SDK Example

```python
# Inside a Corva app
response = api.get(
    '/api/v1/data/corva/wits/',
    params={
        'query': json.dumps({'asset_id': event.asset_id}),
        'limit': 500,
        'sort': json.dumps({'timestamp': -1}),
        'fields': 'timestamp,data.hole_depth,data.bit_depth,data.weight_on_bit'
    }
)
records = response.json()
```

### Dataset Naming Convention

- Format: `{provider}#{collection_name}` (e.g., `corva#wits`)
- API path: `/api/v1/data/{provider}/{collection_name}/`
- The `#` in the name becomes `/` in the API path

### Data Types

| Type | Description |
|---|---|
| `time` | Time-indexed data, queried by `timestamp` and `asset_id` |
| `depth` | Depth-indexed data, queried by `measured_depth` and `asset_id` |
| `reference` | Reference/configuration data, not time-series |
| `timeseries` | MongoDB time-series collection (newer format) |

---

## Glossary of Common Drilling Terms

| Term | Definition |
|---|---|
| **BHA** | Bottom Hole Assembly - the lower portion of the drill string |
| **WITS** | Wellsite Information Transfer Specification - real-time drilling data |
| **ROP** | Rate of Penetration - speed of drilling (ft/hr) |
| **WOB** | Weight on Bit - downward force applied to the drill bit (klbs) |
| **MSE** | Mechanical Specific Energy - energy required to remove rock |
| **SPP** | Standpipe Pressure - pump pressure at surface (psi) |
| **RPM** | Rotations Per Minute - rotary speed of the drill string |
| **TVD** | True Vertical Depth - vertical distance from surface |
| **MD** | Measured Depth - length of wellbore from surface |
| **ECD** | Equivalent Circulating Density - effective mud weight while circulating (ppg) |
| **PDM** | Positive Displacement Motor - downhole motor for directional drilling |
| **MWD** | Measurement While Drilling - downhole sensors for surveys |
| **NPT** | Non-Productive Time - time lost to unplanned events |
| **TFA** | Total Flow Area - combined nozzle area of the drill bit |
| **DLS** | Dog Leg Severity - rate of wellbore curvature (deg/100ft) |
| **Frac** | Hydraulic fracturing - completions stimulation technique |
| **ISIP** | Instantaneous Shut-In Pressure - pressure after pumping stops |
| **ppg** | Pounds per gallon - unit for mud weight / density |
| **klbs** | Thousands of pounds - unit for hookload, WOB |
