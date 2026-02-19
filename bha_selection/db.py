"""Centralized data access layer for BHA Selection Tool.

Provides SQLite for relational/metadata and Parquet for heavy analytical data.
All scripts import this module instead of doing direct CSV I/O.

Usage:
    import db

    # Get or create an analysis run
    run_id = db.get_or_create_run("58836173", radius=15.0)

    # Save offset wells
    db.save_offset_wells(run_id, wells_list)

    # Read them back
    wells = db.get_offset_wells(run_id)

    # Heavy data via Parquet
    db.save_1ft_data("Production_Vertical", df)
    df = db.load_1ft_data("Production_Vertical", columns=["rop_ft_hr", "state"])

    # CSV debug export
    db.export_csv(wells, "offset_wells")
"""

import csv
import json
import os
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Any

import pandas as pd

# ── Paths ──

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "bha_selection.db")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
EXPORT_DIR = os.path.join(SCRIPT_DIR, "exports")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

# ── Schema ──

_SCHEMA_SQL = """
-- Analysis sessions (replaces current_analysis_state.json + file naming hacks)
CREATE TABLE IF NOT EXISTS analysis_runs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    target_asset_id     TEXT NOT NULL,
    search_radius       REAL DEFAULT 15.0,
    created_at          TEXT DEFAULT (datetime('now')),
    offset_csv_path     TEXT,
    status              TEXT DEFAULT 'active'
);
CREATE INDEX IF NOT EXISTS idx_ar_asset ON analysis_runs(target_asset_id);

-- Offset wells discovered near the target
CREATE TABLE IF NOT EXISTS offset_wells (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id              INTEGER NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    asset_id            TEXT NOT NULL,
    well_name           TEXT,
    operator            TEXT,
    basin               TEXT,
    target_formation    TEXT,
    rig                 TEXT,
    distance_miles      REAL,
    hole_depth_ft       REAL,
    section             TEXT,
    hole_diameter       REAL,
    mud_type            TEXT,
    mud_density         TEXT,
    bit_size            TEXT,
    bit_type            TEXT,
    state               TEXT,
    spud_date           TEXT,
    lat                 REAL,
    lon                 REAL,
    string_design       TEXT,
    well_state          TEXT
);
CREATE INDEX IF NOT EXISTS idx_ow_run ON offset_wells(run_id);
CREATE INDEX IF NOT EXISTS idx_ow_asset ON offset_wells(asset_id);

-- BHA runs from offset wells
CREATE TABLE IF NOT EXISTS bha_runs (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id                  INTEGER NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    asset_id                TEXT NOT NULL,
    well_name               TEXT,
    operator                TEXT,
    distance_miles          REAL,
    section_type            TEXT,
    bha_number              TEXT,
    start_depth             REAL,
    end_depth               REAL,
    run_length              REAL,
    section_start_depth     REAL,
    lateral_start_depth     REAL,
    set_date                TEXT,
    num_components          INTEGER,
    is_rss                  INTEGER DEFAULT 0,
    has_agitator            INTEGER DEFAULT 0,
    -- Bit fields
    bit_manufacturer        TEXT,
    bit_model               TEXT,
    bit_size                TEXT,
    bit_serial              TEXT,
    bit_tfa                 TEXT,
    bit_jets                TEXT,
    -- Parsed bit fields
    parsed_blades           TEXT,
    parsed_cutter_mm        TEXT,
    parse_confidence        TEXT,
    parse_method            TEXT,
    -- Motor fields
    motor_manufacturer      TEXT,
    motor_model             TEXT,
    motor_od                TEXT,
    motor_bend              TEXT,
    motor_rpg               TEXT,
    motor_lobe_config       TEXT,
    motor_rpg_band          TEXT,
    -- Grouping
    equiv_bha_key           TEXT,
    -- Section filtering results
    section_name            TEXT,
    hole_size_filter        REAL,
    formation_coverage      REAL,
    formations_covered      TEXT
);
CREATE INDEX IF NOT EXISTS idx_bha_run ON bha_runs(run_id);
CREATE INDEX IF NOT EXISTS idx_bha_asset ON bha_runs(asset_id);
CREATE INDEX IF NOT EXISTS idx_bha_section ON bha_runs(section_name);
CREATE INDEX IF NOT EXISTS idx_bha_equiv ON bha_runs(equiv_bha_key);

-- Formation tops (raw and canonical)
CREATE TABLE IF NOT EXISTS formation_tops (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id            TEXT NOT NULL,
    well_name           TEXT,
    formation_name      TEXT NOT NULL,
    canonical_name      TEXT,
    md_top              REAL,
    tvd_top             REAL,
    md_thickness        REAL,
    tvd_thickness       REAL,
    lithology           TEXT,
    is_canonical        INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_ft_asset ON formation_tops(asset_id);
CREATE INDEX IF NOT EXISTS idx_ft_canonical ON formation_tops(canonical_name);

-- Canonical formation mappings (replaces canonical_map.json)
CREATE TABLE IF NOT EXISTS canonical_formations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id              INTEGER REFERENCES analysis_runs(id) ON DELETE CASCADE,
    canonical_name      TEXT NOT NULL,
    display_order       INTEGER,
    target_tvd_top      REAL,
    target_tvd_bottom   REAL
);
CREATE INDEX IF NOT EXISTS idx_cf_run ON canonical_formations(run_id);

CREATE TABLE IF NOT EXISTS canonical_sub_formations (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_formation_id      INTEGER REFERENCES canonical_formations(id) ON DELETE CASCADE,
    sub_formation_name          TEXT NOT NULL
);

-- Target well sections (replaces target_sections.json)
CREATE TABLE IF NOT EXISTS target_sections (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id              INTEGER NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    name                TEXT NOT NULL,
    hole_size           REAL,
    mode                TEXT DEFAULT 'vertical',
    top_md              REAL,
    bottom_md           REAL,
    section_length      REAL,
    top_tvd             REAL,
    bottom_tvd          REAL,
    start_formation     TEXT,
    end_formation       TEXT,
    formations_json     TEXT
);
CREATE INDEX IF NOT EXISTS idx_ts_run ON target_sections(run_id);

-- Equivalent BHA group summaries
CREATE TABLE IF NOT EXISTS equiv_bha_groups (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id              INTEGER REFERENCES analysis_runs(id) ON DELETE CASCADE,
    section_name        TEXT,
    group_key           TEXT NOT NULL,
    num_runs            INTEGER,
    num_wells           INTEGER,
    num_operators       INTEGER,
    operators           TEXT,
    avg_run_ft          REAL,
    min_run_ft          REAL,
    max_run_ft          REAL,
    total_ft            REAL,
    runs_with_agitator  INTEGER,
    runs_with_rss       INTEGER,
    bit_manufacturers   TEXT,
    bit_models_seen     TEXT,
    motor_models_seen   TEXT,
    avg_start_depth     REAL,
    avg_end_depth       REAL
);
CREATE INDEX IF NOT EXISTS idx_eg_run ON equiv_bha_groups(run_id);

-- TTD rankings
CREATE TABLE IF NOT EXISTS ttd_rankings (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id              INTEGER REFERENCES analysis_runs(id) ON DELETE CASCADE,
    section_name        TEXT,
    group_key           TEXT,
    num_runs            INTEGER,
    num_wells           INTEGER,
    target_length       REAL,
    expected_slide_pct  REAL,
    ttd_hours           REAL,
    ttd_days            REAL,
    bins_with_data      INTEGER,
    bins_missing        INTEGER
);
CREATE INDEX IF NOT EXISTS idx_ttd_run ON ttd_rankings(run_id);

-- Asset IDs cache (avoids re-paginating the platform API)
CREATE TABLE IF NOT EXISTS asset_ids_cache (
    asset_id            INTEGER PRIMARY KEY,
    fetched_at          TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_aic_fetched ON asset_ids_cache(fetched_at);

-- Well cache records (pre-extracted well info to avoid re-fetching well_cache)
CREATE TABLE IF NOT EXISTS well_cache_records (
    asset_id            TEXT PRIMARY KEY,
    well_name           TEXT,
    operator            TEXT,
    basin               TEXT,
    target_formation    TEXT,
    rig                 TEXT,
    distance_miles      REAL,
    hole_depth_ft       REAL,
    section             TEXT,
    hole_diameter       REAL,
    mud_type            TEXT,
    mud_density         TEXT,
    bit_size            TEXT,
    bit_type            TEXT,
    state               TEXT,
    spud_date           TEXT,
    lat                 REAL,
    lon                 REAL,
    string_design       TEXT,
    well_state          TEXT,
    fetched_at          TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_wcr_basin ON well_cache_records(basin);
CREATE INDEX IF NOT EXISTS idx_wcr_fetched ON well_cache_records(fetched_at);
CREATE INDEX IF NOT EXISTS idx_wcr_lat ON well_cache_records(lat);
CREATE INDEX IF NOT EXISTS idx_wcr_lon ON well_cache_records(lon);

-- Bit catalog (reference data)
CREATE TABLE IF NOT EXISTS bit_catalog (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    bit_manufacturer    TEXT,
    bit_model           TEXT,
    bit_diameters       TEXT,
    parsed_blades       TEXT,
    parsed_cutter_mm    TEXT,
    parse_confidence    TEXT,
    parse_method        TEXT,
    total_runs          INTEGER,
    operators           TEXT,
    sources             TEXT,
    UNIQUE(bit_manufacturer, bit_model)
);
"""

