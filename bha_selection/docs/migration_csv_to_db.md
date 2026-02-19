# Migration: CSV to SQLite + Parquet

**Status: COMPLETE** (all phases implemented)

## Overview

Replace ~20 ad-hoc CSV files with a single SQLite database for relational/metadata
and Parquet files for heavy analytical data. CSV exports remain available as a
debug/inspection flag on every script.

## Current Pain Points

| Problem | Example |
|---|---|
| No asset linkage | `offset_wells_15mi_*.csv` reused for wrong target well |
| Full-scan on every read | `_formation_tops_has_asset()` reads entire file for one asset |
| Everything is strings | Constant `float(row["md_top"])` casting |
| No indexing | Filter 1ft data by asset+depth = scan all rows |
| File-naming as state | Glob patterns like `bhas_*.csv` are fragile |
| Large 1ft data is slow | 500K rows read/written as text repeatedly |

## Target Architecture

```
bha_selection/
  bha_selection.db          <-- SQLite: all relational/metadata
  data/
    rop_1ft_{section}.parquet       <-- Parquet: heavy analytical
    rop_curves_{section}.parquet
    full_bit_scan.parquet
  exports/                  <-- CSV debug dumps (gitignored)
    offset_wells.csv
    bhas_Production_Vertical_8.75in.csv
    ...
  db.py                     <-- Data access layer
```

## SQLite Schema

### Core Tables

```sql
-- Tracks each analysis session (replaces current_analysis_state.json)
CREATE TABLE analysis_runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    target_asset_id TEXT NOT NULL,
    search_radius   REAL DEFAULT 15.0,
    created_at      TEXT DEFAULT (datetime('now')),
    offset_csv_path TEXT,
    UNIQUE(target_asset_id, search_radius)
);

-- Replaces offset_wells_*.csv
CREATE TABLE offset_wells (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    asset_id        TEXT NOT NULL,
    well_name       TEXT,
    operator        TEXT,
    basin           TEXT,
    target_formation TEXT,
    rig             TEXT,
    distance_miles  REAL,
    hole_depth_ft   REAL,
    section         TEXT,
    hole_diameter   REAL,
    spud_date       TEXT,
    lat             REAL,
    lon             REAL,
    well_state      TEXT
);
CREATE INDEX idx_ow_analysis ON offset_wells(analysis_run_id);
CREATE INDEX idx_ow_asset ON offset_wells(asset_id);

-- Replaces all_bhas_*.csv, bhas_*.csv, lateral_bhas_*.csv
CREATE TABLE bha_runs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_run_id     INTEGER REFERENCES analysis_runs(id),
    asset_id            TEXT NOT NULL,
    well_name           TEXT,
    operator            TEXT,
    distance_miles      REAL,
    section_type        TEXT,
    bha_number          INTEGER,
    start_depth         REAL,
    end_depth           REAL,
    run_length          REAL,
    section_start_depth REAL,
    lateral_start_depth REAL,
    set_date            TEXT,
    num_components      INTEGER,
    is_rss              INTEGER DEFAULT 0,
    has_agitator        INTEGER DEFAULT 0,
    -- Bit fields
    bit_manufacturer    TEXT,
    bit_model           TEXT,
    bit_size            TEXT,
    parsed_blades       TEXT,
    parsed_cutter_mm    TEXT,
    parse_confidence    TEXT,
    parse_method        TEXT,
    -- Motor fields
    motor_model         TEXT,
    motor_rpg           TEXT,
    motor_lobe_config   TEXT,
    motor_rpg_band      TEXT,
    -- Grouping
    equiv_bha_key       TEXT,
    -- Section filtering
    section_name        TEXT,         -- which target section this was filtered into
    hole_size_filter    REAL,         -- hole size used for filtering
    formation_coverage  REAL,
    formations_covered  TEXT
);
CREATE INDEX idx_bha_analysis ON bha_runs(analysis_run_id);
CREATE INDEX idx_bha_asset ON bha_runs(asset_id);
CREATE INDEX idx_bha_section ON bha_runs(section_name);
CREATE INDEX idx_bha_equiv ON bha_runs(equiv_bha_key);

-- Replaces formation_tops.csv and formation_tops_canonical.csv
CREATE TABLE formation_tops (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id        TEXT NOT NULL,
    well_name       TEXT,
    formation_name  TEXT NOT NULL,
    canonical_name  TEXT,           -- NULL until normalization runs
    md_top          REAL,
    tvd_top         REAL,
    md_thickness    REAL,
    tvd_thickness   REAL,
    lithology       TEXT,
    is_canonical    INTEGER DEFAULT 0  -- 1 after normalization
);
CREATE INDEX idx_fm_asset ON formation_tops(asset_id);
CREATE INDEX idx_fm_canonical ON formation_tops(canonical_name);

-- Replaces target_sections.json
CREATE TABLE target_sections (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    name            TEXT NOT NULL,
    hole_size       REAL,
    mode            TEXT DEFAULT 'vertical',
    top_md          REAL,
    bottom_md       REAL,
    section_length  REAL,
    top_tvd         REAL,
    bottom_tvd      REAL,
    start_formation TEXT,
    end_formation   TEXT,
    formations_json TEXT   -- JSON array of formation names in section
);
CREATE INDEX idx_ts_analysis ON target_sections(analysis_run_id);

-- Replaces equiv_bha_groups_*.csv
CREATE TABLE equiv_bha_groups (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    section_name    TEXT,
    group_key       TEXT NOT NULL,
    num_runs        INTEGER,
    num_wells       INTEGER,
    num_operators   INTEGER,
    operators       TEXT,
    avg_run_ft      REAL,
    min_run_ft      REAL,
    max_run_ft      REAL,
    total_ft        REAL,
    runs_with_agitator INTEGER,
    runs_with_rss   INTEGER
);

-- Replaces bit_catalog.csv
CREATE TABLE bit_catalog (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    bit_manufacturer TEXT,
    bit_model       TEXT,
    bit_diameters   TEXT,
    parsed_blades   TEXT,
    parsed_cutter_mm TEXT,
    parse_confidence TEXT,
    total_runs      INTEGER,
    operators       TEXT,
    UNIQUE(bit_manufacturer, bit_model)
);

-- Replaces canonical_map.json
CREATE TABLE canonical_formations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    canonical_name  TEXT NOT NULL,
    display_order   INTEGER,
    target_tvd_top  REAL,
    target_tvd_bottom REAL
);

CREATE TABLE canonical_sub_formations (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_formation_id  INTEGER REFERENCES canonical_formations(id),
    sub_formation_name      TEXT NOT NULL
);

-- Replaces ttd_ranking*.csv
CREATE TABLE ttd_rankings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    section_name    TEXT,
    group_key       TEXT,
    num_runs        INTEGER,
    num_wells       INTEGER,
    target_length   REAL,
    expected_slide_pct REAL,
    ttd_hours       REAL,
    ttd_days        REAL,
    bins_with_data  INTEGER,
    bins_missing    INTEGER
);
```

