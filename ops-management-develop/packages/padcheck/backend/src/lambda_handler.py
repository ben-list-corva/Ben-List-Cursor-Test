"""
Lambda handler for Pipeline Checker.

Orchestrates all pipeline validation checks:
A) Corva Pad -> Wells enumeration
B) Corva Well -> Completion Streams
C) Corva Stream -> Source App Settings
D) Stream Platform -> Well Lookup
E) Stream Platform -> Stages Check
"""

import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

from .api.corva_client import CorvaClient, CorvaClientError, get_corva_client
from .api.stream_client import StreamClient, StreamClientError, get_stream_client
from .validators.stream_validator import StreamValidator
from .validators.source_app_validator import SourceAppValidator
from .validators.stage_validator import StageValidator
from .validators.schedule_validator import ScheduleValidator
from .models.types import (
    PadResult,
    WellResult,
    CheckStatus,
    PipelineCheckRequest,
    PipelineCheckResponse,
    StreamPlatformCheck,
    StreamPadCheck,
    StreamPadInfo,
    CorvaStream,
    ViewerResult,
    ViewerStreamResult,
    StreamType,
    StreamStatus,
    PadConfiguration,
    PadConfigType,
    ScheduleCheck,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def compute_overall_status(
    failures: List[str],
    warnings: List[str]
) -> CheckStatus:
    """Compute overall status from failures and warnings."""
    if failures:
        return CheckStatus.FAIL
    elif warnings:
        return CheckStatus.WARN
    return CheckStatus.PASS


def normalize_name(name: str) -> str:
    """Normalize a name for comparison by lowercasing and removing special chars."""
    import re
    # Lowercase and remove special characters except spaces
    normalized = re.sub(r'[^a-z0-9\s]', '', name.lower())
    # Collapse multiple spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


def validate_viewer_name_match(pad_name: str, viewer_name: str) -> tuple[bool, float]:
    """
    Check if the viewer name matches the pad name.
    
    Returns (is_match, similarity_score).
    The viewer name should contain the pad name as a prefix.
    """
    # Normalize both names
    norm_pad = normalize_name(pad_name)
    norm_viewer = normalize_name(viewer_name)
    
    # Check if pad name is contained in viewer name (viewer = "pad name / fleet / viewer")
    if norm_pad in norm_viewer:
        return True, 1.0
    
    # Check word overlap for partial matches
    pad_words = set(norm_pad.split())
    viewer_words = set(norm_viewer.split())
    
    if not pad_words:
        return False, 0.0
    
    # Calculate Jaccard-like similarity
    common_words = pad_words.intersection(viewer_words)
    similarity = len(common_words) / len(pad_words)
    
    # Consider it a match if >70% of pad words are in viewer name
    return similarity >= 0.7, similarity


def extract_line_name_from_viewer(viewer_name: str) -> Optional[str]:
    """
    Extract the line name from a viewer name.
    
    Examples:
    - "Pad / Fleet / Viewer / Line A" -> "Line A"
    - "Pad / Fleet / Viewer / Line B Passenger" -> "Line B Passenger"
    - "Pad / Fleet / Viewer" -> None (no line, zipper config)
    """
    # Split by "/" and look for "Line" in parts after "Viewer"
    parts = [p.strip() for p in viewer_name.split('/')]
    
    viewer_idx = None
    for i, part in enumerate(parts):
        if part.lower() == 'viewer':
            viewer_idx = i
            break
    
    if viewer_idx is not None and viewer_idx + 1 < len(parts):
        # Everything after "Viewer" is the line name
        line_parts = parts[viewer_idx + 1:]
        line_name = ' / '.join(line_parts)
        if line_name:
            return line_name
    
    return None


def validate_single_viewer(
    corva_client: CorvaClient,
    stream_client: Optional['StreamClient'],
    viewer_asset: 'CorvaAsset',
    pad_name: str,
) -> ViewerResult:
    """
    Validate a single viewer asset.
    
    Checks:
    F.1) Viewer Name Match - Validate viewer name matches pad name
    G) Viewer Stream Validation - Check viewer's Frac/WL/PD streams
    H) Viewer → Stream Platform Link - Validate viewer's api_number in Stream
    """
    logger.info(f"Validating viewer: {viewer_asset.name} (id: {viewer_asset.id})")
    
    # Extract line name from viewer name
    line_name = extract_line_name_from_viewer(viewer_asset.name)
    
    # Validate viewer name matches pad name
    name_matches, similarity = validate_viewer_name_match(pad_name, viewer_asset.name)
    if not name_matches:
        logger.warning(f"Viewer name mismatch! Pad: '{pad_name}', Viewer: '{viewer_asset.name}' (similarity: {similarity:.0%})")
        return ViewerResult(
            viewer_asset_id=viewer_asset.id,
            viewer_name=viewer_asset.name,
            viewer_status=viewer_asset.status,
            line_name=line_name,
            check_status=CheckStatus.FAIL,
            failures=[
                f"Viewer name does not match pad name (similarity: {similarity:.0%})",
                f"Expected viewer name to contain: '{pad_name}'",
                f"Found viewer name: '{viewer_asset.name}'",
            ],
            warnings=["Viewer may be configured for a different pad - verify viewer pad assignment"],
        )
    
    viewer_failures: List[str] = []
    viewer_warnings: List[str] = []
    
    # Get frac fleet name if available
    frac_fleet_name = None
    if viewer_asset.frac_fleet_id:
        fleet_info = corva_client.get_frac_fleet(viewer_asset.frac_fleet_id)
        if fleet_info:
            frac_fleet_name = fleet_info.get("name")
    
    # Get viewer streams
    viewer_streams: Dict[str, Optional[ViewerStreamResult]] = {
        "frac": None, "wireline": None, "pumpdown": None
    }
    viewer_api_number: Optional[str] = None
    
    try:
        streams = corva_client.get_well_streams(viewer_asset.id, segment="completion")
        
        for stream in streams:
            # Skip historical streams
            if StreamValidator.is_historical_stream(stream):
                continue
            
            stream_type = StreamValidator.identify_stream_type(stream)
            if not stream_type:
                continue
            
            stream_type_key = stream_type.value
            
            # Get connected app IDs and names from stream
            from .constants import get_app_name
            connected_app_ids = [conn.app_id for conn in stream.app_connections if conn.app_id]
            connected_app_names = [get_app_name(app_id) for app_id in connected_app_ids]
            
            # Check for apps that shouldn't be on viewer streams
            stream_warnings = []
            PAD_METRICS_SCHEDULER_APP_ID = 291
            if PAD_METRICS_SCHEDULER_APP_ID in connected_app_ids:
                stream_warnings.append(f"Pad Metrics Scheduler should not be on viewer streams - check stream configuration")
                logger.warning(f"Viewer stream {stream.name} has Pad Metrics Scheduler (app 291) connected")
            
            # Create viewer stream result
            # Don't warn just for idle status - it's normal for inactive pads
            initial_status = CheckStatus.PASS
            if stream_warnings:
                initial_status = CheckStatus.WARN
            
            stream_result = ViewerStreamResult(
                stream_id=stream.id,
                stream_type=stream_type,
                stream_name=stream.name,
                stream_status=StreamStatus(stream.status) if stream.status else StreamStatus.UNKNOWN,
                connected_app_ids=connected_app_ids,
                connected_app_names=connected_app_names,
                check_status=initial_status,
                warnings=stream_warnings,
            )
            
            # Check source app settings using validate_source_app
            source_app_info = SourceAppValidator.validate_source_app(
                stream, stream_type_key, None  # No well api_number to compare for viewer
            )
            if source_app_info and source_app_info.status != "missing":
                stream_result.source_app = source_app_info
                
                # Get api_number from frac source app (primary)
                if source_app_info.settings and source_app_info.settings.api_number:
                    if stream_type_key == "frac" or not viewer_api_number:
                        viewer_api_number = source_app_info.settings.api_number
                
                # Check for issues
                if source_app_info.check_status == CheckStatus.FAIL:
                    stream_result.check_status = CheckStatus.FAIL
                    stream_result.failures = source_app_info.failures
                elif source_app_info.check_status == CheckStatus.WARN:
                    if stream_result.check_status != CheckStatus.FAIL:
                        stream_result.check_status = CheckStatus.WARN
                    # Extend warnings, don't replace (preserve stream-level warnings)
                    stream_result.warnings.extend(source_app_info.warnings)
            else:
                stream_result.check_status = CheckStatus.FAIL
                stream_result.failures = [f"No source app found for {stream_type_key} stream"]
            
            viewer_streams[stream_type_key] = stream_result
            
            # Collect issues
            viewer_failures.extend(stream_result.failures)
            viewer_warnings.extend(stream_result.warnings)
    
    except CorvaClientError as e:
        logger.error(f"Failed to fetch viewer streams: {e}")
        viewer_failures.append(f"Failed to fetch viewer streams: {str(e)}")
    
    # Use api_number from viewer asset settings if not found in source apps
    if not viewer_api_number:
        viewer_api_number = viewer_asset.api_number
    
    # Validate viewer in Stream Platform
    stream_platform_well_id: Optional[str] = None
    stream_platform_well_name: Optional[str] = None
    stream_platform_check: Optional[StreamPlatformCheck] = None
    stage_status = None
    
    if viewer_api_number and stream_client:
        logger.info(f"Checking viewer in Stream Platform: API {viewer_api_number}")
        
        try:
            stream_wells = stream_client.lookup_well_by_api_number(viewer_api_number)
            stream_platform_well_id, stream_platform_well_name, stream_platform_check = StageValidator.validate_well_lookup(
                stream_wells,
                viewer_api_number,
            )
            
            viewer_failures.extend(stream_platform_check.failures)
            viewer_warnings.extend(stream_platform_check.warnings)
            
            # Check stages if well found
            if stream_platform_well_id:
                try:
                    stages = stream_client.get_well_stages(stream_platform_well_id)
                    # Viewers should have stages - use is_viewer=True for stricter validation
                    stage_status = StageValidator.validate_stages(stages, is_viewer=True)
                    
                    viewer_failures.extend(stage_status.failures)
                    viewer_warnings.extend(stage_status.warnings)
                    
                except Exception as e:
                    logger.error(f"Failed to fetch viewer stages: {e}")
                    viewer_warnings.append(f"Failed to fetch viewer stages: {str(e)}")
        
        except Exception as e:
            logger.error(f"Failed to lookup viewer in Stream Platform: {e}")
            viewer_failures.append(f"Stream Platform lookup failed: {str(e)}")
    
    elif not viewer_api_number:
        viewer_failures.append("No api_number configured for viewer - cannot link to Stream Platform")
    
    elif not stream_client:
        viewer_warnings.append("Stream Platform validation skipped (token not configured)")
    
    # Compute overall viewer status
    overall_status = compute_overall_status(viewer_failures, viewer_warnings)
    
    return ViewerResult(
        viewer_asset_id=viewer_asset.id,
        viewer_name=viewer_asset.name,
        viewer_status=viewer_asset.status,
        viewer_pad_id=viewer_asset.pad_id,
        frac_fleet_id=viewer_asset.frac_fleet_id,
        frac_fleet_name=frac_fleet_name,
        line_name=line_name,
        api_number=viewer_api_number,
        streams=viewer_streams,
        stream_platform_well_id=stream_platform_well_id,
        stream_platform_well_name=stream_platform_well_name,
        stream_platform_check=stream_platform_check,
        stage_status=stage_status,
        check_status=overall_status,
        failures=viewer_failures,
        warnings=viewer_warnings,
    )


def validate_viewers(
    corva_client: CorvaClient,
    stream_client: Optional['StreamClient'],
    pad_name: str,
) -> List[ViewerResult]:
    """
    Find and validate ALL viewer assets for a pad.
    
    For SimulFrac pads, multiple viewers may exist (one per line).
    For Zipper pads, typically one viewer.
    
    Returns:
        List of ViewerResult objects, one per discovered viewer.
        Returns empty list if no viewers found.
    """
    logger.info(f"Searching for viewers for pad: {pad_name}")
    
    # Search for all viewer assets by pad name
    viewer_assets = corva_client.search_viewers_for_pad(pad_name)
    
    if not viewer_assets:
        logger.warning(f"No viewer assets found for pad: {pad_name}")
        return []
    
    logger.info(f"Found {len(viewer_assets)} viewer(s) for pad: {pad_name}")
    
    # Validate each viewer
    viewer_results: List[ViewerResult] = []
    for viewer_asset in viewer_assets:
        result = validate_single_viewer(
            corva_client=corva_client,
            stream_client=stream_client,
            viewer_asset=viewer_asset,
            pad_name=pad_name,
        )
        viewer_results.append(result)
    
    return viewer_results


def run_pipeline_check(
    pad_id: int,
    well_asset_id: Optional[int] = None
) -> PadResult:
    """
    Run all pipeline checks for a pad (and optionally a specific well).
    
    This function orchestrates checks A-E as specified in the requirements.
    """
    logger.info(f"Starting pipeline check for pad {pad_id}, well {well_asset_id}")
    
    # Initialize clients
    corva_client = get_corva_client()
    
    # Try to initialize Stream client (may fail if token not configured)
    stream_client: Optional[StreamClient] = None
    try:
        stream_client = get_stream_client()
    except StreamClientError as e:
        logger.warning(f"Stream client not available: {e}")
    
    # ========================================
    # Check A: Get pad and wells
    # ========================================
    logger.info("Check A: Fetching pad and wells")
    
    try:
        pad = corva_client.get_pad(pad_id)
        pad_name = pad.name
    except CorvaClientError as e:
        logger.error(f"Failed to fetch pad: {e}")
        return PadResult(
            pad_id=pad_id,
            pad_name=f"Pad {pad_id}",
            wells=[],
            overall_status=CheckStatus.FAIL,
            total_failures=1,
            total_warnings=0,
            checked_at=datetime.utcnow().isoformat(),
        )
    
    # Get wells
    try:
        if well_asset_id:
            # Single well mode
            well = corva_client.get_well(well_asset_id)
            wells = [well]
        else:
            # All wells on pad
            wells = corva_client.get_pad_wells(pad_id)
    except CorvaClientError as e:
        logger.error(f"Failed to fetch wells: {e}")
        return PadResult(
            pad_id=pad_id,
            pad_name=pad_name,
            wells=[],
            overall_status=CheckStatus.FAIL,
            total_failures=1,
            total_warnings=0,
            checked_at=datetime.utcnow().isoformat(),
        )
    
    if not wells:
        logger.warning("No wells found on pad")
        return PadResult(
            pad_id=pad_id,
            pad_name=pad_name,
            wells=[],
            overall_status=CheckStatus.FAIL,
            total_failures=1,
            total_warnings=0,
            checked_at=datetime.utcnow().isoformat(),
        )
    
    logger.info(f"Found {len(wells)} wells to check")
    
    # ========================================
    # Fetch pad configuration (Zipper vs SimulFrac)
    # ========================================
    logger.info("Fetching pad configuration (Zipper vs SimulFrac)")
    
    pad_config: Optional[PadConfiguration] = None
    try:
        pad_config = corva_client.get_pad_configuration(pad_id)
        if pad_config:
            logger.info(f"Pad configuration: {pad_config.config_type.value}")
            if pad_config.lines:
                for line in pad_config.lines:
                    logger.info(f"  {line.name}: {len(line.well_ids)} wells")
    except Exception as e:
        logger.warning(f"Failed to fetch pad configuration: {e}")
    
    # ========================================
    # Fetch detailed well info (for colors)
    # ========================================
    logger.info("Fetching detailed well info (colors)")
    
    well_details: Dict[int, Dict[str, Any]] = {}  # well_id -> details
    try:
        detailed_wells = corva_client.get_pad_wells_detailed(pad_id)
        for dw in detailed_wells:
            well_id = dw.get("well_id")
            if well_id:
                well_details[well_id] = dw
                # Also map by asset_id for lookups
                asset_id = dw.get("asset_id")
                if asset_id:
                    well_details[asset_id] = dw
    except Exception as e:
        logger.warning(f"Failed to fetch detailed well info: {e}")
    
    # Build well_id -> line_name mapping from configuration
    well_line_assignments: Dict[int, str] = {}
    if pad_config and pad_config.config_type == PadConfigType.SIMULFRAC:
        for line in pad_config.lines:
            for wid in line.well_ids:
                well_line_assignments[wid] = line.name
    
    # ========================================
    # Check F: Find and validate viewer assets
    # ========================================
    logger.info("Check F: Searching for viewer assets")
    
    viewer_results = validate_viewers(
        corva_client=corva_client,
        stream_client=stream_client,
        pad_name=pad_name,
    )
    
    logger.info(f"Found {len(viewer_results)} viewer(s)")
    
    # Process each well
    well_results: List[WellResult] = []
    total_failures = 0
    total_warnings = 0
    
    for well in wells:
        logger.info(f"Processing well {well.name} ({well.id})")
        
        well_failures: List[str] = []
        well_warnings: List[str] = []
        
        # ========================================
        # Check B: Get completion streams for well
        # ========================================
        logger.info(f"Check B: Fetching streams for well {well.id}")
        
        streams: List[CorvaStream] = []
        streams_by_type: Dict[str, CorvaStream] = {}
        
        try:
            streams = corva_client.get_well_streams(well.id, segment="completion")
            
            # Index LIVE streams by type (skip historical)
            for stream in streams:
                # Skip historical streams
                if StreamValidator.is_historical_stream(stream):
                    continue
                    
                stream_type = StreamValidator.identify_stream_type(stream)
                if stream_type and stream_type.value not in streams_by_type:
                    streams_by_type[stream_type.value] = stream
                    
        except CorvaClientError as e:
            logger.error(f"Failed to fetch streams for well {well.id}: {e}")
            well_failures.append(f"Failed to fetch streams: {str(e)}")
        
        # Validate streams
        stream_results = StreamValidator.validate_streams(streams)
        
        # ========================================
        # Check C: Validate Source App settings
        # ========================================
        logger.info(f"Check C: Validating source apps for well {well.id}")
        
        for stream_type, stream_result in stream_results.items():
            if stream_result:
                stream = streams_by_type.get(stream_type)
                stream_result = SourceAppValidator.enrich_stream_result(
                    stream_result,
                    stream,
                    well.api_number,
                )
                stream_results[stream_type] = stream_result
                
                # Collect issues
                well_failures.extend(stream_result.failures)
                well_warnings.extend(stream_result.warnings)
        
        # ========================================
        # Checks D & E: Stream Platform validation
        # ========================================
        stream_platform_well_id: Optional[str] = None
        stream_platform_well_name: Optional[str] = None
        stream_platform_check = None
        stage_status = None
        
        # CRITICAL: API number MUST come from Source App settings
        # This is the link to app.stream - manually added during build out
        # Common failure point: API number mismatch between Corva source app and app.stream
        source_app_api_number = None
        source_app_type = None
        
        # Get api_number from Frac source app first (required), then others
        for stream_type in ["frac", "wireline", "pumpdown"]:
            stream_result = stream_results.get(stream_type)
            if stream_result and stream_result.source_app and stream_result.source_app.settings:
                if stream_result.source_app.settings.api_number:
                    source_app_api_number = stream_result.source_app.settings.api_number
                    source_app_type = stream_type
                    logger.info(f"Using api_number from {stream_type} Source App: {source_app_api_number}")
                    break
        
        if source_app_api_number and stream_client:
            # Check D: Look up well in Stream Platform using Source App api_number
            logger.info(f"Check D: Looking up well in Stream Platform by API {source_app_api_number} (from {source_app_type} Source App)")
            
            try:
                stream_wells = stream_client.lookup_well_by_api_number(source_app_api_number)
                stream_platform_well_id, stream_platform_well_name, stream_platform_check = StageValidator.validate_well_lookup(
                    stream_wells,
                    source_app_api_number,
                )
                
                well_failures.extend(stream_platform_check.failures)
                well_warnings.extend(stream_platform_check.warnings)
                
                # Check E: Get stages if well found
                if stream_platform_well_id:
                    logger.info(f"Check E: Fetching stages for Stream well {stream_platform_well_id}")
                    
                    try:
                        stages = stream_client.get_well_stages(stream_platform_well_id)
                        # Wells: no stages is just a warning (pad may not be active yet)
                        stage_status = StageValidator.validate_stages(stages, is_viewer=False)
                        
                        well_failures.extend(stage_status.failures)
                        well_warnings.extend(stage_status.warnings)
                        
                    except StreamClientError as e:
                        logger.error(f"Failed to fetch stages: {e}")
                        well_failures.append(f"Failed to fetch stages: {str(e)}")
                        
            except StreamClientError as e:
                logger.error(f"Failed to lookup well in Stream Platform: {e}")
                well_failures.append(f"Stream Platform lookup failed: {str(e)}")
        
        elif not source_app_api_number:
            # No API number in Source App settings - CRITICAL: can't link to Stream Platform
            stream_platform_check = StreamPlatformCheck(
                check_status=CheckStatus.FAIL,
                failures=["No api_number configured in Source App settings - cannot link to Stream Platform"],
                warnings=[],
            )
            well_failures.extend(stream_platform_check.failures)
            
        elif not stream_client:
            # Stream client not available
            stream_platform_check = StreamPlatformCheck(
                check_status=CheckStatus.WARN,
                failures=[],
                warnings=["Stream Platform validation skipped (token not configured)"],
            )
            well_warnings.extend(stream_platform_check.warnings)
        
        # ========================================
        # Schedule Check (Informational)
        # ========================================
        schedule_check: Optional[ScheduleCheck] = None
        
        try:
            logger.info(f"Checking pumping schedules for well {well.id}")
            schedule_check = ScheduleValidator.check_schedules(corva_client, well.id)
            
            # Log schedule status (informational only - doesn't affect overall status)
            if schedule_check.stage_1_has_schedule is not None:
                logger.info(f"  Stage 1 schedule: {'Yes' if schedule_check.stage_1_has_schedule else 'No'}")
            if schedule_check.last_stage_number is not None:
                logger.info(f"  Stage {schedule_check.last_stage_number} schedule: {'Yes' if schedule_check.last_stage_has_schedule else 'No'}")
                
        except Exception as e:
            logger.warning(f"Failed to check schedules for well {well.id}: {e}")
            # Don't fail the well check - this is informational only
        
        # Compute well overall status
        overall_status = compute_overall_status(well_failures, well_warnings)
        
        # Count issues for totals
        total_failures += len(well_failures)
        total_warnings += len(well_warnings)
        
        # Get well color and line assignment from detailed info
        well_detail = well_details.get(well.id, {})
        well_color = well_detail.get("color")
        well_id = well_detail.get("well_id")
        
        # Look up line assignment by well_id (not asset_id)
        line_assignment = None
        if well_id:
            line_assignment = well_line_assignments.get(well_id)
        
        # Build well result
        well_result = WellResult(
            corva_well_asset_id=well.id,
            well_id=well_id,
            well_name=well.name,
            api_number=well.api_number,
            color=well_color,
            line_assignment=line_assignment,
            corva_streams=stream_results,
            stream_platform_well_id=stream_platform_well_id,
            stream_platform_well_name=stream_platform_well_name,
            stream_platform_check=stream_platform_check or StreamPlatformCheck(
                check_status=CheckStatus.FAIL,
                failures=["Stream Platform check not performed"],
                warnings=[],
            ),
            stage_status=stage_status,
            schedule_check=schedule_check,
            overall_status=overall_status,
            failures=well_failures,
            warnings=well_warnings,
        )
        
        well_results.append(well_result)
    
    # Add viewer failures/warnings to totals
    for viewer_result in viewer_results:
        total_failures += len(viewer_result.failures)
        total_warnings += len(viewer_result.warnings)
    
    # ========================================
    # Stream Platform Pad Check - Find ALL matching pads
    # ========================================
    stream_pad_check: Optional[StreamPadCheck] = None
    
    if stream_client and pad_name:
        logger.info(f"Checking Stream Platform pads for '{pad_name}'")
        try:
            all_stream_pads = []
            seen_pad_ids = set()
            
            # Search by Corva pad name (finds well pads)
            logger.info(f"Searching Stream pads by pad name: '{pad_name}'")
            stream_pads = stream_client.search_pads(pad_name, limit=20)
            for sp in stream_pads:
                if sp.id not in seen_pad_ids:
                    seen_pad_ids.add(sp.id)
                    all_stream_pads.append(sp)
                    logger.info(f"  Found: {sp.name}")
            
            # Also search by viewer names (finds viewer pads)
            # Viewer pad naming convention: "{Fleet} / Viewer - Server {N}" or "{Fleet} / Viewer - Line {X}"
            viewer_search_done = set()  # Track what we've already searched
            
            # Get fleet name from pad configuration or viewer results
            fleet_names_to_search = set()
            
            # Try pad configuration first
            if pad_config and pad_config.frac_fleet_name:
                fleet_names_to_search.add(pad_config.frac_fleet_name)
                logger.info(f"Using fleet name from pad config: {pad_config.frac_fleet_name}")
            
            # Also check viewer results
            for viewer_result in viewer_results:
                if viewer_result.frac_fleet_name:
                    fleet_names_to_search.add(viewer_result.frac_fleet_name)
                
                # Try to extract fleet name from viewer name pattern: "{Pad} / {Fleet} / Viewer / {Line}"
                if viewer_result.viewer_name:
                    parts = [p.strip() for p in viewer_result.viewer_name.split('/')]
                    # Look for the part before "Viewer"
                    for i, part in enumerate(parts):
                        if 'viewer' in part.lower() and i > 0:
                            potential_fleet = parts[i-1]
                            if potential_fleet and potential_fleet.lower() != pad_name.lower():
                                fleet_names_to_search.add(potential_fleet)
                                logger.info(f"Extracted fleet name from viewer name: {potential_fleet}")
                            break
            
            # Search for viewer pads using each fleet name
            # Build a set of keywords from the Corva pad name for validation
            pad_name_keywords = set()
            for word in pad_name.lower().split():
                if len(word) > 2:  # Skip short words like "/"
                    pad_name_keywords.add(word)
            logger.info(f"Pad name keywords for validation: {pad_name_keywords}")
            
            for fleet_name in fleet_names_to_search:
                if fleet_name in viewer_search_done:
                    continue
                viewer_search_done.add(fleet_name)
                
                # Try both patterns: "Viewer - {Fleet}" and "{Fleet} / Viewer"
                search_patterns = [
                    f"Viewer - {fleet_name}",
                    f"{fleet_name} / Viewer",
                ]
                
                for search_term in search_patterns:
                    logger.info(f"Searching Stream pads by viewer pattern: '{search_term}'")
                    viewer_pads = stream_client.search_pads(search_term, limit=10)
                    
                    for sp in viewer_pads:
                        # Only add if it looks like a viewer pad for this fleet
                        if sp.id not in seen_pad_ids and sp.name:
                            sp_name_lower = sp.name.lower()
                            fleet_lower = fleet_name.lower()
                            
                            # Verify it's actually a viewer pad for this fleet
                            if 'viewer' in sp_name_lower and fleet_lower in sp_name_lower:
                                seen_pad_ids.add(sp.id)
                                all_stream_pads.append(sp)
                                logger.info(f"  Found viewer pad: {sp.name}")
            
            if not all_stream_pads:
                logger.warning(f"No Stream pads found matching '{pad_name}'")
                stream_pad_check = StreamPadCheck(
                    check_status=CheckStatus.FAIL,
                    failures=[f"No Stream pads found for '{pad_name}'"],
                )
                total_failures += 1
            else:
                # Build StreamPadInfo for each pad found
                pad_info_list = []
                well_pad_count = 0
                viewer_pad_count = 0
                
                for sp in all_stream_pads:
                    # Determine if this is a viewer pad or well pad
                    is_viewer = 'viewer' in (sp.name or '').lower()
                    pad_type = "viewer" if is_viewer else "well"
                    
                    if is_viewer:
                        viewer_pad_count += 1
                    else:
                        well_pad_count += 1
                    
                    # Get well names for active wells display
                    active_wells = [w.name for w in sp.wells if w.name]
                    
                    # For viewer pads, check if wells match the Corva pad
                    wells_match = True
                    active_job_warning = None
                    
                    if is_viewer and active_wells:
                        # Check if any well name contains keywords from the Corva pad name
                        found_match = False
                        for well_name in active_wells:
                            well_name_lower = well_name.lower()
                            matching_keywords = sum(1 for kw in pad_name_keywords if kw in well_name_lower)
                            if matching_keywords >= 1:  # At least 1 keyword match
                                found_match = True
                                break
                        
                        if not found_match:
                            wells_match = False
                            active_job_warning = f"Check active job for fleet - viewer may be on different pad"
                            logger.info(f"  Viewer pad '{sp.name}' wells don't match Corva pad '{pad_name}'")
                    
                    pad_info = StreamPadInfo(
                        stream_pad_id=sp.id,
                        pad_name=sp.name or "Unknown",
                        pad_type=pad_type,
                        active_wells=active_wells,
                        company_name=sp.company_name,
                        frac_fleet_name=sp.frac_fleet_name,
                        frac_sb_id=sp.frac_sb_id,
                        wireline_sb_id=sp.wireline_sb_id,
                        pumpdown_sb_id=sp.pumpdown_sb_id,
                        status=sp.status,
                        wells_match_corva_pad=wells_match,
                        active_job_warning=active_job_warning,
                    )
                    pad_info_list.append(pad_info)
                
                logger.info(f"Found {len(pad_info_list)} Stream pads: {well_pad_count} well pads, {viewer_pad_count} viewer pads")
                
                # Validate - check that we have at least one well pad with wells
                pad_failures = []
                pad_warnings = []
                
                if well_pad_count == 0:
                    pad_warnings.append("No well pads found in Stream Platform")
                
                # Check if any pad is missing streamboxes
                pads_without_frac_sb = [p.pad_name for p in pad_info_list if not p.frac_sb_id]
                if pads_without_frac_sb:
                    pad_warnings.append(f"{len(pads_without_frac_sb)} pad(s) missing Frac streambox")
                
                check_status = CheckStatus.PASS
                if pad_failures:
                    check_status = CheckStatus.FAIL
                    total_failures += len(pad_failures)
                elif pad_warnings:
                    check_status = CheckStatus.WARN
                    total_warnings += len(pad_warnings)
                
                stream_pad_check = StreamPadCheck(
                    pads=pad_info_list,
                    total_pads_found=len(pad_info_list),
                    well_pads_found=well_pad_count,
                    viewer_pads_found=viewer_pad_count,
                    check_status=check_status,
                    failures=pad_failures,
                    warnings=pad_warnings,
                )
                
        except StreamClientError as e:
            logger.error(f"Stream pad check failed: {e}")
            stream_pad_check = StreamPadCheck(
                check_status=CheckStatus.FAIL,
                failures=[f"Stream pad lookup failed: {str(e)}"],
            )
            total_failures += 1
    
    # Compute pad overall status (worst across viewers and all wells)
    pad_status = CheckStatus.PASS
    
    # Check viewer statuses
    for viewer_result in viewer_results:
        if viewer_result.check_status == CheckStatus.FAIL:
            pad_status = CheckStatus.FAIL
            break
        elif viewer_result.check_status == CheckStatus.WARN and pad_status != CheckStatus.FAIL:
            pad_status = CheckStatus.WARN
    
    # Check well statuses
    for well_result in well_results:
        if well_result.overall_status == CheckStatus.FAIL:
            pad_status = CheckStatus.FAIL
            break
        elif well_result.overall_status == CheckStatus.WARN and pad_status != CheckStatus.FAIL:
            pad_status = CheckStatus.WARN
    
    # Check stream pad status
    if stream_pad_check and stream_pad_check.check_status == CheckStatus.FAIL:
        pad_status = CheckStatus.FAIL
    elif stream_pad_check and stream_pad_check.check_status == CheckStatus.WARN and pad_status != CheckStatus.FAIL:
        pad_status = CheckStatus.WARN
    
    logger.info(f"Pipeline check complete: {pad_status.value}")
    
    return PadResult(
        pad_id=pad_id,
        pad_name=pad_name,
        configuration=pad_config,
        viewers=viewer_results,
        wells=well_results,
        stream_pad_check=stream_pad_check,
        overall_status=pad_status,
        total_failures=total_failures,
        total_warnings=total_warnings,
        checked_at=datetime.utcnow().isoformat(),
    )


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for Pipeline Checker.
    
    Accepts requests via:
    - Direct invocation with body containing pad_id
    - API Gateway with JSON body
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse request body
        body = event
        if "body" in event:
            if isinstance(event["body"], str):
                body = json.loads(event["body"])
            else:
                body = event["body"]
        
        # Validate request
        request = PipelineCheckRequest(**body)
        
        # Run pipeline check
        result = run_pipeline_check(
            pad_id=request.pad_id,
            well_asset_id=request.well_asset_id,
        )
        
        # Build success response
        response = PipelineCheckResponse(
            success=True,
            data=result,
            error=None,
        )
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": response.model_dump_json(),
        }
        
    except Exception as e:
        logger.exception(f"Pipeline check failed: {e}")
        
        response = PipelineCheckResponse(
            success=False,
            data=None,
            error=str(e),
        )
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": response.model_dump_json(),
        }


# For local development server
if __name__ == "__main__":
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import sys
    
    class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == "/api/pipeline-check":
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)
                
                event = {"body": body.decode("utf-8")}
                result = handler(event, None)
                
                self.send_response(result["statusCode"])
                for key, value in result["headers"].items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(result["body"].encode("utf-8"))
            else:
                self.send_error(404)
        
        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
            self.end_headers()
        
        def do_GET(self):
            if self.path == "/api/health":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "timestamp": datetime.utcnow().isoformat()
                }).encode("utf-8"))
            else:
                self.send_error(404)
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Starting development server on port {port}...")
    HTTPServer(("0.0.0.0", port), RequestHandler).serve_forever()