# ── Connection Management ──

def _get_conn() -> sqlite3.Connection:
    """Get a connection with dict-like row access and WAL mode."""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def connection():
    """Context manager for database connections."""
    conn = _get_conn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create all tables and indexes if they don't exist."""
    with connection() as conn:
        conn.executescript(_SCHEMA_SQL)
    print(f"  DB initialized: {DB_PATH}")


# Auto-initialize on import
init_db()


# ── Helpers ──

def _row_to_dict(row: sqlite3.Row | None) -> dict | None:
    """Convert a sqlite3.Row to a plain dict."""
    if row is None:
        return None
    return dict(row)


def _rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    """Convert a list of sqlite3.Row to list of dicts."""
    return [dict(r) for r in rows]


def _safe_float(val, default=None):
    """Convert to float, returning default on failure."""
    if val is None or val == "" or val == "N/A":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _safe_int(val, default=None):
    """Convert to int, returning default on failure."""
    if val is None or val == "" or val == "N/A":
        return default
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


# ═══════════════════════════════════════════════════════════════════
#  ANALYSIS RUNS
# ═══════════════════════════════════════════════════════════════════

def get_or_create_run(target_asset_id: str, radius: float = 15.0) -> int:
    """Get the most recent active run for this asset+radius, or create one.

    Returns the run_id.
    """
    with connection() as conn:
        row = conn.execute(
            """SELECT id FROM analysis_runs
               WHERE target_asset_id = ? AND search_radius = ? AND status = 'active'
               ORDER BY created_at DESC LIMIT 1""",
            (str(target_asset_id), radius),
        ).fetchone()
        if row:
            return row["id"]
        cur = conn.execute(
            """INSERT INTO analysis_runs (target_asset_id, search_radius)
               VALUES (?, ?)""",
            (str(target_asset_id), radius),
        )
        return cur.lastrowid


