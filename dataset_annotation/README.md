# Corva Dataset Documentation

This repository contains structured documentation for all Corva platform datasets. The documentation is designed to improve dataset discoverability for frontend engineers, AI agents, and anyone working with Corva's oil & gas data APIs.

## Purpose

Corva is an oil & gas analytics SaaS platform that exposes data via APIs. This documentation provides:

- **Structured metadata** for each dataset
- **Field-by-field descriptions** with data types
- **Use case guidance** for building applications
- **Sample records** where available
- **Keywords** for searchability

## Folder Structure

```
dataset_annotation/
├── README.md                    # This file
├── datasets.md                  # Source data (sample records, API info)
├── wits.md                      # Reference template (drilling)
├── directional.accuracy.md      # Reference template (drilling)
├── drilling_datasets/           # 61 drilling dataset docs
│   ├── wits.md
│   ├── activities.md
│   ├── operations.md
│   └── ...
└── completions_datasets/        # 26 completion dataset docs
    ├── completion_wits.md
    ├── completion_data_stages.md
    └── ...
```

## Documentation Format

Each dataset file follows a consistent structure:

1. **Title & Overview** - What the dataset contains
2. **When to use this dataset** - Selection guidance
3. **Example queries** - Alerting, visualization, and Q&A use cases
4. **Frequency** - How often data is recorded
5. **Primary keys** - Fields for filtering and querying
6. **Available fields** - Complete field list with types and descriptions
7. **Collection schema** - JSON schema representation
8. **Sample record** - Example data (when available)
9. **Keywords** - Search terms for discoverability

---

## Drilling Datasets (61 files)

Located in `drilling_datasets/`

### Real-Time Data
| File | Dataset | Description |
|------|---------|-------------|
| `wits.md` | `corva#wits` | Real-time drilling sensor data (WITS) |
| `wits_summary_1m.md` | `corva#wits.summary-1m` | 1-minute aggregated WITS |
| `wits_summary_30m.md` | `corva#wits.summary-30m` | 30-minute aggregated WITS |
| `wits_summary_1ft.md` | `corva#wits.summary-1ft` | 1-foot depth-based WITS |

### Activity & Operations
| File | Dataset | Description |
|------|---------|-------------|
| `activities.md` | `corva#activities` | Automated rig activity detection |
| `operations.md` | `corva#operations` | High-level drilling operations |
| `metrics.md` | `corva#metrics` | Calculated drilling KPIs |

### Directional Drilling (9 files)
| File | Dataset | Description |
|------|---------|-------------|
| `directional_surveys.md` | `corva#directional.surveys` | Enriched survey data |
| `directional_accuracy.md` | `corva#directional.accuracy` | Survey vs plan comparison |
| `data_actual_survey.md` | `corva#data.actual-survey` | Raw MWD/LWD surveys |
| `data_plan_survey.md` | `corva#data.plan-survey` | Planned trajectory |
| `directional_projection.md` | `corva#directional.projection` | Projected survey stations |
| `directional_slide_sheet.md` | `corva#directional.slide-sheet` | Slide tracking data |
| `directional_trend.md` | `corva#directional.trend` | Directional trend analysis |
| `directional_tortuosity.md` | `corva#directional.tortuosity` | Wellbore tortuosity |
| `directional_guidance.md` | `corva#directional.guidance` | Drilling guidance recommendations |

