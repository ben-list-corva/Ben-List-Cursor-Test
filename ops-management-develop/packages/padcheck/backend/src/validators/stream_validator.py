"""
Stream validator.

Validates Corva streams for wells:
- Check B: Stream exists for each type
- Stream status (active/idle)
"""

import logging
from typing import List, Optional, Dict, Tuple

from ..models.types import (
    StreamResult,
    StreamType,
    StreamStatus,
    CheckStatus,
    CorvaStream,
)
from ..constants import (
    SOURCE_APP_IDS,
    REQUIRED_STREAM_TYPES,
    OPTIONAL_STREAM_TYPES,
    SILENT_STREAM_TYPES,
    get_app_name,
)

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


class StreamValidator:
    """Validates Corva streams for a well."""
    
    @staticmethod
    def identify_stream_type(stream: CorvaStream) -> Optional[StreamType]:
        """
        Identify the stream type based on source_type, name, or connected apps.
        
        Returns the StreamType if identifiable, None otherwise.
        """
        # First check source_type field (most reliable)
        if hasattr(stream, 'source_type') and stream.source_type:
            source_type_lower = stream.source_type.lower()
            if source_type_lower == "frac":
                return StreamType.FRAC
            elif source_type_lower in ("wireline", "wl"):
                return StreamType.WIRELINE
            elif source_type_lower in ("pumpdown", "pd"):
                return StreamType.PUMPDOWN
        
        # Check stream name for type hints
        if stream.name:
            name_lower = stream.name.lower()
            if "frac" in name_lower:
                return StreamType.FRAC
            elif "wireline" in name_lower or "wl" in name_lower:
                return StreamType.WIRELINE
            elif "pumpdown" in name_lower or "pd" in name_lower:
                return StreamType.PUMPDOWN
        
        # Check connected source apps
        for conn in stream.app_connections:
            if conn.app_id == SOURCE_APP_IDS["frac"]:
                return StreamType.FRAC
            elif conn.app_id == SOURCE_APP_IDS["wireline"]:
                return StreamType.WIRELINE
            elif conn.app_id == SOURCE_APP_IDS["pumpdown"]:
                return StreamType.PUMPDOWN
        
        return None
    
    @staticmethod
    def validate_stream(
        stream: CorvaStream,
        stream_type: StreamType,
        is_required: bool = False
    ) -> StreamResult:
        """
        Validate a single stream.
        
        Checks:
        - Stream exists
        - Stream status is active (WARN if idle)
        """
        failures: List[str] = []
        warnings: List[str] = []
        
        # Determine stream status
        stream_status = StreamStatus.ACTIVE
        if stream.status:
            status_lower = stream.status.lower()
            if status_lower == "active":
                stream_status = StreamStatus.ACTIVE
            elif status_lower in ("idle", "inactive"):
                stream_status = StreamStatus.IDLE
            else:
                stream_status = StreamStatus.UNKNOWN
        
        # Only warn for unknown status - idle is normal for inactive pads
        if stream_status == StreamStatus.UNKNOWN:
            warnings.append(f"Stream status is unknown: {stream.status}")
        
        # Get connected app info
        connected_app_ids = [conn.app_id for conn in stream.app_connections]
        connected_app_names = [get_app_name(app_id) for app_id in connected_app_ids]
        
        # Determine overall check status
        if failures:
            check_status = CheckStatus.FAIL
        elif warnings:
            check_status = CheckStatus.WARN
        else:
            check_status = CheckStatus.PASS
        
        return StreamResult(
            stream_id=stream.id,
            stream_type=stream_type,
            stream_name=stream.name,
            stream_status=stream_status,
            connected_app_ids=connected_app_ids,
            connected_app_names=connected_app_names,
            source_app=None,  # Will be filled by SourceAppValidator
            check_status=check_status,
            failures=failures,
            warnings=warnings,
        )
    
    @staticmethod
    def is_historical_stream(stream: CorvaStream) -> bool:
        """Check if a stream is historical (not live)."""
        if hasattr(stream, 'data_source') and stream.data_source:
            return stream.data_source.lower() == "historical"
        return False
    
    @staticmethod
    def validate_streams(
        streams: List[CorvaStream],
    ) -> Dict[str, Optional[StreamResult]]:
        """
        Validate all streams for a well.
        
        Groups streams by type and validates each.
        Only validates LIVE streams - historical streams are noted but not checked.
        Returns dict mapping stream type to StreamResult.
        """
        results: Dict[str, Optional[StreamResult]] = {
            "frac": None,
            "wireline": None,
            "pumpdown": None,
        }
        
        # Separate live and historical streams
        live_streams_by_type: Dict[str, CorvaStream] = {}
        historical_streams: List[CorvaStream] = []
        
        for stream in streams:
            stream_type = StreamValidator.identify_stream_type(stream)
            
            if StreamValidator.is_historical_stream(stream):
                # Track historical streams but don't validate
                historical_streams.append(stream)
                logger.info(f"Found historical stream: {stream.name} (type: {stream_type})")
                continue
            
            if stream_type:
                # Use the first live stream of each type found
                if stream_type.value not in live_streams_by_type:
                    live_streams_by_type[stream_type.value] = stream
        
        # Log historical streams found
        if historical_streams:
            logger.info(f"Found {len(historical_streams)} historical stream(s) - skipping validation")
        
        # Validate each live stream type
        for type_name in ["frac", "wireline", "pumpdown"]:
            is_required = type_name in REQUIRED_STREAM_TYPES
            is_optional = type_name in OPTIONAL_STREAM_TYPES
            is_silent = type_name in SILENT_STREAM_TYPES
            
            if type_name in live_streams_by_type:
                stream = live_streams_by_type[type_name]
                results[type_name] = StreamValidator.validate_stream(
                    stream,
                    StreamType(type_name),
                    is_required=is_required,
                )
            else:
                # Live stream not found
                failures = []
                warnings = []
                
                if is_required:
                    failures.append(f"Live {type_name.capitalize()} stream not found")
                    check_status = CheckStatus.FAIL
                elif is_optional:
                    warnings.append(f"Live {type_name.capitalize()} stream not configured")
                    check_status = CheckStatus.WARN
                else:
                    # Silent stream types (like pumpdown) - no warning, just PASS
                    check_status = CheckStatus.PASS
                
                results[type_name] = StreamResult(
                    stream_id=None,
                    stream_type=StreamType(type_name),
                    stream_name=None,
                    stream_status=StreamStatus.MISSING,
                    connected_app_ids=[],
                    connected_app_names=[],
                    source_app=None,
                    check_status=check_status,
                    failures=failures,
                    warnings=warnings,
                )
        
        return results