def get_current_run(target_asset_id: str) -> dict | None:
    """Get the most recent analysis run for an asset (any radius)."""
    with connection() as conn:
        row = conn.execute(
            """SELECT * FROM analysis_runs
               WHERE target_asset_id = ? AND status = 'active'
               ORDER BY created_at DESC LIMIT 1""",
            (str(target_asset_id),),
        ).fetchone()
        return _row_to_dict(row)


def get_latest_run() -> dict | None:
    """Get the most recent analysis run across all assets."""
    with connection() as conn:
        row = conn.execute(
            """SELECT * FROM analysis_runs
               WHERE status = 'active'
               ORDER BY created_at DESC LIMIT 1""",
        ).fetchone()
        return _row_to_dict(row)


def deactivate_runs(target_asset_id: str):
    """Mark all runs for an asset as inactive (when re-analyzing)."""
    with connection() as conn:
        conn.execute(
            """UPDATE analysis_runs SET status = 'inactive'
               WHERE target_asset_id = ?""",
            (str(target_asset_id),),
        )


# ═══════════════════════════════════════════════════════════════════
#  OFFSET WELLS
# ═══════════════════════════════════════════════════════════════════

_OW_COLUMNS = [
    "asset_id", "well_name", "operator", "basin", "target_formation",
    "rig", "distance_miles", "hole_depth_ft", "section", "hole_diameter",
    "mud_type", "mud_density", "bit_size", "bit_type", "state",
    "spud_date", "lat", "lon", "string_design", "well_state",
]


def save_offset_wells(run_id: int, wells: list[dict]):
    """Bulk insert offset wells for an analysis run.

    Clears any existing wells for this run first.
    """
    with connection() as conn:
        conn.execute("DELETE FROM offset_wells WHERE run_id = ?", (run_id,))
        for w in wells:
            conn.execute(
                f"""INSERT INTO offset_wells (run_id, {', '.join(_OW_COLUMNS)})
                    VALUES (?, {', '.join('?' for _ in _OW_COLUMNS)})""",
                (run_id, *[w.get(c) for c in _OW_COLUMNS]),
            )
    print(f"  DB: Saved {len(wells)} offset wells (run {run_id})")


def get_offset_wells(run_id: int) -> list[dict]:
    """Get all offset wells for a run."""
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM offset_wells WHERE run_id = ? ORDER BY distance_miles",
            (run_id,),
        ).fetchall()
        return _rows_to_dicts(rows)


def get_offset_filter_options(run_id: int) -> dict:
    """Return distinct basin and target_formation values for a run's offset wells."""
    with connection() as conn:
        basins = [
            r[0] for r in conn.execute(
                "SELECT DISTINCT basin FROM offset_wells "
                "WHERE run_id = ? AND basin IS NOT NULL AND basin != 'N/A' "
                "ORDER BY basin", (run_id,),
            ).fetchall()
        ]
        formations = [
            r[0] for r in conn.execute(
                "SELECT DISTINCT target_formation FROM offset_wells "
                "WHERE run_id = ? AND target_formation IS NOT NULL "
                "AND target_formation != 'N/A' "
                "ORDER BY target_formation", (run_id,),
            ).fetchall()
        ]
        return {"basins": basins, "target_formations": formations}


def count_offset_wells(run_id: int) -> int:
    """Quick count of offset wells."""
    with connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM offset_wells WHERE run_id = ?",
            (run_id,),
        ).fetchone()
        return row["cnt"]


# ═══════════════════════════════════════════════════════════════════
#  BHA RUNS
# ═══════════════════════════════════════════════════════════════════

_BHA_COLUMNS = [
    "asset_id", "well_name", "operator", "distance_miles",
    "section_type", "bha_number", "start_depth", "end_depth",
    "run_length", "section_start_depth", "lateral_start_depth",
    "set_date", "num_components", "is_rss", "has_agitator",
    "bit_manufacturer", "bit_model", "bit_size", "bit_serial",
    "bit_tfa", "bit_jets",
    "parsed_blades", "parsed_cutter_mm", "parse_confidence", "parse_method",
    "motor_manufacturer", "motor_model", "motor_od", "motor_bend",
    "motor_rpg", "motor_lobe_config", "motor_rpg_band",
    "equiv_bha_key",
    "section_name", "hole_size_filter", "formation_coverage",
    "formations_covered",
]


def save_bha_runs(run_id: int, runs: list[dict], replace: bool = True):
    """Bulk insert BHA runs for an analysis run.

    If replace=True, clears existing runs for this run_id first.
    """
    with connection() as conn:
        if replace:
            conn.execute("DELETE FROM bha_runs WHERE run_id = ?", (run_id,))
        for r in runs:
            vals = []
            for c in _BHA_COLUMNS:
                v = r.get(c)
                if c in ("distance_miles", "start_depth", "end_depth",
                         "run_length", "section_start_depth",
                         "lateral_start_depth", "hole_size_filter",
                         "formation_coverage"):
                    v = _safe_float(v)
                elif c in ("num_components", "is_rss", "has_agitator"):
                    v = _safe_int(v, 0)
                vals.append(v)
            conn.execute(
                f"""INSERT INTO bha_runs (run_id, {', '.join(_BHA_COLUMNS)})
                    VALUES (?, {', '.join('?' for _ in _BHA_COLUMNS)})""",
                (run_id, *vals),
            )
    print(f"  DB: Saved {len(runs)} BHA runs (run {run_id})")


def get_bha_runs(run_id: int, section_name: str | None = None,
                 asset_id: str | None = None) -> list[dict]:
    """Get BHA runs with optional filters."""
    with connection() as conn:
        sql = "SELECT * FROM bha_runs WHERE run_id = ?"
        params: list[Any] = [run_id]
        if section_name:
            sql += " AND section_name = ?"
            params.append(section_name)
        if asset_id:
            sql += " AND asset_id = ?"
            params.append(asset_id)
        sql += " ORDER BY asset_id, bha_number"
        rows = conn.execute(sql, params).fetchall()
        return _rows_to_dicts(rows)


