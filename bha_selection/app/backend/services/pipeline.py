"""Wraps the existing BHA selection Python scripts via subprocess.

Each step in the per-section pipeline is run as a child process so the
FastAPI server stays responsive.  Uses asyncio.to_thread + subprocess.run
for Windows compatibility (asyncio.create_subprocess_exec is unreliable
on Windows).

Scripts now save to both SQLite (via db.py) and legacy CSV. The pipeline
uses the DB for state tracking and the scripts handle their own DB writes.
"""

import asyncio
import subprocess
import os
import sys
import glob as _glob
import csv as _csv

# Add the bha_selection root to sys.path so we can import db
SCRIPT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import db as _db  # noqa: E402
from . import jobs  # noqa: E402

PYTHON = sys.executable


def _run_sync(cmd: list[str], cwd: str | None = None) -> tuple[int, str]:
    """Run a command synchronously and return (returncode, combined output)."""
    result = subprocess.run(
        cmd,
        cwd=cwd or SCRIPT_DIR,
        capture_output=True,
        text=True,
    )
    output = result.stdout or ""
    if result.stderr:
        output += "\n" + result.stderr
    return result.returncode, output.strip()


async def _run_script(cmd: list[str], job_id: str, step: int, label: str):
    """Run a single script in a thread, updating job progress."""
    jobs.update_job(job_id, step=step, progress=label, status="running")
    rc, output = await asyncio.to_thread(_run_sync, cmd)
    last_line = ""
    for line in output.splitlines():
        stripped = line.strip()
        if stripped:
            last_line = stripped[:120]
    if last_line:
        jobs.update_job(job_id, progress=last_line)
    return rc, output


async def _find_offset_wells(
    asset_id: str,
    radius_miles: float,
    spud_date_filter: str | None = None,
) -> str | None:
    """Run find_offsets_all_operators.py if needed.

    Checks the DB first -- if we already have offset wells for this
    specific asset+radius, skip the Corva API call entirely.
    The spud date filter is applied during the initial pull and cached
    with the results, so subsequent pulls with the same parameters
    are instant.
    """
    # Check DB first -- reuse if we have data for this asset+radius
    run = _db.get_current_run(str(asset_id))
    if run and _db.count_offset_wells(run["id"]) > 0:
        if run.get("search_radius") == radius_miles:
            print(f"  Using cached offset wells for {asset_id} "
                  f"(run {run['id']}, {_db.count_offset_wells(run['id'])} wells)")
            return None  # Data is in DB, no CSV needed

    # No DB data for this asset -- run the script
    script = os.path.join(SCRIPT_DIR, "find_offsets_all_operators.py")
    if not os.path.exists(script):
        return None

    cmd = [PYTHON, script, asset_id, str(radius_miles)]
    if spud_date_filter:
        cmd += ["--spud-after", spud_date_filter]

    rc, output = await asyncio.to_thread(_run_sync, cmd)

    # The script saves to both CSV and DB. Return the CSV path if it
    # was generated (still needed by some downstream scripts).
    import time as _time
    radius_strs = [str(radius_miles)]
    if radius_miles == int(radius_miles):
        radius_strs.append(str(int(radius_miles)))

    now = _time.time()
    for rs in radius_strs:
        pattern = os.path.join(SCRIPT_DIR, f"offset_wells_{rs}mi_*.csv")
        matches = sorted(
            _glob.glob(pattern), key=os.path.getmtime, reverse=True
        )
        for m in matches:
            if now - os.path.getmtime(m) < 120:  # Created in last 2 min
                return m

    return None


