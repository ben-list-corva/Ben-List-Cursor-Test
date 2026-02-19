# BHA Selection Process

Complete workflow for selecting the optimal BHA (bit + motor combination) for a target well section, driven by observed performance data across offset wells.

**Last updated**: Feb 16, 2026

---

## Overview

The goal is to select the BHA that gives the lowest **Time to TD** for a target well section. We do this by:

1. Finding comparable offset wells in the same basin/formation/area
2. Pulling all BHA runs from those offsets
3. Parsing bit and motor models to extract key specifications
4. Grouping runs into "Equivalent BHA" categories (same blade count + cutter size + motor lobe config + RPG band)
5. Pulling per-foot drilling data and classifying each foot as rotary or slide
6. Building ROP type curves (P10/P50/P90) for each equivalent BHA group
7. Calculating expected Time to TD for each group and ranking them

The recommended BHA is the equivalent BHA group with the lowest expected Time to TD and sufficient statistical support (runs).

Two BHAs are "equivalent" if they share the same bit characteristics (blade count + cutter size) and motor characteristics (lobe configuration + RPG band). Manufacturer and model suffix are intentionally excluded -- different vendors make functionally equivalent equipment.

## Step 1: Select Target Well and Find Offsets

**Script**: `find_offsets_all_operators.py`

- Input: Target asset ID
- Filters: Basin, target formation (fuzzy match), radius (default 15 mi), min hole depth (1000 ft)
- Output: `offset_wells_*.csv` with all matching wells across all operators

## Step 2: Pull BHA Data for Offset Wells

**Scripts**: `pull_lateral_bhas.py` (lateral section) or `pull_bhas_by_size.py` (by bit diameter)

- Input: Offset wells CSV
- Process: Fetch `corva#data.drillstring` for each well, extract bit and motor component details
- Also fetches `corva#data.well-sections` to find the lateral start depth
- Detects **RSS** and **Agitator** components in each BHA (see "Additional BHA Detection" below)
- Output: `lateral_bhas_*.csv` or `bhas_*in_*.csv`

Each output row includes: well info, BHA number, bit model, motor model, RPG, start/end depth, drilled interval, and flags for `is_rss`, `has_agitator`, and `lateral_start_depth`.

## Step 3: Parse Bit and Motor Models

**Script**: `parse_bit_motors.py`

### Bit Classification

Extract two key parameters from the bit model string:

1. **Blade count** (typically 3-8 blades)
2. **Cutter size** (in mm: 8, 11, 13, 16, 19, 22)

**Important reclassification**: All 15mm cutter sizes are grouped as **16mm**. Rationale: 5/8" = 15.875mm, which is closer to 16mm than 15mm. Both the fractional-inch convention (5/8") and the metric convention converge on the same physical cutter, so we unify them under 16mm for consistent grouping.

Two encoding conventions exist across manufacturers:

| Convention | Manufacturers | Digit Order | Cutter Encoding |
|-----------|--------------|-------------|-----------------|
| Fractional Inch | Baker Hughes, Halliburton | Cutter-0-Blades (Baker) or Blades-Cutter (Halliburton) | X/8 inch: 4=13mm, 5=16mm (5/8"=15.875mm → 16mm) |
| Metric | NOV, Schlumberger, Ulterra, Taurex, Varel | Blades-Cutter | Last digit of mm (2-dig) or literal mm (3-dig); 15→16mm |

The parser uses **model string shape** (regex patterns on the model string) rather than the manufacturer field, which is often inconsistent in the data.

**Confidence levels**:
- **High**: Matched a known manufacturer prefix pattern
- **Check**: Matched a fallback pattern with sane values (probably correct, but unverified prefix)
- **Unknown**: No numeric pattern found

See `bit_characterization_logic.md` for full pattern tables, edge cases, and per-manufacturer examples.

### Motor Classification

Extract two key parameters:

1. **Lobe configuration**: Extracted as `X/Y` from the motor model string (e.g., "5/6" = 5 rotor lobes, 6 stator lobes)
2. **RPG band**: From the numeric RPG field, binned as:
   - lo: <= 0.30 rev/gal
   - mid: 0.31 - 0.45
   - hi: 0.46 - 0.55
   - vhi: > 0.55

## Step 4: Group into Equivalent BHAs

An **Equivalent BHA** is defined by the combination of:

| Parameter | Source | Example |
|-----------|--------|---------|
| Bit blade count | Parsed from bit model | 6 |
| Bit cutter size (mm) | Parsed from bit model | 13 |
| Motor lobe config | Parsed from motor model | 5/6 |
| Motor RPG band | From motor RPG value | mid |

**Group key**: `{blades}B-{cutter}mm-{lobes}-{rpg_band}`

Example: `6B-13mm-5/6-mid` = 6-blade bit with 13mm cutters, 5/6 lobe motor, mid RPG

### What we intentionally exclude from grouping

- **Bit manufacturer**: Different vendors make equivalent bits. A Baker DD506TS and a NOV TK65 are both 6-blade 16mm bits.
- **Motor manufacturer**: Power sections are commodity items. A ProDirectional 5/6 and a NOV 5/6 are functionally equivalent.
- **Bit model suffix**: The suffix (e.g., "-G9", "TS", "SM") indicates design variants within the same blade/cutter family -- relevant for detailed analysis but not for initial grouping.
- **Motor stages**: While stages affect torque output, the lobe config + RPG band captures the key drilling behavior.

## Step 5: Pull Per-Foot Drilling Data

**Script**: `pull_1ft_for_runs.py`

- Input: Parsed BHA CSV (e.g., `lateral_bhas.csv`)
- Fetches `corva#wits.summary-1ft` for each BHA run's depth range
- Uses `ThreadPoolExecutor` with 10 workers for parallel API calls across all runs
- API pagination: 10,000 records per request, sorted by `measured_depth`

### ROP derivation
Each foot in `wits.summary-1ft` has `data.timestamp_max` and `data.timestamp_min`:
```
rop_ft_hr = 3600 / (timestamp_max - timestamp_min)
```
This gives the instantaneous ROP for drilling that one foot.

### Rig state classification
Each foot is classified by `data.state_max`:
- **"Rotary Drilling"** → rotary curve
- **"Slide Drilling"** → slide curve
- All other states (tripping, connections, etc.) → excluded

### Distance metrics
Two distance metrics are tracked per foot -- this is critical:
- **`distance_from_run_start`** = hole_depth - BHA start_depth → used for **rotary** ROP curves (captures **bit wear** effect)
- **`distance_from_lateral_start`** = hole_depth - lateral_start_depth → used for **slide** ROP curves (captures **friction/drag** effect that increases with lateral length)

### Filters
| Filter | Value | Rationale |
|--------|-------|-----------|
| Drilling states | Rotary Drilling, Slide Drilling only | Exclude non-drilling activities |
| ROP minimum | 5 ft/hr | Remove stuck/stalled pipe (bad data) |
| ROP maximum | 500 ft/hr | Remove timestamp artifacts |
| Min run length | 1,000 ft | Exclude short test runs that don't show degradation trend |

### Output columns
`rop_1ft_data.csv` — one row per drilled foot:
- `well_name`, `asset_id`, `bha_number`, `bit_model`, `motor_model`
- `equiv_bha_key`, `has_agitator`
- `hole_depth`, `distance_from_run_start`, `distance_from_lateral_start`
- `state` (Rotary Drilling / Slide Drilling)
- `rop_ft_hr`

## Step 6: Build ROP Type Curves

**Script**: `build_rop_curves.py`

### Dual x-axis approach
This is the key insight of the analysis. Rotary and slide ROP degrade from different mechanisms, so they use **different x-axes**:

| Mode | X-axis | Degradation mechanism |
|------|--------|----------------------|
| **Rotary** | Distance from BHA start (run length) | **Bit wear** — cutter dulling, gauge wear |
| **Slide** | Distance from lateral start | **Friction/drag** — longer lateral = more drag on slide |

### Binning strategy

| Mode | Bin size | Rationale |
|------|----------|-----------|
| **Rotary** | 100 ft | Sufficient data density per bin; captures bit wear progression |
| **Slide** | 250 ft | Slide footage is sparser; larger bins prevent noisy/empty bins |

Within each bin, the **median** ROP is used (robust to outliers).

### Per-run curves
Each BHA run produces two binned curves:
- **Rotary curve**: median ROP per 100-ft bin of `distance_from_run_start`
- **Slide curve**: median ROP per 250-ft bin of `distance_from_lateral_start`

### Per-group P10/P50/P90 curves
For each equivalent BHA group, aggregate per-run curves at each bin:
- **P10** = 10th percentile of run-level medians (pessimistic)
- **P50** = 50th percentile (expected performance)
- **P90** = 90th percentile (optimistic)
- Bins with < 3 contributing runs are flagged `low_confidence`

### Smoothing
Both rotary and slide group curves are smoothed with a **rolling median** (window = 5 bins) to remove bin-to-bin noise while preserving the overall degradation trend. Raw (unsmoothed) data is also retained for comparison.

### Agitator overlay
Within slide curves, runs with `has_agitator=True` are tracked separately to show agitator impact on slide ROP — **without splitting the BHA groups**. Agitators improve slide ROP but have no effect on rotary ROP.

### Time to TD (TTD) ranking
For a given target lateral length and expected slide percentage, calculate expected drilling time per equivalent BHA group:

```
For each segment of the lateral (at the finer bin resolution):
  TTD_segment = seg_len × (1 - slide%) / rotary_P50  +  seg_len × slide% / slide_P50
Total TTD = sum of all segments
```

- Uses the smoothed P50 curves
- Where P50 data is missing for a bin, extrapolates from the nearest available bin
- Groups are ranked from fastest to slowest TTD

### Outputs

| File | Contents |
|------|----------|
| `rop_curves_per_run.csv` | Per-run binned ROP (rotary + slide) |
| `rop_curves_by_group.csv` | Per-group P10/P50/P90 ROP at each bin (smoothed) |
| `ttd_ranking.csv` | Time-to-TD ranking for each equivalent BHA group |

## Step 7: Generate Charts

**Script**: `plot_type_curves.py`

Generates matplotlib charts in the `charts/` directory:

### Per-group charts (one pair per equivalent BHA):
1. **Rotary ROP type curve** — P10/P50/P90 bands + individual run traces, x-axis = distance from BHA start (ft)
2. **Slide ROP type curve** — P10/P50/P90 bands + individual run traces, x-axis = distance from lateral start (ft)

### Comparison charts (all groups together):
3. **Head-to-head rotary** — P50 rotary ROP for all groups on one chart
4. **Head-to-head slide** — P50 slide ROP for all groups on one chart

### Ranking chart:
5. **TTD ranking** — horizontal bar chart showing expected hours to TD for each group

All charts use smoothed data (rolling median, window=5 bins). Chart subtitles indicate bin size and smoothing parameters.

Output: `charts/*.png`

---

## Vertical / Intermediate Section Workflow

The lateral workflow above uses **distance** as the x-axis for ROP curves. For vertical and intermediate sections, ROP is dominated by **formation** (hard rock vs soft rock), so we normalize the x-axis to **% formation** -- allowing offset wells with different formation depths to be compared on the same grid.

### Key Differences from Lateral

| Aspect | Lateral | Vertical/Intermediate |
|--------|---------|----------------------|
| X-axis | Distance (ft) | % Formation (0-100%) |
| Rotary x-axis | Distance from BHA start | % Formation |
| Slide x-axis | Distance from lateral start | % Formation |
| Bin size | 100 ft (rotary), 250 ft (slide) | 10% formation segments |
| Smoothing window | 5 bins | 3 segments |
| Primary ROP driver | Bit wear (rotary), drag (slide) | Formation hardness |
| Section identification | `data.name` contains "lateral" | `data.name` contains "intermediate" or "vertical" |

### Formation Roadmap Concept

The target well defines a **roadmap** -- a sequence of formations from section start to section end, each divided into 10% segments:

```
Example: Section Start = Wilcox 50%, Section End = Chalk 50%

Wilcox:   [50%][60%][70%][80%][90%][100%]     -- 5 segments
Reklaw:   [0%][10%][20%]...[90%][100%]         -- 10 segments
Anacacho: [0%][10%][20%]...[90%][100%]         -- 10 segments
Chalk:    [0%][10%][20%][30%][40%][50%]        -- 5 segments
                                         Total: 30 segments
```

Each offset well's BHA runs are mapped onto this roadmap using their own formation tops and TVD data.

### Step V1: Pull Formation Tops

**Script**: `pull_formation_tops.py`

- Fetches `corva#data.formations` for each offset well
- Output: `formation_tops.csv` with one row per formation per well
- Fields: `asset_id`, `well_name`, `formation_name`, `md_top`, `tvd_top`, `md_thickness`, `tvd_thickness`, `lithology`

### Step V1b: Normalize Formation Names

**Script**: `normalize_formations.py`

Different operators (and even different wells within the same operator) use inconsistent formation names. For example, "Eagle Ford", "Eagle Ford Lower", "Lower Eagle Ford", "Lower Eagle Ford 2a", and "Upper Eagle Ford_6a" all refer to sub-zones of the Eagle Ford. Without normalization, these create hundreds of sparse bins that prevent meaningful P10/P50/P90 aggregation.

**Two modes:**

| Mode | CLI Flag | Algorithm |
|------|----------|-----------|
| **Target-well-reference** (default) | `--target-asset <id>` | Use the target well's formations as canonical reference. Auto-consolidate sub-formations by name hierarchy + TVD proximity. Map offset wells by TVD range. |
| **TVD-only** | `--mode tvd-only --tvd-gap 200` | Cluster all formation tops by TVD proximity, ignoring names. Name each cluster by the most common formation name. |

**Auto-consolidation algorithm (target-reference mode):**
1. Extract root formation name by stripping prefixes ("Upper", "Lower", "Base", "Middle") and suffixes (ordinals like "2a"/"6a", bench letters like "B Bench", lithology like "Shale"/"Sand"/"Carbonate")
2. Group target well's formations by root name
3. Orphan names (like standalone "B Bench") are merged into the nearest preceding parent group by TVD proximity
4. Build canonical TVD ranges from consolidated groups
5. Map each offset well's formation tops to the canonical formation whose TVD range contains it
6. Consolidate per-well entries: merge sub-formations into one row per canonical formation

**Example (Galvan Ranch):** 20 raw formations → 10 canonical formations. "Austin Chalk", "B Bench", "C Bench", "D Bench", "E Bench" → single "Austin Chalk". Six Eagle Ford sub-zones → single "Eagle Ford".

**Overrides:** Users can provide a JSON file (`--overrides overrides.json`) with explicit groupings to customize the auto-detected hierarchy. This is designed for future FE integration where users can visually adjust formation groupings.

**Outputs:**
- `formation_tops_canonical.csv` — same schema as `formation_tops.csv`, but with canonical names and consolidated rows. **This is the file passed to downstream steps.**
- `canonical_map.json` — full mapping details for FE display: canonical formations, sub-formations, per-well mappings, excluded wells

**Impact:** In the Galvan Ranch test case, bin population improved from 5-40% to 27-90% per group, and TTD calculation went from many missing segments to 0 missing segments for 7 of 8 groups.

### Step V2: Pull BHAs for Intermediate/Vertical Sections

**Script**: `pull_lateral_bhas.py --section-type intermediate`

- Same script as lateral, but `--section-type intermediate` filters for intermediate sections
- Section matching is by `data.name` substring (case-insensitive): "intermediate", "int "
- Other supported types: `vertical`, `surface`, `curve`
- Output: `intermediate_bhas_*.csv`

### Step V3: Pull Per-Foot Data with Formation Mapping

**Script**: `pull_1ft_for_runs.py [bha_csv] --mode vertical --formations formation_tops_canonical.csv`

- Same API calls as lateral, but adds formation mapping columns:
  - `formation_name` -- which formation each foot falls in (by TVD), using canonical names
  - `formation_pct` -- position within the formation (0-100%)
  - `formation_segment` -- discretized 10% bin (0, 10, 20, ..., 90)
- Requires `formation_tops_canonical.csv` from Step V1b (or raw `formation_tops.csv` from V1 if normalization is skipped)
- Uses `data.true_vertical_depth_mean` from wits.summary-1ft to map feet to formations
- Output: `rop_1ft_data_vertical.csv`

### Step V4: Build Formation-Based ROP Curves

**Script**: `build_rop_curves.py --mode vertical`

- Bins by `formation_name|segment` (e.g., "Wilcox|50") instead of distance
- Both rotary and slide use the same x-axis (% formation)
- P10/P50/P90 at each formation segment
- Rolling median smoothing (window=3 segments)
- TTD calculation uses formation segment MD lengths
- Output: `rop_curves_per_run_vertical.csv`, `rop_curves_by_group_vertical.csv`, `ttd_ranking_vertical.csv`, `formation_roadmap.csv`

### Step V5: Generate Formation-Based Charts

**Script**: `plot_type_curves.py --mode vertical`

- X-axis shows formation segments with formation names as boundary labels
- Formation boundaries marked with dashed vertical lines
- Same chart types as lateral: per-group rotary/slide, comparisons, TTD ranking
- Output: `charts/vert_*.png`

### Vertical Execution Order

```
1. python find_offsets_all_operators.py                               # same as lateral
2. python pull_formation_tops.py [wells_csv]                          # → formation_tops.csv
3. python normalize_formations.py --target-asset <TARGET_ID>          # → formation_tops_canonical.csv + canonical_map.json
4. python pull_lateral_bhas.py [wells_csv] --section-type intermediate # → intermediate_bhas_*.csv
5. python parse_bit_motors.py [bha_csv]                               # same as lateral
6. python group_equivalent_bhas.py [bha_csv]                          # same as lateral
7. python pull_1ft_for_runs.py [bha_csv] --mode vertical --formations formation_tops_canonical.csv
8. python build_rop_curves.py --mode vertical                         # → rop_curves_*_vertical.csv
9. python plot_type_curves.py --mode vertical                         # → charts/vert_*.png
```

---

## Additional BHA Detection

### RSS (Rotary Steerable System)
- Detected in `pull_lateral_bhas.py` from `data.components[]`:
  - `family == "rss"`, OR
  - `name` or `model` contains "rotary steerable" (case-insensitive)
- **Grouping impact**: RSS BHAs have `motor_key = "RSS"` instead of lobe/RPG, producing group keys like `6B-16mm | RSS`
- **Curve impact**: RSS BHAs have no slide drilling — the entire curve is rotary
- RSS BHAs are treated as a distinct category because their drilling dynamics are fundamentally different from motor-driven BHAs

### Agitators
- Detected in `pull_lateral_bhas.py` from `data.components[]`:
  - `family == "agitator"`, OR
  - `name` or `model` contains "agitator" (case-insensitive)
- **Grouping impact**: None — agitators do **not** split equivalent BHA groups
- **Curve impact**: Runs with agitators are flagged and tracked as an overlay within slide performance curves
- Agitators improve slide ROP (reduce friction during slide) but have no measurable effect on rotary ROP

---

## Data Sources (Corva API)

| Dataset | API Path | Used In | Key Fields |
|---------|----------|---------|------------|
| `corva#data.drillstring` | `/api/v1/data/corva/data.drillstring/` | Step 2 | `data.components[]`, `data.start_depth`, `data.end_depth`, `data.id` |
| `corva#data.well-sections` | `/api/v1/data/corva/data.well-sections/` | Step 2 | `data.name`, `data.top_depth`, `data.bottom_depth` |
| `corva#data.formations` | `/api/v1/data/corva/data.formations/` | Step V1 | `data.formation_name`, `data.md`, `data.td`, `data.lithology` |
| `corva#wits.summary-1ft` | `/api/v1/data/corva/wits.summary-1ft/` | Step 5/V3 | `data.hole_depth`, `data.state_max`, `data.timestamp_max`, `data.timestamp_min`, `data.true_vertical_depth_mean` |

All queries use `asset_id` + depth or timestamp filters. API base: `https://data.corva.ai`

---

## Typical Execution Order (Single-Section, Lateral)

```
1. python find_offsets_all_operators.py      # → offset_wells_*.csv
2. python pull_lateral_bhas.py               # → lateral_bhas_*.csv
3. python parse_bit_motors.py                # updates lateral_bhas with parsed fields
4. python group_equivalent_bhas.py           # → equiv_bha_groups.csv
5. python pull_1ft_for_runs.py               # → rop_1ft_data.csv  (slow — API calls)
6. python build_rop_curves.py                # → rop_curves_*.csv, ttd_ranking.csv
7. python plot_type_curves.py                # → charts/*.png
```

Steps 1-4 are fast (minutes). Step 5 is the bottleneck (~10 min for ~50 wells with 10 parallel workers). Steps 6-7 are fast (seconds).

---

## Section-Driven Workflow (All Sections at Once)

**Script**: `run_all_sections.py --asset <TARGET_ID>`

This orchestrator runs the full pipeline for **every section** of a target well in one command. It replaces the need to manually run each section type separately.

### How It Works

1. **Analyze target well** (`analyze_target_well.py`): Fetches `corva#data.well-sections` for the target well, auto-detects vertical vs lateral mode per section, maps each section to canonical formations, and outputs `target_sections.json`.

2. **Pull ALL BHA runs** (`pull_lateral_bhas.py --all-runs`): Fetches every BHA run from every offset well with no section-type filtering. This produces a single master CSV (`all_bhas_*.csv`) that contains all 173+ runs across all hole sizes and depths.

3. **Parse bit & motor models** (`parse_bit_motors.py`): Standard parsing on the master CSV to extract blade count, cutter size, lobe config, RPG band.

4. **Filter per section** (`filter_bhas_by_section.py`): For each target section, filters the master BHA list by:
   - **Hole size match**: `bit_size` must equal the section's `diameter` (within 0.1")
   - **Depth overlap**: BHA run's MD range must overlap the section's MD range
   - **Minimum formation coverage** (vertical only, default 50%): The fraction of the section's canonical formations that the offset run covers

5. **Per-section pipeline**: For each section that has filtered BHA runs:
   - `group_equivalent_bhas.py` — group the section's BHAs
   - `pull_1ft_for_runs.py` — fetch 1ft data (lateral or vertical mode)
   - `build_rop_curves.py` — build P10/P50/P90 curves and TTD
   - `plot_type_curves.py` — generate charts with section name + hole size in titles

### Section-Driven Execution

```
python run_all_sections.py --asset 82512872
```

Optional flags:
- `--wells offset_wells_15mi.csv` — offset wells CSV (default: offset_wells_15mi.csv)
- `--skip-pull` — skip BHA pulling (use existing all_bhas CSV)
- `--skip-1ft` — skip 1ft data fetch (use existing)
- `--min-coverage 0.5` — minimum formation coverage filter (default: 50%)

### Output Structure

Each section gets its own output directory under `sections/`:

```
bha_selection/
  sections/
    Surface/
      rop_1ft_data_vertical.csv
      rop_curves_*.csv
      formation_roadmap.csv
      charts/
        vert_rotary_*.png
        vert_slide_*.png
        vert_comparison_*.png
        vert_ttd_ranking.png
    Intermediate/
      ...
    Production_Vertical/
      ...
    Production_Curve/
      ...
    Production_Lateral/
      rop_1ft_data.csv
      rop_curves_*.csv
      charts/
        rotary_*.png
        slide_*.png
        comparison_*.png
        ttd_ranking.png
```

### Galvan Ranch Results (5 sections)

| Section | Hole Size | Mode | Offset Runs | Groups | Charts |
|---------|-----------|------|-------------|--------|--------|
| Surface | 17.5" | vertical | 3 | 1 | 2 |
| Intermediate | 12.25" | vertical | 12 | 4 | 7 |
| Production Vertical | 8.75" | vertical | 36 | 6 | 7 |
| Production Curve | 8.75" | vertical | 11 | 3 | 5 |
| Production Lateral | 8.75" | lateral | 60 | 10 | 12 |

Total: ~33 charts in ~2.3 minutes.

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Group by blade + cutter + lobe + RPG | Yes | Captures 80%+ of drilling performance variance |
| Exclude bit manufacturer from grouping | Yes | Different vendors make equivalent bits |
| 15mm → 16mm reclassification | Yes | 5/8" = 15.875mm, closer to 16mm; unifies fractional/metric conventions |
| Rotary x-axis = run length | Yes | Bit wear is the primary rotary degradation mechanism |
| Slide x-axis = lateral length | Yes | Friction/drag (not bit wear) drives slide degradation |
| 100-ft rotary bins, 250-ft slide bins | Yes | Slide footage is sparser; larger bins prevent noisy results |
| Rolling median smoothing (window=5) | Yes | Removes bin-to-bin noise while preserving degradation trend |
| ROP from timestamps (not data.rop) | Yes | `data.rop` is often stale or interpolated; `3600/(tmax-tmin)` is more accurate per foot |
| RSS as separate group | Yes | No slide drilling; fundamentally different dynamics |
| Agitator as overlay, not group split | Yes | Same BHA, different completion; compare within group |
| Min 3 runs per bin for confidence | Yes | Statistical minimum for P10/P50/P90 to be meaningful |
| Min 1,000 ft run length | Yes | Short runs don't show meaningful degradation trend |
| Vertical x-axis = % formation | Yes | Formation hardness dominates ROP in vertical; normalizes across wells with different formation depths |
| 10% formation segments (vertical) | Yes | Sufficient resolution per formation; matches PDF reference approach |
| Rolling median window=3 (vertical) | Yes | Fewer segments than lateral bins; smaller window prevents over-smoothing |
| Configurable section type | Yes | Same script handles lateral, intermediate, vertical, surface via `--section-type` |
| Formation name normalization | Yes | Operators name formations inconsistently; auto-consolidate sub-formations into canonical groups using target-well-reference (default) or TVD-only clustering |
| Target-well-reference as default | Yes | Basin-agnostic — the target well's own stratigraphy defines the canonical formations; no lookup tables to maintain per basin |
| Orphan sub-unit detection | Yes | Names like "B Bench" without a parent prefix are merged into nearest preceding canonical group by TVD proximity |
| canonical_map.json for FE | Yes | Outputs full mapping details (hierarchy, per-well mappings, excluded wells) for future FE display and user override |
| Section-driven workflow | Yes | Analyze target well's sections, pull ALL offset BHAs, filter by hole size + formation overlap per section. Replaces manual per-section runs. |
| Hole size matching | Yes | Offset BHA runs must match section hole size (within 0.1") to prevent mixing 8.75" and 12.25" data |
| Minimum formation coverage (50%) | Yes | Offset runs must cover at least 50% of the target section's formations to be included in vertical curves. Prevents partial-coverage runs from skewing TTD. |
| Max missing formations per group (1) | Yes | After building group curves, exclude any equivalent BHA group that has no confident rotary data in 2+ formations. A formation counts as 'covered' if at least 1 of its 10% segments has a confident rotary entry. Configurable via `--max-missing-formations` (default 1). |
| --all-runs mode | Yes | Pull every BHA run from offsets without section filtering; filter later per section. More efficient than pulling each section type separately. |
| Per-section output directories | Yes | Each section's curves and charts go to `sections/<name>/` to keep outputs organized and prevent filename collisions. |
| Auto-detect vertical vs lateral | Yes | Section is lateral if "lateral" appears in section name; otherwise defaults to vertical. Can be overridden. |
| Section label in chart titles | Yes | All charts display section name + hole size (e.g., "Intermediate (12.25in)") to prevent confusion when comparing across sections. |

---

## Files Reference

| File | Purpose |
|------|---------|
| **Scripts** | |
| `find_offsets_all_operators.py` | Find offset wells by basin/formation/radius |
| `pull_lateral_bhas.py` | Extract BHAs from offset wells by section type (`--section-type lateral/intermediate/vertical`) or all runs (`--all-runs`) |
| `pull_bhas_by_size.py` | Extract BHAs by bit diameter (alternative to section-based pull) |
| `analyze_target_well.py` | Analyze target well's planned sections, map to formations, output `target_sections.json` |
| `filter_bhas_by_section.py` | Filter master BHA CSV by hole size + depth overlap + formation coverage per section |
| `run_all_sections.py` | Orchestrator: runs the full pipeline for every section of a target well in one command |
| `pull_formation_tops.py` | Fetch formation tops per well from `corva#data.formations` (vertical workflow) |
| `normalize_formations.py` | Normalize formation names: target-well-reference (default) or TVD-only clustering. Outputs `formation_tops_canonical.csv` + `canonical_map.json` |
| `parse_bit_motors.py` | Parse bit models → blade count + cutter size; motor models → lobe config + RPG band |
| `group_equivalent_bhas.py` | Group BHAs into equivalent categories; summarize group statistics |
| `pull_1ft_for_runs.py` | Fetch `wits.summary-1ft` per run; derive ROP; supports `--mode lateral/vertical` |
| `build_rop_curves.py` | Build per-run/per-group curves; supports `--mode lateral/vertical` |
| `plot_type_curves.py` | Generate matplotlib charts; supports `--mode lateral/vertical` |
| `build_bit_catalog.py` | Build deduplicated bit model catalog across all wells |
| `full_corva_bit_scan.py` | Full-Corva scan for bit classification (57,776 wells) |
| **Documentation** | |
| **Documentation** | |
| `classification_process.md` | This document — master BHA selection workflow |
| `bit_characterization_logic.md` | Detailed bit encoding conventions, edge cases, per-manufacturer patterns |
| `.cursor/rules/corva-learnings.mdc` | Persistent Corva API patterns, data model knowledge, and quirks |
| **Generated Data** | |
| `canonical_map.json` | Formation normalization mapping (for FE display/overrides) |
| `formation_tops_canonical.csv` | Consolidated formation tops with canonical names |
