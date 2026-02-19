# Corva Platform – Complete Datasets Reference

> **Total Datasets**: 647  
> **Source**: Corva Dataset Explorer API (`/api/v1/data/corva/dataset/`)  
> **Generated**: 2026-02-11  

---

## Summary Statistics

### By Data Type

| Data Type | Count |
|---|---|
| time | 481 |
| reference | 151 |
| depth | 12 |
| timeseries | 3 |

### By Category

| Category | Count |
|---|---|
| WITS / Real-Time Drilling | 18 |
| Drilling | 40 |
| Directional | 26 |
| Torque & Drag | 14 |
| Hydraulics | 5 |
| PDM / Motor | 3 |
| Circulation | 3 |
| Activities / Operations | 15 |
| Well Data (data.*) | 53 |
| Completions / Frac | 78 |
| Wireline | 3 |
| Pumpdown | 2 |
| Drillout | 23 |
| Anti-Collision | 24 |
| Cementing | 2 |
| Geosteering | 7 |
| Formation Evaluation | 2 |
| Downhole Sensors | 6 |
| Predictive Drilling / ML | 7 |
| Alerts | 11 |
| Well Design | 5 |
| Well Design (design.*) | 7 |
| Metrics / KPIs | 8 |
| Time Log | 4 |
| Production (Enverus) | 26 |
| Sustainability / ESG | 10 |
| Wellness / Check-Up | 16 |
| Stream Quality | 7 |
| Handover / Mission Control | 7 |
| Interventions (Workover) | 38 |
| Launchpad / Connectivity | 9 |
| AskCorva / AI | 3 |
| Bowtie / Insights | 2 |
| Frac Third-Party | 7 |
| Nabors Integration | 15 |
| WITS (Other Phases) | 34 |
| Other | 107 |

---

## Dataset Catalog by Category

### 1. WITS / Real-Time Drilling (18 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#wits` | wits | time |  | Historical and streaming wits data after passing through data quality checks and true vertical depth functions |
| 2 | `corva#wits.comments` | wits.comments | time |  |  |
| 3 | `corva#wits.etl-latency` | wits.etl-latency | time |  |  |
| 4 | `corva#wits.metadata` | wits.metadata | time |  | This dataset stores the WITSML channels directly from the WITSML store. This includes the mnemonic that is received f... |
| 5 | `corva#wits.secondary` | wits.secondary | time | Yes | WITS Secondary Channels |
| 6 | `corva#wits.summary-10s` | wits.summary-10s | timeseries |  |  |
| 7 | `corva#wits.summary-15ft` | wits.summary-15ft | time |  | This dataset stores aggregated drilling data at 15-foot depth intervals, derived from the wits.summary-1ft dataset. I... |
| 8 | `corva#wits.summary-1ft` | wits.summary-1ft | time |  | 1 ft summary of corrected wits data |
| 9 | `corva#wits.summary-1ft.metadata` | wits.summary-1ft.metadata | time |  |  |
| 10 | `corva#wits.summary-1m` | wits.summary-1m | time |  | 1 minute Summary of corrected wits data (median values) |
| 11 | `corva#wits.summary-1m.metadata` | wits.summary-1m.metadata | time |  |  |
| 12 | `corva#wits.summary-30m` | wits.summary-30m | time |  | 30 minute summary of corrected wits data (median values) |
| 13 | `corva#wits.summary-30m.metadata` | wits.summary-30m.metadata | time |  |  |
| 14 | `corva#wits.summary-30s` | wits.summary-30s | time |  |  |
| 15 | `corva#wits.summary-6h` | wits.summary-6h | time |  | 6 hour Summary of corrected wits data (median values) |
| 16 | `corva#wits.summary-6h.metadata` | wits.summary-6h.metadata | time |  |  |
| 17 | `corva#witsml-log.metadata` | witsml-log.metadata | time |  |  |
| 18 | `corva#witsml_tubular` | witsml_tubular | time |  |  |

### 2. Drilling (40 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#drilling-ai` | drilling-ai | time |  |  |
| 2 | `corva#drilling-dysfunction` | drilling-dysfunction | time |  |  |
| 3 | `corva#drilling-efficiency.mse` | drilling-efficiency.mse | time |  |  |
| 4 | `corva#drilling-efficiency.mse-heatmap` | drilling-efficiency.mse-heatmap | time |  |  |
| 5 | `corva#drilling-efficiency.mse.imports` | drilling-efficiency.mse.imports | time |  |  |
| 6 | `corva#drilling-efficiency.optimization` | drilling-efficiency.optimization | time |  | Actual drilling parameters (inclination, RPM, ROP, Mud flow, WOB, gamma ray, bit size, state) vs recommended drilling... |
| 7 | `corva#drilling-efficiency.predictions` | drilling-efficiency.predictions | time |  |  |
| 8 | `corva#drilling-efficiency.rop-heatmap` | drilling-efficiency.rop-heatmap | time |  |  |
| 9 | `corva#drilling-roadmap` | drilling-roadmap | time |  | Drilling roadmap which has WOB, Diff pressures, RPM, Torque, MSE. ROP's. Mud densities, Flow In's, and Hazards from o... |
| 10 | `corva#drilling-roadmap.hazard` | drilling-roadmap.hazard | time |  |  |
| 11 | `corva#drilling-roadmap.hazard.log` | drilling-roadmap.hazard.log | time |  |  |
| 12 | `corva#drilling-roadmap.scoring` | drilling-roadmap.scoring | time |  | Actuals values for drillers roadmap WOB, Diff pressures, RPM, Torque, MSE. ROP's. Mud densities, Flow In's, and Hazar... |
| 13 | `corva#drilling.24-and-48-hr-footage-drilled` | drilling.24-and-48-hr-footage-drilled | time | Yes |  |
| 14 | `corva#drilling.aerion.centrifuge.data` | drilling.aerion.centrifuge.data | time |  |  |
| 15 | `corva#drilling.aerion.mudsensor.data` | drilling.aerion.mudsensor.data | time |  | Aerion Mudsensor data |
| 16 | `corva#drilling.bit-pressure.depth.summary` | drilling.bit-pressure.depth.summary | time |  |  |
| 17 | `corva#drilling.drilling2.summary-1ft` | drilling.drilling2.summary-1ft | time |  |  |
| 18 | `corva#drilling.ecd` | drilling.ecd | time |  |  |
| 19 | `corva#drilling.halliburton.cerebro-raw` | drilling.halliburton.cerebro-raw | reference |  | Captures continuous high-resolution bit sensor data |
| 20 | `corva#drilling.hookload-plus-weight-on-bit` | drilling.hookload-plus-weight-on-bit | time | Yes |  |
| 21 | `corva#drilling.mud-ops` | drilling.mud-ops | time |  | This dataset saves drilling ops mud data that includes pit information, inventory information, volumes, material pric... |
| 22 | `corva#drilling.mudlog.depth` | drilling.mudlog.depth | depth |  | The mudLog object is used to capture information in a mud log. This includes lithologic information derived from cutt... |
| 23 | `corva#drilling.mudlog.depth.metadata` | drilling.mudlog.depth.metadata | depth |  | Metadata for mudlogs collection |
| 24 | `corva#drilling.neptune.backreaming.pipelimit` | drilling.neptune.backreaming.pipelimit | reference |  |  |
| 25 | `corva#drilling.petro.summary-1ft` | drilling.petro.summary-1ft | time |  |  |
| 26 | `corva#drilling.petro.summary-1ft.metadata` | drilling.petro.summary-1ft.metadata | time |  |  |
| 27 | `corva#drilling.pipetally.upload` | drilling.pipetally.upload | reference |  |  |
| 28 | `corva#drilling.timelog-aux.data` | drilling.timelog-aux.data | time |  |  |
| 29 | `corva#drilling.timelog.data` | drilling.timelog.data | time |  |  |
| 30 | `corva#drilling.topdrive.powercurve` | drilling.topdrive.powercurve | reference |  |  |
| 31 | `corva#drilling.wits.depth` | drilling.wits.depth | depth |  |  |
| 32 | `corva#drilling.wits.depth.metadata` | drilling.wits.depth.metadata | time |  |  |
| 33 | `corva#drilling.wits.depth.summary-0.5ft` | drilling.wits.depth.summary-0.5ft | depth |  |  |
| 34 | `corva#drilling.wits.depth.summary-0.5ft.tvd` | drilling.wits.depth.summary-0.5ft.tvd | depth |  |  |
| 35 | `corva#drilling.wits.depth.summary-10ft` | drilling.wits.depth.summary-10ft | depth |  |  |
| 36 | `corva#drilling.wits.depth.summary-10ft.tvd` | drilling.wits.depth.summary-10ft.tvd | depth |  | Depth summary calculated by TVD value, instead of MD |
| 37 | `corva#drilling.wits.depth.summary-1ft` | drilling.wits.depth.summary-1ft | depth |  |  |
| 38 | `corva#drilling.wits.depth.summary-1ft.tvd` | drilling.wits.depth.summary-1ft.tvd | depth |  | Depth summary calculated by TVD value, instead of MD |
| 39 | `corva#drilling_mechanics_memory` | drilling_mechanics_memory | time | Yes | Drilling Mechanics Memory |
| 40 | `corva#drilling_program_automation` | drilling_program_automation | reference |  |  |