async def _ensure_formation_data(asset_id: str, wells_csv: str | None):
    """Pull formation tops and normalize if the target well has no data.

    Checks the DB first. If formation data exists there, skips Corva pull.
    """
    def _load_asset_ids(csv_path: str, col: str = "asset_id") -> set[str]:
        ids: set[str] = set()
        try:
            with open(csv_path, encoding="utf-8") as f:
                for row in _csv.DictReader(f):
                    aid = str(row.get(col, "")).strip()
                    if aid:
                        ids.add(aid)
        except Exception:
            return set()
        return ids

    def _formation_coverage(formations_path: str, required_assets: set[str]) -> tuple[int, int]:
        if not required_assets:
            return 0, 0
        fm_assets = _load_asset_ids(formations_path, "asset_id")
        covered = len(required_assets & fm_assets)
        return covered, len(required_assets)

    required_assets: set[str] = set()
    if wells_csv and os.path.exists(wells_csv):
        required_assets = _load_asset_ids(wells_csv, "asset_id")

    fm_canonical = os.path.join(SCRIPT_DIR, "formation_tops_canonical.csv")
    fm_raw = os.path.join(SCRIPT_DIR, "formation_tops.csv")
    existing = fm_canonical if os.path.exists(fm_canonical) else (
        fm_raw if os.path.exists(fm_raw) else None
    )

    # Always validate existing formation-file coverage against the current
    # offset-well asset set when available.
    force_refresh = False
    if existing and required_assets:
        covered, total = _formation_coverage(existing, required_assets)
        if covered > 0:
            return existing
        force_refresh = True

    # Check DB for target asset only after coverage validation.
    if _db.formation_tops_exist(str(asset_id)):
        if existing:
            if not force_refresh:
                return existing
        else:
            # DB has data but no CSVs; allow downstream DB fallback.
            return None

    # If target-asset DB tops are absent, only reuse existing raw file when
    # we are not in a forced refresh path.
    if os.path.exists(fm_raw) and not force_refresh:
        # Raw CSV exists, run normalization
        normalize_script = os.path.join(SCRIPT_DIR, "normalize_formations.py")
        if os.path.exists(normalize_script):
            await asyncio.to_thread(
                _run_sync,
                [PYTHON, normalize_script,
                 "--target-asset", asset_id, "--input", fm_raw],
            )
        if os.path.exists(fm_canonical):
            return fm_canonical
        return fm_raw

    # Need to pull from Corva
    pull_script = os.path.join(SCRIPT_DIR, "pull_formation_tops.py")
    if not os.path.exists(pull_script) or not wells_csv:
        return None

    # Clear stale formation files before re-pulling for current offset set.
    for p in (fm_canonical, fm_raw):
        try:
            if os.path.exists(p):
                os.remove(p)
        except OSError:
            pass

    await asyncio.to_thread(
        _run_sync, [PYTHON, pull_script, wells_csv]
    )

    # Normalize
    if os.path.exists(fm_raw):
        normalize_script = os.path.join(SCRIPT_DIR, "normalize_formations.py")
        if os.path.exists(normalize_script):
            await asyncio.to_thread(
                _run_sync,
                [PYTHON, normalize_script,
                 "--target-asset", asset_id, "--input", fm_raw],
            )
        if os.path.exists(fm_canonical):
            return fm_canonical
        return fm_raw

    return None


def get_analysis_state(asset_id: str | None = None) -> dict:
    """Read the current analysis state from the database.

    If asset_id is provided, returns the run for that specific asset.
    Otherwise falls back to the most recent run across all assets.
    """
    run = None
    if asset_id:
        run = _db.get_current_run(str(asset_id))
    if not run:
        run = _db.get_latest_run()
    if run:
        return {
            "target_asset_id": run["target_asset_id"],
            "run_id": run["id"],
            "search_radius": run.get("search_radius", 15.0),
        }
    return {}


def _clean_stale_section_files(asset_id: str):
    """Remove all analysis artifacts from previous wells.

    When switching target wells, every intermediate and output file must
    be purged to prevent cross-well data contamination.
    """
    import shutil as _shutil

    patterns = [
        "bhas_*.csv",
        "all_bhas_*.csv",
        "offset_wells_*.csv",
        "target_sections.json",
    ]
    removed = 0
    for pat in patterns:
        for f in _glob.glob(os.path.join(SCRIPT_DIR, pat)):
            try:
                os.remove(f)
                removed += 1
            except OSError:
                pass

    # Clean all section output directories (charts, TTD, 1ft data, curves)
    sections_root = os.path.join(SCRIPT_DIR, "sections")
    if os.path.isdir(sections_root):
        for entry in os.listdir(sections_root):
            entry_path = os.path.join(sections_root, entry)
            if os.path.isdir(entry_path):
                try:
                    _shutil.rmtree(entry_path)
                    removed += 1
                except OSError:
                    pass
        print(f"  Cleaned section output directories")

    # Purge bha_runs from DB for stale runs of OTHER assets
    prev = _db.get_latest_run()
    if prev and str(prev.get("target_asset_id")) != str(asset_id):
        run_id = prev["id"]
        try:
            with _db.connection() as conn:
                conn.execute("DELETE FROM bha_runs WHERE run_id = ?",
                             (run_id,))
            print(f"  Purged stale bha_runs for run {run_id}")
        except Exception as e:
            print(f"  Warning: could not purge stale bha_runs: {e}")

    if removed:
        print(f"  Cleaned {removed} stale artifacts for new well {asset_id}")