def get_bha_runs_df(run_id: int, section_name: str | None = None) -> pd.DataFrame:
    """Get BHA runs as a DataFrame."""
    conn = _get_conn()
    sql = "SELECT * FROM bha_runs WHERE run_id = ?"
    params: list[Any] = [run_id]
    if section_name:
        sql += " AND section_name = ?"
        params.append(section_name)
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df


def update_bha_parsed_fields(run_id: int, bha_id: int, fields: dict):
    """Update parsed bit/motor fields on a single BHA run."""
    with connection() as conn:
        sets = ", ".join(f"{k} = ?" for k in fields.keys())
        conn.execute(
            f"UPDATE bha_runs SET {sets} WHERE id = ? AND run_id = ?",
            (*fields.values(), bha_id, run_id),
        )


def update_bha_equiv_keys(run_id: int, updates: list[tuple[str, str, str]]):
    """Bulk update equiv_bha_key by (asset_id, bha_number) -> key.

    updates: list of (asset_id, bha_number, equiv_bha_key)
    """
    with connection() as conn:
        for asset_id, bha_number, key in updates:
            conn.execute(
                """UPDATE bha_runs SET equiv_bha_key = ?
                   WHERE run_id = ? AND asset_id = ? AND bha_number = ?""",
                (key, run_id, asset_id, str(bha_number)),
            )


def update_bha_section_filter(run_id: int, bha_db_id: int,
                               section_name: str, hole_size: float,
                               coverage: float, formations: str):
    """Mark a BHA run as filtered into a specific section."""
    with connection() as conn:
        conn.execute(
            """UPDATE bha_runs
               SET section_name = ?, hole_size_filter = ?,
                   formation_coverage = ?, formations_covered = ?
               WHERE id = ? AND run_id = ?""",
            (section_name, hole_size, coverage, formations, bha_db_id, run_id),
        )


def get_section_bha_summary(run_id: int, section_name: str) -> list[dict]:
    """Get unique wells with run counts for a section (for the offset-wells endpoint)."""
    with connection() as conn:
        rows = conn.execute(
            """SELECT asset_id, well_name, operator,
                      MIN(distance_miles) as distance_miles,
                      COUNT(DISTINCT bha_number) as runs
               FROM bha_runs
               WHERE run_id = ? AND section_name = ?
               GROUP BY asset_id
               ORDER BY distance_miles""",
            (run_id, section_name),
        ).fetchall()
        return _rows_to_dicts(rows)


def get_all_bha_well_summary(run_id: int) -> list[dict]:
    """Get unique wells with run counts across all BHA runs (fallback for offset-wells)."""
    with connection() as conn:
        rows = conn.execute(
            """SELECT asset_id, well_name, operator,
                      MIN(distance_miles) as distance_miles,
                      COUNT(*) as runs
               FROM bha_runs
               WHERE run_id = ?
               GROUP BY asset_id
               ORDER BY distance_miles""",
            (run_id,),
        ).fetchall()
        return _rows_to_dicts(rows)


# ═══════════════════════════════════════════════════════════════════
#  FORMATION TOPS
# ═══════════════════════════════════════════════════════════════════

def save_formation_tops(tops: list[dict], replace_asset: str | None = None):
    """Save formation tops. If replace_asset is set, clears that asset first."""
    with connection() as conn:
        if replace_asset:
            conn.execute(
                "DELETE FROM formation_tops WHERE asset_id = ?",
                (str(replace_asset),),
            )
        for t in tops:
            conn.execute(
                """INSERT INTO formation_tops
                   (asset_id, well_name, formation_name, md_top, tvd_top,
                    md_thickness, tvd_thickness, lithology)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(t.get("asset_id", "")),
                    t.get("well_name"),
                    t.get("formation_name", ""),
                    _safe_float(t.get("md_top")),
                    _safe_float(t.get("tvd_top")),
                    _safe_float(t.get("md_thickness")),
                    _safe_float(t.get("tvd_thickness")),
                    t.get("lithology"),
                ),
            )
    n_assets = len(set(str(t.get("asset_id", "")) for t in tops))
    print(f"  DB: Saved {len(tops)} formation tops ({n_assets} wells)")


def get_formation_tops(asset_id: str, canonical_only: bool = False) -> list[dict]:
    """Get formation tops for a specific well."""
    with connection() as conn:
        sql = "SELECT * FROM formation_tops WHERE asset_id = ?"
        params: list[Any] = [str(asset_id)]
        if canonical_only:
            sql += " AND is_canonical = 1"
        sql += " ORDER BY md_top"
        rows = conn.execute(sql, params).fetchall()
        return _rows_to_dicts(rows)


def get_all_formation_tops() -> list[dict]:
    """Get all formation tops (all wells)."""
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM formation_tops ORDER BY asset_id, md_top"
        ).fetchall()
        return _rows_to_dicts(rows)


def formation_tops_exist(asset_id: str) -> bool:
    """Quick check if formation data exists for an asset."""
    with connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM formation_tops WHERE asset_id = ? LIMIT 1",
            (str(asset_id),),
        ).fetchone()
        return row is not None


def update_canonical_names(mapping: dict[str, str], asset_id: str | None = None):
    """Update canonical_name on formation_tops based on a mapping.

    mapping: {original_name: canonical_name}
    """
    with connection() as conn:
        for orig, canonical in mapping.items():
            sql = "UPDATE formation_tops SET canonical_name = ?, is_canonical = 1 WHERE formation_name = ?"
            params: list[Any] = [canonical, orig]
            if asset_id:
                sql += " AND asset_id = ?"
                params.append(str(asset_id))
            conn.execute(sql, params)


# ═══════════════════════════════════════════════════════════════════
#  CANONICAL FORMATIONS
# ═══════════════════════════════════════════════════════════════════

def save_canonical_formations(run_id: int, formations: list[dict]):
    """Save canonical formation mappings.

    Each dict: {canonical_name, order, target_tvd_top, target_tvd_bottom, sub_formations: [str]}
    """
    with connection() as conn:
        conn.execute("DELETE FROM canonical_formations WHERE run_id = ?", (run_id,))
        for fm in formations:
            cur = conn.execute(
                """INSERT INTO canonical_formations
                   (run_id, canonical_name, display_order, target_tvd_top, target_tvd_bottom)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    run_id,
                    fm.get("canonical_name", ""),
                    fm.get("order", 0),
                    _safe_float(fm.get("target_tvd_top")),
                    _safe_float(fm.get("target_tvd_bottom")),
                ),
            )
            cf_id = cur.lastrowid
            for sub in fm.get("sub_formations", fm.get("target_sub_formations", [])):
                conn.execute(
                    """INSERT INTO canonical_sub_formations
                       (canonical_formation_id, sub_formation_name)
                       VALUES (?, ?)""",
                    (cf_id, sub),
                )
    print(f"  DB: Saved {len(formations)} canonical formations (run {run_id})")