### Parquet Files (Heavy Analytical Data)

| File | Replaces | Rows | Columns |
|---|---|---|---|
| `data/rop_1ft_{section}.parquet` | `rop_1ft_data*.csv` | 10K-500K | asset_id, bha_number, hole_depth, state, rop_ft_hr, formation_*, equiv_bha_key |
| `data/rop_curves_{section}.parquet` | `rop_curves_per_run*.csv` + `rop_curves_by_group*.csv` | 1K-10K | Binned curve data with curve_level column (run vs group) |
| `data/full_bit_scan.parquet` | `full_bit_scan.csv` | 10K-100K+ | All bit scan fields |

Why Parquet for these:
- **10-30x compression** over CSV (columnar + snappy)
- **Column pruning**: read only needed columns (e.g., just rop_ft_hr + state)
- **Predicate pushdown**: filter by asset_id without scanning full file
- **Native pandas support**: `pd.read_parquet()` / `df.to_parquet()`
- **Type preservation**: no more string-to-float casting

## Data Access Layer (`db.py`)

Central module that all scripts import. Provides:

```python
# db.py - Data access layer

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "bha_selection.db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")

# ── Connection management ──

def get_conn() -> sqlite3.Connection:
    """Get a connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    """Create tables if they don't exist."""
    ...

# ── Analysis runs ──

def get_or_create_analysis_run(asset_id: str, radius: float) -> int:
    """Get existing or create new analysis run. Returns run_id."""
    ...

def get_current_run(asset_id: str) -> dict | None:
    """Get the most recent analysis run for an asset."""
    ...

# ── Offset wells ──

def save_offset_wells(run_id: int, wells: list[dict]):
    """Bulk insert offset wells for an analysis run."""
    ...

def get_offset_wells(run_id: int) -> list[dict]:
    """Get offset wells for a run."""
    ...

# ── BHA runs ──

def save_bha_runs(run_id: int, runs: list[dict]):
    """Bulk insert BHA runs."""
    ...

def get_bha_runs(run_id: int, section_name: str = None) -> list[dict]:
    """Get BHA runs, optionally filtered by section."""
    ...

def get_bha_runs_as_df(run_id: int, section_name: str = None) -> pd.DataFrame:
    """Get BHA runs as a DataFrame for analytical operations."""
    ...

# ── Formation tops ──

def save_formation_tops(tops: list[dict]):
    """Upsert formation tops (by asset_id + formation_name + md_top)."""
    ...

def get_formation_tops(asset_id: str, canonical_only: bool = False) -> list[dict]:
    """Get formation tops for a well."""
    ...

def formation_tops_exist(asset_id: str) -> bool:
    """Quick check without loading data."""
    ...

# ── 1ft data (Parquet) ──

def save_1ft_data(section_name: str, df: pd.DataFrame):
    """Write 1ft data as Parquet."""
    path = os.path.join(DATA_DIR, f"rop_1ft_{section_name}.parquet")
    df.to_parquet(path, index=False, compression="snappy")

def load_1ft_data(section_name: str, columns: list[str] = None) -> pd.DataFrame:
    """Read 1ft data, optionally selecting specific columns."""
    path = os.path.join(DATA_DIR, f"rop_1ft_{section_name}.parquet")
    return pd.read_parquet(path, columns=columns)

# ── ROP curves (Parquet) ──

def save_rop_curves(section_name: str, per_run_df: pd.DataFrame, group_df: pd.DataFrame):
    """Write both per-run and group-level curves."""
    ...

def load_rop_curves(section_name: str, level: str = "group") -> pd.DataFrame:
    """Read ROP curves. level = 'run' | 'group'."""
    ...

# ── CSV export ──

def export_csv(table_or_df, name: str):
    """Dump a table or DataFrame to exports/ for debugging."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{name}.csv")
    if isinstance(table_or_df, pd.DataFrame):
        table_or_df.to_csv(path, index=False)
    elif isinstance(table_or_df, list):
        # list of dicts
        import csv
        if not table_or_df:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=table_or_df[0].keys())
            w.writeheader()
            w.writerows(table_or_df)
    print(f"  CSV export: {path}")
```