### Well Data (15 files)
| File | Dataset | Description |
|------|---------|-------------|
| `data_drillstring.md` | `corva#data.drillstring` | BHA and drillstring components |
| `data_casing.md` | `corva#data.casing` | Casing and liner data |
| `data_formations.md` | `corva#data.formations` | Geological formations |
| `data_mud.md` | `corva#data.mud` | Drilling fluid properties |
| `data_well_sections.md` | `corva#data.well-sections` | Well section definitions |
| `data_npt_events.md` | `corva#data.npt-events` | Non-productive time events |
| `data_afe.md` | `corva#data.afe` | Authorization for Expenditure |
| `data_costs.md` | `corva#data.costs` | Daily cost tracking |
| `data_crews.md` | `corva#data.crews` | Crew and shift information |
| `data_files.md` | `corva#data.files` | Document attachments |
| `data_lessons_learned.md` | `corva#data.lessons-learned` | Lessons learned records |
| `data_offset_wells.md` | `corva#data.offset-wells` | Offset well configurations |
| `data_surface_equipment.md` | `corva#data.surface-equipment` | Surface equipment config |
| `data_operation_summaries.md` | `corva#data.operation-summaries` | Daily operation reports |
| `data_pressure_gradient.md` | `corva#data.pressure-gradient` | Pressure gradient profiles |

### Depth-Based Analysis (2 files)
| File | Dataset | Description |
|------|---------|-------------|
| `drilling_wits_depth.md` | `corva#drilling.wits-depth` | Depth-summarized WITS |
| `drilling_wits_depth_summary_1ft.md` | `corva#drilling.wits-depth.summary-1ft` | 1-foot depth summary |

### Drilling Efficiency (4 files)
| File | Dataset | Description |
|------|---------|-------------|
| `drilling_efficiency_mse.md` | `corva#drilling.efficiency.mse` | Mechanical Specific Energy |
| `drilling_efficiency_optimization.md` | `corva#drilling.efficiency.optimization` | Drilling optimization data |
| `drilling_efficiency_mse_heatmap.md` | `corva#drilling.efficiency.mse-heatmap` | MSE heatmap data |
| `drilling_efficiency_rop_heatmap.md` | `corva#drilling.efficiency.rop-heatmap` | ROP heatmap data |

### Time Logging (2 files)
| File | Dataset | Description |
|------|---------|-------------|
| `drilling_timelog_data.md` | `corva#drilling.timelog-data` | Drilling timelog entries |
| `timelog_data.md` | `corva#timelog-data` | General timelog data |

### Hydraulics & Circulation (7 files)
| File | Dataset | Description |
|------|---------|-------------|
| `hydraulics_pressure_loss.md` | `corva#hydraulics.pressure-loss` | Pressure loss calculations |
| `hydraulics_overview.md` | `corva#hydraulics.overview` | Hydraulics summary |
| `hydraulics_surge_and_swab.md` | `corva#hydraulics.surge-and-swab` | Surge/swab pressures |
| `hydraulics_cuttings_transport.md` | `corva#hydraulics.cuttings-transport` | Hole cleaning analysis |
| `hydraulics_pressure_trend.md` | `corva#hydraulics.pressure-trend` | Pressure trend analysis |
| `circulation_volumetric.md` | `corva#circulation.volumetric` | Volumetric circulation data |
| `circulation_lag_depth.md` | `corva#circulation.lag-depth` | Lag depth calculations |

### Torque & Drag (8 files)
| File | Dataset | Description |
|------|---------|-------------|
| `torque_and_drag_overview.md` | `corva#torque-and-drag.overview` | T&D calculation summary |
| `torque_and_drag_hookload_trend.md` | `corva#torque-and-drag.hookload-trend` | Hookload trend analysis |
| `torque_and_drag_friction_factor.md` | `corva#torque-and-drag.friction-factor` | Friction factor calculations |
| `torque_and_drag_axial_load.md` | `corva#torque-and-drag.axial-load` | Axial load calculations |
| `torque_and_drag_torque.md` | `corva#torque-and-drag.torque` | Torque calculations |
| `torque_and_drag_torque_trend.md` | `corva#torque-and-drag.torque-trend` | Torque trend analysis |
| `torque_and_drag_stress.md` | `corva#torque-and-drag.stress` | Von Mises stress calculations |
| `torque_and_drag_predictions.md` | `corva#torque-and-drag.predictions` | T&D predictions |

