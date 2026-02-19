"""Pull wits.summary-1ft data for all BHA runs and compute per-foot ROP.

For each BHA run in the input CSV, fetches 1-ft depth-summary data from Corva,
derives ROP from timestamps, classifies each foot as Rotary or Slide drilling,
and tracks distance/formation metrics.

Lateral mode (default):
  - distance_from_run_start: for rotary ROP degradation (bit wear)
  - distance_from_lateral_start: for slide ROP degradation (friction/drag)

Vertical mode (--mode vertical):
  - Loads formation tops from formation_tops.csv
  - Maps each foot's TVD to a formation name and % position
  - Discretizes into 10% formation segments for ROP curves

Performance optimizations (v2):
  - Well-level batching: one API call per well, not per BHA run
  - 10K batch size: 20x fewer HTTP round trips than 500
  - Per-run caching: re-runs skip wells already in the output CSV
  - 20 parallel workers with shared session (connection pooling)

Usage:
    python pull_1ft_for_runs.py [bha_csv]                          # lateral (default)
    python pull_1ft_for_runs.py [bha_csv] --mode vertical          # vertical/intermediate
    python pull_1ft_for_runs.py intermediate_bhas.csv --mode vertical
"""
import csv
import json
import os
import subprocess
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import db

load_dotenv()