## Migration Phases

### Phase 0: Foundation (do first)
**Goal**: Create `db.py`, install `pyarrow`, set up schema. No script changes yet.

| Task | Effort |
|---|---|
| Create `db.py` with all table DDL and helper functions | Medium |
| `pip install pyarrow` | Trivial |
| Create `data/` and `exports/` directories | Trivial |
| Add `exports/` and `*.parquet` and `*.db` to `.gitignore` | Trivial |
| Create `requirements.txt` with all dependencies | Small |

### Phase 1: State & Metadata (highest ROI)
**Goal**: Eliminate the stale-file bugs. Migrate relational data to SQLite.

Scripts to update (in dependency order):

| Script | What changes | CSV kept? |
|---|---|---|
| `find_offsets_all_operators.py` | Write to `offset_wells` table via `db.save_offset_wells()` | `--export-csv` flag |
| `find_offsets_enriched.py` | Same pattern | `--export-csv` flag |
| `pull_formation_tops.py` | Write to `formation_tops` table | `--export-csv` flag |
| `normalize_formations.py` | Write to `formation_tops` (canonical_name col) + `canonical_formations` table | `--export-csv` flag |
| `analyze_target_well.py` | Write to `target_sections` table, read formations from DB | `--export-csv` flag |
| `pull_lateral_bhas.py` | Write to `bha_runs` table | `--export-csv` flag |
| `filter_bhas_by_section.py` | Update `bha_runs.section_name` + coverage cols | `--export-csv` flag |
| `parse_bit_motors.py` | Update `bha_runs` parsed columns in-place | `--export-csv` flag |
| `group_equivalent_bhas.py` | Write to `equiv_bha_groups` table, update `bha_runs.equiv_bha_key` | `--export-csv` flag |
| `build_bit_catalog.py` | Write to `bit_catalog` table | `--export-csv` flag |
| `pipeline.py` (backend) | Use `db.get_*()` instead of glob patterns and CSV reads | N/A |
| `wells.py` (backend) | Use `db.get_offset_wells()` instead of reading CSV | N/A |
| `sections.py` (backend) | Use `db.get_*()` for TTD and group data | N/A |