def get_canonical_formations(run_id: int, tvd_top: float | None = None,
                              tvd_bottom: float | None = None) -> list[dict]:
    """Get canonical formations with sub-formation names."""
    with connection() as conn:
        sql = "SELECT * FROM canonical_formations WHERE run_id = ?"
        params: list[Any] = [run_id]
        if tvd_top is not None:
            sql += " AND (target_tvd_bottom IS NULL OR target_tvd_bottom >= ?)"
            params.append(tvd_top)
        if tvd_bottom is not None:
            sql += " AND (target_tvd_top IS NULL OR target_tvd_top <= ?)"
            params.append(tvd_bottom)
        sql += " ORDER BY display_order"
        formations = conn.execute(sql, params).fetchall()

        result = []
        for fm in formations:
            fm_dict = dict(fm)
            subs = conn.execute(
                """SELECT sub_formation_name FROM canonical_sub_formations
                   WHERE canonical_formation_id = ? ORDER BY id""",
                (fm["id"],),
            ).fetchall()
            fm_dict["sub_formations"] = [s["sub_formation_name"] for s in subs]
            result.append(fm_dict)
        return result


# ═══════════════════════════════════════════════════════════════════
#  TARGET SECTIONS
# ═══════════════════════════════════════════════════════════════════

def save_target_sections(run_id: int, sections: list[dict]):
    """Save target well sections."""
    with connection() as conn:
        conn.execute("DELETE FROM target_sections WHERE run_id = ?", (run_id,))
        for s in sections:
            fms = s.get("formations_in_section", [])
            conn.execute(
                """INSERT INTO target_sections
                   (run_id, name, hole_size, mode, top_md, bottom_md,
                    section_length, top_tvd, bottom_tvd,
                    start_formation, end_formation, formations_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    run_id,
                    s.get("name", "Unknown"),
                    _safe_float(s.get("hole_size")),
                    s.get("mode", "vertical"),
                    _safe_float(s.get("top_md")),
                    _safe_float(s.get("bottom_md")),
                    _safe_float(s.get("section_length_md", s.get("section_length"))),
                    _safe_float(s.get("top_tvd")),
                    _safe_float(s.get("bottom_tvd")),
                    s.get("start_formation"),
                    s.get("end_formation"),
                    json.dumps(fms) if fms else None,
                ),
            )
    print(f"  DB: Saved {len(sections)} target sections (run {run_id})")


def get_target_sections(run_id: int) -> list[dict]:
    """Get target sections for a run."""
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM target_sections WHERE run_id = ? ORDER BY top_md",
            (run_id,),
        ).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            if d.get("formations_json"):
                d["formations_in_section"] = json.loads(d["formations_json"])
            else:
                d["formations_in_section"] = []
            result.append(d)
        return result


# ═══════════════════════════════════════════════════════════════════
#  EQUIV BHA GROUPS
# ═══════════════════════════════════════════════════════════════════

_EG_COLUMNS = [
    "section_name", "group_key", "num_runs", "num_wells", "num_operators",
    "operators", "avg_run_ft", "min_run_ft", "max_run_ft", "total_ft",
    "runs_with_agitator", "runs_with_rss", "bit_manufacturers",
    "bit_models_seen", "motor_models_seen", "avg_start_depth", "avg_end_depth",
]


def save_equiv_bha_groups(run_id: int, section_name: str, groups: list[dict]):
    """Save equivalent BHA group summaries."""
    with connection() as conn:
        conn.execute(
            "DELETE FROM equiv_bha_groups WHERE run_id = ? AND section_name = ?",
            (run_id, section_name),
        )
        for g in groups:
            g_copy = dict(g)
            g_copy["section_name"] = section_name
            conn.execute(
                f"""INSERT INTO equiv_bha_groups (run_id, {', '.join(_EG_COLUMNS)})
                    VALUES (?, {', '.join('?' for _ in _EG_COLUMNS)})""",
                (run_id, *[g_copy.get(c) for c in _EG_COLUMNS]),
            )
    print(f"  DB: Saved {len(groups)} equiv BHA groups for {section_name}")


def get_equiv_bha_groups(run_id: int, section_name: str) -> list[dict]:
    """Get equiv BHA groups for a section."""
    with connection() as conn:
        rows = conn.execute(
            """SELECT * FROM equiv_bha_groups
               WHERE run_id = ? AND section_name = ?
               ORDER BY num_runs DESC""",
            (run_id, section_name),
        ).fetchall()
        return _rows_to_dicts(rows)


# ═══════════════════════════════════════════════════════════════════
#  TTD RANKINGS
# ═══════════════════════════════════════════════════════════════════

def save_ttd_rankings(run_id: int, section_name: str, rankings: list[dict]):
    """Save TTD ranking results."""
    with connection() as conn:
        conn.execute(
            "DELETE FROM ttd_rankings WHERE run_id = ? AND section_name = ?",
            (run_id, section_name),
        )
        for r in rankings:
            conn.execute(
                """INSERT INTO ttd_rankings
                   (run_id, section_name, group_key, num_runs, num_wells,
                    target_length, expected_slide_pct, ttd_hours, ttd_days,
                    bins_with_data, bins_missing)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    run_id, section_name,
                    r.get("group_key"),
                    _safe_int(r.get("num_runs")),
                    _safe_int(r.get("num_wells")),
                    _safe_float(r.get("target_lateral_ft", r.get("target_section_ft", r.get("target_length")))),
                    _safe_float(r.get("expected_slide_pct")),
                    _safe_float(r.get("ttd_hours")),
                    _safe_float(r.get("ttd_days")),
                    _safe_int(r.get("bins_with_data", r.get("segments_with_data"))),
                    _safe_int(r.get("bins_missing", r.get("segments_missing"))),
                ),
            )
    print(f"  DB: Saved {len(rankings)} TTD rankings for {section_name}")