async def analyze_well(
    asset_id: str,
    search_radius_miles: float = 15.0,
    spud_date_filter: str | None = None,
) -> dict:
    """Run find_offsets + analyze_target_well.py and return parsed sections JSON."""
    import json

    # Clean stale per-section files when switching to a different well
    prev = _db.get_latest_run()
    if prev and str(prev.get("target_asset_id")) != str(asset_id):
        _clean_stale_section_files(asset_id)

    # Create/get analysis run in DB
    run_id = _db.get_or_create_run(str(asset_id), search_radius_miles)

    # Step 1: Find offset wells at the requested radius
    wells_csv = await _find_offset_wells(
        asset_id, search_radius_miles, spud_date_filter
    )

    # Step 2: Ensure formation data exists for this target well + offsets.
    wells_csv_for_formations = wells_csv
    if not wells_csv_for_formations:
        wells_csv_for_formations = _find_offset_csv(asset_id, search_radius_miles)
    fm_csv = await _ensure_formation_data(asset_id, wells_csv_for_formations)

    # Step 3: Analyze target well sections
    # Skip re-analysis if sections JSON is fresh and for the same asset
    sections_json = os.path.join(SCRIPT_DIR, "target_sections.json")
    reuse_sections = False
    if os.path.exists(sections_json):
        try:
            with open(sections_json, encoding="utf-8") as f:
                cached = json.load(f)
            # Reuse if the cached data is for the same asset
            cached_asset = str(cached.get("target_asset_id", ""))
            if cached_asset == str(asset_id) and cached.get("sections"):
                reuse_sections = True
                print(f"  Reusing cached sections for asset {asset_id}")
        except Exception:
            pass

    if not reuse_sections:
        cmd = [
            PYTHON,
            os.path.join(SCRIPT_DIR, "analyze_target_well.py"),
            "--asset", asset_id,
            "--output", sections_json,
        ]
        if fm_csv:
            cmd += ["--formations", fm_csv]

        rc, output = await asyncio.to_thread(_run_sync, cmd)

        if not os.path.exists(sections_json):
            return {"error": f"Failed to analyze well (rc={rc}): {output[:500]}"}

    with open(sections_json, encoding="utf-8") as f:
        result = json.load(f)

    if wells_csv:
        result["offset_wells_csv"] = wells_csv
        result["search_radius_miles"] = search_radius_miles

    result["run_id"] = run_id
    return result


