"""
Stage validator.

Validates stages from Stream Platform:
- Check D: Stream Platform well lookup
- Check E: Stages exist and have active stage
"""

import logging
from typing import List, Optional, Tuple

from ..models.types import (
    StageStatus,
    StageInfo,
    StreamPlatformCheck,
    CheckStatus,
    StreamWell,
    StreamStage,
)

logger = logging.getLogger(__name__)


class StageValidator:
    """Validates Stream Platform well lookup and stages."""
    
    @staticmethod
    def validate_well_lookup(
        wells: List[StreamWell],
        api_number: str
    ) -> Tuple[Optional[str], Optional[str], StreamPlatformCheck]:
        """
        Validate Stream Platform well lookup result.
        
        Check D:
        - 0 results -> FAIL
        - >1 results -> FAIL (ambiguous)
        - exactly 1 -> PASS, return (streamWellId, streamWellName)
        
        Returns: (stream_well_id, stream_well_name, check_result)
        """
        failures: List[str] = []
        warnings: List[str] = []
        stream_well_id: Optional[str] = None
        stream_well_name: Optional[str] = None
        
        if len(wells) == 0:
            failures.append(
                f"No well found in Stream Platform for API number '{api_number}'"
            )
            check_status = CheckStatus.FAIL
        
        elif len(wells) > 1:
            failures.append(
                f"Multiple wells ({len(wells)}) found in Stream Platform "
                f"for API number '{api_number}' (ambiguous)"
            )
            check_status = CheckStatus.FAIL
        
        else:
            # Exactly one well found
            stream_well_id = wells[0].id
            stream_well_name = wells[0].name
            
            # Verify API number matches (sanity check)
            if wells[0].api_number and wells[0].api_number != api_number:
                warnings.append(
                    f"Stream well API number '{wells[0].api_number}' "
                    f"differs from requested '{api_number}'"
                )
            
            check_status = CheckStatus.WARN if warnings else CheckStatus.PASS
        
        return stream_well_id, stream_well_name, StreamPlatformCheck(
            check_status=check_status,
            failures=failures,
            warnings=warnings,
        )
    
    @staticmethod
    def validate_stages(
        stages: List[StreamStage],
        is_viewer: bool = False,
    ) -> StageStatus:
        """
        Validate stages for a Stream well.
        
        Check E:
        - No stages -> FAIL for viewers, WARN for wells (new pads may not have stages yet)
        - Stages but no active -> WARN
        - Active stage exists -> PASS
        
        Args:
            stages: List of stages from Stream Platform
            is_viewer: If True, treat no stages as FAIL (viewers should have stages)
        """
        failures: List[str] = []
        warnings: List[str] = []
        
        has_stages = len(stages) > 0
        has_active_stage = False
        active_stage: Optional[StreamStage] = None
        
        if not has_stages:
            # For viewers: no stages is a failure
            # For wells: no stages is just a warning (pad may not be active yet)
            if is_viewer:
                failures.append("No stages found in Stream Platform (viewer should have stages)")
                check_status = CheckStatus.FAIL
            else:
                warnings.append("No stages found in Stream Platform (pad may not be active yet)")
                check_status = CheckStatus.WARN
            
            return StageStatus(
                has_stages=False,
                has_active_stage=False,
                check_status=check_status,
                failures=failures,
                warnings=warnings,
            )
        
        # Find active stage
        for stage in stages:
            if stage.status and stage.status.lower() == "active":
                has_active_stage = True
                active_stage = stage
                break
        
        if not has_active_stage:
            warnings.append(
                f"No active stage found (total stages: {len(stages)})"
            )
        
        # Determine check status
        if failures:
            check_status = CheckStatus.FAIL
        elif warnings:
            check_status = CheckStatus.WARN
        else:
            check_status = CheckStatus.PASS
        
        return StageStatus(
            has_stages=has_stages,
            has_active_stage=has_active_stage,
            active_stage_number=active_stage.stage_number if active_stage else None,
            active_stage_action=active_stage.stage_action if active_stage else None,
            sb_id=active_stage.sb_id if active_stage else None,
            stage_start=active_stage.stage_start if active_stage else None,
            check_status=check_status,
            failures=failures,
            warnings=warnings,
        )
    
    @staticmethod
    def validate_no_api_number() -> Tuple[None, StreamPlatformCheck]:
        """
        Handle case where well has no API number.
        
        Cannot look up well in Stream Platform without API number.
        """
        return None, StreamPlatformCheck(
            check_status=CheckStatus.FAIL,
            failures=["Cannot lookup Stream well: Corva well has no API number"],
            warnings=[],
        )