### 3. Directional (26 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#directional.accuracy` | directional.accuracy | time |  |  |
| 2 | `corva#directional.actual_survey_divergence` | directional.actual_survey_divergence | time |  | additional information(divergence values) for data.actual_survey records |
| 3 | `corva#directional.custom_bit_projection` | directional.custom_bit_projection | time |  | Custom bit projections - RSS bit projection, Motor bit projection, etc. Generated in either Auto Projection Scheduler... |
| 4 | `corva#directional.custom_bit_projection.logging` | directional.custom_bit_projection.logging | reference |  | optional log/history of custom_bit_projection records, needed for accuracy evaluation, controlled by hidden toggle on FE |
| 5 | `corva#directional.default_bit_projection` | directional.default_bit_projection | time |  | Default bit projection, based on motor bit projection. Generated mostly in Auto Projection Scheduler and sometimes in... |
| 6 | `corva#directional.enriched-surveys` | directional.enriched-surveys | time |  |  |
| 7 | `corva#directional.guidance` | directional.guidance | time |  |  |
| 8 | `corva#directional.guidance_log` | directional.guidance_log | time |  |  |
| 9 | `corva#directional.guidance_recommendation` | directional.guidance_recommendation | time |  |  |
| 10 | `corva#directional.guidance_settings` | directional.guidance_settings | time |  |  |
| 11 | `corva#directional.guidance_step_history` | directional.guidance_step_history | time |  |  |
| 12 | `corva#directional.motor_yield.summary-1ft` | directional.motor_yield.summary-1ft | depth |  |  |
| 13 | `corva#directional.pre-post-slide` | directional.pre-post-slide | time |  | pre post slide calculation |
| 14 | `corva#directional.projection` | directional.projection | time |  |  |
| 15 | `corva#directional.projection_to_bit` | directional.projection_to_bit | time |  |  |
| 16 | `corva#directional.rotational-tendency` | directional.rotational-tendency | time |  | Build and turn rate by depth as measured by MWD tool. If continuous inclination is available from the MWD tool, then ... |
| 17 | `corva#directional.scenario-manual` | directional.scenario-manual | time |  | Manual scenarios for directional projections(Survey Projection Calculator app) |
| 18 | `corva#directional.settings` | directional.settings | reference |  |  |
| 19 | `corva#directional.slide-sheet` | directional.slide-sheet | time |  |  |
| 20 | `corva#directional.surveys` | directional.surveys | time |  | Planned and actual surveys in the same collection |
| 21 | `corva#directional.tool-face-orientation` | directional.tool-face-orientation | time |  |  |
| 22 | `corva#directional.tool_face` | directional.tool_face | depth |  |  |
| 23 | `corva#directional.toolface.summary-1ft` | directional.toolface.summary-1ft | time |  | This collection is a 1-foot summary of the toolface values (both magnetic and gravity) and the active type while Slid... |
| 24 | `corva#directional.tortuosity` | directional.tortuosity | time |  |  |
| 25 | `corva#directional.trend` | directional.trend | time |  |  |
| 26 | `corva#directional.wellbore-quality` | directional.wellbore-quality | time |  | Stores H&P Wellbore Quality Data |

### 4. Torque & Drag (14 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#torque-and-drag.axial-load` | torque-and-drag.axial-load | time |  |  |
| 2 | `corva#torque-and-drag.downhole-transfer` | torque-and-drag.downhole-transfer | time |  |  |
| 3 | `corva#torque-and-drag.friction-factor` | torque-and-drag.friction-factor | time |  |  |
| 4 | `corva#torque-and-drag.friction-factor-overrides` | torque-and-drag.friction-factor-overrides | time |  |  |
| 5 | `corva#torque-and-drag.hookload-trend` | torque-and-drag.hookload-trend | time |  |  |
| 6 | `corva#torque-and-drag.hookload-trend.actual` | torque-and-drag.hookload-trend.actual | time |  |  |
| 7 | `corva#torque-and-drag.hookload-trend.imports` | torque-and-drag.hookload-trend.imports | time |  |  |
| 8 | `corva#torque-and-drag.overview` | torque-and-drag.overview | time |  |  |
| 9 | `corva#torque-and-drag.predictions` | torque-and-drag.predictions | time |  |  |
| 10 | `corva#torque-and-drag.stress` | torque-and-drag.stress | time |  |  |
| 11 | `corva#torque-and-drag.torque` | torque-and-drag.torque | time |  |  |
| 12 | `corva#torque-and-drag.torque-trend` | torque-and-drag.torque-trend | time |  |  |
| 13 | `corva#torque-and-drag.torque-trend.actual` | torque-and-drag.torque-trend.actual | time |  |  |
| 14 | `corva#torque-and-drag.torque-trend.imports` | torque-and-drag.torque-trend.imports | time |  |  |

### 5. Hydraulics (5 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#hydraulics.cuttings-transport` | hydraulics.cuttings-transport | time |  |  |
| 2 | `corva#hydraulics.overview` | hydraulics.overview | time |  |  |
| 3 | `corva#hydraulics.pressure-loss` | hydraulics.pressure-loss | time |  |  |
| 4 | `corva#hydraulics.pressure-trend` | hydraulics.pressure-trend | time |  |  |
| 5 | `corva#hydraulics.surge-and-swab` | hydraulics.surge-and-swab | time |  |  |

### 6. PDM / Motor (3 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#pdm.operating-condition` | pdm.operating-condition | time |  |  |
| 2 | `corva#pdm.overview` | pdm.overview | time |  |  |
| 3 | `corva#pdm.stall-detection` | pdm.stall-detection | time |  |  |

### 7. Circulation (3 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#circulation.lag-depth` | circulation.lag-depth | time |  |  |
| 2 | `corva#circulation.lost-circulation` | circulation.lost-circulation | time |  |  |
| 3 | `corva#circulation.volumetric` | circulation.volumetric | time |  |  |