def get_ttd_rankings(run_id: int, section_name: str) -> list[dict]:
    """Get TTD rankings for a section."""
    with connection() as conn:
        rows = conn.execute(
            """SELECT * FROM ttd_rankings
               WHERE run_id = ? AND section_name = ?
               ORDER BY ttd_hours""",
            (run_id, section_name),
        ).fetchall()
        return _rows_to_dicts(rows)


# ═══════════════════════════════════════════════════════════════════
#  BIT CATALOG
# ═══════════════════════════════════════════════════════════════════

def save_bit_catalog(entries: list[dict]):
    """Save/update the bit catalog (upsert by manufacturer+model)."""
    with connection() as conn:
        for e in entries:
            conn.execute(
                """INSERT INTO bit_catalog
                   (bit_manufacturer, bit_model, bit_diameters, parsed_blades,
                    parsed_cutter_mm, parse_confidence, parse_method,
                    total_runs, operators, sources)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(bit_manufacturer, bit_model) DO UPDATE SET
                    bit_diameters = excluded.bit_diameters,
                    parsed_blades = excluded.parsed_blades,
                    parsed_cutter_mm = excluded.parsed_cutter_mm,
                    parse_confidence = excluded.parse_confidence,
                    total_runs = excluded.total_runs,
                    operators = excluded.operators,
                    sources = excluded.sources""",
                (
                    e.get("bit_manufacturer"),
                    e.get("bit_model"),
                    e.get("bit_diameters"),
                    e.get("parsed_blades"),
                    e.get("parsed_cutter_mm"),
                    e.get("parse_confidence"),
                    e.get("parse_method"),
                    _safe_int(e.get("total_runs")),
                    e.get("operators"),
                    e.get("sources"),
                ),
            )
    print(f"  DB: Saved {len(entries)} bit catalog entries")


def get_bit_catalog() -> list[dict]:
    """Get the full bit catalog."""
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM bit_catalog ORDER BY total_runs DESC"
        ).fetchall()
        return _rows_to_dicts(rows)


# ═══════════════════════════════════════════════════════════════════
#  WELL CACHE (Asset IDs + Well Info Cache for Offset Finder)
# ═══════════════════════════════════════════════════════════════════

_WELL_CACHE_COLUMNS = [
    "asset_id", "well_name", "operator", "basin", "target_formation",
    "rig", "distance_miles", "hole_depth_ft", "section", "hole_diameter",
    "mud_type", "mud_density", "bit_size", "bit_type", "state",
    "spud_date", "lat", "lon", "string_design", "well_state",
]


def get_cached_asset_ids(max_age_seconds: int = 3600) -> list[int] | None:
    """Return cached asset IDs if the cache is fresh enough, else None.

    Args:
        max_age_seconds: Maximum age in seconds (default 1 hour).
    """
    with connection() as conn:
        row = conn.execute(
            """SELECT MIN(fetched_at) as oldest, COUNT(*) as cnt
               FROM asset_ids_cache"""
        ).fetchone()
        if not row or row["cnt"] == 0:
            return None
        oldest = row["oldest"]
        if not oldest:
            return None
        # Parse the datetime string and compare
        try:
            fetched_dt = datetime.fromisoformat(oldest)
        except ValueError:
            fetched_dt = datetime.strptime(oldest, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        age = (now - fetched_dt).total_seconds()
        if age > max_age_seconds:
            return None
        rows = conn.execute("SELECT asset_id FROM asset_ids_cache").fetchall()
        return [r["asset_id"] for r in rows]


def save_asset_ids_cache(asset_ids: list[int]):
    """Replace the asset ID cache with a fresh set."""
    with connection() as conn:
        conn.execute("DELETE FROM asset_ids_cache")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.executemany(
            "INSERT OR REPLACE INTO asset_ids_cache (asset_id, fetched_at) VALUES (?, ?)",
            [(aid, now_str) for aid in asset_ids],
        )
    print(f"  DB cache: Saved {len(asset_ids)} asset IDs")


def get_cached_well_records() -> list[dict]:
    """Return all cached well info records."""
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM well_cache_records"
        ).fetchall()
        return _rows_to_dicts(rows)


