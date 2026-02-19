"""
Source App validator.

Validates Source App settings in stream app_connections:
- Check C: Source app exists and is configured correctly
- API number matches
- Required settings present
"""

import logging
from typing import Optional, List

from ..models.types import (
    StreamResult,
    SourceAppInfo,
    StreamSettings,
    CheckStatus,
    CorvaStream,
    CorvaAppConnection,
)
from ..constants import (
    SOURCE_APP_IDS,
    EXPECTED_STREAM_API_ROOT_URL,
    get_app_name,
)

logger = logging.getLogger(__name__)


def mask_api_key(key: Optional[str]) -> Optional[str]:
    """Mask an API key for safe display."""
    if not key:
        return None
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}****{key[-4:]}"


class SourceAppValidator:
    """Validates Source App settings in stream app_connections."""
    
    @staticmethod
    def find_source_app_connection(
        stream: CorvaStream,
        stream_type: str
    ) -> Optional[CorvaAppConnection]:
        """
        Find the Source App connection for a stream type.
        
        Source app IDs:
        - Frac: 169
        - Wireline: 170
        - Pumpdown: 599
        """
        expected_app_id = SOURCE_APP_IDS.get(stream_type)
        if not expected_app_id:
            return None
        
        logger.debug(f"Looking for app_id {expected_app_id} in stream {stream.id}")
        logger.debug(f"Stream has {len(stream.app_connections)} app_connections")
        
        for conn in stream.app_connections:
            logger.debug(f"  Checking conn app_id={conn.app_id}")
            if conn.app_id == expected_app_id:
                return conn
        
        return None
    
    @staticmethod
    def validate_source_app(
        stream: CorvaStream,
        stream_type: str,
        well_api_number: Optional[str]
    ) -> SourceAppInfo:
        """
        Validate Source App settings for a stream.
        
        Checks:
        - Source app connection exists (FAIL if missing for required)
        - Source app status is active (WARN if not)
        - settings.api_number matches well api_number (FAIL if mismatch)
        - stream_api_root_url is present (WARN if missing)
        - stream_api_log_path is present (WARN if missing)
        - force_start_from is present (WARN if missing)
        """
        failures: List[str] = []
        warnings: List[str] = []
        
        # Find source app connection
        conn = SourceAppValidator.find_source_app_connection(stream, stream_type)
        
        if not conn:
            # Source app not connected
            return SourceAppInfo(
                app_id=SOURCE_APP_IDS.get(stream_type, 0),
                app_name=get_app_name(SOURCE_APP_IDS.get(stream_type, 0)),
                status="missing",
                settings=None,
                check_status=CheckStatus.FAIL,
                failures=["Source app not connected to stream"],
                warnings=[],
            )
        
        # Check source app status - only warn for truly problematic states, not idle
        app_status = (conn.status or "unknown").lower()
        # idle is normal for inactive pads, don't warn about it
        
        # Parse and validate settings
        settings = conn.settings or {}
        
        # Extract settings values
        settings_api_number = settings.get("api_number")
        force_start_from = settings.get("force_start_from")
        stream_api_root_url = settings.get("stream_api_root_url")
        stream_api_log_path = settings.get("stream_api_log_path")
        stream_api_key = settings.get("stream_api_key")
        
        # Validate api_number match
        if well_api_number and settings_api_number:
            if settings_api_number != well_api_number:
                failures.append(
                    f"API number mismatch: source app has '{settings_api_number}', "
                    f"well has '{well_api_number}'"
                )
        elif not settings_api_number:
            warnings.append("Source app settings missing api_number")
        
        # Validate stream_api_root_url
        if not stream_api_root_url:
            warnings.append("Source app settings missing stream_api_root_url")
        elif stream_api_root_url != EXPECTED_STREAM_API_ROOT_URL:
            warnings.append(
                f"Unexpected stream_api_root_url: '{stream_api_root_url}' "
                f"(expected: '{EXPECTED_STREAM_API_ROOT_URL}')"
            )
        
        # Validate stream_api_log_path
        if not stream_api_log_path:
            warnings.append("Source app settings missing stream_api_log_path")
        
        # Check for manual pumpdown (pumpdown stream using frac log_path)
        is_manual_pumpdown = False
        if stream_type == "pumpdown" and stream_api_log_path:
            log_path_lower = stream_api_log_path.lower()
            if "frac" in log_path_lower and "pumpdown" not in log_path_lower:
                is_manual_pumpdown = True
                warnings.append("Manual pumpdown detected (using frac streambox) - verify pumpdown data is flowing through frac")
        
        # force_start_from is optional - no warning if missing
        
        # Build settings object with masked key
        parsed_settings = StreamSettings(
            api_number=settings_api_number,
            force_start_from=force_start_from,
            stream_api_root_url=stream_api_root_url,
            stream_api_log_path=stream_api_log_path,
            stream_api_key_masked=mask_api_key(stream_api_key),
        )
        
        # Determine check status
        if failures:
            check_status = CheckStatus.FAIL
        elif warnings:
            check_status = CheckStatus.WARN
        else:
            check_status = CheckStatus.PASS
        
        return SourceAppInfo(
            app_id=conn.app_id,
            app_name=get_app_name(conn.app_id),
            status=app_status,
            settings=parsed_settings,
            check_status=check_status,
            failures=failures,
            warnings=warnings,
            is_manual_pumpdown=is_manual_pumpdown,
        )
    
    @staticmethod
    def enrich_stream_result(
        stream_result: StreamResult,
        stream: Optional[CorvaStream],
        well_api_number: Optional[str]
    ) -> StreamResult:
        """
        Enrich a StreamResult with Source App validation.
        
        Updates the StreamResult with source_app info and adjusts
        check_status based on source app validation.
        """
        if not stream or stream_result.stream_status.value == "missing":
            # No stream to validate
            return stream_result
        
        # Validate source app
        source_app = SourceAppValidator.validate_source_app(
            stream,
            stream_result.stream_type.value,
            well_api_number,
        )
        
        # Update stream result
        stream_result.source_app = source_app
        
        # Merge failures and warnings
        stream_result.failures.extend(source_app.failures)
        stream_result.warnings.extend(source_app.warnings)
        
        # Update overall check status (worst of stream + source app)
        if source_app.check_status == CheckStatus.FAIL:
            stream_result.check_status = CheckStatus.FAIL
        elif source_app.check_status == CheckStatus.WARN and stream_result.check_status == CheckStatus.PASS:
            stream_result.check_status = CheckStatus.WARN
        
        return stream_result