**Key win**: `pipeline.py` no longer needs `_find_offset_wells()` glob logic,
`_csv_matches_asset()`, `_clean_stale_section_files()`, or `current_analysis_state.json`.
A simple `db.get_or_create_analysis_run(asset_id, radius)` replaces all of it.

### Phase 2: Heavy Analytical Data (biggest perf win)
**Goal**: Migrate 1ft data and ROP curves to Parquet.

| Script | What changes | Perf gain |
|---|---|---|
| `pull_1ft_for_runs.py` | Write `rop_1ft_{section}.parquet` via `db.save_1ft_data()` | 5-10x write speed, 10-30x smaller file |
| `build_rop_curves.py` | Read from Parquet, write curves to Parquet | 5-10x read speed, column pruning |
| `plot_type_curves.py` | Read curves from Parquet | Faster load |
| `full_corva_bit_scan.py` | Write `full_bit_scan.parquet` | Major for 100K+ row scans |

### Phase 3: Backend & Cleanup
**Goal**: Remove all direct CSV I/O from backend, clean up legacy code.

| Task | Details |
|---|---|
| Update `pipeline.py` | Remove all file-path hacks, use `db.*` functions |
| Update `wells.py` | `get_offset_wells` reads from DB, no CSV fallback needed |
| Update `sections.py` | Read TTD/curves from DB/Parquet |
| Remove `current_analysis_state.json` logic | `analysis_runs` table replaces it |
| Remove stale-file cleanup code | Not needed with DB-keyed data |
| Update `run_all_sections.py` | Pass `run_id` instead of file paths between steps |
| Add `--export-csv` to all scripts | Global flag for debug dumps |

## Script-by-Script Migration Pattern

Each script follows the same pattern:

```python
# BEFORE (current)
def main():
    # Read from CSV
    with open("offset_wells_15mi.csv") as f:
        rows = list(csv.DictReader(f))
    
    # ... process ...
    
    # Write to CSV
    with open("output.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=[...])
        writer.writeheader()
        writer.writerows(results)

# AFTER (migrated)
import db

def main():
    parser.add_argument("--export-csv", action="store_true",
                        help="Also dump CSV to exports/ for debugging")
    
    # Read from DB
    run_id = db.get_current_run_id(asset_id)
    rows = db.get_offset_wells(run_id)
    
    # ... process (same logic) ...
    
    # Write to DB
    db.save_results(run_id, results)
    
    # Optional CSV export
    if args.export_csv:
        db.export_csv(results, "output")
```

## Performance Comparison

| Operation | CSV (current) | SQLite + Parquet |
|---|---|---|
| Check if asset has formation data | ~200ms (scan full CSV) | <1ms (indexed query) |
| Load 1ft data (200K rows) | ~5-8s | ~0.3-0.5s |
| Filter BHAs by section + hole size | ~100ms (scan) | <5ms (indexed) |
| Write 1ft data (200K rows) | ~3-5s | ~0.5s (Parquet) |
| Find offset wells for asset | ~500ms (glob + scan) | <1ms (indexed) |
| Switch target well (clean stale data) | Delete files, hope nothing is stale | Query by run_id, always correct |
| Disk space (1ft data, 200K rows) | ~50MB CSV | ~3-5MB Parquet |

## New Dependencies

```
pyarrow>=15.0      # Parquet support for pandas
```

`sqlite3` is built into Python. `pandas` is already installed.

## Migration Order (Recommended)

```
Phase 0 ──► Phase 1a ──► Phase 1b ──► Phase 2 ──► Phase 3
             │              │            │            │
         db.py +         find_offsets  pull_1ft     backend
         schema          pull_bhas     build_curves cleanup
                         formations    plot_curves
                         analyze
                         filter/group
```

Each phase is independently deployable. After Phase 1a, the stale-file bugs
are eliminated. After Phase 2, the performance gains are realized.

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| SQLite write contention (parallel scripts) | WAL mode + short transactions; only one pipeline runs at a time |
| Parquet requires pyarrow dependency | Already common; fallback to CSV if import fails |
| Existing CSVs from prior runs | Phase 1 scripts check for legacy CSVs and auto-import on first run |
| Breaking `run_all_sections.py` | Migrate last; it already calls scripts via subprocess |
| DB corruption | SQLite is battle-tested; WAL mode handles crashes |