def get_cached_wells_near(lat: float, lon: float, radius_miles: float) -> list[dict]:
    """Return cached wells within a bounding box around the target location.

    Uses a generous bounding box (1.2x radius) to avoid missing wells
    near the corners. Actual haversine distance check is done in Python.
    """
    import math
    margin = 1.2
    lat_delta = (radius_miles * margin) / 69.0
    lon_delta = (radius_miles * margin) / (69.0 * math.cos(math.radians(lat)))

    with connection() as conn:
        rows = conn.execute(
            """SELECT * FROM well_cache_records
               WHERE lat BETWEEN ? AND ?
                 AND lon BETWEEN ? AND ?
                 AND lat IS NOT NULL AND lon IS NOT NULL""",
            (lat - lat_delta, lat + lat_delta,
             lon - lon_delta, lon + lon_delta),
        ).fetchall()
        return _rows_to_dicts(rows)


def get_cached_well_asset_ids() -> set[str]:
    """Return the set of asset IDs that are already cached in well_cache_records."""
    with connection() as conn:
        rows = conn.execute(
            "SELECT asset_id FROM well_cache_records"
        ).fetchall()
        return {str(r["asset_id"]) for r in rows}


def get_target_asset_formation(asset_id: str) -> str | None:
    """Return the cached target formation for the given target asset."""
    with connection() as conn:
        row = conn.execute(
            """SELECT target_formation
               FROM well_cache_records
               WHERE asset_id = ?
                 AND target_formation IS NOT NULL
                 AND target_formation != 'N/A'
               LIMIT 1""",
            (str(asset_id),),
        ).fetchone()
        if not row:
            return None
        val = row["target_formation"]
        if val is None:
            return None
        sval = str(val).strip()
        return sval if sval else None


_WCR_FLOAT_COLS = {"distance_miles", "hole_depth_ft", "hole_diameter", "lat", "lon"}


def save_well_cache_records(records: list[dict]):
    """Upsert well info records into the cache.

    Each record is a dict with keys matching _WELL_CACHE_COLUMNS.
    Numeric fields are coerced via _safe_float to avoid storing "N/A" strings.
    """
    if not records:
        return
    with connection() as conn:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cols = _WELL_CACHE_COLUMNS + ["fetched_at"]
        placeholders = ", ".join("?" for _ in cols)
        col_names = ", ".join(cols)
        for r in records:
            vals = []
            for c in _WELL_CACHE_COLUMNS:
                v = r.get(c)
                if c in _WCR_FLOAT_COLS:
                    v = _safe_float(v)
                elif v == "N/A":
                    v = None
                vals.append(v)
            vals.append(now_str)
            conn.execute(
                f"INSERT OR REPLACE INTO well_cache_records ({col_names}) VALUES ({placeholders})",
                vals,
            )
    print(f"  DB cache: Saved {len(records)} well cache records")


def count_well_cache_records() -> int:
    """Quick count of cached well records."""
    with connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM well_cache_records"
        ).fetchone()
        return row["cnt"]


def clear_well_cache():
    """Clear both caches (for testing or forced refresh)."""
    with connection() as conn:
        conn.execute("DELETE FROM asset_ids_cache")
        conn.execute("DELETE FROM well_cache_records")
    print("  DB cache: Cleared asset IDs and well cache records")


# ═══════════════════════════════════════════════════════════════════
#  PARQUET - Helpers
# ═══════════════════════════════════════════════════════════════════

def _parquet_path(name: str) -> str:
    """Get the path for a Parquet file in the data directory."""
    return os.path.join(DATA_DIR, f"{name}.parquet")


def _run_prefix(run_id: int | None) -> str:
    """Return 'run{N}_' prefix if run_id given, else '' for legacy compat."""
    if run_id is None:
        return ""
    return f"run{run_id}_"


def _resolve_run_id(run_id: int | None) -> int | None:
    """If run_id is None, try to resolve from latest run."""
    if run_id is not None:
        return run_id
    latest = get_latest_run()
    return latest["id"] if latest else None


# ═══════════════════════════════════════════════════════════════════
#  PARQUET - 1FT DATA (Heavy Analytical)
# ═══════════════════════════════════════════════════════════════════

def save_1ft_data(section_name: str, df: pd.DataFrame, mode: str = "lateral",
                  run_id: int | None = None):
    """Save 1ft drilling data as Parquet, scoped by run_id.

    Args:
        section_name: Safe section name (e.g. "Production_Vertical")
        df: DataFrame with 1ft data
        mode: "lateral" or "vertical" (affects filename)
        run_id: Analysis run ID (included in filename to prevent cross-well contamination)
    """
    rid = _resolve_run_id(run_id)
    suffix = "_vertical" if mode == "vertical" else ""
    path = _parquet_path(f"{_run_prefix(rid)}rop_1ft_{section_name}{suffix}")
    df.to_parquet(path, index=False, compression="snappy")
    size_mb = os.path.getsize(path) / 1024 / 1024
    print(f"  Parquet: Saved {len(df)} rows to {os.path.basename(path)} "
          f"({size_mb:.1f} MB)")


def load_1ft_data(section_name: str, mode: str = "lateral",
                  columns: list[str] | None = None,
                  run_id: int | None = None) -> pd.DataFrame:
    """Load 1ft data from Parquet.

    Args:
        section_name: Safe section name
        mode: "lateral" or "vertical"
        columns: Optional list of columns to load (for speed)
        run_id: Analysis run ID
    """
    rid = _resolve_run_id(run_id)
    suffix = "_vertical" if mode == "vertical" else ""
    path = _parquet_path(f"{_run_prefix(rid)}rop_1ft_{section_name}{suffix}")
    if not os.path.exists(path):
        # Fallback to legacy (unscoped) filename
        legacy = _parquet_path(f"rop_1ft_{section_name}{suffix}")
        if os.path.exists(legacy):
            return pd.read_parquet(legacy, columns=columns)
        return pd.DataFrame()
    return pd.read_parquet(path, columns=columns)