### 8. Activities / Operations (15 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#activities` | activities | time |  | Description of rig activity states |
| 2 | `corva#activities.summary-1m` | activities.summary-1m | time |  | List of activities that have occurred within the last minute (1 minute) |
| 3 | `corva#activities.summary-1w` | activities.summary-1w | time |  | List of activities that have occurred within the last week (1 week) |
| 4 | `corva#activities.summary-2tours` | activities.summary-2tours | time |  |  |
| 5 | `corva#activities.summary-3m` | activities.summary-3m | time |  |  |
| 6 | `corva#activities.summary-continuous` | activities.summary-continuous | time |  |  |
| 7 | `corva#activity-groups` | activity-groups | time |  | Data from activities collection is aggregated by activity-groups |
| 8 | `corva#activity_tracker` | activity_tracker | time |  |  |
| 9 | `corva#activity_tracker_pad_metadata` | activity_tracker_pad_metadata | reference |  |  |
| 10 | `corva#operations` | operations | time |  | Description of rig operations in 20 sec intervals. Data: shift, well section, hole size, operation (tripping out/in, ... |
| 11 | `corva#operations.summary-1m` | operations.summary-1m | time |  |  |
| 12 | `corva#operations.summary-1w` | operations.summary-1w | time |  |  |
| 13 | `corva#operations.summary-2tours` | operations.summary-2tours | time |  |  |
| 14 | `corva#operations.summary-3m` | operations.summary-3m | time |  |  |
| 15 | `corva#operations.summary-continuous` | operations.summary-continuous | time |  |  |

### 9. Well Data (data.*) (53 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#data.actual_survey` | data.actual_survey | time |  | Survey data: MD, inclination, azimuth, tvd, northing, easting, dls, and vertical section |
| 2 | `corva#data.actual_survey.edm` | data.actual_survey.edm | time |  | Actual survey extracted from EDM file(in anti collision app). |
| 3 | `corva#data.actual_survey.email` | data.actual_survey.email | time |  |  |
| 4 | `corva#data.actual_survey.manual` | data.actual_survey.manual | time |  |  |
| 5 | `corva#data.actual_survey.source` | data.actual_survey.source | time |  |  |
| 6 | `corva#data.actual_survey.witsml` | data.actual_survey.witsml | time |  |  |
| 7 | `corva#data.actual_survey_divergence` | data.actual_survey_divergence | time |  |  |
| 8 | `corva#data.afe` | data.afe | time |  |  |
| 9 | `corva#data.afe.curve` | data.afe.curve | time |  |  |
| 10 | `corva#data.analytics.drillstring` | data.analytics.drillstring | time |  |  |
| 11 | `corva#data.bha.dd_comments` | data.bha.dd_comments | time |  |  |
| 12 | `corva#data.bha.run_summary` | data.bha.run_summary | time |  |  |
| 13 | `corva#data.casing` | data.casing | time |  |  |
| 14 | `corva#data.completion.npt-codes` | data.completion.npt-codes | reference |  | Collection to store completion NPT code mapping |
| 15 | `corva#data.costs` | data.costs | time |  |  |
| 16 | `corva#data.crew-shift` | data.crew-shift | time |  |  |
| 17 | `corva#data.crews` | data.crews | time |  |  |
| 18 | `corva#data.custom_curves` | data.custom_curves | time |  |  |
| 19 | `corva#data.cuttings` | data.cuttings | time |  |  |
| 20 | `corva#data.dd-mission-control-well-notes` | data.dd-mission-control-well-notes | time |  |  |
| 21 | `corva#data.diaries` | data.diaries | time |  |  |
| 22 | `corva#data.drilling-window` | data.drilling-window | time |  |  |
| 23 | `corva#data.drilling.sop` | data.drilling.sop | reference |  | Drilling analyst uses SOPs to coordinate and escalate confirmed Corva platform outages quickly and consistently. The ... |
| 24 | `corva#data.drillstring` | data.drillstring | time |  | Describes full drillstring (drill pipe/collars, pdm, bits, etc.) and parameters associated with each component |
| 25 | `corva#data.drillstring.drillpipe_specs` | data.drillstring.drillpipe_specs | reference |  | Contains data of Ops expectation of the drill pipe on location at the rig. Data is refreshed daily from a spreadsheet... |
| 26 | `corva#data.drillstring.planned` | data.drillstring.planned | time |  |  |
| 27 | `corva#data.emission-factor` | data.emission-factor | reference |  |  |
| 28 | `corva#data.files` | data.files | time |  |  |
| 29 | `corva#data.formation-dips` | data.formation-dips | time |  | Dataset for storing formation dips |
| 30 | `corva#data.formations` | data.formations | time |  | Formation (lithology and name) data by Asset with TVD and MD. |
| 31 | `corva#data.headquarters-well-notes` | data.headquarters-well-notes | time |  |  |
| 32 | `corva#data.hole-cleaning` | data.hole-cleaning | time |  |  |
| 33 | `corva#data.insights.events` | data.insights.events | time |  |  |
| 34 | `corva#data.insights.files` | data.insights.files | time |  |  |
| 35 | `corva#data.lessons-learned` | data.lessons-learned | time |  | Collection for lessons learned |
| 36 | `corva#data.lessons-learned-codes` | data.lessons-learned-codes | reference |  | Collection for lessons learned codes |
| 37 | `corva#data.lessons-learned.settings` | data.lessons-learned.settings | time |  | Collection for lessons learned settings |
| 38 | `corva#data.map` | data.map | time |  |  |
| 39 | `corva#data.mud` | data.mud | time |  | The data in this dataset represents drilling mud data. This data is represented in the WellHub Fluid Checks page in t... |
| 40 | `corva#data.mud.plan` | data.mud.plan | time |  |  |
| 41 | `corva#data.npt-codes` | data.npt-codes | reference |  | Collection to store npt code mapping |
| 42 | `corva#data.npt-events` | data.npt-events | time |  |  |
| 43 | `corva#data.offset-wells.bic` | data.offset-wells.bic | time |  | Collection for best in class offset wells |
| 44 | `corva#data.offset_wells` | data.offset_wells | time |  |  |
| 45 | `corva#data.operation-summaries` | data.operation-summaries | time |  |  |
| 46 | `corva#data.plan_survey` | data.plan_survey | time |  | Planned survey data: MD, inclination, azimuth, tvd, northing, easting, dls, and vertical section |
| 47 | `corva#data.pressure-gradient` | data.pressure-gradient | time |  |  |
| 48 | `corva#data.surface-equipment` | data.surface-equipment | time |  |  |
| 49 | `corva#data.survey-projections` | data.survey-projections | time |  |  |
| 50 | `corva#data.survey_management_system.cache` | data.survey_management_system.cache | time |  | Used as an intermediate cache collection b/w survey management task and stream applications |
| 51 | `corva#data.sustainability` | data.sustainability | time |  |  |
| 52 | `corva#data.well-sections` | data.well-sections | time |  |  |
| 53 | `corva#data.well-sections.phases` | data.well-sections.phases | time |  |  |

### 10. Completions / Frac (78 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#completion-teams` | completion-teams | reference |  |  |
| 2 | `corva#completion.activity.summary-stage` | completion.activity.summary-stage | time |  | Contains a summarized start/end time for all activities on each individual frac stage. |
| 3 | `corva#completion.activity.viewer` | completion.activity.viewer | time |  |  |
| 4 | `corva#completion.ccl-annotations` | completion.ccl-annotations | time |  |  |
| 5 | `corva#completion.ccl-annotations-test` | completion.ccl-annotations-test | time |  |  |
| 6 | `corva#completion.ccl-anomalies` | completion.ccl-anomalies | reference |  |  |
| 7 | `corva#completion.ccl-anomalies-model-runs` | completion.ccl-anomalies-model-runs | time |  | This dataset stores the model runs for detecting casing anomalies from high frequency wireline CCL data. |
| 8 | `corva#completion.ccl-collars` | completion.ccl-collars | reference |  |  |
| 9 | `corva#completion.ccl-filtered-summary-runs` | completion.ccl-filtered-summary-runs | time |  | This dataset stores the wireline state, RIH / POOH, for the real time high frequency data. |
| 10 | `corva#completion.ccl-raw-data` | completion.ccl-raw-data | time |  | This dataset stores real time, high frequency CCL, Line Tension, Line Speed, measured depth, mean CCL, min CCL, max C... |
| 11 | `corva#completion.ccl-settings` | completion.ccl-settings | time |  |  |
| 12 | `corva#completion.ccl-settings-test` | completion.ccl-settings-test | time |  |  |
| 13 | `corva#completion.ccl-summary` | completion.ccl-summary | reference |  |  |
| 14 | `corva#completion.custom_metrics` | completion.custom_metrics | time |  | completion metrics tailored to client specifications |
| 15 | `corva#completion.data.actual-stages` | completion.data.actual-stages | time |  | Contains post-job report information received from the frac service provider. It contains fluids, chemical, proppant,... |
| 16 | `corva#completion.data.actual-steps` | completion.data.actual-steps | time |  |  |
| 17 | `corva#completion.data.afe` | completion.data.afe | time |  | Summary of days, depth and cost of a well |
| 18 | `corva#completion.data.costs` | completion.data.costs | time |  | Contains daily cost information received in morning reports. |
| 19 | `corva#completion.data.crews` | completion.data.crews | time |  | Contains information on which service companies are providing frac/wireline/chemical services. |
| 20 | `corva#completion.data.fiber-optic.heatmap` | completion.data.fiber-optic.heatmap | time |  |  |
| 21 | `corva#completion.data.fiber-optic.table` | completion.data.fiber-optic.table | time |  |  |
| 22 | `corva#completion.data.files` | completion.data.files | time |  | These are file names and unique identifiers that are uploaded to Corva Wellhub. |
| 23 | `corva#completion.data.job-settings` | completion.data.job-settings | time |  | Prejob settings input into Wellhub Job Settings section. |
| 24 | `corva#completion.data.master-frac` | completion.data.master-frac | time |  | PJR data for master frac |
| 25 | `corva#completion.data.npt-events` | completion.data.npt-events | time |  | Contains information surrounding NPT for each individual well received from morning reports. |
| 26 | `corva#completion.data.operation-summaries` | completion.data.operation-summaries | time |  | Contains summary information from 24 hour morning reports. |
| 27 | `corva#completion.data.plugid` | completion.data.plugid | time |  | Plug identification fields |
| 28 | `corva#completion.data.plugs` | completion.data.plugs | time |  | Contains frac plug data for drill-outs and more specific plug information than what is found in completion.data.stages. |
| 29 | `corva#completion.data.plugs.actual` | completion.data.plugs.actual | time |  |  |
| 30 | `corva#completion.data.proposed-stages` | completion.data.proposed-stages | time |  |  |
| 31 | `corva#completion.data.proposed-stages.metadata` | completion.data.proposed-stages.metadata | time |  |  |
| 32 | `corva#completion.data.purged_stages` | completion.data.purged_stages | reference |  | Collection for tracking purge frac stages |
| 33 | `corva#completion.data.stages` | completion.data.stages | time |  | Contains design information. This is typically uploaded before the job has begun once designs are received. |
| 34 | `corva#completion.data.time-log` | completion.data.time-log | time |  | Contains data for time analysis app. Has a near-uninterrupted continuous summary of operations for each well (frac an... |
| 35 | `corva#completion.data.time-log.wv` | completion.data.time-log.wv | time |  |  |
| 36 | `corva#completion.data.well-goals` | completion.data.well-goals | time |  |  |
| 37 | `corva#completion.data_quality.report` | completion.data_quality.report | time |  |  |
| 38 | `corva#completion.detailed-costs` | completion.detailed-costs | time |  | BE collection for completions cost detailed with line items. |
| 39 | `corva#completion.dynamic-frac-stats` | completion.dynamic-frac-stats | time |  |  |
| 40 | `corva#completion.evo_metrics_stages` | completion.evo_metrics_stages | time |  |  |
| 41 | `corva#completion.fdi` | completion.fdi | time |  |  |
| 42 | `corva#completion.fracvision-notifications` | completion.fracvision-notifications | time |  |  |
| 43 | `corva#completion.fracvision-recommendations` | completion.fracvision-recommendations | time |  | Staging recommendations to display in Frac Vision app |
| 44 | `corva#completion.fracvision-settings` | completion.fracvision-settings | time |  |  |
| 45 | `corva#completion.insights` | completion.insights | time |  | Completion insights app dataset |
| 46 | `corva#completion.manual.phases` | completion.manual.phases | time |  |  |
| 47 | `corva#completion.manual.points` | completion.manual.points | time |  |  |
| 48 | `corva#completion.metrics` | completion.metrics | time |  | Contains aggregated data used to generate pad metrics app. |
| 49 | `corva#completion.mis.mapping` | completion.mis.mapping | reference |  | Dataset for storing WITSML Schema mappings |
| 50 | `corva#completion.note` | completion.note | time |  | collect user notes for frac operations |
| 51 | `corva#completion.offset.abra` | completion.offset.abra | time |  | Completion offset COP data from Abra |
| 52 | `corva#completion.offset.abra.metadata` | completion.offset.abra.metadata | time |  | metadata for abra offset |
| 53 | `corva#completion.pad_sequence` | completion.pad_sequence | reference |  |  |
| 54 | `corva#completion.predictions` | completion.predictions | time |  | Breakdown, ISIP pressure predictions by elapsed time (pressure, flow rate, cumulative volumes) |
| 55 | `corva#completion.pumps` | completion.pumps | time |  | Coldbore pump data |
| 56 | `corva#completion.pumps.pad` | completion.pumps.pad | reference |  | Coldbore pump data collected per pad |
| 57 | `corva#completion.pumps.summary-1m` | completion.pumps.summary-1m | time |  | Coldbore pump metrics 1m summary |
| 58 | `corva#completion.pumps_metrics` | completion.pumps_metrics | time |  |  |
| 59 | `corva#completion.pumps_stages` | completion.pumps_stages | time |  |  |
| 60 | `corva#completion.redzone-status` | completion.redzone-status | time |  | Status for fleet records to assist with staging and notifications |
| 61 | `corva#completion.schedule-adherence` | completion.schedule-adherence | time |  | metrics for measuring the adherence to the pumping schedule |
| 62 | `corva#completion.stage-running-average-1min` | completion.stage-running-average-1min | time |  | save averages from guided insights |
| 63 | `corva#completion.stage-times` | completion.stage-times | time |  | Frac stage start and end times and stage duration. |
| 64 | `corva#completion.time_at_rates_metrics` | completion.time_at_rates_metrics | time |  |  |
| 65 | `corva#completion.tracking` | completion.tracking | time |  |  |
| 66 | `corva#completion.tracking.events` | completion.tracking.events | time |  |  |
| 67 | `corva#completion.trouble-stage` | completion.trouble-stage | time |  | saves detected troubles for stages |
| 68 | `corva#completion.valve` | completion.valve | time |  |  |
| 69 | `corva#completion.well-track` | completion.well-track | time |  |  |
| 70 | `corva#completions-handover-contact-notes` | completions-handover-contact-notes | time |  | Contact details left by the analysts in the mission-control-completions application. |
| 71 | `corva#completions-handover-notes` | completions-handover-notes | time |  | Notes and comments left by the analysts in the mission-control-completions application. |
| 72 | `corva#completions-handover-review-info` | completions-handover-review-info | time |  | Collection stores who and when reviewed the fleet, also who marked fleet as important in the mission-control-completi... |
| 73 | `corva#completions.autostaging-stats` | completions.autostaging-stats | reference |  |  |
| 74 | `corva#completions.mgb.fuelcell.calc` | completions.mgb.fuelcell.calc | time |  |  |
| 75 | `corva#completions.mgb.fuelcell.calc.summary` | completions.mgb.fuelcell.calc.summary | time |  |  |
| 76 | `corva#completions.mgb.fuelcell.enginedata` | completions.mgb.fuelcell.enginedata | reference |  |  |
| 77 | `corva#completions.mgb.fuelcell.fuel-costs` | completions.mgb.fuelcell.fuel-costs | reference |  |  |
| 78 | `corva#completions.mgb.fuelcell.raw` | completions.mgb.fuelcell.raw | time |  |  |

### 11. Wireline (3 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#wireline.activity.summary-stage` | wireline.activity.summary-stage | time |  | Contains a summarized times for all activities on each individual wireline stage. |
| 2 | `corva#wireline.predictions` | wireline.predictions | time |  |  |
| 3 | `corva#wireline.stage-times` | wireline.stage-times | time |  | Wireline stage start and end times and stage duration |

### 12. Pumpdown (2 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#pumpdown.activity.summary-stage` | pumpdown.activity.summary-stage | time |  | Contains a summarized times for all activities on each individual pumpdown stage. |
| 2 | `corva#pumpdown.predictions` | pumpdown.predictions | time |  |  |

### 13. Drillout (23 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#drillout.activities` | drillout.activities | time |  |  |
| 2 | `corva#drillout.activities.summary-2tours` | drillout.activities.summary-2tours | time |  |  |
| 3 | `corva#drillout.activities.summary-continuous` | drillout.activities.summary-continuous | time |  |  |
| 4 | `corva#drillout.activity-groups` | drillout.activity-groups | time |  |  |
| 5 | `corva#drillout.circulation.volumetric` | drillout.circulation.volumetric | time |  |  |
| 6 | `corva#drillout.data.costs` | drillout.data.costs | time |  |  |
| 7 | `corva#drillout.data.crews` | drillout.data.crews | time |  |  |
| 8 | `corva#drillout.data.drillstring` | drillout.data.drillstring | time |  |  |
| 9 | `corva#drillout.data.files` | drillout.data.files | time |  |  |
| 10 | `corva#drillout.data.mud` | drillout.data.mud | time |  |  |
| 11 | `corva#drillout.data.npt-events` | drillout.data.npt-events | time |  |  |
| 12 | `corva#drillout.data.operation-summaries` | drillout.data.operation-summaries | time |  |  |
| 13 | `corva#drillout.data.surface-equipment` | drillout.data.surface-equipment | time |  |  |
| 14 | `corva#drillout.hydraulics.pressure-loss` | drillout.hydraulics.pressure-loss | time |  |  |
| 15 | `corva#drillout.hydraulics.pressure-trend` | drillout.hydraulics.pressure-trend | time |  |  |
| 16 | `corva#drillout.operations` | drillout.operations | time |  |  |
| 17 | `corva#drillout.parameter-sheet` | drillout.parameter-sheet | time |  |  |
| 18 | `corva#drillout.torque-and-drag.axial-load` | drillout.torque-and-drag.axial-load | time |  |  |
| 19 | `corva#drillout.torque-and-drag.hookload-trend` | drillout.torque-and-drag.hookload-trend | time |  |  |
| 20 | `corva#drillout.torque-and-drag.hookload-trend.actual` | drillout.torque-and-drag.hookload-trend.actual | time |  |  |
| 21 | `corva#drillout.torque-and-drag.stress` | drillout.torque-and-drag.stress | time |  |  |
| 22 | `corva#drillout.torque-and-drag.torque-trend` | drillout.torque-and-drag.torque-trend | time |  |  |
| 23 | `corva#drillout.torque-and-drag.torque-trend.actual` | drillout.torque-and-drag.torque-trend.actual | time |  |  |

### 14. Anti-Collision (24 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#anti-collision.alert` | anti-collision.alert | time |  |  |
| 2 | `corva#anti-collision.boundary-lines` | anti-collision.boundary-lines | time |  |  |
| 3 | `corva#anti-collision.clearance` | anti-collision.clearance | time |  |  |
| 4 | `corva#anti-collision.clearance-plan` | anti-collision.clearance-plan | time |  | Anti-collision clearance calculations for the well plan surveys. |
| 5 | `corva#anti-collision.clearance.projection` | anti-collision.clearance.projection | time |  |  |
| 6 | `corva#anti-collision.clearance.projection-manual` | anti-collision.clearance.projection-manual | time |  |  |
| 7 | `corva#anti-collision.clearances` | anti-collision.clearances | time |  | A collection used for storing anti-collision results such as separation factors |
| 8 | `corva#anti-collision.edm-data.metadata-edm` | anti-collision.edm-data.metadata-edm | reference |  |  |
| 9 | `corva#anti-collision.edm-data.metadata-well` | anti-collision.edm-data.metadata-well | reference |  |  |
| 10 | `corva#anti-collision.error.offset` | anti-collision.error.offset | time |  |  |
| 11 | `corva#anti-collision.error.offset-tracked` | anti-collision.error.offset-tracked | time |  |  |
| 12 | `corva#anti-collision.error.reference` | anti-collision.error.reference | time |  |  |
| 13 | `corva#anti-collision.error.reference.projection` | anti-collision.error.reference.projection | time |  |  |
| 14 | `corva#anti-collision.error.reference.projection-manual` | anti-collision.error.reference.projection-manual | time |  |  |
| 15 | `corva#anti-collision.errors` | anti-collision.errors | reference |  |  |
| 16 | `corva#anti-collision.errors.offsets` | anti-collision.errors.offsets | reference |  |  |
| 17 | `corva#anti-collision.metadata-edm` | anti-collision.metadata-edm | reference |  |  |
| 18 | `corva#anti-collision.metadata-well` | anti-collision.metadata-well | reference |  |  |
| 19 | `corva#anti-collision.plot` | anti-collision.plot | time |  |  |
| 20 | `corva#anti-collision.plot-3d` | anti-collision.plot-3d | time |  |  |
| 21 | `corva#anti-collision.setting` | anti-collision.setting | time |  |  |
| 22 | `corva#anti-collision.setting.updated` | anti-collision.setting.updated | time |  |  |
| 23 | `corva#anti-collision.settings` | anti-collision.settings | reference |  |  |
| 24 | `corva#anti-collision.tool-error-model` | anti-collision.tool-error-model | reference |  |  |

### 15. Cementing (2 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#cement.csv-1s` | cement.csv-1s | time | Yes |  |
| 2 | `corva#cement.csv-1s.metadata` | cement.csv-1s.metadata | time |  |  |

### 16. Geosteering (7 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#geosteering.data.interpretation` | geosteering.data.interpretation | time |  |  |
| 2 | `corva#geosteering.data.interpretation.metadata` | geosteering.data.interpretation.metadata | time |  |  |
| 3 | `corva#geosteering.horizons.data` | geosteering.horizons.data | time |  |  |
| 4 | `corva#geosteering.segments.data` | geosteering.segments.data | time |  |  |
| 5 | `corva#geosteering.segments.metadata` | geosteering.segments.metadata | time |  |  |
| 6 | `corva#geosteering.typewell.data` | geosteering.typewell.data | time |  |  |
| 7 | `corva#geosteering.typewell.metadata` | geosteering.typewell.metadata | time |  |  |

### 17. Formation Evaluation (2 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#formation-evaluation.data` | formation-evaluation.data | time |  |  |
| 2 | `corva#formation-evaluation.metadata` | formation-evaluation.metadata | time |  |  |

### 18. Downhole Sensors (6 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#downhole.sensor.adjustment` | downhole.sensor.adjustment | time |  | downhole.sensor.adjustment |
| 2 | `corva#downhole.sensor.data` | downhole.sensor.data | time |  |  |
| 3 | `corva#downhole.sensor.data-1m` | downhole.sensor.data-1m | time |  |  |
| 4 | `corva#downhole.sensor.data-30m` | downhole.sensor.data-30m | time |  |  |
| 5 | `corva#downhole.sensor.data-6h` | downhole.sensor.data-6h | time |  |  |
| 6 | `corva#downhole.sensor.data.header` | downhole.sensor.data.header | time |  |  |

### 19. Predictive Drilling / ML (7 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#machine-learning.rop` | machine-learning.rop | time |  |  |
| 2 | `corva#predictive-drilling.aggregation` | predictive-drilling.aggregation | time |  |  |
| 3 | `corva#rotary-automation` | rotary-automation | time | Yes |  |
| 4 | `corva#rotary-automation.company-settings` | rotary-automation.company-settings | reference |  |  |
| 5 | `corva#rotary-automation.limits` | rotary-automation.limits | time |  |  |
| 6 | `corva#rotary-automation.limits-changelog` | rotary-automation.limits-changelog | time |  | Limit changelogs for the Predictive Drilling application |
| 7 | `corva#rotary-automation.settings.log` | rotary-automation.settings.log | time |  |  |

### 20. Alerts (11 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#alerts-plus.company-configs` | alerts-plus.company-configs | reference |  |  |
| 2 | `corva#alerts-plus.history` | alerts-plus.history | reference |  |  |
| 3 | `corva#custom_alerts_test_log` | custom_alerts_test_log | time |  |  |
| 4 | `corva#predictive-alerts.stuck-pipe` | predictive-alerts.stuck-pipe | time | Yes |  |
| 5 | `corva#predictive-alerts.stuck-pipe-config` | predictive-alerts.stuck-pipe-config | time |  |  |
| 6 | `corva#predictive-alerts.stuck-pipe-groups` | predictive-alerts.stuck-pipe-groups | reference |  |  |
| 7 | `corva#predictive-alerts.stuck-pipe-v1` | predictive-alerts.stuck-pipe-v1 | time | Yes | Collection for stuck pipe bench model 1 |
| 8 | `corva#predictive-alerts.stuck-pipe-v2` | predictive-alerts.stuck-pipe-v2 | time | Yes | Collection for stuck pipe bench model 2 |
| 9 | `corva#python-alerts` | python-alerts | reference |  |  |
| 10 | `corva#python-alerts-response` | python-alerts-response | time |  |  |
| 11 | `corva#python-alerts-results` | python-alerts-results | time |  | This collection stores the results of python alerts contexts that were triggered |

### 21. Well Design (5 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#well-design.composite-design.meta` | well-design.composite-design.meta | time |  | Store composite design configuration information per asset |
| 2 | `corva#well-design.optimization` | well-design.optimization | time |  |  |
| 3 | `corva#well-design.optimization.timelog` | well-design.optimization.timelog | time |  | Collection to store the composite and average well phase data |
| 4 | `corva#well-design.well-objective` | well-design.well-objective | time |  | Collection to store well objectives (aggregated metrics) |
| 5 | `corva#well-design.well-objective.meta` | well-design.well-objective.meta | time |  | Collection to store well objective metadata (info used to generate aggregated metrics) |

### 22. Well Design (design.*) (7 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#design.data.casing` | design.data.casing | time |  |  |
| 2 | `corva#design.data.drillstring` | design.data.drillstring | time |  |  |
| 3 | `corva#design.data.mud` | design.data.mud | time |  |  |
| 4 | `corva#design.data.operation-inputs` | design.data.operation-inputs | time |  |  |
| 5 | `corva#design.data.plan_survey` | design.data.plan_survey | time |  |  |
| 6 | `corva#design.torque-and-drag.hookload-trend` | design.torque-and-drag.hookload-trend | time |  |  |
| 7 | `corva#design.torque-and-drag.torque-trend` | design.torque-and-drag.torque-trend | time |  |  |

### 23. Metrics / KPIs (8 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#metrics` | metrics | time |  |  |
| 2 | `corva#metrics-improvements` | metrics-improvements | reference |  | Records of manual improvements into metrics KPI performance |
| 3 | `corva#metrics-interventions` | metrics-interventions | reference |  | Records of manual interventions into metrics KPI performance |
| 4 | `corva#metrics.definitions` | metrics.definitions | reference |  | Custom metrics definitions |
| 5 | `corva#metrics.edit` | metrics.edit | time |  |  |
| 6 | `corva#metrics.global` | metrics.global | reference |  |  |
| 7 | `corva#metrics.rop-1d` | metrics.rop-1d | time |  |  |
| 8 | `corva#metrics.rop-1h` | metrics.rop-1h | time |  |  |

### 24. Time Log (4 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#timelog.activity-codes` | timelog.activity-codes | time |  |  |
| 2 | `corva#timelog.custom.metrics` | timelog.custom.metrics | time |  |  |
| 3 | `corva#timelog.data` | timelog.data | time |  |  |
| 4 | `corva#timelog.data.summary` | timelog.data.summary | time |  | Collection to hold the summary of timelog data |

### 25. Production (Enverus) (26 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#production.casing` | production.casing | reference |  | Enverus casing data |
| 2 | `corva#production.clusters` | production.clusters | reference |  | Enverus data |
| 3 | `corva#production.completion.headers` | production.completion.headers | reference |  | Enverus Completion Headers Data Objects |
| 4 | `corva#production.cumulative` | production.cumulative | reference |  | Enverus data storage |
| 5 | `corva#production.cumulative.metadata` | production.cumulative.metadata | reference |  | asset_id grouping for production.cumulative |
| 6 | `corva#production.fleet.history` | production.fleet.history | reference |  | Enverus data |
| 7 | `corva#production.formations` | production.formations | reference |  | Enverus Formation Top Data Objects |
| 8 | `corva#production.frac.design` | production.frac.design | reference |  | Enverus data |
| 9 | `corva#production.headers` | production.headers | reference |  | Enverus Producing Entity Header data |
| 10 | `corva#production.injections` | production.injections | reference |  | Enverus details for a Injection Data |
| 11 | `corva#production.monthly` | production.monthly | reference |  | Enverus monthly dataset |
| 12 | `corva#production.oil.analysis` | production.oil.analysis | reference |  | Enverus data |
| 13 | `corva#production.permits` | production.permits | reference |  | Envrus list of Permit Data Objects |
| 14 | `corva#production.revenue` | production.revenue | reference |  | Enverus Data |
| 15 | `corva#production.rig.history` | production.rig.history | reference |  | Enverus list of Rigs through time Objects |
| 16 | `corva#production.shows` | production.shows | reference |  | Enverus list of Show Data Objects |
| 17 | `corva#production.spacing` | production.spacing | reference |  | Enverus list of Full Spacings Data Objects |
| 18 | `corva#production.stages` | production.stages | reference |  | Enverus data |
| 19 | `corva#production.summary` | production.summary | time |  |  |
| 20 | `corva#production.summary.welldatabase` | production.summary.welldatabase | time |  |  |
| 21 | `corva#production.tubing` | production.tubing | reference |  | Enverus list of Tubing Data Objects |
| 22 | `corva#production.units` | production.units | reference |  | Enverus Landtrac Units data |
| 23 | `corva#production.water.analysis` | production.water.analysis | reference |  | Enverus data |
| 24 | `corva#production.well.header` | production.well.header | reference |  | Enverus list of Well Headers Data Objects |
| 25 | `corva#production.wits` | production.wits | time |  | Wits data from external APIs |
| 26 | `corva#production.xref` | production.xref | reference |  | Enverus Producing Entity Xref data |

### 26. Sustainability / ESG (10 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#sustainability.metrics.comparison` | sustainability.metrics.comparison | time |  |  |
| 2 | `corva#sustainability.metrics.components` | sustainability.metrics.components | time |  |  |
| 3 | `corva#sustainability.metrics.mapping` | sustainability.metrics.mapping | time |  |  |
| 4 | `corva#sustainability.processed` | sustainability.processed | time |  |  |
| 5 | `corva#sustainability.real-time.data` | sustainability.real-time.data | time |  | This dataset includes real-time sustainability data. |
| 6 | `corva#sustainability.water_quality_lab_data` | sustainability.water_quality_lab_data | reference |  |  |
| 7 | `corva#sustainability.water_quality_real_time_data` | sustainability.water_quality_real_time_data | time |  | Real time Data from StreamX app that is pulling data from Azure SQL DB using ODBC connection and whitelisted IP |
| 8 | `corva#sustainability.water_quality_real_time_rates` | sustainability.water_quality_real_time_rates | time |  | stores hourly flow rate and chemical dosage kpis calculated from streamx_db.aris |
| 9 | `corva#sustainability.water_quality_real_time_summary_1h` | sustainability.water_quality_real_time_summary_1h | time |  | 1 hour data aggregations of sustainability.water_quality_real_time_data |
| 10 | `corva#sustainability.water_quality_real_time_summary_24h` | sustainability.water_quality_real_time_summary_24h | time |  | 24 hour data aggregations of sustainability.water_quality_real_time_data |

### 27. Wellness / Check-Up (16 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#wcu-coord-metadata` | wcu-coord-metadata | reference |  |  |
| 2 | `corva#wcu-csv-rerun-updates` | wcu-csv-rerun-updates | reference |  |  |
| 3 | `corva#wcu-custom-rule-settings` | wcu-custom-rule-settings | reference |  |  |
| 4 | `corva#wcu-eow-asset-metadata` | wcu-eow-asset-metadata | reference |  | Asset Notes and other metadata for WCU EOW view |
| 5 | `corva#wcu-eow-reports` | wcu-eow-reports | time |  |  |
| 6 | `corva#wcu-manual-alert-metadata` | wcu-manual-alert-metadata | reference |  | Collection holding information create by wellness helper task app. This information is read when wellness scheduled a... |
| 7 | `corva#wcu-rule-check-time` | wcu-rule-check-time | time |  |  |
| 8 | `corva#wcu-rule-notes` | wcu-rule-notes | reference |  |  |
| 9 | `corva#wcu_rule_mapping` | wcu_rule_mapping | reference |  |  |
| 10 | `corva#wellness_alerts` | wellness_alerts | time |  | Dataset for corva wellness application alerts |
| 11 | `corva#wellness_checks_results` | wellness_checks_results | time |  | Collection for assisting WCU+ with external lambdas |
| 12 | `corva#wellness_rule_settings` | wellness_rule_settings | reference |  | This collection contains the settings for all of the rules associated with WELLness app. |
| 13 | `corva#wellness_rule_settings_history` | wellness_rule_settings_history | reference |  | History of changes for wellness_rule_settings records |
| 14 | `corva#wellness_scores` | wellness_scores | time |  | Used for scoring metrics of the wellness application |
| 15 | `corva#wellness_scores_history` | wellness_scores_history | reference |  |  |
| 16 | `corva#wellness_tasks` | wellness_tasks | time |  | used with task helper to pass messages to the wellness app. |

### 28. Stream Quality (7 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#stream-quality-custom-settings` | stream-quality-custom-settings | reference |  |  |
| 2 | `corva#stream-quality-defaults` | stream-quality-defaults | reference |  |  |
| 3 | `corva#stream-quality-delays.time-series` | stream-quality-delays.time-series | timeseries |  | Stores delay values for rule 7 of Stream Quality app |
| 4 | `corva#stream-quality-results` | stream-quality-results | reference |  |  |
| 5 | `corva#stream-quality-scores` | stream-quality-scores | time |  | Latest Stream Quality score for the well |
| 6 | `corva#stream-quality-scores-history` | stream-quality-scores-history | time |  | Stream Quality score history for the well |
| 7 | `corva#stream-quality-settings-history` | stream-quality-settings-history | reference |  |  |

### 29. Handover / Mission Control (7 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#handover-asset-metadata` | handover-asset-metadata | time |  | Used to keep track of the assets in and out of the 'cue' created by the handover-automation application. The asset me... |
| 2 | `corva#handover-notes` | handover-notes | time |  | Notes and comments left by the analysts in the handover-automation application. There are four levels of notes, namel... |
| 3 | `corva#handover-records` | handover-records | time |  | The main dataset of the handover-automation application. Houses the tabular-level records for each asset (rig) of the... |
| 4 | `corva#handover-rig-metadata` | handover-rig-metadata | reference |  |  |
| 5 | `corva#handover-snapshot` | handover-snapshot | time |  | An hourly store of the state of the handover-automation application. Used for internal analytics and tracking purposes. |
| 6 | `corva#handover-teams` | handover-teams | reference |  | The team mapping used for operation-based dev center applications. |
| 7 | `corva#handover_automation_logs` | handover_automation_logs | time |  | Used to store random logging/debugging. |

### 30. Interventions (Workover) (38 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#interventions.activities` | interventions.activities | time |  |  |
| 2 | `corva#interventions.activity-groups` | interventions.activity-groups | time |  |  |
| 3 | `corva#interventions.circulation.volumetric` | interventions.circulation.volumetric | time |  |  |
| 4 | `corva#interventions.data.drillstring` | interventions.data.drillstring | time |  |  |
| 5 | `corva#interventions.data.mud` | interventions.data.mud | time |  |  |
| 6 | `corva#interventions.data.npt-events` | interventions.data.npt-events | reference |  |  |
| 7 | `corva#interventions.data.surface-equipment` | interventions.data.surface-equipment | time |  |  |
| 8 | `corva#interventions.drilling-efficiency.mse` | interventions.drilling-efficiency.mse | time |  |  |
| 9 | `corva#interventions.drilling-efficiency.mse-heatmap` | interventions.drilling-efficiency.mse-heatmap | time |  |  |
| 10 | `corva#interventions.drilling-efficiency.optimization` | interventions.drilling-efficiency.optimization | time |  |  |
| 11 | `corva#interventions.drilling-efficiency.rop-heatmap` | interventions.drilling-efficiency.rop-heatmap | time |  |  |
| 12 | `corva#interventions.hydraulics.cuttings-transport` | interventions.hydraulics.cuttings-transport | time |  |  |
| 13 | `corva#interventions.hydraulics.overview` | interventions.hydraulics.overview | time |  |  |
| 14 | `corva#interventions.hydraulics.pressure-loss` | interventions.hydraulics.pressure-loss | time |  |  |
| 15 | `corva#interventions.hydraulics.pressure-trend` | interventions.hydraulics.pressure-trend | time |  |  |
| 16 | `corva#interventions.hydraulics.surge-and-swab` | interventions.hydraulics.surge-and-swab | time |  |  |
| 17 | `corva#interventions.metrics` | interventions.metrics | time |  |  |
| 18 | `corva#interventions.next-well-info` | interventions.next-well-info | reference |  |  |
| 19 | `corva#interventions.operations` | interventions.operations | time |  |  |
| 20 | `corva#interventions.pdm.operating-condition` | interventions.pdm.operating-condition | time |  |  |
| 21 | `corva#interventions.pdm.overview` | interventions.pdm.overview | time |  |  |
| 22 | `corva#interventions.surface-equipment-templates` | interventions.surface-equipment-templates | reference |  |  |
| 23 | `corva#interventions.timelog-reference.data` | interventions.timelog-reference.data | reference |  |  |
| 24 | `corva#interventions.timelog.data` | interventions.timelog.data | reference |  |  |
| 25 | `corva#interventions.timelog.data.summary` | interventions.timelog.data.summary | time |  |  |
| 26 | `corva#interventions.torque-and-drag.axial-load` | interventions.torque-and-drag.axial-load | time |  |  |
| 27 | `corva#interventions.torque-and-drag.downhole-transfer` | interventions.torque-and-drag.downhole-transfer | time |  |  |
| 28 | `corva#interventions.torque-and-drag.friction-factor` | interventions.torque-and-drag.friction-factor | time |  |  |
| 29 | `corva#interventions.torque-and-drag.hookload-trend` | interventions.torque-and-drag.hookload-trend | time |  |  |
| 30 | `corva#interventions.torque-and-drag.hookload-trend.actual` | interventions.torque-and-drag.hookload-trend.actual | time |  |  |
| 31 | `corva#interventions.torque-and-drag.overview` | interventions.torque-and-drag.overview | time |  |  |
| 32 | `corva#interventions.torque-and-drag.predictions` | interventions.torque-and-drag.predictions | time |  |  |
| 33 | `corva#interventions.torque-and-drag.stress` | interventions.torque-and-drag.stress | time |  |  |
| 34 | `corva#interventions.torque-and-drag.torque` | interventions.torque-and-drag.torque | time |  |  |
| 35 | `corva#interventions.torque-and-drag.torque-trend` | interventions.torque-and-drag.torque-trend | time |  |  |
| 36 | `corva#interventions.torque-and-drag.torque-trend.actual` | interventions.torque-and-drag.torque-trend.actual | time |  |  |
| 37 | `corva#interventions.well-plan.data` | interventions.well-plan.data | reference |  |  |
| 38 | `corva#interventions.well_search_results` | interventions.well_search_results | reference |  |  |

### 31. Launchpad / Connectivity (9 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#launchpad_asset_depth_traces` | launchpad_asset_depth_traces | reference |  |  |
| 2 | `corva#launchpad_autoconnect_configs` | launchpad_autoconnect_configs | reference |  |  |
| 3 | `corva#launchpad_credentials_health_tracking` | launchpad_credentials_health_tracking | reference |  |  |
| 4 | `corva#launchpad_external_notifications` | launchpad_external_notifications | reference |  |  |
| 5 | `corva#launchpad_notifications` | launchpad_notifications | reference |  |  |
| 6 | `corva#launchpad_tasks` | launchpad_tasks | reference |  |  |
| 7 | `corva#launchpad_witsml_recommendations` | launchpad_witsml_recommendations | reference |  |  |
| 8 | `corva#launchpad_witsml_wellbores` | launchpad_witsml_wellbores | reference |  |  |
| 9 | `corva#launchpad_witsml_wellbores_cache` | launchpad_witsml_wellbores_cache | reference |  |  |

### 32. AskCorva / AI (3 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#askcorva.history` | askcorva.history | reference |  |  |
| 2 | `corva#askcorva.prompts` | askcorva.prompts | reference |  |  |
| 3 | `corva#askcorva.settings` | askcorva.settings | reference |  |  |

### 33. Bowtie / Insights (2 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#bowtie.insights.events` | bowtie.insights.events | reference |  | Rig data |
| 2 | `corva#bowtie.insights.files` | bowtie.insights.files | reference |  |  |

### 34. Frac Third-Party (7 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#frac.abra.offset-monitoring` | frac.abra.offset-monitoring | time |  |  |
| 2 | `corva#frac.nextier.dgb` | frac.nextier.dgb | time |  |  |
| 3 | `corva#frac.slb.valvecommander` | frac.slb.valvecommander | time |  | Stores historical operational data for SLB's Valve Commander app. |
| 4 | `corva#frac.tallyrestream.fracstream.data` | frac.tallyrestream.fracstream.data | time |  |  |
| 5 | `corva#frac.tallyrestream.fracstream.data.test` | frac.tallyrestream.fracstream.data.test | time |  |  |
| 6 | `corva#frac.tallyrestream.fracstream.fields` | frac.tallyrestream.fracstream.fields | reference |  |  |
| 7 | `corva#fracvision-recommendations-test` | fracvision-recommendations-test | time |  |  |

### 35. Nabors Integration (15 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#nabors_dailyservice_ext` | nabors_dailyservice_ext | reference |  |  |
| 2 | `corva#nabors_ei_logs` | nabors_ei_logs | reference |  |  |
| 3 | `corva#nabors_nav_active_well_config` | nabors_nav_active_well_config | reference |  |  |
| 4 | `corva#nabors_nav_calculation_option` | nabors_nav_calculation_option | reference |  |  |
| 5 | `corva#nabors_nav_drilldown_parameter` | nabors_nav_drilldown_parameter | time |  |  |
| 6 | `corva#nabors_nav_mo_settings` | nabors_nav_mo_settings | reference |  |  |
| 7 | `corva#nabors_nav_target_slide_rop` | nabors_nav_target_slide_rop | reference |  |  |
| 8 | `corva#nabors_operation_ext` | nabors_operation_ext | reference |  |  |
| 9 | `corva#nabors_report_ext` | nabors_report_ext | reference |  |  |
| 10 | `corva#nabors_smartplan_actuals` | nabors_smartplan_actuals | time |  |  |
| 11 | `corva#nabors_time_ext` | nabors_time_ext | reference |  |  |
| 12 | `corva#nabors_tour_ext` | nabors_tour_ext | reference |  |  |
| 13 | `corva#nabors_toursheetdata_ext` | nabors_toursheetdata_ext | reference |  |  |
| 14 | `corva#nabors_well_by_id` | nabors_well_by_id | reference |  |  |
| 15 | `corva#nabors_work_ext` | nabors_work_ext | reference |  |  |

### 36. WITS (Other Phases) (34 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#completion.wits` | completion.wits | time |  | Historical and streaming 1 second wits data after passing through data quality checks and true vertical depth functions. |
| 2 | `corva#completion.wits.raw` | completion.wits.raw | time |  | Historical and streaming 1 second wits data before passing through data quality checks and true vertical depth functi... |
| 3 | `corva#completion.wits.summary-10s` | completion.wits.summary-10s | time |  | Historical and streaming 1 second wits data summariezed for every 10 seconds after passing through data quality check... |
| 4 | `corva#completion.wits.summary-1m` | completion.wits.summary-1m | time |  | Historical and streaming 1 second wits data summariezed for every 1minute after passing through data quality checks a... |
| 5 | `corva#completion.wits.summary-30m` | completion.wits.summary-30m | time |  |  |
| 6 | `corva#drillout.wits` | drillout.wits | time |  |  |
| 7 | `corva#drillout.wits.metadata` | drillout.wits.metadata | time |  | Drillout wits metadata |
| 8 | `corva#drillout.wits.raw` | drillout.wits.raw | time |  |  |
| 9 | `corva#drillout.wits.summary-1m` | drillout.wits.summary-1m | time |  |  |
| 10 | `corva#drillout.wits.summary-1m.metadata` | drillout.wits.summary-1m.metadata | time |  |  |
| 11 | `corva#drillout.wits.summary-30m` | drillout.wits.summary-30m | time |  |  |
| 12 | `corva#drillout.wits.summary-30m.metadata` | drillout.wits.summary-30m.metadata | time |  |  |
| 13 | `corva#drillout.wits.summary-6h` | drillout.wits.summary-6h | time |  |  |
| 14 | `corva#drillout.wits.summary-6h.metadata` | drillout.wits.summary-6h.metadata | time |  |  |
| 15 | `corva#interventions.wits` | interventions.wits | time |  |  |
| 16 | `corva#interventions.wits.comments` | interventions.wits.comments | time |  |  |
| 17 | `corva#interventions.wits.metadata` | interventions.wits.metadata | time |  |  |
| 18 | `corva#interventions.wits.summary-1ft` | interventions.wits.summary-1ft | time |  |  |
| 19 | `corva#interventions.wits.summary-1ft.metadata` | interventions.wits.summary-1ft.metadata | time |  |  |
| 20 | `corva#interventions.wits.summary-1m` | interventions.wits.summary-1m | time |  |  |
| 21 | `corva#interventions.wits.summary-1m.metadata` | interventions.wits.summary-1m.metadata | time |  |  |
| 22 | `corva#interventions.wits.summary-30m` | interventions.wits.summary-30m | time |  |  |
| 23 | `corva#interventions.wits.summary-30m.metadata` | interventions.wits.summary-30m.metadata | time |  |  |
| 24 | `corva#interventions.wits.summary-6h` | interventions.wits.summary-6h | time |  |  |
| 25 | `corva#interventions.wits.summary-6h.metadata` | interventions.wits.summary-6h.metadata | time |  |  |
| 26 | `corva#pumpdown.wits` | pumpdown.wits | time | Yes | Historical and streaming 1 second wits data after passing through data quality checks and true vertical depth functions. |
| 27 | `corva#pumpdown.wits.summary-10s` | pumpdown.wits.summary-10s | time | Yes | Historical and streaming 1 second wits data summariezed for every 10 seconds after passing through data quality check... |
| 28 | `corva#pumpdown.wits.summary-1m` | pumpdown.wits.summary-1m | time |  |  |
| 29 | `corva#pumpdown.wits.summary-30s` | pumpdown.wits.summary-30s | time |  |  |
| 30 | `corva#wireline.wits` | wireline.wits | time | Yes | Historical and streaming 1 second wits data after passing through data quality checks and true vertical depth functions. |
| 31 | `corva#wireline.wits.raw` | wireline.wits.raw | time |  |  |
| 32 | `corva#wireline.wits.summary-10s` | wireline.wits.summary-10s | time | Yes |  |
| 33 | `corva#wireline.wits.summary-1m` | wireline.wits.summary-1m | time |  |  |
| 34 | `corva#wireline.wits.summary-30s` | wireline.wits.summary-30s | time |  |  |

### 37. Other (107 datasets)

| # | Dataset (`provider#name`) | Friendly Name | Type | Plottable | Description |
|---|---|---|---|---|---|
| 1 | `corva#adi_mapper` | adi_mapper | reference |  | This collection is used to configure how the BE Advacned Data Integration (ADI) app runs. |
| 2 | `corva#ainomaly` | ainomaly | time |  |  |
| 3 | `corva#analytics.krevs` | analytics.krevs | time | Yes |  |
| 4 | `corva#asset.status-10m` | asset.status-10m | time |  |  |
| 5 | `corva#asset_archive_manifest` | asset_archive_manifest | reference |  |  |
| 6 | `corva#asset_pad_mapping` | asset_pad_mapping | reference |  | used as hash for asset -> pad_id, fleet_id, etc. |
| 7 | `corva#assets` | assets | time |  | Metadata associated with a well in Corva |
| 8 | `corva#auto-time-log.data` | auto-time-log.data | time | Yes | A collection for storing asset activity data derived from the WITS collection. |
| 9 | `corva#baker_memory` | baker_memory | time | Yes | baker_memory |
| 10 | `corva#bha-inventory.company-components` | bha-inventory.company-components | reference |  |  |
| 11 | `corva#checkup` | checkup | time |  |  |
| 12 | `corva#chronos-notifications` | chronos-notifications | time |  |  |
| 13 | `corva#chronos-settings` | chronos-settings | time |  |  |
| 14 | `corva#composite-curves` | composite-curves | time |  |  |
| 15 | `corva#composite-roadmaps` | composite-roadmaps | time |  | Storing composite roadmaps from Predictive Drilling |
| 16 | `corva#config-response` | config-response | time |  |  |
| 17 | `corva#corva.column-mapper.settings` | corva.column-mapper.settings | time |  |  |
| 18 | `corva#cost_commander_configuration` | cost_commander_configuration | time |  | place to store config data for cost commander app |
| 19 | `corva#darkfibr` | darkfibr | reference |  | Store for darkfibr data |
| 20 | `corva#dashcheck` | dashcheck | reference |  | For storing corva dashboard performance |
| 21 | `corva#dc-cp-records` | dc-cp-records | time |  | Continuous pumping records |
| 22 | `corva#dd-mission-control-notes` | dd-mission-control-notes | reference |  |  |
| 23 | `corva#diesel.displacement.table.summary` | diesel.displacement.table.summary | time |  |  |
| 24 | `corva#diff_derating` | diff_derating | reference |  | Diff Derating changes from Predictive Drilling |
| 25 | `corva#diff_derating.settings` | diff_derating.settings | reference |  | Diff Derating Settings |
| 26 | `corva#digital-mud-engineer` | digital-mud-engineer | time |  |  |
| 27 | `corva#dls-traces-custom` | dls-traces-custom | time |  | DLS Traces Calculation |
| 28 | `corva#dmytro_test_dataset` | dmytro_test_dataset | time |  |  |
| 29 | `corva#drill2frac.depth` | drill2frac.depth | depth |  | drill2frac depth data |
| 30 | `corva#drill2frac.meta` | drill2frac.meta | time |  | drill2frac metadata |
| 31 | `corva#dysfunction.settings` | dysfunction.settings | reference |  | Dysfunction Detection Setting Overrides |
| 32 | `corva#dysfunctions` | dysfunctions | time |  | Corva Detected Dysfunctions |
| 33 | `corva#dysfunctions.auto-driller` | dysfunctions.auto-driller | time | Yes |  |
| 34 | `corva#ecm_output` | ecm_output | reference |  |  |
| 35 | `corva#fleet.metrics` | fleet.metrics | reference |  |  |
| 36 | `corva#fusion-test` | fusion-test | time |  |  |
| 37 | `corva#fv_auto_manual_stages` | fv_auto_manual_stages | reference |  |  |
| 38 | `corva#geo-prog` | geo-prog | reference |  |  |
| 39 | `corva#grids.data` | grids.data | reference |  |  |
| 40 | `corva#grids.metadata` | grids.metadata | reference |  |  |
| 41 | `corva#historical-import-app.metadata` | historical-import-app.metadata | time |  |  |
| 42 | `corva#historical-import.errors` | historical-import.errors | time |  |  |
| 43 | `corva#hlpwob` | hlpwob | time |  |  |
| 44 | `corva#hookload-plus-wob-so` | hookload-plus-wob-so | time |  |  |
| 45 | `corva#ids_drillpipes` | ids_drillpipes | reference |  |  |
| 46 | `corva#insights-reports` | insights-reports | reference |  |  |
| 47 | `corva#integrations.ext-int-tracking` | integrations.ext-int-tracking | reference |  | dataset to track external integration pipeline runs |
| 48 | `corva#intervention.openwells.active-wells` | intervention.openwells.active-wells | reference |  |  |
| 49 | `corva#kick-detection` | kick-detection | time |  |  |
| 50 | `corva#mcd.predictive_drilling_check_results` | mcd.predictive_drilling_check_results | reference |  |  |
| 51 | `corva#mgb-fuel` | mgb-fuel | time |  | MGB Fuel & Emission Data |
| 52 | `corva#microdls_be` | microdls_be | time |  |  |
| 53 | `corva#milling-console-real-time` | milling-console-real-time | time |  |  |
| 54 | `corva#milling-console-sections` | milling-console-sections | time |  | Once a casing shoe has been milled out, a retrospective record is created showing an aggregation of the data received... |
| 55 | `corva#ml-data-export-queue` | ml-data-export-queue | reference |  |  |
| 56 | `corva#mock-idas-drm-payload` | mock-idas-drm-payload | reference |  | Stores mock payload responses from the Exxon API |
| 57 | `corva#motor-yield-comparison` | motor-yield-comparison | reference |  |  |
| 58 | `corva#mse.offsets` | mse.offsets | time |  |  |
| 59 | `corva#mud.inventory.codes` | mud.inventory.codes | reference |  |  |
| 60 | `corva#mud.inventory.default_codes` | mud.inventory.default_codes | reference |  |  |
| 61 | `corva#mycelx.realtime` | mycelx.realtime | time |  |  |
| 62 | `corva#offset-drilling-troubles` | offset-drilling-troubles | reference |  |  |
| 63 | `corva#ops_documents` | ops_documents | time |  |  |
| 64 | `corva#pad.metrics` | pad.metrics | reference |  |  |
| 65 | `corva#pad_schedule` | pad_schedule | time |  |  |
| 66 | `corva#pae-custom-traces` | pae-custom-traces | time | Yes |  |
| 67 | `corva#peloton-integration` | peloton-integration | time |  | Used to store the data capture and any relevant application state from the peloton application |
| 68 | `corva#peloton-tokens` | peloton-tokens | reference |  | used to store refresh token for authenticating peloton integration. |
| 69 | `corva#planilla-test-dataset` | planilla-test-dataset | time |  |  |
| 70 | `corva#procedural-compliance` | procedural-compliance | time |  |  |
| 71 | `corva#procedural-compliance-comstock` | procedural-compliance-comstock | time |  |  |
| 72 | `corva#restricted-operations` | restricted-operations | time |  | Restricted Operations records |
| 73 | `corva#rigcast` | rigcast | time |  | Dataset for storing real time video streaming |
| 74 | `corva#rss-analytics.downlinks` | rss-analytics.downlinks | time |  | Collection to hold downlinks detected when running RSS. |
| 75 | `corva#rss-steer-mode-changes.depth` | rss-steer-mode-changes.depth | time |  | Stores changes about RSS steer modes |
| 76 | `corva#run_plan_output` | run_plan_output | time |  | Used as an output store for the Run Plan Generator task app |
| 77 | `corva#simops.configurations` | simops.configurations | time |  |  |
| 78 | `corva#smart-analytics` | smart-analytics | time |  | smart plan analytics |
| 79 | `corva#smart-stage-notifications` | smart-stage-notifications | reference |  |  |
| 80 | `corva#smart-stream-notifications` | smart-stream-notifications | time |  | Notifications on channel anomalies, adds, drops, etc...detected via the Smart Stream application. |
| 81 | `corva#stand_length` | stand_length | time |  |  |
| 82 | `corva#streambox-fleet-mapping` | streambox-fleet-mapping | reference |  | Used to store relationships between streambox object and fleet object |
| 83 | `corva#streamboxes` | streamboxes | reference |  | Used to track available streamboxes for the activity tracker application |
| 84 | `corva#survey_manager.settings` | survey_manager.settings | time |  | Used to store settings and configurations for the survey management system |
| 85 | `corva#tasks.survey-minimum-curvature` | tasks.survey-minimum-curvature | time |  |  |
| 86 | `corva#tasks.survey-parser` | tasks.survey-parser | time |  |  |
| 87 | `corva#temporary-state` | temporary-state | time |  |  |
| 88 | `corva#test.fleet.metrics.temp` | test.fleet.metrics.temp | reference |  |  |
| 89 | `corva#test_dataset` | test_dataset | time |  |  |
| 90 | `corva#testseven` | testseven | time |  |  |
| 91 | `corva#time-cost-variance.log` | time-cost-variance.log | time |  |  |
| 92 | `corva#traces.offsets` | traces.offsets | time |  |  |
| 93 | `corva#trend-analysis` | trend-analysis | time |  |  |
| 94 | `corva#trip-sheet` | trip-sheet | time |  |  |
| 95 | `corva#ttdp.configs` | ttdp.configs | time |  |  |
| 96 | `corva#vibration_monitoring` | vibration_monitoring | time |  |  |
| 97 | `corva#warning_indicator_settings` | warning_indicator_settings | time |  | Store app settings |
| 98 | `corva#washout_detection_history` | washout_detection_history | time |  |  |
| 99 | `corva#wdc.apps.settings` | wdc.apps.settings | time |  |  |
| 100 | `corva#weather.time-series` | weather.time-series | timeseries |  | Wells weather data |
| 101 | `corva#well-intervention` | well-intervention | time |  |  |
| 102 | `corva#well_cache` | well_cache | time |  |  |
| 103 | `corva#well_check_up_wireline` | well_check_up_wireline | time |  | Used to store wireline based data quality alerts from the well checkup application |
| 104 | `corva#well_checkup_wireline` | well_checkup_wireline | time |  | Well Check Up rule alerts for wireline |
| 105 | `corva#ypf-alert-history` | ypf-alert-history | reference |  |  |
| 106 | `corva#ypf-pressure-channels-test` | ypf-pressure-channels-test | time |  |  |
| 107 | `corva#ypf_pressure_channels_test` | ypf_pressure_channels_test | time |  |  |

---

## Datasets with Defined Schemas

The following datasets have schema definitions, making them the most useful for app development:

**102 datasets** have schema definitions.

| Dataset | Type | Category | Schema Fields (top-level) |
|---|---|---|---|
| `corva#activities.summary-2tours` | time | Activities / Operations | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#activities.summary-3m` | time | Activities / Operations | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#activities.summary-continuous` | time | Activities / Operations | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#activity-groups` | time | Activities / Operations | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#anti-collision.metadata-edm` | reference | Anti-Collision | `_id`, `data`, `version`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#anti-collision.metadata-well` | reference | Anti-Collision | `_id`, `data`, `version`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#askcorva.settings` | reference | AskCorva / AI | `kpi_name`, `pipeline`, `company_id`, `kpi_segment` |
| `corva#assets` | time | Other | `_id`, `rig`, `name`, `type`, `basin`, `stats`, `county`, `status` ... (+16 more) |
| `corva#circulation.lag-depth` | time | Circulation | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#circulation.volumetric` | time | Circulation | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#completion.ccl-annotations` | time | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+1 more) |
| `corva#completion.ccl-anomalies` | reference | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+1 more) |
| `corva#completion.ccl-settings` | time | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#completion.ccl-summary` | reference | Completions / Frac | `_id`, `data`, `app_key`, `version`, `asset_id`, `provider`, `collection`, `company_id` ... (+1 more) |
| `corva#completion.custom_metrics` | time | Completions / Frac | `hhp`, `HVFRS`, `HVRFL`, `hhp_zone`, `fluid_system`, `pumping_hours`, `average_slurry_rate`, `stage_end_timestamp` ... (+3 more) |
| `corva#completion.data.files` | time | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#completion.data.job-settings` | time | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#completion.data.time-log` | time | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#completion.offset.abra` | time | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `company_id`, `stage_number` |
| `corva#completion.predictions` | time | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+3 more) |
| `corva#completion.stage-times` | time | Completions / Frac | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+1 more) |
| `corva#completion.wits` | time | WITS (Other Phases) | `default_units` |
| `corva#completion.wits.raw` | time | WITS (Other Phases) | `_id`, `app`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+2 more) |
| `corva#completion.wits.summary-10s` | time | WITS (Other Phases) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+1 more) |
| `corva#completion.wits.summary-1m` | time | WITS (Other Phases) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+1 more) |
| `corva#config-response` | time | Other | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.actual_survey` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.afe` | time | Well Data (data.*) | `_id`, `data`, `_pre_id`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+1 more) |
| `corva#data.casing` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.crews` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.diaries` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.drillstring` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.files` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.formations` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.lessons-learned` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.mud` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.npt-events` | time | Well Data (data.*) | `_id`, `data`, `_pre_id`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+1 more) |
| `corva#data.operation-summaries` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.plan_survey` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.surface-equipment` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#data.well-sections` | time | Well Data (data.*) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#directional.accuracy` | time | Directional | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#directional.projection_to_bit` | time | Directional | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#directional.rotational-tendency` | time | Directional | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#directional.surveys` | time | Directional | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#directional.tortuosity` | time | Directional | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#directional.trend` | time | Directional | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drilling-dysfunction` | time | Drilling | `_id`, `data`, `type`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+1 more) |
| `corva#drilling-efficiency.mse` | time | Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drilling-efficiency.mse-heatmap` | time | Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drilling-efficiency.optimization` | time | Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drilling-efficiency.predictions` | time | Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drilling-efficiency.rop-heatmap` | time | Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drilling.mud-ops` | time | Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drillout.data.drillstring` | time | Drillout | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drillout.data.mud` | time | Drillout | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drillout.data.surface-equipment` | time | Drillout | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drillout.torque-and-drag.axial-load` | time | Drillout | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drillout.torque-and-drag.hookload-trend` | time | Drillout | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drillout.torque-and-drag.stress` | time | Drillout | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drillout.torque-and-drag.torque-trend` | time | Drillout | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#drillout.wits.summary-6h` | time | WITS (Other Phases) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#formation-evaluation.metadata` | time | Formation Evaluation | `_id`, `app`, `data`, `file`, `version`, `asset_id`, `provider`, `timestamp` ... (+3 more) |
| `corva#hydraulics.cuttings-transport` | time | Hydraulics | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#hydraulics.overview` | time | Hydraulics | `_id`, `app`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+1 more) |
| `corva#hydraulics.pressure-loss` | time | Hydraulics | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#hydraulics.pressure-trend` | time | Hydraulics | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#hydraulics.surge-and-swab` | time | Hydraulics | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#kick-detection` | time | Other | `_id`, `data`, `type`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+1 more) |
| `corva#launchpad_witsml_recommendations` | reference | Launchpad / Connectivity | `_id`, `data`, `app_key`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+1 more) |
| `corva#machine-learning.rop` | time | Predictive Drilling / ML | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#metrics` | time | Metrics / KPIs | `_id`, `data`, `asset_id`, `metadata`, `timestamp`, `collection`, `company_id` |
| `corva#milling-console-real-time` | time | Other | `data`, `asset_id`, `timestamp`, `company_id` |
| `corva#operations` | time | Activities / Operations | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#pdm.operating-condition` | time | PDM / Motor | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#pdm.overview` | time | PDM / Motor | `_id`, `app`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+1 more) |
| `corva#pdm.stall-detection` | time | PDM / Motor | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#procedural-compliance` | time | Other | `_id`, `data`, `version`, `asset_id`, `provider`, `procedure`, `timestamp`, `collection` ... (+1 more) |
| `corva#production.wits` | time | Production (Enverus) | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#pumpdown.wits` | time | WITS (Other Phases) | `_id`, `data`, `app_key`, `version`, `asset_id`, `metadata`, `provider`, `timestamp` ... (+3 more) |
| `corva#torque-and-drag.axial-load` | time | Torque & Drag | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#torque-and-drag.downhole-transfer` | time | Torque & Drag | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#torque-and-drag.friction-factor` | time | Torque & Drag | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#torque-and-drag.hookload-trend` | time | Torque & Drag | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#torque-and-drag.overview` | time | Torque & Drag | `_id`, `app`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+1 more) |
| `corva#torque-and-drag.stress` | time | Torque & Drag | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#torque-and-drag.torque` | time | Torque & Drag | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#torque-and-drag.torque-trend` | time | Torque & Drag | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#traces.offsets` | time | Other | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#trend-analysis` | time | Other | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#trip-sheet` | time | Other | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+1 more) |
| `corva#well_cache` | time | Other | `_id`, `rig`, `alert`, `asset`, `company`, `program`, `asset_id`, `location` ... (+21 more) |
| `corva#wellness_rule_settings_history` | reference | Wellness / Check-Up | `_id`, `data`, `version`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#wireline.activity.summary-stage` | time | Wireline | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+1 more) |
| `corva#wireline.stage-times` | time | Wireline | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` ... (+1 more) |
| `corva#wireline.wits` | time | WITS (Other Phases) | `_id`, `app`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+2 more) |
| `corva#wireline.wits.summary-10s` | time | WITS (Other Phases) | `_id`, `app`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection` ... (+2 more) |
| `corva#wits` | time | WITS / Real-Time Drilling | `default_units` |
| `corva#wits.summary-1ft` | time | WITS / Real-Time Drilling | `_id`, `app`, `data`, `version`, `asset_id`, `metadata`, `provider`, `timestamp` ... (+2 more) |
| `corva#wits.summary-1m` | time | WITS / Real-Time Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#wits.summary-30m` | time | WITS / Real-Time Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |
| `corva#wits.summary-6h` | time | WITS / Real-Time Drilling | `_id`, `data`, `version`, `asset_id`, `provider`, `timestamp`, `collection`, `company_id` |

---

## API Access Patterns

### Data API (Recommended for Apps)

```
GET /api/v1/data/{provider}/{dataset}/
```

**Common query parameters:**

| Parameter | Description | Example |
|---|---|---|
| `query` | MongoDB-style query (JSON string) | `{"asset_id": 12345}` |
| `sort` | Sort order (JSON string) | `{"timestamp": -1}` |
| `limit` | Max records to return | `500` |
| `skip` | Records to skip (pagination) | `0` |
| `fields` | Comma-separated field list | `timestamp,data.hole_depth` |

### Example: Pull WITS data

```python
# Python SDK (inside a Corva app)
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