API_KEY = os.getenv("CORVA_API_KEY")
DATA_API = "https://data.corva.ai"
HEADERS = {"Authorization": f"API {API_KEY}"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Rig states we consider "on-bottom drilling"
DRILLING_STATES = {"Rotary Drilling", "Slide Drilling"}

# ROP sanity bounds (ft/hr)
ROP_MIN = 5
ROP_MAX = 500

# Minimum run length (ft) to include in curves
MIN_RUN_LENGTH = 1000

# Formation segment resolution (% per bin)
FORMATION_SEGMENT_PCT = 10

# --- Performance tuning ---
BATCH_SIZE = 10000       # records per API call (was 500)
MAX_WORKERS = 20         # parallel well-fetch workers (was 8)

# Shared session with connection pooling and retry
_session = None


def _get_session():
    """Return a shared requests.Session with connection pooling and retry."""
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(HEADERS)
        retry = Retry(total=3, backoff_factor=1,
                      status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(
            max_retries=retry,
            pool_connections=MAX_WORKERS,
            pool_maxsize=MAX_WORKERS,
        )
        _session.mount("https://", adapter)
        _session.mount("http://", adapter)
    return _session


def load_formation_tops(csv_path):
    """Load formation tops from the CSV produced by pull_formation_tops.py.

    Returns dict keyed by asset_id, each containing a sorted list of
    formation tops with name, md_top, tvd_top, md_thickness, tvd_thickness.
    """
    by_asset = defaultdict(list)
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            aid = row.get("asset_id", "").strip()
            if not aid:
                continue
            try:
                top = {
                    "formation_name": row.get("formation_name", "").strip(),
                    "md_top": float(row["md_top"]),
                    "tvd_top": float(row["tvd_top"]),
                    "md_thickness": float(row["md_thickness"]) if row.get("md_thickness") else None,
                    "tvd_thickness": float(row["tvd_thickness"]) if row.get("tvd_thickness") else None,
                }
                by_asset[aid].append(top)
            except (ValueError, KeyError):
                continue

    # Ensure sorted by md_top within each asset
    for aid in by_asset:
        by_asset[aid].sort(key=lambda x: x["md_top"])

    return dict(by_asset)


def map_foot_to_formation(tvd, md, formation_tops):
    """Map a single foot to its formation and % position.

    Uses TVD to determine which formation the foot falls in, since
    formation tops are defined in TVD.

    Returns (formation_name, formation_pct, formation_segment) or
    (None, None, None) if the foot can't be mapped.
    """
    if not formation_tops or tvd is None:
        return None, None, None

    # Find which formation this TVD falls in
    for i, top in enumerate(formation_tops):
        # Determine the bottom of this formation (= top of next, or infinity)
        if i + 1 < len(formation_tops):
            next_tvd = formation_tops[i + 1]["tvd_top"]
        elif top["tvd_thickness"] is not None:
            next_tvd = top["tvd_top"] + top["tvd_thickness"]
        else:
            next_tvd = top["tvd_top"] + 1000  # fallback

        if top["tvd_top"] <= tvd < next_tvd:
            thickness = next_tvd - top["tvd_top"]
            if thickness <= 0:
                return top["formation_name"], 0.0, 0
            pct = (tvd - top["tvd_top"]) / thickness * 100.0
            pct = max(0.0, min(pct, 99.99))
            segment = int(pct // FORMATION_SEGMENT_PCT) * FORMATION_SEGMENT_PCT
            return top["formation_name"], round(pct, 1), segment

    # Foot is deeper than all formations -- assign to last formation at 100%
    if formation_tops:
        return formation_tops[-1]["formation_name"], 100.0, 90

    return None, None, None


def load_bha_runs(csv_path):
    """Load BHA runs from the parsed lateral_bhas CSV."""
    runs = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                start = float(row["start_depth"])
                end = float(row["end_depth"])
            except (ValueError, KeyError, TypeError):
                continue
            run_length = end - start
            if run_length < MIN_RUN_LENGTH:
                continue
            runs.append(row)
    return runs


def estimate_lateral_starts(runs):
    """Estimate lateral start depth per asset from the shallowest BHA start.

    If the CSV has a 'lateral_start_depth' column, use it directly.
    Otherwise, use the minimum start_depth among all lateral BHAs for that asset.
    """
    def fetch_lateral_start_from_sections(asset_id):
        """Fetch lateral section top depth from well-sections API for one asset."""
        session = _get_session()
        query = {"asset_id": int(asset_id)}
        skip = 0
        batch = 100
        tops = []
        while True:
            try:
                r = session.get(
                    f"{DATA_API}/api/v1/data/corva/data.well-sections/",
                    params={
                        "limit": batch,
                        "skip": skip,
                        "sort": json.dumps({"data.top_depth": 1}),
                        "query": json.dumps(query),
                        "fields": "data.name,data.top_depth",
                    },
                    timeout=30,
                )
                r.raise_for_status()
            except requests.exceptions.RequestException:
                break
            rows = r.json()
            if not rows:
                break
            for row in rows:
                data = row.get("data", {})
                name = str(data.get("name", "")).lower()
                if "lateral" not in name:
                    continue
                top = data.get("top_depth")
                if top is None:
                    continue
                try:
                    tops.append(float(top))
                except (ValueError, TypeError):
                    continue
            if len(rows) < batch:
                break
            skip += batch
        return min(tops) if tops else None

    lateral_starts = {}

    # First pass: check for explicit lateral_start_depth
    for r in runs:
        aid = r["asset_id"]
        lsd = r.get("lateral_start_depth", "")
        if lsd and lsd != "N/A":
            try:
                lateral_starts[aid] = float(lsd)
            except (ValueError, TypeError):
                pass

    # Second pass: fetch lateral section top from well-sections API
    # when run CSV does not provide lateral_start_depth.
    fetched_from_sections = 0
    for aid in {r["asset_id"] for r in runs if r.get("asset_id")}:
        if aid in lateral_starts:
            continue
        sec_top = fetch_lateral_start_from_sections(aid)
        if sec_top is not None:
            lateral_starts[aid] = sec_top
            fetched_from_sections += 1

    # Third pass: estimate from minimum run start depth if still unavailable
    asset_starts = defaultdict(list)
    for r in runs:
        aid = r["asset_id"]
        if aid in lateral_starts:
            continue
        try:
            asset_starts[aid].append(float(r["start_depth"]))
        except (ValueError, TypeError):
            pass

    for aid, starts in asset_starts.items():
        if starts:
            lateral_starts[aid] = min(starts)

    return lateral_starts


# ---------------------------------------------------------------------------
#  Phase 1: Fetch raw 1ft data per WELL (not per run)
# ---------------------------------------------------------------------------

def fetch_well_1ft(asset_id, min_depth, max_depth):
    """Fetch all wits.summary-1ft records for a well's full depth range.

    Uses batch_size=10000 and a shared session with connection pooling.
    Returns list of raw API records.
    """
    session = _get_session()
    all_records = []
    skip = 0

    query = {
        "asset_id": int(asset_id),
        "data.hole_depth": {"$gte": min_depth, "$lte": max_depth},
    }
    fields = (
        "data.hole_depth,data.state_max,"
        "data.timestamp_max,data.timestamp_min,"
        "data.true_vertical_depth_mean,"
        "metadata.drillstring"
    )

    while True:
        try:
            r = session.get(
                f"{DATA_API}/api/v1/data/corva/wits.summary-1ft/",
                params={
                    "limit": BATCH_SIZE,
                    "skip": skip,
                    "sort": json.dumps({"data.hole_depth": 1}),
                    "query": json.dumps(query),
                    "fields": fields,
                },
                timeout=90,
            )
            r.raise_for_status()
        except requests.exceptions.RequestException:
            break

        records = r.json()
        if not records:
            break
        all_records.extend(records)
        if len(records) < BATCH_SIZE:
            break
        skip += BATCH_SIZE

    return all_records


# ---------------------------------------------------------------------------
#  Phase 2: Process pre-fetched records for a single BHA run (CPU only)
# ---------------------------------------------------------------------------

def process_run_from_cache(run, records, lateral_starts, mode="lateral",
                           formation_tops_by_asset=None):
    """Process pre-fetched 1ft records for a single BHA run.

    Unlike the old process_run(), this does NOT make any API calls.
    Records have already been fetched per-well in Phase 1.
    """
    asset_id = run["asset_id"]
    start_depth = float(run["start_depth"])
    end_depth = float(run["end_depth"])
    lateral_start = lateral_starts.get(asset_id, start_depth)
    effective_run_start = max(start_depth, lateral_start) if mode == "lateral" else start_depth

    well_formations = None
    if mode == "vertical" and formation_tops_by_asset:
        well_formations = formation_tops_by_asset.get(asset_id, [])

    rows_out = []
    dropped_pre_lateral = 0
    for rec in records:
        data = rec.get("data", {})
        state = data.get("state_max", "")

        if state not in DRILLING_STATES:
            continue

        hole_depth = data.get("hole_depth")
        ts_max = data.get("timestamp_max")
        ts_min = data.get("timestamp_min")

        if hole_depth is None or ts_max is None or ts_min is None:
            continue

        # Only include records within THIS run's depth range
        if hole_depth < start_depth or hole_depth > end_depth:
            continue

        dt = ts_max - ts_min
        if dt <= 0:
            continue

        rop = 3600.0 / dt
        if rop < ROP_MIN or rop > ROP_MAX:
            continue

        if mode == "lateral" and hole_depth < effective_run_start:
            dropped_pre_lateral += 1
            continue

        dist_run = hole_depth - effective_run_start
        tvd_raw = data.get("true_vertical_depth_mean", "")
        tvd = float(tvd_raw) if tvd_raw else None
        ds_id = (rec.get("metadata") or {}).get("drillstring", "")

        row = {
            "asset_id": asset_id,
            "well_name": run.get("well_name", ""),
            "operator": run.get("operator", ""),
            "bha_number": run.get("bha_number", ""),
            "equiv_bha_key": run.get("_equiv_key", ""),
            "has_agitator": run.get("has_agitator", "False"),
            "bit_manufacturer": run.get("bit_manufacturer", ""),
            "bit_model": run.get("bit_model", ""),
            "motor_od": run.get("motor_od", ""),
            "motor_model": run.get("motor_model", ""),
            "motor_stages": run.get("motor_stages", ""),
            "motor_lobe_config": run.get("motor_lobe_config", ""),
            "hole_depth": round(hole_depth, 1),
            "distance_from_run_start": round(dist_run, 1),
            "state": state,
            "rop_ft_hr": round(rop, 1),
            "tvd": round(tvd, 1) if tvd is not None else "",
            "drillstring_id": ds_id,
        }

        if mode == "lateral":
            dist_lat = hole_depth - lateral_start
            # Rotary axis for lateral mode is now anchored to lateral start
            # (not BHA run start) to avoid curve-footage bias.
            row["distance_from_run_start"] = round(dist_lat, 1)
            row["distance_from_lateral_start"] = round(dist_lat, 1)
        elif mode == "vertical":
            fm_name, fm_pct, fm_segment = map_foot_to_formation(
                tvd, hole_depth, well_formations
            )
            row["formation_name"] = fm_name or ""
            row["formation_pct"] = round(fm_pct, 1) if fm_pct is not None else ""
            row["formation_segment"] = fm_segment if fm_segment is not None else ""

        rows_out.append(row)

    return rows_out


# ---------------------------------------------------------------------------
#  Caching: load previously-fetched run data from existing CSV
# ---------------------------------------------------------------------------

def load_cached_runs(output_dir, mode):
    """Load already-processed rows from an existing output CSV.

    Returns:
        cached_rows: list of dicts (CSV rows for runs already fetched)
        cached_keys: set of (asset_id, bha_number) already present
    """
    suffix = "_vertical" if mode == "vertical" else ""
    csv_path = os.path.join(output_dir, f"rop_1ft_data{suffix}.csv")

    if not os.path.exists(csv_path):
        return [], set()

    cached_rows = []
    cached_keys = set()
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required_columns = {
                "bit_manufacturer",
                "bit_model",
                "motor_od",
                "motor_model",
                "motor_stages",
                "motor_lobe_config",
            }
            existing_columns = set(reader.fieldnames or [])
            missing_required = sorted(required_columns - existing_columns)
            if missing_required:
                return [], set()
            for row in reader:
                cached_rows.append(row)
                cached_keys.add((row.get("asset_id", ""), row.get("bha_number", "")))
    except Exception:
        return [], set()

    return cached_rows, cached_keys


def build_equiv_keys(runs):
    """Pre-compute equivalent BHA group key for each run.

    Uses the same logic as group_equivalent_bhas.py but inline so we
    don't need to import it (keeps this script self-contained).
    """
    for r in runs:
        blades = r.get("parsed_blades", "").strip()
        cutter = r.get("parsed_cutter_mm", "").strip()
        lobes = r.get("motor_lobe_config", "").strip()
        rpg_band = r.get("motor_rpg_band", "").strip()
        is_rss = str(r.get("is_rss", "")).strip().lower() in ("true", "1", "yes")

        if not blades or blades == "?" or "?" in str(cutter):
            bit_key = "unparsed"
        else:
            bit_key = f"{blades}B-{cutter}mm"

        if is_rss:
            motor_key = "RSS"
        elif not lobes or lobes == "?":
            motor_key = "no_motor"
        else:
            motor_key = f"{lobes}-{rpg_band}" if rpg_band and rpg_band != "?" else lobes

        r["_equiv_key"] = f"{bit_key} | {motor_key}"


def main():
    # Parse arguments
    csv_path = None
    mode = "lateral"
    formations_csv = None
    output_dir = None
    export_csv = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--mode" and i + 1 < len(args):
            mode = args[i + 1].lower()
            i += 2
        elif args[i] == "--formations" and i + 1 < len(args):
            formations_csv = args[i + 1]
            i += 2
        elif args[i] == "--output-dir" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        elif args[i] == "--export-csv":
            export_csv = True
            i += 1
        elif not args[i].startswith("--"):
            csv_path = args[i]
            i += 1
        else:
            i += 1

    if output_dir is None:
        output_dir = SCRIPT_DIR
    elif not os.path.isabs(output_dir):
        output_dir = os.path.join(SCRIPT_DIR, output_dir)
    os.makedirs(output_dir, exist_ok=True)

    if csv_path is None:
        csv_path = os.path.join(SCRIPT_DIR, "lateral_bhas.csv")
    elif not os.path.isabs(csv_path):
        csv_path = os.path.join(SCRIPT_DIR, csv_path)

    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found")
        sys.exit(1)

    # Load formation tops if in vertical mode
    formation_tops_by_asset = None
    if mode == "vertical":
        if formations_csv is None:
            formations_csv = os.path.join(SCRIPT_DIR, "formation_tops.csv")
        elif not os.path.isabs(formations_csv):
            formations_csv = os.path.join(SCRIPT_DIR, formations_csv)

        if not os.path.exists(formations_csv):
            print(f"ERROR: Formation tops file not found: {formations_csv}")
            print(f"  Run pull_formation_tops.py first.")
            sys.exit(1)

        formation_tops_by_asset = load_formation_tops(formations_csv)
        print(f"  Loaded formation tops for {len(formation_tops_by_asset)} wells")

    runs = load_bha_runs(csv_path)
    build_equiv_keys(runs)
    lateral_starts = estimate_lateral_starts(runs)

    # Filter out unparsed / no-motor runs for performance curves
    valid_runs = [r for r in runs if "unparsed" not in r["_equiv_key"]
                  and "no_motor" not in r["_equiv_key"]]

    # Vertical safeguard: if formation tops have no overlap with current
    # run assets, repull and reload formation tops for this run CSV.
    if mode == "vertical" and formation_tops_by_asset:
        run_asset_ids = {
            str(r.get("asset_id", "")).strip()
            for r in valid_runs if r.get("asset_id")
        }
        fm_asset_ids = set(formation_tops_by_asset.keys())
        covered = len(run_asset_ids & fm_asset_ids)
        total = len(run_asset_ids)

        if total > 0 and covered == 0:
            print("  WARNING: Formation file has zero overlap with current run assets; repulling...")
            pull_script = os.path.join(SCRIPT_DIR, "pull_formation_tops.py")
            normalize_script = os.path.join(SCRIPT_DIR, "normalize_formations.py")
            try:
                subprocess.run(
                    [sys.executable, pull_script, csv_path],
                    cwd=SCRIPT_DIR,
                    check=False,
                )
                raw_path = os.path.join(SCRIPT_DIR, "formation_tops.csv")
                if os.path.exists(raw_path):
                    target_asset_for_norm = (
                        str(valid_runs[0].get("asset_id", ""))
                        if valid_runs else ""
                    )
                    subprocess.run(
                        [sys.executable, normalize_script,
                         "--target-asset", target_asset_for_norm,
                         "--input", raw_path],
                        cwd=SCRIPT_DIR,
                        check=False,
                    )
                preferred = os.path.join(SCRIPT_DIR, "formation_tops_canonical.csv")
                reload_path = preferred if os.path.exists(preferred) else raw_path
                if os.path.exists(reload_path):
                    formation_tops_by_asset = load_formation_tops(reload_path)
                    fm_asset_ids = set(formation_tops_by_asset.keys())
                    covered = len(run_asset_ids & fm_asset_ids)
            except Exception as exc:
                print(f"  WARNING: Formation repull failed: {exc}")

    mode_label = mode.upper()
    unique_wells = set(r["asset_id"] for r in valid_runs)
    print(f"\n{'=' * 80}")
    print(f"  PULL WITS.SUMMARY-1FT FOR BHA RUNS ({mode_label} MODE)")
    print(f"  Total runs in CSV: {len(runs)} (>= {MIN_RUN_LENGTH} ft)")
    print(f"  Valid runs (parsed bit + motor): {len(valid_runs)}")
    print(f"  Unique wells: {len(unique_wells)}")
    if mode == "vertical" and formation_tops_by_asset:
        matched = sum(1 for r in valid_runs if r["asset_id"] in formation_tops_by_asset)
        print(f"  Runs with formation data: {matched}/{len(valid_runs)}")
    print(f"  Batch size: {BATCH_SIZE} | Workers: {MAX_WORKERS}")
    print(f"{'=' * 80}\n")

    t0 = time.time()

    # ── Caching: load previously-fetched run data ──
    cached_rows, cached_keys = load_cached_runs(output_dir, mode)
    cached_run_count = 0
    fresh_runs = []
    for r in valid_runs:
        key = (r["asset_id"], r.get("bha_number", ""))
        if key in cached_keys:
            cached_run_count += 1
        else:
            fresh_runs.append(r)

    # Vertical formation mapping has changed during debugging; force fresh
    # reprocessing to avoid reusing stale unmapped cached rows.
    if mode == "vertical" and cached_run_count > 0:
        cached_rows = []
        cached_keys = set()
        cached_run_count = 0
        fresh_runs = list(valid_runs)

    # Rotary-axis semantics for lateral mode now use lateral-start distance.
    # Force a fresh rebuild so legacy cached rows (run-start anchored) are not reused.
    if mode == "lateral" and cached_run_count > 0:
        cached_rows = []
        cached_keys = set()
        cached_run_count = 0
        fresh_runs = list(valid_runs)

    if cached_run_count:
        print(f"  Cache hit: {cached_run_count} runs already in output CSV "
              f"({len(cached_rows):,} rows)")
        print(f"  Fresh runs to fetch: {len(fresh_runs)}")
    else:
        print(f"  No cached data found, fetching all {len(valid_runs)} runs")

    if not fresh_runs:
        # All data is cached -- skip API entirely
        elapsed = time.time() - t0
        all_1ft_rows = cached_rows
        print(f"\n  All data from cache! {len(all_1ft_rows):,} rows in {elapsed:.1f}s")
    else:
        # ── Phase 1: Fetch raw data per WELL (parallel, 20 workers) ──
        # Group fresh runs by asset_id to fetch once per well
        wells = defaultdict(list)
        for r in fresh_runs:
            wells[r["asset_id"]].append(r)

        # Compute depth range per well (union of all runs)
        well_ranges = {}
        for asset_id, well_runs in wells.items():
            min_d = min(float(r["start_depth"]) for r in well_runs)
            max_d = max(float(r["end_depth"]) for r in well_runs)
            well_ranges[asset_id] = (min_d, max_d)

        well_ids = list(wells.keys())
        print(f"\n  Phase 1: Fetching {len(well_ids)} wells "
              f"({len(fresh_runs)} runs) with {MAX_WORKERS} workers...")

        well_data = {}  # asset_id -> list of raw API records
        completed_wells = 0

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {}
            for aid in well_ids:
                min_d, max_d = well_ranges[aid]
                future = executor.submit(fetch_well_1ft, aid, min_d, max_d)
                futures[future] = aid

            for future in as_completed(futures):
                aid = futures[future]
                try:
                    records = future.result()
                    well_data[aid] = records
                except Exception as e:
                    print(f"  ERROR fetching well {aid}: {e}")
                    well_data[aid] = []

                completed_wells += 1
                if completed_wells % 10 == 0 or completed_wells == len(well_ids):
                    elapsed = time.time() - t0
                    total_recs = sum(len(v) for v in well_data.values())
                    print(f"  {completed_wells}/{len(well_ids)} wells fetched, "
                          f"{total_recs:,} raw records, {elapsed:.0f}s")

        fetch_elapsed = time.time() - t0
        total_recs = sum(len(v) for v in well_data.values())
        print(f"\n  Phase 1 complete: {total_recs:,} raw records "
              f"from {len(well_data)} wells in {fetch_elapsed:.1f}s")

        # ── Phase 2: Process per run from in-memory data (CPU only) ──
        print(f"\n  Phase 2: Processing {len(fresh_runs)} runs...")
        t1 = time.time()

        fresh_rows = []
        for run in fresh_runs:
            asset_id = run["asset_id"]
            records = well_data.get(asset_id, [])
            rows = process_run_from_cache(
                run, records, lateral_starts,
                mode=mode,
                formation_tops_by_asset=formation_tops_by_asset,
            )
            fresh_rows.extend(rows)

        proc_elapsed = time.time() - t1
        print(f"  Phase 2 complete: {len(fresh_rows):,} processed rows "
              f"in {proc_elapsed:.1f}s")

        # Combine cached + fresh
        all_1ft_rows = cached_rows + fresh_rows

    elapsed = time.time() - t0
    print(f"\n  Done: {len(all_1ft_rows):,} total 1ft drilling records in {elapsed:.1f}s")

    # Stats
    rotary_count = sum(1 for r in all_1ft_rows if r.get("state") == "Rotary Drilling")
    slide_count = sum(1 for r in all_1ft_rows if r.get("state") == "Slide Drilling")
    print(f"  Rotary feet: {rotary_count:,}")
    print(f"  Slide feet:  {slide_count:,}")
    if rotary_count + slide_count:
        print(f"  Slide %:     {100 * slide_count / (rotary_count + slide_count):.1f}%")

    # Formation mapping stats (vertical mode)
    if mode == "vertical":
        mapped = sum(1 for r in all_1ft_rows if r.get("formation_name"))
        unmapped = len(all_1ft_rows) - mapped
        print(f"  Mapped to formation: {mapped:,}")
        if unmapped:
            print(f"  Unmapped (no formation data): {unmapped:,}")

        fm_counts = defaultdict(int)
        for r in all_1ft_rows:
            if r.get("formation_name"):
                fm_counts[r["formation_name"]] += 1
        if fm_counts:
            print(f"\n  Feet by formation:")
            for fm, cnt in sorted(fm_counts.items(), key=lambda x: -x[1]):
                print(f"    {fm:<30} {cnt:>7,} feet")

    # Group key summary
    key_counts = defaultdict(int)
    for r in all_1ft_rows:
        key_counts[r.get("equiv_bha_key", "?")] += 1
    print(f"\n  Records by Equivalent BHA:")
    for key, cnt in sorted(key_counts.items(), key=lambda x: -x[1]):
        print(f"    {key:<30} {cnt:>7,} feet")

    # Save
    if not all_1ft_rows:
        print("\nNo 1ft data retrieved.")
        return

    suffix = "vertical" if mode == "vertical" else ""
    out_name = f"rop_1ft_data{'_' + suffix if suffix else ''}.csv"
    out_path = os.path.join(output_dir, out_name)
    fieldnames = list(all_1ft_rows[0].keys())
    try:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_1ft_rows)
        print(f"\n  Saved to: {out_path}")
    except PermissionError:
        backup = out_path.replace(".csv", f"_{int(time.time())}.csv")
        with open(backup, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_1ft_rows)
        print(f"\n  WARNING: File locked. Saved to: {backup}")

    # Save as Parquet for faster subsequent reads (scoped by run_id)
    try:
        df = pd.DataFrame(all_1ft_rows)
        # Normalize numeric columns (cached rows from CSV are strings)
        numeric_cols = ["hole_depth", "distance_from_run_start", "rop_ft_hr",
                        "tvd", "distance_from_lateral_start",
                        "formation_pct", "formation_segment"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        section_name = os.path.basename(output_dir) if output_dir != "." else "default"
        latest = db.get_latest_run()
        rid = latest["id"] if latest else None
        db.save_1ft_data(section_name, df, mode=mode, run_id=rid)
    except Exception as e:
        print(f"  Parquet save warning: {e}")

    if export_csv:
        suffix = "_vertical" if mode == "vertical" else ""
        db.export_csv(all_1ft_rows, f"rop_1ft_data{suffix}")


if __name__ == "__main__":
    main()
