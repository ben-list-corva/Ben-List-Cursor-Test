"""Routes for well analysis and offset well discovery."""

import os
import sys
import csv
import json as _json
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..models import (
    AnalyzeWellRequest,
    AnalyzeWellResponse,
    WellSection,
    OffsetWellsResponse,
    OffsetWell,
    OffsetFilterOptions,
    CanonicalFormation,
    CanonicalFormationsResponse,
)
from ..services import pipeline

# Import db module from bha_selection root
if pipeline.SCRIPT_DIR not in sys.path:
    sys.path.insert(0, pipeline.SCRIPT_DIR)
import db as _db  # noqa: E402

router = APIRouter(prefix="/api", tags=["wells"])

SCRIPT_DIR = pipeline.SCRIPT_DIR


@router.post("/analyze-well", response_model=AnalyzeWellResponse)
async def analyze_well(req: AnalyzeWellRequest):
    """Call analyze_target_well.py and return discovered sections."""
    import traceback as _tb
    try:
        result = await pipeline.analyze_well(
            req.asset_id,
            search_radius_miles=req.search_radius_miles,
            spud_date_filter=req.spud_date_filter,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}\n{''.join(_tb.format_exception(exc))}"
        )

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    sections = []
    for s in result.get("sections", []):
        sections.append(
            WellSection(
                name=s.get("name", "Unknown"),
                hole_size=s.get("hole_size"),
                mode=s.get("mode", "vertical"),
                top_md=s.get("top_md", 0),
                bottom_md=s.get("bottom_md", 0),
                section_length_md=s.get("section_length_md", 0),
                formations_in_section=s.get("formations_in_section", []),
                start_formation=s.get("start_formation"),
                end_formation=s.get("end_formation"),
                top_tvd=s.get("top_tvd"),
                bottom_tvd=s.get("bottom_tvd"),
            )
        )

    well_name = result.get("well_name",
                          result.get("target_well_name",
                          result.get("target_well", "Unknown")))

    return AnalyzeWellResponse(
        target_asset_id=req.asset_id,
        well_name=well_name,
        sections=sections,
    )


def _read_wells_from_csv(csv_path: str, hole_size: float = 0) -> tuple[int, list[OffsetWell]]:
    """Parse an offset wells or filtered BHA CSV into OffsetWell objects."""
    wells_list: list[OffsetWell] = []
    total = 0
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total = len(rows)
            seen_wells: dict[str, dict] = {}
            for row in rows:
                aid = row.get("asset_id", "")
                if aid not in seen_wells:
                    seen_wells[aid] = {
                        "asset_id": aid,
                        "well_name": row.get("well_name", ""),
                        "operator": row.get("operator", "N/A"),
                        "distance_miles": row.get("distance_miles", "N/A"),
                        "runs": 0,
                    }
                seen_wells[aid]["runs"] += 1

            for aid, info in seen_wells.items():
                wells_list.append(
                    OffsetWell(
                        asset_id=info["asset_id"],
                        well_name=info["well_name"],
                        operator=info["operator"],
                        distance_miles=str(info["distance_miles"]),
                        runs=info["runs"],
                        bha_number="",
                        bit_size=str(hole_size),
                        run_length="",
                        formation_coverage="",
                    )
                )
    except Exception:
        pass
    return total, wells_list


def _wells_from_db(run_id: int, section_name: str | None = None,
                   hole_size: float = 0) -> tuple[int, list[OffsetWell]]:
    """Read offset wells from the database."""
    wells_list: list[OffsetWell] = []

    # Try section-specific BHA data first
    if section_name:
        candidate_names = [section_name]
        safe_name = section_name.replace(" ", "_").replace("/", "-")
        if safe_name != section_name:
            candidate_names.append(safe_name)

        for candidate in candidate_names:
            summary = _db.get_section_bha_summary(run_id, candidate)
            if summary:
                total = sum(w.get("runs", 0) for w in summary)
                for w in summary:
                    wells_list.append(
                        OffsetWell(
                            asset_id=str(w.get("asset_id", "")),
                            well_name=w.get("well_name", ""),
                            operator=w.get("operator", "N/A"),
                            distance_miles=str(w.get("distance_miles", "N/A")),
                            runs=w.get("runs", 0),
                            bha_number="",
                            bit_size=str(hole_size),
                            run_length="",
                            formation_coverage="",
                        )
                    )
                return total, wells_list

    # Fall back to all offset wells
    offset_wells = _db.get_offset_wells(run_id)
    if offset_wells:
        for w in offset_wells:
            wells_list.append(
                OffsetWell(
                    asset_id=str(w.get("asset_id", "")),
                    well_name=w.get("well_name", ""),
                    operator=w.get("operator", "N/A"),
                    distance_miles=str(w.get("distance_miles", "N/A")),
                    runs=0,
                    bha_number="",
                    bit_size=str(hole_size),
                    run_length="",
                    formation_coverage="",
                )
            )
        return len(offset_wells), wells_list

    return 0, []


