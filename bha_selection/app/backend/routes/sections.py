"""Routes for running section analysis and retrieving results."""

import os
import sys
import csv
import asyncio
import json
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import Optional

from ..models import (
    RunSectionRequest,
    RunSectionResponse,
    JobStatus,
    SectionResults,
    ChartInfo,
    TTDEntry,
    TTDBucket,
    MotorSummary,
    BitTTDEntry,
    GroupInfo,
)
from ..services import jobs, pipeline

# Import db module from bha_selection root
if pipeline.SCRIPT_DIR not in sys.path:
    sys.path.insert(0, pipeline.SCRIPT_DIR)
import db as _db  # noqa: E402

router = APIRouter(prefix="/api", tags=["sections"])

SCRIPT_DIR = pipeline.SCRIPT_DIR


def _parse_json_field(raw, default):
    if raw is None:
        return default
    text = str(raw).strip()
    if not text:
        return default
    try:
        return json.loads(text)
    except Exception:
        return default


def _parse_bit_ttd_entries(raw) -> list[BitTTDEntry]:
    parsed = _parse_json_field(raw, [])
    result: list[BitTTDEntry] = []
    if not isinstance(parsed, list):
        return result
    for item in parsed:
        if not isinstance(item, dict):
            continue
        try:
            result.append(BitTTDEntry(
                bit_manufacturer=str(item.get("bit_manufacturer", "")),
                bit_model=str(item.get("bit_model", "")),
                num_runs=int(item.get("num_runs", 0) or 0),
                ttd_hours=float(item.get("ttd_hours", 0) or 0),
                ttd_days=float(item.get("ttd_days", 0) or 0),
            ))
        except (TypeError, ValueError):
            continue
    return result


@router.post("/run-section", response_model=RunSectionResponse)
async def run_section(req: RunSectionRequest, background_tasks: BackgroundTasks):
    """Launch the per-section pipeline as a background task."""
    job_id = jobs.create_job()

    section_length = req.section_length or 10000

    async def _wrapper():
        await pipeline.run_section_pipeline(
            job_id=job_id,
            asset_id=req.asset_id,
            section_name=req.section_name,
            mode=req.mode,
            hole_size=req.hole_size,
            section_length=section_length,
            min_coverage=req.min_coverage,
            max_missing_formations=req.max_missing_formations,
            basin_filter=req.basin_filter,
            target_formations=req.target_formations,
            hole_size_tolerance=req.hole_size_tolerance,
            bha_type=req.bha_type,
        )

    asyncio.get_event_loop().create_task(_wrapper())
    return RunSectionResponse(job_id=job_id)