def has_1ft_data(section_name: str, mode: str = "lateral",
                 run_id: int | None = None) -> bool:
    """Check if 1ft Parquet file exists."""
    rid = _resolve_run_id(run_id)
    suffix = "_vertical" if mode == "vertical" else ""
    path = _parquet_path(f"{_run_prefix(rid)}rop_1ft_{section_name}{suffix}")
    if os.path.exists(path):
        return True
    # Fallback to legacy
    return os.path.exists(_parquet_path(f"rop_1ft_{section_name}{suffix}"))


# ═══════════════════════════════════════════════════════════════════
#  PARQUET - ROP CURVES
# ═══════════════════════════════════════════════════════════════════

def save_rop_curves_per_run(section_name: str, df: pd.DataFrame,
                             mode: str = "lateral", run_id: int | None = None):
    """Save per-run ROP curves as Parquet, scoped by run_id."""
    rid = _resolve_run_id(run_id)
    suffix = "_vertical" if mode == "vertical" else ""
    path = _parquet_path(f"{_run_prefix(rid)}rop_curves_per_run_{section_name}{suffix}")
    df.to_parquet(path, index=False, compression="snappy")
    print(f"  Parquet: Saved {len(df)} per-run curve rows to {os.path.basename(path)}")


def save_rop_curves_by_group(section_name: str, df: pd.DataFrame,
                              mode: str = "lateral", run_id: int | None = None):
    """Save group-level P10/P50/P90 curves as Parquet, scoped by run_id."""
    rid = _resolve_run_id(run_id)
    suffix = "_vertical" if mode == "vertical" else ""
    path = _parquet_path(f"{_run_prefix(rid)}rop_curves_by_group_{section_name}{suffix}")
    df.to_parquet(path, index=False, compression="snappy")
    print(f"  Parquet: Saved {len(df)} group curve rows to {os.path.basename(path)}")


def load_rop_curves_per_run(section_name: str, mode: str = "lateral",
                             columns: list[str] | None = None,
                             run_id: int | None = None) -> pd.DataFrame:
    """Load per-run ROP curves, scoped by run_id."""
    rid = _resolve_run_id(run_id)
    suffix = "_vertical" if mode == "vertical" else ""
    path = _parquet_path(f"{_run_prefix(rid)}rop_curves_per_run_{section_name}{suffix}")
    if not os.path.exists(path):
        legacy = _parquet_path(f"rop_curves_per_run_{section_name}{suffix}")
        if os.path.exists(legacy):
            return pd.read_parquet(legacy, columns=columns)
        return pd.DataFrame()
    return pd.read_parquet(path, columns=columns)


def load_rop_curves_by_group(section_name: str, mode: str = "lateral",
                              columns: list[str] | None = None,
                              run_id: int | None = None) -> pd.DataFrame:
    """Load group-level ROP curves, scoped by run_id."""
    rid = _resolve_run_id(run_id)
    suffix = "_vertical" if mode == "vertical" else ""
    path = _parquet_path(f"{_run_prefix(rid)}rop_curves_by_group_{section_name}{suffix}")
    if not os.path.exists(path):
        legacy = _parquet_path(f"rop_curves_by_group_{section_name}{suffix}")
        if os.path.exists(legacy):
            return pd.read_parquet(legacy, columns=columns)
        return pd.DataFrame()
    return pd.read_parquet(path, columns=columns)


# ═══════════════════════════════════════════════════════════════════
#  PARQUET - FULL BIT SCAN
# ═══════════════════════════════════════════════════════════════════

def save_bit_scan(df: pd.DataFrame):
    """Save full bit scan results as Parquet."""
    path = _parquet_path("full_bit_scan")
    df.to_parquet(path, index=False, compression="snappy")
    size_mb = os.path.getsize(path) / 1024 / 1024
    print(f"  Parquet: Saved {len(df)} bit scan rows ({size_mb:.1f} MB)")


def load_bit_scan(columns: list[str] | None = None) -> pd.DataFrame:
    """Load full bit scan."""
    path = _parquet_path("full_bit_scan")
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_parquet(path, columns=columns)


# ═══════════════════════════════════════════════════════════════════
#  CSV EXPORT (Debug)
# ═══════════════════════════════════════════════════════════════════

def export_csv(data, name: str, quiet: bool = False):
    """Dump data to exports/ as CSV for debugging.

    Args:
        data: list[dict], pd.DataFrame, or sqlite3 table name (str)
        name: Output filename (without .csv)
        quiet: Suppress print message
    """
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{name}.csv")

    if isinstance(data, pd.DataFrame):
        data.to_csv(path, index=False)
    elif isinstance(data, list):
        if not data:
            return
        if isinstance(data[0], dict):
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=data[0].keys(),
                                   extrasaction="ignore")
                w.writeheader()
                w.writerows(data)
        else:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerows(data)
    elif isinstance(data, str):
        conn = _get_conn()
        df = pd.read_sql_query(f"SELECT * FROM {data}", conn)
        df.to_csv(path, index=False)
        conn.close()
    else:
        raise TypeError(f"Cannot export {type(data)}")

    if not quiet:
        print(f"  CSV export: {path}")


def export_table(table_name: str, name: str | None = None):
    """Export an entire SQLite table to CSV."""
    export_csv(table_name, name or table_name)


# ═══════════════════════════════════════════════════════════════════
#  LEGACY CSV IMPORT (One-time migration helpers)
# ═══════════════════════════════════════════════════════════════════

def import_offset_wells_csv(run_id: int, csv_path: str) -> int:
    """Import an existing offset_wells CSV into the database."""
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    save_offset_wells(run_id, rows)
    return len(rows)


def import_formation_tops_csv(csv_path: str) -> int:
    """Import an existing formation_tops CSV into the database."""
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    save_formation_tops(rows)
    return len(rows)


def import_bha_runs_csv(run_id: int, csv_path: str) -> int:
    """Import an existing BHA runs CSV into the database."""
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    save_bha_runs(run_id, rows)
    return len(rows)
