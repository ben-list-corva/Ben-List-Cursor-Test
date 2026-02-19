"""
Data models for Pipeline Checker results.

These Pydantic models define the structure of API responses
and ensure type safety throughout the backend.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class CheckStatus(str, Enum):
    """Status of a pipeline check."""
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class StreamType(str, Enum):
    """Types of completion streams."""
    FRAC = "frac"
    WIRELINE = "wireline"
    PUMPDOWN = "pumpdown"


class PadConfigType(str, Enum):
    """Pad frac configuration type."""
    ZIPPER = "zipper"
    SIMULFRAC = "simulfrac"
    UNKNOWN = "unknown"


class StreamStatus(str, Enum):
    """Status of a stream."""
    ACTIVE = "active"
    IDLE = "idle"
    MISSING = "missing"
    UNKNOWN = "unknown"


class StreamSettings(BaseModel):
    """Source App settings from app_connections."""
    api_number: Optional[str] = None
    force_start_from: Optional[str | int] = None  # Can be timestamp (int) or string
    stream_api_root_url: Optional[str] = None
    stream_api_log_path: Optional[str] = None
    stream_api_key_masked: Optional[str] = None


class SourceAppInfo(BaseModel):
    """Information about a Source App connection."""
    app_id: int
    app_name: str
    status: str = "unknown"
    settings: Optional[StreamSettings] = None
    check_status: CheckStatus = CheckStatus.PASS
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    is_manual_pumpdown: bool = False  # True if pumpdown is routed through frac streambox


class StreamResult(BaseModel):
    """Result for a single stream (Frac/Wireline/Pumpdown)."""
    stream_id: Optional[int] = None
    stream_type: StreamType
    stream_name: Optional[str] = None
    stream_status: StreamStatus = StreamStatus.MISSING
    connected_app_ids: List[int] = Field(default_factory=list)
    connected_app_names: List[str] = Field(default_factory=list)
    source_app: Optional[SourceAppInfo] = None
    check_status: CheckStatus = CheckStatus.FAIL
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class StageInfo(BaseModel):
    """Information about a single stage."""
    stage_number: int
    stage_action: Optional[str] = None
    stage_start: Optional[str] = None
    sb_id: Optional[str] = None
    status: str = "unknown"


class StageStatus(BaseModel):
    """Stage status summary."""
    has_stages: bool = False
    has_active_stage: bool = False
    active_stage_number: Optional[int] = None
    active_stage_action: Optional[str] = None
    sb_id: Optional[str] = None
    stage_start: Optional[str | int] = None  # Can be timestamp (int) or ISO string
    check_status: CheckStatus = CheckStatus.FAIL
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class StreamPlatformCheck(BaseModel):
    """Result of Stream Platform well lookup."""
    check_status: CheckStatus = CheckStatus.FAIL
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class ScheduleCheck(BaseModel):
    """Pumping schedule check results (informational only)."""
    stage_1_has_schedule: Optional[bool] = None
    last_stage_number: Optional[int] = None
    last_stage_has_schedule: Optional[bool] = None


class WellResult(BaseModel):
    """Result for a single well."""
    corva_well_asset_id: int
    well_id: Optional[int] = None  # Corva well ID (from v2/pads)
    well_name: str
    api_number: Optional[str] = None
    color: Optional[str] = None  # Wellhead color from custom_properties
    line_assignment: Optional[str] = None  # For SimulFrac: "Line A", "Line B", etc.
    corva_streams: Dict[str, Optional[StreamResult]] = Field(
        default_factory=lambda: {"frac": None, "wireline": None, "pumpdown": None}
    )
    stream_platform_well_id: Optional[str] = None
    stream_platform_well_name: Optional[str] = None  # Name from Stream Platform
    stream_platform_check: StreamPlatformCheck = Field(default_factory=StreamPlatformCheck)
    stage_status: Optional[StageStatus] = None
    schedule_check: Optional[ScheduleCheck] = None  # Pumping schedule check (informational)
    overall_status: CheckStatus = CheckStatus.FAIL
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class ViewerStreamResult(BaseModel):
    """Result for a viewer stream check."""
    stream_id: Optional[int] = None
    stream_type: StreamType
    stream_name: Optional[str] = None
    stream_status: StreamStatus = StreamStatus.MISSING
    connected_app_ids: List[int] = Field(default_factory=list)
    connected_app_names: List[str] = Field(default_factory=list)
    source_app: Optional[SourceAppInfo] = None
    check_status: CheckStatus = CheckStatus.FAIL
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class ViewerResult(BaseModel):
    """Result for the viewer asset check."""
    viewer_asset_id: Optional[int] = None
    viewer_name: Optional[str] = None
    viewer_status: Optional[str] = None
    viewer_pad_id: Optional[int] = None
    frac_fleet_id: Optional[str] = None
    frac_fleet_name: Optional[str] = None
    line_name: Optional[str] = None  # For SimulFrac: "Line A", "Line B", etc.
    api_number: Optional[str] = None  # From viewer's Source App settings
    streams: Dict[str, Optional[ViewerStreamResult]] = Field(
        default_factory=lambda: {"frac": None, "wireline": None, "pumpdown": None}
    )
    stream_platform_well_id: Optional[str] = None
    stream_platform_well_name: Optional[str] = None  # Name from Stream Platform
    stream_platform_check: Optional[StreamPlatformCheck] = None
    stage_status: Optional[StageStatus] = None
    check_status: CheckStatus = CheckStatus.FAIL
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class FracFleetLine(BaseModel):
    """Frac fleet line for SimulFrac pads."""
    line_id: int
    name: str  # e.g., "Line A Driver", "Line B Passenger"
    well_ids: List[int] = Field(default_factory=list)  # Corva well IDs assigned to this line
    viewer_well_id: Optional[int] = None  # If viewer is assigned to this line


class PadConfiguration(BaseModel):
    """Pad frac configuration (Zipper vs SimulFrac)."""
    config_type: PadConfigType = PadConfigType.UNKNOWN
    frac_fleet_id: Optional[int] = None
    frac_fleet_name: Optional[str] = None
    lines: List[FracFleetLine] = Field(default_factory=list)  # Empty for Zipper, populated for SimulFrac


class StreamPadInfo(BaseModel):
    """Single Stream Platform pad info."""
    stream_pad_id: str
    pad_name: str
    pad_type: str = "well"  # "well" or "viewer"
    active_wells: List[str] = Field(default_factory=list)  # Well names
    company_name: Optional[str] = None
    frac_fleet_name: Optional[str] = None
    frac_sb_id: Optional[str] = None
    wireline_sb_id: Optional[str] = None
    pumpdown_sb_id: Optional[str] = None
    status: Optional[str] = None
    wells_match_corva_pad: bool = True  # False if viewer pad is on a different job
    active_job_warning: Optional[str] = None  # Warning message if wells don't match


class StreamPadCheck(BaseModel):
    """Result of Stream Platform pad lookup and validation."""
    pads: List[StreamPadInfo] = Field(default_factory=list)  # All matching Stream pads
    total_pads_found: int = 0
    well_pads_found: int = 0
    viewer_pads_found: int = 0
    check_status: CheckStatus = CheckStatus.FAIL
    failures: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class PadResult(BaseModel):
    """Result for the entire pad."""
    pad_id: int
    pad_name: str
    configuration: Optional[PadConfiguration] = None  # Zipper vs SimulFrac
    viewers: List[ViewerResult] = Field(default_factory=list)  # Viewer asset check results (can be multiple for SimulFrac)
    wells: List[WellResult] = Field(default_factory=list)
    stream_pad_check: Optional[StreamPadCheck] = None  # Stream Platform pad check
    overall_status: CheckStatus = CheckStatus.FAIL
    total_failures: int = 0
    total_warnings: int = 0
    checked_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# Request/Response models

class PipelineCheckRequest(BaseModel):
    """Request to run pipeline checks."""
    pad_id: int
    well_asset_id: Optional[int] = None


class PipelineCheckResponse(BaseModel):
    """Response from pipeline check."""
    success: bool
    data: Optional[PadResult] = None
    error: Optional[str] = None


# Corva API response models

class CorvaWell(BaseModel):
    """Well from Corva API."""
    id: int = Field(..., alias="asset_id")
    name: str
    api_number: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        populate_by_name = True


class CorvaPad(BaseModel):
    """Pad from Corva API."""
    id: int
    name: str
    wells: List[CorvaWell] = Field(default_factory=list)


class CorvaAppConnection(BaseModel):
    """App connection from stream."""
    app_id: int
    status: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class CorvaStream(BaseModel):
    """Stream from Corva API."""
    id: int
    name: Optional[str] = None
    status: Optional[str] = None
    segment: Optional[str] = None
    source_type: Optional[str] = None  # frac, wireline, pumpdown
    data_source: Optional[str] = None  # historical, live, etc.
    app_connections: List[CorvaAppConnection] = Field(default_factory=list)


class CorvaAsset(BaseModel):
    """Asset from Corva API (v1/assets endpoint - includes viewer assets)."""
    id: int
    name: str
    status: Optional[str] = None
    state: Optional[str] = None
    asset_type: Optional[str] = None
    pad_id: Optional[int] = None
    parent_asset_id: Optional[int] = None
    parent_asset_name: Optional[str] = None
    frac_fleet_id: Optional[str] = None  # From settings
    api_number: Optional[str] = None  # From settings


# Stream Platform API response models

class StreamWell(BaseModel):
    """Well from Stream Platform API."""
    id: str
    api_number: Optional[str] = None
    name: Optional[str] = None


class StreamStage(BaseModel):
    """Stage from Stream Platform API."""
    id: str
    stage_number: int
    status: Optional[str] = None
    stage_action: Optional[str] = None
    stage_start: Optional[str | int] = None  # Can be timestamp (int) or ISO string
    sb_id: Optional[str] = None


class StreamPadWell(BaseModel):
    """Well info embedded in Stream Platform pad response."""
    id: str
    name: Optional[str] = None
    api_number: Optional[str] = None
    status: Optional[str] = None


class StreamPad(BaseModel):
    """Pad from Stream Platform API."""
    id: str
    name: Optional[str] = None
    frac_fleet_name: Optional[str] = None
    company_name: Optional[str] = None
    wells: List[StreamPadWell] = Field(default_factory=list)
    frac_sb_id: Optional[str] = None
    wireline_sb_id: Optional[str] = None
    pumpdown_sb_id: Optional[str] = None
    status: Optional[str] = None