def _find_offset_csv(asset_id: str, radius_miles: float) -> str | None:
    """Find or create an offset wells CSV for this specific asset/radius.

    Always exports from the DB to guarantee the CSV matches the current
    asset's offset wells, avoiding cross-well contamination from stale
    CSV files left on disk.
    """
    run = _db.get_current_run(str(asset_id))
    if not run:
        return None

    offset_wells = _db.get_offset_wells(run["id"])
    if not offset_wells:
        return None

    import csv as _csv
    from datetime import datetime as _dt

    ts = _dt.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(
        SCRIPT_DIR, f"offset_wells_{radius_miles}mi_{ts}.csv"
    )
    fieldnames = [
        "asset_id", "well_name", "operator", "basin", "target_formation",
        "rig", "distance_miles", "hole_depth_ft", "section", "hole_diameter",
        "mud_type", "mud_density", "bit_size", "bit_type", "state",
        "spud_date", "lat", "lon", "string_design", "well_state",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = _csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for w in offset_wells:
            row = {k: (w.get(k) if w.get(k) is not None else "N/A")
                   for k in fieldnames}
            writer.writerow(row)
    print(f"  Exported {len(offset_wells)} offset wells from DB -> {csv_path}")
    return csv_path


def _find_all_bhas_csv() -> str | None:
    """Find the most recent all_bhas_*.csv file."""
    matches = sorted(
        _glob.glob(os.path.join(SCRIPT_DIR, "all_bhas_*.csv")),
        key=os.path.getmtime,
        reverse=True,
    )
    return matches[0] if matches else None


async def run_section_pipeline(
    job_id: str,
    asset_id: str,
    section_name: str,
    mode: str,
    hole_size: float | None,
    section_length: float,
    min_coverage: float,
    max_missing_formations: int,
    basin_filter: list[str] | None = None,
    target_formations: list[str] | None = None,
    hole_size_tolerance: float = 0.0,
    bha_type: str = "both",
):
    """Run the full per-section pipeline as background steps.

    Steps 1-3 are prerequisites (BHA pull, parse, filter) that only run
    if their outputs don't already exist. Steps 4-8 are the per-section
    analysis pipeline.
    """
    try:
        import json as _json
        import shutil as _shutil

        safe_name = section_name.replace(" ", "_").replace("/", "-")
        hs_str = f"{hole_size}in" if hole_size else "unknown"
        sec_bha_csv = os.path.join(SCRIPT_DIR, f"bhas_{safe_name}_{hs_str}.csv")
        sec_out_dir = os.path.join(SCRIPT_DIR, "sections", safe_name)

        # Clean stale results if they belong to a different asset
        marker_path = os.path.join(sec_out_dir, "_run_info.json")
        if os.path.exists(marker_path):
            try:
                with open(marker_path, encoding="utf-8") as f:
                    marker = _json.load(f)
                if str(marker.get("asset_id")) != str(asset_id):
                    print(f"  Cleaning stale results for {safe_name} "
                          f"(was {marker.get('asset_id')}, now {asset_id})")
                    _shutil.rmtree(sec_out_dir, ignore_errors=True)
            except Exception:
                pass

        os.makedirs(sec_out_dir, exist_ok=True)

        # Write asset marker so we know which asset these results belong to
        with open(marker_path, "w", encoding="utf-8") as f:
            _json.dump({"asset_id": str(asset_id),
                        "section_name": section_name,
                        "hole_size": hole_size,
                        "mode": mode}, f)

        sections_json = os.path.join(SCRIPT_DIR, "target_sections.json")

        # ── Step 1: Pull ALL BHA runs from offset wells (if needed) ──
        run = _db.get_current_run(str(asset_id))
        run_id = run["id"] if run else None
        radius = run.get("search_radius", 15.0) if run else 15.0

        all_bhas_csv = _find_all_bhas_csv()
        if not all_bhas_csv:
            offset_csv = _find_offset_csv(asset_id, radius)

            if not offset_csv:
                jobs.update_job(
                    job_id, status="failed",
                    error="No offset wells CSV found. Pull offsets first.",
                )
                return

            pull_bha_cmd = [
                PYTHON, os.path.join(SCRIPT_DIR, "pull_lateral_bhas.py"),
                offset_csv, "--all-runs",
            ]
            if run_id is not None:
                pull_bha_cmd += ["--run-id", str(run_id)]

            rc, output = await _run_script(
                pull_bha_cmd,
                job_id, 1, "Pulling BHA runs from offset wells...",
            )
            if rc != 0:
                jobs.update_job(
                    job_id, status="failed",
                    error=f"Failed to pull BHA runs: {output[:300]}",
                )
                return
            all_bhas_csv = _find_all_bhas_csv()
            if not all_bhas_csv:
                jobs.update_job(
                    job_id, status="failed",
                    error="BHA pull completed but no all_bhas CSV found.",
                )
                return
        else:
            jobs.update_job(job_id, step=1, progress="BHA runs already pulled",
                            status="running")

        # ── Step 2: Parse bit & motor models ──
        rc, _ = await _run_script(
            [PYTHON, os.path.join(SCRIPT_DIR, "parse_bit_motors.py")],
            job_id, 2, "Parsing bit & motor models...",
        )

        # ── Step 3: Filter BHAs by section (always re-run with current filter params) ──
        if not os.path.exists(sections_json):
            jobs.update_job(
                job_id, status="failed",
                error="target_sections.json not found. Run Pull Offsets first.",
            )
            return

        fm_csv = None
        for candidate in ["formation_tops_canonical.csv",
                          "formation_tops.csv"]:
            p = os.path.join(SCRIPT_DIR, candidate)
            if os.path.exists(p):
                fm_csv = p
                break

        filter_cmd = [
            PYTHON, os.path.join(SCRIPT_DIR, "filter_bhas_by_section.py"),
            sections_json, all_bhas_csv,
            "--hole-size-tolerance", str(hole_size_tolerance),
            "--bha-type", bha_type,
        ]
        if run_id is not None:
            filter_cmd += ["--run-id", str(run_id)]
        if basin_filter:
            filter_cmd += ["--basin-filter", ",".join(basin_filter)]
        if target_formations:
            filter_cmd += ["--target-formations", ",".join(target_formations)]
        if fm_csv:
            filter_cmd += ["--formations", fm_csv]

        rc, output = await _run_script(
            filter_cmd,
            job_id, 3, "Filtering BHAs by section...",
        )

        if not os.path.exists(sec_bha_csv):
            jobs.update_job(
                job_id, status="failed",
                error=f"No BHA runs matched section {section_name} "
                      f"({hs_str}). Filter output:\n{output[:500]}",
            )
            return

        # For vertical mode, refresh formation tops against current offsets
        # before pulling 1ft rows so formation mapping is up to date.
        formation_csv_for_vertical = None
        if mode == "vertical":
            wells_csv_for_formations = _find_offset_csv(asset_id, radius)
            formation_csv_for_vertical = await _ensure_formation_data(
                asset_id, wells_csv_for_formations
            )

        # ── Step 4: Group equivalent BHAs ──
        rc, _ = await _run_script(
            [PYTHON, os.path.join(SCRIPT_DIR, "group_equivalent_bhas.py"),
             sec_bha_csv],
            job_id, 4, "Grouping equivalent BHAs...",
        )

        # ── Step 5: Pull 1ft data ──
        pull_cmd = [
            PYTHON, os.path.join(SCRIPT_DIR, "pull_1ft_for_runs.py"),
            sec_bha_csv,
            "--mode", mode,
            "--output-dir", sec_out_dir,
        ]
        fm_csv = None
        for candidate in ["formation_tops_canonical.csv", "formation_tops.csv"]:
            p = os.path.join(SCRIPT_DIR, candidate)
            if os.path.exists(p):
                fm_csv = p
                break
        if mode == "vertical":
            chosen_fm_csv = formation_csv_for_vertical or fm_csv
            if chosen_fm_csv:
                pull_cmd += ["--formations", chosen_fm_csv]
            # In vertical mode, force a fresh 1ft rebuild for the section so
            # cached unmapped rows do not persist across retries.
            onefoot_cache = os.path.join(sec_out_dir, "rop_1ft_data_vertical.csv")
            try:
                if os.path.exists(onefoot_cache):
                    os.remove(onefoot_cache)
            except OSError:
                pass

        rc, _ = await _run_script(pull_cmd, job_id, 5, "Pulling 1ft data...")
        if rc != 0:
            jobs.update_job(job_id, status="failed",
                            error="Failed to pull 1ft data")
            return

        # ── Step 6: Build ROP curves ──
        if mode == "vertical":
            onefoot_csv = os.path.join(sec_out_dir, "rop_1ft_data_vertical.csv")
        else:
            onefoot_csv = os.path.join(sec_out_dir, "rop_1ft_data.csv")

        if not os.path.exists(onefoot_csv):
            jobs.update_job(job_id, status="failed",
                            error=f"1ft data file not found: {onefoot_csv}")
            return

        build_cmd = [
            PYTHON, os.path.join(SCRIPT_DIR, "build_rop_curves.py"),
            onefoot_csv,
            "--mode", mode,
            "--section-length", str(section_length),
            "--output-dir", sec_out_dir,
        ]
        if mode == "vertical":
            build_cmd += ["--max-missing-formations",
                          str(max_missing_formations)]

        rc, _ = await _run_script(build_cmd, job_id, 6,
                                  "Building ROP curves...")
        if rc != 0:
            jobs.update_job(job_id, status="failed",
                            error="Failed to build ROP curves")
            return

        # ── Step 7: Plot charts ──
        chart_out = os.path.join(sec_out_dir, "charts")
        os.makedirs(chart_out, exist_ok=True)
        section_label = f"{section_name} ({hs_str})"

        rc, _ = await _run_script(
            [PYTHON, os.path.join(SCRIPT_DIR, "plot_type_curves.py"),
             "--mode", mode,
             "--data-dir", sec_out_dir,
             "--output-dir", chart_out,
             "--section-label", section_label],
            job_id, 7, "Generating charts...",
        )
        if rc != 0:
            jobs.update_job(job_id, status="failed",
                            error="Failed to generate charts")
            return

        # Wait briefly for artifact files to land before reporting completion.
        artifact_ready = False
        for _ in range(10):
            has_png = False
            if os.path.isdir(chart_out):
                has_png = any(
                    fname.lower().endswith(".png")
                    for fname in os.listdir(chart_out)
                )
            has_ttd = (
                os.path.exists(os.path.join(sec_out_dir, "ttd_ranking.csv"))
                or os.path.exists(os.path.join(sec_out_dir, "ttd_ranking_vertical.csv"))
            )
            if has_png or has_ttd:
                artifact_ready = True
                break
            await asyncio.sleep(0.5)

        if not artifact_ready:
            jobs.update_job(
                job_id,
                status="failed",
                error="Analysis finished but no result artifacts were generated",
            )
            return

        # ── Step 8: Done ──
        jobs.update_job(job_id, step=8, status="completed",
                        progress="Analysis complete",
                        section_name=safe_name)

    except Exception as exc:
        jobs.update_job(job_id, status="failed", error=str(exc))
