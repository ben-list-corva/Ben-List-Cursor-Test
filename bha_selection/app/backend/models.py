"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional


class AnalyzeWellRequest(BaseModel):
    asset_id: str
    search_radius_miles: float = 15.0
    spud_date_filter: Optional[str] = None  # ISO date string cutoff, e.g. "2025-02-01"


class WellSection(BaseModel):
    name: str
    hole_size: Optional[float] = None
    mode: str = "vertical"
    top_md: float = 0
    bottom_md: float = 0
    section_length_md: float = 0
    formations_in_section: list[str] = []
    start_formation: Optional[str] = None
    end_formation: Optional[str] = None
    top_tvd: Optional[float] = None
    bottom_tvd: Optional[float] = None


class AnalyzeWellResponse(BaseModel):
    target_asset_id: str
    well_name: str
    sections: list[WellSection]


class OffsetWell(BaseModel):
    asset_id: str
    well_name: str
    operator: str = "N/A"
    distance_miles: str = "N/A"
    runs: int = 0
    bha_number: str = ""
    bit_size: str = ""
    run_length: str = ""
    formation_coverage: str = ""


class OffsetWellsResponse(BaseModel):
    total: int
    filtered: int
    wells: list[OffsetWell]


class RunSectionRequest(BaseModel):
    asset_id: str
    section_name: str
    mode: str = "vertical"
    hole_size: Optional[float] = None
    min_coverage: float = 0.5
    max_missing_formations: int = 1
    section_length: Optional[float] = None
    target_formations: Optional[list[str]] = None
    basin_filter: Optional[list[str]] = None
    hole_size_tolerance: float = 0.0
    bha_type: str = "conventional"


class RunSectionResponse(BaseModel):
    job_id: str


class JobStatus(BaseModel):
    job_id: str
    status: str = "pending"
    progress: str = ""
    step: int = 0
    total_steps: int = 5
    error: Optional[str] = None


class ChartInfo(BaseModel):
    name: str
    url: str


class TTDBucket(BaseModel):
    label: str
    length_ft: float = 0
    rotary_rop: float = 0
    rotary_time: float = 0
    slide_rop: float = 0
    slide_time: float = 0
    total_time: float = 0


class MotorSummary(BaseModel):
    motor_diam: str = "N/A"
    rotor_lobes: str = "N/A"
    stator_lobes: str = "N/A"
    stages: str = "N/A"
    label: str = "N/A"


class BitTTDEntry(BaseModel):
    bit_manufacturer: str = ""
    bit_model: str = ""
    num_runs: int = 0
    ttd_hours: float = 0
    ttd_days: float = 0


class TTDEntry(BaseModel):
    group_key: str
    num_runs: int = 0
    num_wells: int = 0
    ttd_hours: float = 0
    ttd_days: float = 0
    actual_slide_pct: float = 0
    is_rss: bool = False
    common_motor: MotorSummary = MotorSummary()
    bit_ttd_by_mfg_model: list[BitTTDEntry] = []
    fastest_bit: Optional[BitTTDEntry] = None
    buckets: list[TTDBucket] = []


class GroupInfo(BaseModel):
    group_key: str
    num_runs: int = 0
    num_wells: int = 0


class SectionResults(BaseModel):
    section_name: str
    hole_size: Optional[float] = None
    mode: str = "vertical"
    charts: list[ChartInfo] = []
    ttd_ranking: list[TTDEntry] = []
    groups: list[GroupInfo] = []
    filtered_runs: int = 0
    runs_with_data: int = 0
    runs_in_curves: int = 0
    analyzed_runs: int = 0


class OffsetFilterOptions(BaseModel):
    basins: list[str] = []
    target_formations: list[str] = []
    target_asset_formation: Optional[str] = None


class CanonicalFormation(BaseModel):
    canonical_name: str
    order: int = 0
    tvd_top: Optional[float] = None
    tvd_bottom: Optional[float] = None
    sub_formations: list[str] = []


class CanonicalFormationsResponse(BaseModel):
    formations: list[CanonicalFormation] = []
    total_canonical: int = 0
    total_raw: int = 0
