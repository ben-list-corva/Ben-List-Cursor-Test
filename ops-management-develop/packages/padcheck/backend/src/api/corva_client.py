"""
Corva Platform API client.

Handles all interactions with the Corva Platform API for:
- Pad information and well enumeration
- App streams for wells
- App connection details
"""

import os
import logging
from typing import List, Optional, Dict, Any

import requests

from ..constants import CORVA_API_BASE_URL, CORVA_DATA_API_BASE_URL, API_TIMEOUT, DEFAULT_PAGE_SIZE
from ..models.types import (
    CorvaPad, CorvaWell, CorvaStream, CorvaAppConnection, CorvaAsset,
    PadConfiguration, PadConfigType, FracFleetLine
)

logger = logging.getLogger(__name__)


class CorvaClientError(Exception):
    """Custom exception for Corva API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class CorvaClient:
    """
    Client for Corva Platform API.
    
    Uses the CORVA_API_KEY environment variable for authentication.
    In Dev Center Lambda, this is automatically provided.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.environ.get("CORVA_API_KEY")
        if not self.api_key:
            raise CorvaClientError("CORVA_API_KEY environment variable is not set")
        
        self.base_url = base_url or CORVA_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"API {self.api_key}",
            "Content-Type": "application/json",
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make an authenticated request to the Corva API."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=API_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            raise CorvaClientError(f"Request timed out: {endpoint}")
        
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {response.status_code}: {endpoint}"
            try:
                error_data = response.json()
                if "message" in error_data:
                    error_msg = error_data["message"]
            except Exception:
                pass
            raise CorvaClientError(error_msg, response.status_code, response.text)
        
        except requests.exceptions.RequestException as e:
            raise CorvaClientError(f"Request failed: {str(e)}")
    
    def get_pad(self, pad_id: int) -> CorvaPad:
        """
        Get pad information.
        
        Endpoint: GET /v2/pads/{padId}
        Returns JSON:API format with data.attributes structure
        """
        logger.info(f"Fetching pad {pad_id}")
        
        data = self._request("GET", f"/v2/pads/{pad_id}")
        
        # Handle JSON:API format
        if "data" in data:
            pad_data = data["data"]
            attrs = pad_data.get("attributes", {})
            return CorvaPad(
                id=int(pad_data.get("id", pad_id)),
                name=attrs.get("name", f"Pad {pad_id}"),
                wells=[],
            )
        
        return CorvaPad(
            id=data.get("id", pad_id),
            name=data.get("name", f"Pad {pad_id}"),
            wells=[],  # Wells fetched separately
        )
    
    def get_pad_wells(self, pad_id: int) -> List[CorvaWell]:
        """
        Get wells for a pad.
        
        Endpoint: GET /v2/pads/{padId}/wells
        Returns JSON:API format with data[].attributes structure
        """
        logger.info(f"Fetching wells for pad {pad_id}")
        
        data = self._request("GET", f"/v2/pads/{pad_id}/wells")
        
        wells = []
        items = data if isinstance(data, list) else data.get("data", data.get("wells", []))
        
        for well_data in items:
            # Handle JSON:API format with attributes
            if "attributes" in well_data:
                attrs = well_data["attributes"]
                well_id = well_data.get("id")
                # Use asset_id from attributes if available, otherwise use well id
                asset_id = attrs.get("asset_id") or well_id
                wells.append(CorvaWell(
                    asset_id=int(asset_id) if asset_id else 0,
                    name=attrs.get("name", "Unknown Well"),
                    api_number=attrs.get("api_number") or attrs.get("apiNumber"),
                    status=attrs.get("status"),
                ))
            else:
                # Fallback for non-JSON:API format
                wells.append(CorvaWell(
                    asset_id=well_data.get("id") or well_data.get("asset_id"),
                    name=well_data.get("name", "Unknown Well"),
                    api_number=well_data.get("api_number") or well_data.get("apiNumber"),
                    status=well_data.get("status"),
                ))
        
        logger.info(f"Found {len(wells)} wells for pad {pad_id}")
        return wells
    
    def get_well(self, well_asset_id: int) -> CorvaWell:
        """
        Get a single well by asset ID.
        
        Endpoint: GET /v2/wells/{wellId}
        """
        logger.info(f"Fetching well {well_asset_id}")
        
        data = self._request("GET", f"/v2/wells/{well_asset_id}")
        
        return CorvaWell(
            asset_id=data.get("id") or data.get("asset_id", well_asset_id),
            name=data.get("name", f"Well {well_asset_id}"),
            api_number=data.get("api_number") or data.get("apiNumber"),
            status=data.get("status"),
        )
    
    def get_well_streams(
        self,
        well_asset_id: int,
        segment: str = "completion"
    ) -> List[CorvaStream]:
        """
        Get streams for a well filtered by segment.
        
        Endpoint: GET /v1/app_streams?asset_id={asset_id}&segment={segment}
        """
        logger.info(f"Fetching {segment} streams for well {well_asset_id}")
        
        params = {
            "asset_id": well_asset_id,
            "segment": segment,
        }
        
        data = self._request("GET", "/v1/app_streams", params=params)
        
        streams = []
        items = data if isinstance(data, list) else data.get("data", [])
        
        for stream_data in items:
            # Parse app_connections
            app_connections = []
            for conn in stream_data.get("app_connections", []):
                app_connections.append(CorvaAppConnection(
                    app_id=conn.get("app_id") or conn.get("app"),
                    status=conn.get("status"),
                    settings=conn.get("settings", {}),
                ))
            
            streams.append(CorvaStream(
                id=stream_data.get("id"),
                name=stream_data.get("name"),
                status=stream_data.get("status"),
                segment=stream_data.get("segment"),
                source_type=stream_data.get("source_type"),
                data_source=stream_data.get("data_source"),
                app_connections=app_connections,
            ))
        
        logger.info(f"Found {len(streams)} {segment} streams for well {well_asset_id}")
        return streams
    
    def get_app_info(self, app_id: int) -> Dict[str, Any]:
        """
        Get app information by ID.
        
        Endpoint: GET /v2/apps/{appId}
        Note: This endpoint may not exist - fallback to hardcoded names if it fails.
        """
        try:
            data = self._request("GET", f"/v2/apps/{app_id}")
            return {
                "id": data.get("id", app_id),
                "name": data.get("name", f"App {app_id}"),
            }
        except CorvaClientError:
            # Endpoint may not exist, return None to use fallback
            return None
    
    def get_asset(self, asset_id: int) -> CorvaAsset:
        """
        Get full asset details including settings (v1 API).
        
        Endpoint: GET /v1/assets/{assetId}
        This returns more details than v2, including settings with frac_fleet_id and api_number.
        """
        logger.info(f"Fetching asset {asset_id}")
        
        data = self._request("GET", f"/v1/assets/{asset_id}")
        
        settings = data.get("settings", {})
        
        return CorvaAsset(
            id=data.get("id", asset_id),
            name=data.get("name", f"Asset {asset_id}"),
            status=data.get("status"),
            state=data.get("state"),
            asset_type=data.get("asset_type"),
            pad_id=data.get("pad_id"),
            parent_asset_id=data.get("parent_asset_id"),
            parent_asset_name=data.get("parent_asset_name"),
            frac_fleet_id=settings.get("frac_fleet_id"),
            api_number=settings.get("api_number"),
        )
    
    def search_viewers_for_pad(self, pad_name: str, min_score: int = 70) -> List[CorvaAsset]:
        """
        Find ALL viewer assets for a pad by searching for assets with matching name pattern.
        
        Viewer naming convention: "{Pad Name} / {Fleet Short Name} / Viewer [/ Line X]"
        
        For SimulFrac pads, multiple viewers may exist (one per line).
        
        Strategy:
        1. Search for active assets with pad name and "Viewer" in the name
        2. Score each result by name similarity
        3. Return ALL matching viewers above the minimum score threshold
        
        Returns:
            List of matching CorvaAsset viewers, sorted by name (to ensure consistent ordering)
        """
        logger.info(f"Searching for viewer assets for pad: {pad_name}")
        
        # URL encode the search term
        search_term = f"{pad_name} Viewer"
        
        # Don't filter by status - idle viewers are valid for new pads
        params = {
            "search": search_term,
            "limit": 20,
        }
        
        try:
            data = self._request("GET", "/v1/assets", params=params)
        except CorvaClientError as e:
            logger.warning(f"Failed to search for viewers: {e}")
            return []
        
        items = data if isinstance(data, list) else data.get("data", [])
        
        # Collect all potential viewers and score them
        candidates = []
        pad_name_lower = pad_name.lower()
        
        for asset_data in items:
            name = asset_data.get("name", "")
            name_lower = name.lower()
            
            # Must contain "viewer" to be considered
            if "viewer" not in name_lower:
                continue
            
            # Calculate similarity score
            # Higher score = better match
            score = 0
            
            # Exact pad name match at start (best case)
            if name_lower.startswith(pad_name_lower):
                score += 100
            # Pad name contained in viewer name
            elif pad_name_lower in name_lower:
                score += 80
            else:
                # Word-based matching
                pad_words = set(pad_name_lower.split())
                viewer_words = set(name_lower.replace('/', ' ').split())
                common = pad_words.intersection(viewer_words)
                if common:
                    score += 50 * len(common) / len(pad_words)
            
            if score >= min_score:
                settings = asset_data.get("settings", {})
                viewer = CorvaAsset(
                    id=asset_data.get("id"),
                    name=name,
                    status=asset_data.get("status"),
                    state=asset_data.get("state"),
                    asset_type=asset_data.get("asset_type"),
                    pad_id=asset_data.get("pad_id"),
                    parent_asset_id=asset_data.get("parent_asset_id"),
                    parent_asset_name=asset_data.get("parent_asset_name"),
                    frac_fleet_id=settings.get("frac_fleet_id"),
                    api_number=settings.get("api_number"),
                )
                candidates.append((score, viewer))
                logger.info(f"Viewer candidate: {name} (id: {viewer.id}, score: {score})")
        
        if not candidates:
            logger.warning(f"No viewers found for pad: {pad_name}")
            return []
        
        # Sort by name for consistent ordering (Line A before Line B, etc.)
        candidates.sort(key=lambda x: x[1].name)
        viewers = [viewer for _, viewer in candidates]
        
        logger.info(f"Found {len(viewers)} viewers for pad: {pad_name}")
        return viewers
    
    def search_viewer_for_pad(self, pad_name: str) -> Optional[CorvaAsset]:
        """
        Find the BEST viewer asset for a pad (legacy method for backwards compatibility).
        
        For SimulFrac pads with multiple viewers, use search_viewers_for_pad() instead.
        """
        viewers = self.search_viewers_for_pad(pad_name)
        return viewers[0] if viewers else None
    
    def get_frac_fleet(self, fleet_id: str) -> Optional[Dict[str, Any]]:
        """
        Get frac fleet information.
        
        Endpoint: GET /v2/frac_fleets/{fleetId}
        """
        try:
            data = self._request("GET", f"/v2/frac_fleets/{fleet_id}")
            
            if "data" in data:
                fleet_data = data["data"]
                attrs = fleet_data.get("attributes", {})
                return {
                    "id": fleet_data.get("id", fleet_id),
                    "name": attrs.get("name", f"Fleet {fleet_id}"),
                }
            
            return {
                "id": data.get("id", fleet_id),
                "name": data.get("name", f"Fleet {fleet_id}"),
            }
        except CorvaClientError as e:
            logger.warning(f"Failed to fetch frac fleet {fleet_id}: {e}")
            return None
    
    def get_pad_configuration(self, pad_id: int) -> PadConfiguration:
        """
        Get pad frac configuration (Zipper vs SimulFrac).
        
        Endpoint: GET /v2/pads/{padId}?fields[]=pad.pad_frac_fleets&fields[]=pad.pad_frac_fleet.frac_fleet_lines
        
        Detection logic:
        - If pad_frac_fleet has frac_fleet_lines with data → SimulFrac
        - Otherwise → Zipper
        
        Returns PadConfiguration with:
        - config_type: ZIPPER, SIMULFRAC, or UNKNOWN
        - frac_fleet_id and frac_fleet_name
        - lines: List of FracFleetLine with well assignments (for SimulFrac)
        """
        logger.info(f"Fetching pad configuration for pad {pad_id}")
        
        params = {
            "fields[]": [
                "pad.name",
                "pad.pad_frac_fleets",
                "pad.pad_frac_fleet.frac_fleet_lines",
            ]
        }
        
        try:
            data = self._request("GET", f"/v2/pads/{pad_id}", params=params)
        except CorvaClientError as e:
            logger.warning(f"Failed to fetch pad configuration: {e}")
            return PadConfiguration(config_type=PadConfigType.UNKNOWN)
        
        included = data.get("included", [])
        
        # Find pad_frac_fleet
        pad_frac_fleets = [i for i in included if i.get("type") == "pad_frac_fleet"]
        if not pad_frac_fleets:
            logger.info(f"No pad_frac_fleet found for pad {pad_id}")
            return PadConfiguration(config_type=PadConfigType.UNKNOWN)
        
        # Use the first (should be current) pad_frac_fleet
        pff = pad_frac_fleets[0]
        pff_attrs = pff.get("attributes", {})
        
        # Extract frac fleet info
        frac_fleet = pff_attrs.get("frac_fleet", {})
        frac_fleet_id = frac_fleet.get("id")
        frac_fleet_name = frac_fleet.get("name")
        
        # Check for frac_fleet_lines (SimulFrac indicator)
        frac_fleet_lines_rel = pff.get("relationships", {}).get("frac_fleet_lines", {}).get("data", [])
        
        # Find all frac_fleet_line objects in included
        lines_data = [i for i in included if i.get("type") == "frac_fleet_line"]
        
        if not frac_fleet_lines_rel or not lines_data:
            # No lines = Zipper
            logger.info(f"Pad {pad_id} is ZIPPER (no frac_fleet_lines)")
            return PadConfiguration(
                config_type=PadConfigType.ZIPPER,
                frac_fleet_id=int(frac_fleet_id) if frac_fleet_id else None,
                frac_fleet_name=frac_fleet_name,
                lines=[],
            )
        
        # SimulFrac - parse line assignments
        lines = []
        for line_data in lines_data:
            line_attrs = line_data.get("attributes", {})
            
            # Get well IDs assigned to this line
            line_wells_rel = line_data.get("relationships", {}).get("frac_fleet_line_wells", {}).get("data", [])
            well_ids = [int(w.get("id")) for w in line_wells_rel if w.get("id")]
            
            # Handle viewer_well which can be a dict with 'id' or a simple value
            viewer_well = line_attrs.get("viewer_well")
            viewer_well_id = None
            if viewer_well:
                if isinstance(viewer_well, dict):
                    viewer_well_id = int(viewer_well.get("id")) if viewer_well.get("id") else None
                else:
                    viewer_well_id = int(viewer_well)
            
            lines.append(FracFleetLine(
                line_id=int(line_data.get("id", 0)),
                name=line_attrs.get("name", "Unknown Line"),
                well_ids=well_ids,
                viewer_well_id=viewer_well_id,
            ))
        
        logger.info(f"Pad {pad_id} is SIMULFRAC with {len(lines)} lines")
        return PadConfiguration(
            config_type=PadConfigType.SIMULFRAC,
            frac_fleet_id=int(frac_fleet_id) if frac_fleet_id else None,
            frac_fleet_name=frac_fleet_name,
            lines=lines,
        )
    
    def get_pad_wells_detailed(self, pad_id: int) -> List[Dict[str, Any]]:
        """
        Get wells for a pad with detailed info including custom_properties (for color).
        
        Endpoint: GET /v2/pads/{padId}?fields[]=pad.wells
        
        Returns list of well dictionaries with:
        - well_id: Corva well ID
        - asset_id: Corva asset ID
        - name: Well name
        - api_number: API number
        - status: Well status
        - color: Wellhead color from custom_properties
        """
        logger.info(f"Fetching detailed wells for pad {pad_id}")
        
        params = {
            "fields[]": ["pad.wells"]
        }
        
        try:
            data = self._request("GET", f"/v2/pads/{pad_id}", params=params)
        except CorvaClientError as e:
            logger.warning(f"Failed to fetch detailed wells: {e}")
            return []
        
        included = data.get("included", [])
        
        wells = []
        for item in included:
            if item.get("type") != "well":
                continue
            
            attrs = item.get("attributes", {})
            custom_props = attrs.get("custom_properties", {})
            
            wells.append({
                "well_id": int(item.get("id", 0)),
                "asset_id": attrs.get("asset_id"),
                "name": attrs.get("name", "Unknown Well"),
                "api_number": attrs.get("api_number"),
                "status": attrs.get("status"),
                "color": custom_props.get("color"),
            })
        
        logger.info(f"Found {len(wells)} detailed wells for pad {pad_id}")
        return wells
    
    def get_stage_schedule(self, asset_id: int, stage_num: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get pumping schedule for a specific stage.
        
        Endpoint: GET https://data.corva.ai/api/v1/data/corva/completion.data.stages/aggregate/
        
        Queries the completion.data.stages dataset for a specific stage number
        and returns the pumping_schedule field if present.
        
        Args:
            asset_id: Corva well asset ID
            stage_num: Stage number to query
            
        Returns:
            List of pumping schedule entries, or None if not found/empty
        """
        import json
        logger.info(f"Fetching schedule for asset {asset_id}, stage {stage_num}")
        
        # Use the aggregate endpoint with match/project params (per updated script)
        params = {
            "match": json.dumps({"asset_id": asset_id, "data.stage_number": stage_num}),
            "sort": json.dumps({"timestamp": -1}),
            "limit": 1,
            "project": json.dumps({"asset_id": 1, "timestamp": 1, "data.stage_number": 1, "data.pumping_schedule": 1}),
        }
        
        try:
            # Data API uses raw API key without prefix
            url = f"{CORVA_DATA_API_BASE_URL}/api/v1/data/corva/completion.data.stages/aggregate/"
            headers = {
                "Authorization": self.api_key,  # Raw API key, no prefix
                "Content-Type": "application/json",
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            logger.warning(f"Failed to fetch stage schedule: HTTP {e.response.status_code}")
            return None
        except Exception as e:
            logger.warning(f"Failed to fetch stage schedule: {e}")
            return None
        
        if not data or not isinstance(data, list) or len(data) == 0:
            logger.info(f"No stage data found for asset {asset_id}, stage {stage_num}")
            return None
        
        pumping_schedule = data[0].get("data", {}).get("pumping_schedule", [])
        
        if pumping_schedule:
            logger.info(f"Found pumping schedule with {len(pumping_schedule)} entries for asset {asset_id}, stage {stage_num}")
        else:
            logger.info(f"No pumping schedule for asset {asset_id}, stage {stage_num}")
        
        return pumping_schedule if pumping_schedule else None
    
    def get_last_stage_number(self, asset_id: int) -> Optional[int]:
        """
        Get the highest stage number for a well.
        
        Endpoint: GET https://data.corva.ai/api/v1/data/corva/completion.data.stages/aggregate/
        
        Queries the completion.data.stages dataset sorted by stage_number descending
        to find the highest stage.
        
        Args:
            asset_id: Corva well asset ID
            
        Returns:
            The highest stage number, or None if no stages found
        """
        import json
        logger.info(f"Finding last stage number for asset {asset_id}")
        
        # Use the aggregate endpoint with match/project params
        params = {
            "match": json.dumps({"asset_id": asset_id}),
            "sort": json.dumps({"data.stage_number": -1}),
            "limit": 1,
            "project": json.dumps({"data.stage_number": 1}),
        }
        
        try:
            # Data API uses raw API key without prefix
            url = f"{CORVA_DATA_API_BASE_URL}/api/v1/data/corva/completion.data.stages/aggregate/"
            headers = {
                "Authorization": self.api_key,  # Raw API key, no prefix
                "Content-Type": "application/json",
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            logger.warning(f"Failed to fetch last stage number: HTTP {e.response.status_code}")
            return None
        except Exception as e:
            logger.warning(f"Failed to fetch last stage number: {e}")
            return None
        
        if not data or not isinstance(data, list) or len(data) == 0:
            logger.info(f"No stages found for asset {asset_id}")
            return None
        
        stage_num = data[0].get("data", {}).get("stage_number")
        logger.info(f"Last stage for asset {asset_id} is {stage_num}")
        return stage_num


# Singleton instance for reuse
_client: Optional[CorvaClient] = None


def get_corva_client() -> CorvaClient:
    """Get or create a Corva API client instance."""
    global _client
    if _client is None:
        _client = CorvaClient()
    return _client