### PDM (Positive Displacement Motor) (3 files)
| File | Dataset | Description |
|------|---------|-------------|
| `pdm_overview.md` | `corva#pdm.overview` | PDM performance overview |
| `pdm_operating_condition.md` | `corva#pdm.operating-condition` | PDM operating conditions |
| `pdm_stall_detection.md` | `corva#pdm.stall-detection` | PDM stall detection |

### Safety & Monitoring (4 files)
| File | Dataset | Description |
|------|---------|-------------|
| `dysfunctions.md` | `corva#dysfunctions` | Drilling dysfunction detection |
| `kick_detection.md` | `corva#kick-detection` | Kick detection monitoring |
| `anti_collision_clearance.md` | `corva#anti-collision.clearance` | Anti-collision clearance |
| `anti_collision_alert.md` | `corva#anti-collision.alert` | Anti-collision alerts |

---

## Completions Datasets (26 files)

Located in `completions_datasets/`

### Real-Time Completion Data (4 files)
| File | Dataset | Description |
|------|---------|-------------|
| `completion_wits.md` | `corva#completion.wits` | Real-time frac WITS data |
| `completion_wits_raw.md` | `corva#completion.wits.raw` | Raw unprocessed frac WITS |
| `completion_wits_summary_10s.md` | `corva#completion.wits.summary-10s` | 10-second aggregated WITS |
| `completion_wits_summary_1m.md` | `corva#completion.wits.summary-1m` | 1-minute aggregated WITS |

### Stage Data (5 files)
| File | Dataset | Description |
|------|---------|-------------|
| `completion_data_stages.md` | `corva#completion.data.stages` | Stage configuration/design |
| `completion_data_actual_stages.md` | `corva#completion.data.actual-stages` | Actual stage execution results |
| `completion_predictions.md` | `corva#completion.predictions` | Frac predictions and analytics |
| `completion_stage_times.md` | `corva#completion.stage-times` | Stage timing and duration |
| `completion_activity_summary_stage.md` | `corva#completion.activity.summary-stage` | Stage activity breakdown |

### Tracking & Monitoring (5 files)
| File | Dataset | Description |
|------|---------|-------------|
| `completion_tracking.md` | `corva#completion.tracking` | Operation progress tracking |
| `completion_pumps.md` | `corva#completion.pumps` | Pump fleet configuration |
| `completion_metrics.md` | `corva#completion.metrics` | Completion KPIs |
| `completion_valve.md` | `corva#completion.valve` | Valve status (zipper frac) |
| `completion_offset.md` | `corva#completion.offset` | Offset well pressure monitoring |

### Completion Data (4 files)
| File | Dataset | Description |
|------|---------|-------------|
| `completion_data_time_log.md` | `corva#completion.data.time-log` | Completion timelog entries |
| `completion_data_files.md` | `corva#completion.data.files` | Document attachments |
| `completion_data_npt_events.md` | `corva#completion.data.npt-events` | Non-productive time events |
| `completion_data_costs.md` | `corva#completion.data.costs` | Completion cost tracking |

### Pumpdown Operations (4 files)
| File | Dataset | Description |
|------|---------|-------------|
| `pumpdown_wits.md` | `corva#pumpdown.wits` | Real-time pumpdown data |
| `pumpdown_wits_summary_1m.md` | `corva#pumpdown.wits.summary-1m` | 1-minute aggregated pumpdown |
| `pumpdown_predictions.md` | `corva#pumpdown.predictions` | Plug tracking predictions |
| `pumpdown_activity_summary_stage.md` | `corva#pumpdown.activity.summary-stage` | Pumpdown activity breakdown |

### Wireline Operations (4 files)
| File | Dataset | Description |
|------|---------|-------------|
| `wireline_wits.md` | `corva#wireline.wits` | Real-time wireline data |
| `wireline_wits_summary_1m.md` | `corva#wireline.wits.summary-1m` | 1-minute aggregated wireline |
| `wireline_stage_times.md` | `corva#wireline.stage-times` | Wireline timing data |
| `wireline_activity_summary_stage.md` | `corva#wireline.activity.summary-stage` | Wireline activity breakdown |

---