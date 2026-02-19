"""
Schedule validator for checking pumping schedules in stage design.

Validates that pumping schedules have been uploaded for stage 1 and the last stage.
This is an informational check and does not affect overall PASS/WARN/FAIL status.
"""

import logging
from typing import Optional

from ..api.corva_client import CorvaClient
from ..models.types import ScheduleCheck

logger = logging.getLogger(__name__)


class ScheduleValidator:
    """
    Validates pumping schedules for wells.
    
    Checks the completion.data.stages dataset to verify that pumping
    schedules have been uploaded for both stage 1 and the last stage.
    """
    
    @staticmethod
    def check_schedules(client: CorvaClient, asset_id: int) -> ScheduleCheck:
        """
        Check if pumping schedules exist for stage 1 and the last stage.
        
        Args:
            client: CorvaClient instance
            asset_id: Corva well asset ID
            
        Returns:
            ScheduleCheck with results for both stages
        """
        logger.info(f"Checking pumping schedules for asset {asset_id}")
        
        result = ScheduleCheck()
        
        # Check stage 1
        try:
            stage_1_schedule = client.get_stage_schedule(asset_id, 1)
            result.stage_1_has_schedule = stage_1_schedule is not None and len(stage_1_schedule) > 0
            logger.info(f"Asset {asset_id} stage 1 has schedule: {result.stage_1_has_schedule}")
        except Exception as e:
            logger.warning(f"Failed to check stage 1 schedule for asset {asset_id}: {e}")
            result.stage_1_has_schedule = None
        
        # Find and check last stage
        try:
            last_stage_num = client.get_last_stage_number(asset_id)
            
            if last_stage_num is not None:
                result.last_stage_number = last_stage_num
                
                # Only check last stage if it's different from stage 1
                if last_stage_num != 1:
                    last_stage_schedule = client.get_stage_schedule(asset_id, last_stage_num)
                    result.last_stage_has_schedule = last_stage_schedule is not None and len(last_stage_schedule) > 0
                else:
                    # Last stage IS stage 1, use the same result
                    result.last_stage_has_schedule = result.stage_1_has_schedule
                
                logger.info(f"Asset {asset_id} stage {last_stage_num} has schedule: {result.last_stage_has_schedule}")
            else:
                logger.info(f"No stages found for asset {asset_id}")
                result.last_stage_number = None
                result.last_stage_has_schedule = None
                
        except Exception as e:
            logger.warning(f"Failed to check last stage schedule for asset {asset_id}: {e}")
            result.last_stage_number = None
            result.last_stage_has_schedule = None
        
        return result