@router.get("/job/{job_id}/status", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Poll the status of a running pipeline job."""
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatus(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        step=job["step"],
        total_steps=job["total_steps"],
        error=job.get("error"),
    )


def _load_ttd_from_db(section_name: str, asset_id: str | None = None) -> list[TTDEntry]:
    """Load TTD rankings from the database."""
    state = pipeline.get_analysis_state(asset_id)
    run_id = state.get("run_id")
    if not run_id:
        return []

    safe_name = section_name.replace(" ", "_").replace("/", "-")
    rankings = _db.get_ttd_rankings(run_id, safe_name)
    result = []
    for r in rankings:
        ttd_hours = r.get("ttd_hours", 0) or 0
        common_motor_raw = r.get("common_motor")
        common_motor = MotorSummary()
        if isinstance(common_motor_raw, str):
            common_motor_raw = _parse_json_field(common_motor_raw, {})
        if isinstance(common_motor_raw, dict):
            common_motor = MotorSummary(
                motor_diam=str(common_motor_raw.get("motor_diam", "N/A")),
                rotor_lobes=str(common_motor_raw.get("rotor_lobes", "N/A")),
                stator_lobes=str(common_motor_raw.get("stator_lobes", "N/A")),
                stages=str(common_motor_raw.get("stages", "N/A")),
                label=str(common_motor_raw.get("label", "N/A")),
            )
        bit_ttd_rows = _parse_bit_ttd_entries(r.get("bit_ttd_by_mfg_model"))
        fastest_bit = None
        fastest_raw = r.get("fastest_bit")
        if isinstance(fastest_raw, str):
            fastest_raw = _parse_json_field(fastest_raw, {})
        if isinstance(fastest_raw, dict):
            try:
                fastest_bit = BitTTDEntry(
                    bit_manufacturer=str(fastest_raw.get("bit_manufacturer", "")),
                    bit_model=str(fastest_raw.get("bit_model", "")),
                    num_runs=int(fastest_raw.get("num_runs", 0) or 0),
                    ttd_hours=float(fastest_raw.get("ttd_hours", 0) or 0),
                    ttd_days=float(fastest_raw.get("ttd_days", 0) or 0),
                )
            except (TypeError, ValueError):
                fastest_bit = None
        result.append(TTDEntry(
            group_key=r.get("group_key", ""),
            num_runs=int(r.get("num_runs", 0) or 0),
            num_wells=int(r.get("num_wells", 0) or 0),
            ttd_hours=float(ttd_hours),
            ttd_days=round(float(ttd_hours) / 24, 2) if ttd_hours else 0,
            common_motor=common_motor,
            bit_ttd_by_mfg_model=bit_ttd_rows,
            fastest_bit=fastest_bit,
        ))
    return result


def _load_groups_from_db(section_name: str, asset_id: str | None = None) -> list[GroupInfo]:
    """Load equiv BHA group info from the database."""
    state = pipeline.get_analysis_state(asset_id)
    run_id = state.get("run_id")
    if not run_id:
        return []

    safe_name = section_name.replace(" ", "_").replace("/", "-")
    groups = _db.get_equiv_bha_groups(run_id, safe_name)
    return [
        GroupInfo(
            group_key=g.get("group_key", ""),
            num_runs=int(g.get("num_runs", 0) or 0),
            num_wells=int(g.get("num_wells", 0) or 0),
        )
        for g in groups
    ]


@router.get("/results/{section_name}", response_model=SectionResults)
async def get_results(
    section_name: str,
    asset_id: Optional[str] = Query(None, description="Target well asset ID"),
):
    """Return charts and TTD ranking for a completed section analysis.

    If asset_id is provided, verifies that the results belong to that
    asset (via _run_info.json marker). Returns empty results if the
    data belongs to a different asset (prevents stale data display).
    """
    safe_name = section_name.replace(" ", "_").replace("/", "-")
    sec_dir = os.path.join(SCRIPT_DIR, "sections", safe_name)
    chart_dir = os.path.join(sec_dir, "charts")

    # ── Verify asset ownership ──
    if asset_id and os.path.isdir(sec_dir):
        marker_path = os.path.join(sec_dir, "_run_info.json")
        if os.path.exists(marker_path):
            try:
                with open(marker_path, encoding="utf-8") as f:
                    marker = json.load(f)
                if str(marker.get("asset_id")) != str(asset_id):
                    # Results belong to a different asset -- return empty
                    return SectionResults(
                        section_name=section_name,
                        hole_size=None, mode="vertical",
                        charts=[], ttd_ranking=[], groups=[],
                        filtered_runs=0, analyzed_runs=0,
                    )
            except Exception:
                pass
        else:
            # No marker file means results are from an old run
            # (before asset-scoping was added). Treat as stale.
            return SectionResults(
                section_name=section_name,
                hole_size=None, mode="vertical",
                charts=[], ttd_ranking=[], groups=[],
                filtered_runs=0, analyzed_runs=0,
            )

    charts: list[ChartInfo] = []
    if os.path.isdir(chart_dir):
        for fname in sorted(os.listdir(chart_dir)):
            if fname.lower().endswith(".png"):
                chart_name = os.path.splitext(fname)[0]
                charts.append(ChartInfo(
                    name=chart_name,
                    url=f"/static/sections/{safe_name}/charts/{fname}",
                ))

    # TTD ranking: try CSV first, then DB
    ttd_ranking: list[TTDEntry] = []
    ttd_csv = os.path.join(sec_dir, "ttd_ranking.csv")
    if not os.path.exists(ttd_csv):
        ttd_csv = os.path.join(sec_dir, "ttd_ranking_vertical.csv")
    if os.path.exists(ttd_csv):
        try:
            with open(ttd_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        ttd_hours = float(row.get("ttd_hours", 0))
                        is_rss_raw = row.get("is_rss", "False")
                        is_rss = str(is_rss_raw).strip().lower() in ("true", "1", "yes")
                        try:
                            asp = float(row.get("actual_slide_pct") or 0)
                        except (ValueError, TypeError):
                            asp = 0.0
                        common_motor_raw = _parse_json_field(row.get("common_motor"), {})
                        if isinstance(common_motor_raw, dict):
                            common_motor = MotorSummary(
                                motor_diam=str(common_motor_raw.get("motor_diam", "N/A")),
                                rotor_lobes=str(common_motor_raw.get("rotor_lobes", "N/A")),
                                stator_lobes=str(common_motor_raw.get("stator_lobes", "N/A")),
                                stages=str(common_motor_raw.get("stages", "N/A")),
                                label=str(common_motor_raw.get("label", "N/A")),
                            )
                        else:
                            common_motor = MotorSummary()
                        bit_ttd_rows = _parse_bit_ttd_entries(row.get("bit_ttd_by_mfg_model"))
                        fastest_bit = None
                        fastest_raw = _parse_json_field(row.get("fastest_bit"), {})
                        if isinstance(fastest_raw, dict) and fastest_raw:
                            try:
                                fastest_bit = BitTTDEntry(
                                    bit_manufacturer=str(fastest_raw.get("bit_manufacturer", "")),
                                    bit_model=str(fastest_raw.get("bit_model", "")),
                                    num_runs=int(fastest_raw.get("num_runs", 0) or 0),
                                    ttd_hours=float(fastest_raw.get("ttd_hours", 0) or 0),
                                    ttd_days=float(fastest_raw.get("ttd_days", 0) or 0),
                                )
                            except (TypeError, ValueError):
                                fastest_bit = None
                        ttd_ranking.append(TTDEntry(
                            group_key=row.get("group_key", ""),
                            num_runs=int(row.get("num_runs", 0)),
                            num_wells=int(row.get("num_wells", 0)),
                            ttd_hours=ttd_hours,
                            ttd_days=round(ttd_hours / 24, 2),
                            actual_slide_pct=asp,
                            is_rss=is_rss,
                            common_motor=common_motor,
                            bit_ttd_by_mfg_model=bit_ttd_rows,
                            fastest_bit=fastest_bit,
                        ))
                    except Exception as row_exc:
                        continue
        except Exception:
            pass
    if not ttd_ranking:
        ttd_ranking = _load_ttd_from_db(section_name, asset_id)

    # Load per-bucket breakdown and attach to TTD entries
    breakdown_csv = os.path.join(sec_dir, "ttd_breakdown.csv")
    if not os.path.exists(breakdown_csv):
        breakdown_csv = os.path.join(sec_dir, "ttd_breakdown_vertical.csv")
    if os.path.exists(breakdown_csv) and ttd_ranking:
        try:
            from collections import defaultdict
            buckets_by_group: dict[str, list[TTDBucket]] = defaultdict(list)
            with open(breakdown_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    gk = row.get("group_key", "")
                    buckets_by_group[gk].append(TTDBucket(
                        label=row.get("bucket_label", ""),
                        length_ft=float(row.get("bucket_length_ft", 0)),
                        rotary_rop=float(row.get("rotary_rop_p50", 0)),
                        rotary_time=float(row.get("rotary_time_hrs", 0)),
                        slide_rop=float(row.get("slide_rop_p50", 0)),
                        slide_time=float(row.get("slide_time_hrs", 0)),
                        total_time=float(row.get("total_time_hrs", 0)),
                    ))
            for entry in ttd_ranking:
                if entry.group_key in buckets_by_group:
                    entry.buckets = buckets_by_group[entry.group_key]
        except Exception:
            pass

    # Group info: try CSV first, then DB
    groups: list[GroupInfo] = []
    group_csv = os.path.join(sec_dir, "rop_curves_by_group.csv")
    if not os.path.exists(group_csv):
        group_csv = os.path.join(sec_dir, "rop_curves_by_group_vertical.csv")
    if os.path.exists(group_csv):
        try:
            seen: set[str] = set()
            with open(group_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    gk = row.get("group_key", row.get("equiv_bha_key", ""))
                    if gk and gk not in seen:
                        seen.add(gk)
                        groups.append(GroupInfo(
                            group_key=gk,
                            num_runs=int(row.get("num_runs", 0)),
                            num_wells=int(row.get("num_wells", 0)),
                        ))
        except Exception:
            pass
    if not groups:
        groups = _load_groups_from_db(section_name, asset_id)

    # Section metadata: try target_sections.json, then DB
    hole_size = None
    mode = "vertical"
    sections_json = os.path.join(SCRIPT_DIR, "target_sections.json")
    if os.path.exists(sections_json):
        try:
            with open(sections_json, encoding="utf-8") as f:
                sections_data = json.load(f)
            for s in sections_data.get("sections", []):
                s_safe = s.get("name", "").replace(" ", "_").replace("/", "-")
                if s_safe == safe_name:
                    hole_size = s.get("hole_size")
                    mode = s.get("mode", "vertical")
                    break
        except Exception:
            pass

    if hole_size is None:
        state = pipeline.get_analysis_state(asset_id)
        run_id = state.get("run_id")
        if run_id:
            sections = _db.get_target_sections(run_id)
            for s in sections:
                s_safe = s.get("name", "").replace(" ", "_").replace("/", "-")
                if s_safe == safe_name:
                    hole_size = s.get("hole_size")
                    mode = s.get("mode", "vertical")
                    break

    # ── Run count breakdown ──
    filtered_runs = 0
    runs_with_data = 0
    runs_in_curves = 0
    analyzed_runs = sum(e.num_runs for e in ttd_ranking)

    # Count section-filtered BHA runs from CSV
    sec_bha_csv = os.path.join(
        SCRIPT_DIR, f"bhas_{safe_name}_{hole_size}in.csv" if hole_size else ""
    )
    if os.path.exists(sec_bha_csv):
        try:
            with open(sec_bha_csv, "r", encoding="utf-8") as f:
                filtered_runs = sum(1 for _ in csv.reader(f)) - 1  # minus header
        except Exception:
            pass

    # Fallback: count from DB
    if not filtered_runs and asset_id:
        state = pipeline.get_analysis_state(asset_id)
        run_id = state.get("run_id")
        if run_id:
            summary = _db.get_section_bha_summary(run_id, safe_name)
            filtered_runs = sum(w.get("runs", 0) for w in summary)

    # Count runs with 1ft WITS data
    ft_suffix = "_vertical" if mode == "vertical" else ""
    ft_data = os.path.join(sec_dir, f"rop_1ft_data{ft_suffix}.csv")
    if os.path.exists(ft_data):
        try:
            unique_runs = set()
            with open(ft_data, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    unique_runs.add(
                        f"{row.get('asset_id', '')}_{row.get('bha_number', '')}"
                    )
            runs_with_data = len(unique_runs)
        except Exception:
            pass

    # Count runs that contributed to per-run curves
    per_run_csv = os.path.join(sec_dir, f"rop_curves_per_run{ft_suffix}.csv")
    if os.path.exists(per_run_csv):
        try:
            curve_runs = set()
            with open(per_run_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    curve_runs.add(
                        f"{row.get('asset_id', '')}_{row.get('bha_number', '')}"
                    )
            runs_in_curves = len(curve_runs)
        except Exception:
            pass

    return SectionResults(
        section_name=section_name,
        hole_size=hole_size,
        mode=mode,
        charts=charts,
        ttd_ranking=ttd_ranking,
        groups=groups,
        filtered_runs=filtered_runs,
        runs_with_data=runs_with_data,
        runs_in_curves=runs_in_curves,
        analyzed_runs=analyzed_runs,
    )