@router.get("/offset-wells", response_model=OffsetWellsResponse)
async def get_offset_wells(
    section_name: str,
    hole_size: float = 0,
    asset_id: Optional[str] = Query(None, description="Target well asset ID"),
):
    """Return offset well info for a section.

    Uses asset_id to look up the correct analysis run, preventing
    cross-well data contamination.
    """
    run_id = None

    # Look up the run for the specific asset
    if asset_id:
        run = _db.get_current_run(str(asset_id))
        if run:
            run_id = run["id"]

    # Fallback to latest run if no asset_id provided
    if not run_id:
        state = pipeline.get_analysis_state()
        run_id = state.get("run_id")

    # 1. Try database (correctly scoped by run_id)
    if run_id:
        total, wells_list = _wells_from_db(run_id, section_name, hole_size)
        if wells_list:
            return OffsetWellsResponse(
                total=total, filtered=len(wells_list), wells=wells_list,
            )

    return OffsetWellsResponse(total=0, filtered=0, wells=[])


@router.get("/offset-filters", response_model=OffsetFilterOptions)
async def get_offset_filter_options(
    asset_id: Optional[str] = Query(None, description="Target well asset ID"),
):
    """Return distinct basins and target formations from offset wells."""
    target_asset_formation = None
    if asset_id:
        target_asset_formation = _db.get_target_asset_formation(str(asset_id))

    run_id = None
    if asset_id:
        run = _db.get_current_run(str(asset_id))
        if run:
            run_id = run["id"]
    if not run_id:
        state = pipeline.get_analysis_state()
        run_id = state.get("run_id")
    if not run_id:
        return OffsetFilterOptions(
            target_asset_formation=target_asset_formation,
        )

    opts = _db.get_offset_filter_options(run_id)
    return OffsetFilterOptions(
        basins=opts.get("basins", []),
        target_formations=opts.get("target_formations", []),
        target_asset_formation=target_asset_formation,
    )


@router.get("/canonical-formations", response_model=CanonicalFormationsResponse)
async def get_canonical_formations(
    tvd_top: Optional[float] = Query(None, description="Filter: min TVD"),
    tvd_bottom: Optional[float] = Query(None, description="Filter: max TVD"),
    asset_id: Optional[str] = Query(None, description="Target well asset ID"),
):
    """Return canonical formation mappings.

    Reads from the database first, falls back to canonical_map.json.
    """
    # Try database first -- use asset-specific run if available
    run_id = None
    if asset_id:
        run = _db.get_current_run(str(asset_id))
        if run:
            run_id = run["id"]
    if not run_id:
        state = pipeline.get_analysis_state()
        run_id = state.get("run_id")
    if run_id:
        db_formations = _db.get_canonical_formations(run_id, tvd_top, tvd_bottom)
        if db_formations:
            formations: list[CanonicalFormation] = []
            total_raw = 0
            for fm in db_formations:
                subs = fm.get("sub_formations", [])
                total_raw += len(subs)
                formations.append(CanonicalFormation(
                    canonical_name=fm.get("canonical_name", ""),
                    order=fm.get("display_order", 0),
                    tvd_top=fm.get("target_tvd_top"),
                    tvd_bottom=fm.get("target_tvd_bottom"),
                    sub_formations=subs,
                ))
            return CanonicalFormationsResponse(
                formations=formations,
                total_canonical=len(formations),
                total_raw=total_raw,
            )

    # Fall back to canonical_map.json
    map_path = os.path.join(SCRIPT_DIR, "canonical_map.json")
    if not os.path.exists(map_path):
        return CanonicalFormationsResponse()

    try:
        with open(map_path, encoding="utf-8") as f:
            data = _json.load(f)
    except Exception:
        return CanonicalFormationsResponse()

    raw_formations = data.get("canonical_formations", [])
    formations = []
    total_raw = 0

    for fm in raw_formations:
        fm_tvd_top = fm.get("target_tvd_top")
        fm_tvd_bottom = fm.get("target_tvd_bottom")

        if tvd_top is not None and fm_tvd_bottom is not None:
            if fm_tvd_bottom < tvd_top:
                continue
        if tvd_bottom is not None and fm_tvd_top is not None:
            if fm_tvd_top > tvd_bottom:
                continue

        subs = fm.get("target_sub_formations", [])
        total_raw += len(subs)
        formations.append(CanonicalFormation(
            canonical_name=fm.get("canonical_name", ""),
            order=fm.get("order", 0),
            tvd_top=fm_tvd_top,
            tvd_bottom=fm_tvd_bottom,
            sub_formations=subs,
        ))

    return CanonicalFormationsResponse(
        formations=formations,
        total_canonical=len(formations),
        total_raw=total_raw,
    )
