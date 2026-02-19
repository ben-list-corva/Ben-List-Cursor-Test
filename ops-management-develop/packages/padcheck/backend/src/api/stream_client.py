"""
Stream Platform API client.

Handles all interactions with the Stream Platform API for:
- Well lookup by API number
- Stage information retrieval
"""

import os
import logging
from typing import List, Optional, Dict, Any

import requests

from ..constants import STREAM_API_BASE_URL, API_TIMEOUT, DEFAULT_PAGE_SIZE
from ..models.types import StreamWell, StreamStage, StreamPad, StreamPadWell

logger = logging.getLogger(__name__)


class StreamClientError(Exception):
    """Custom exception for Stream API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class StreamClient:
    """
    Client for Stream Platform API.
    
    Uses the STREAM_API_TOKEN environment variable for Bearer token authentication.
    This must be configured in the Dev Center backend environment.
    """
    
    def __init__(self, api_token: Optional[str] = None, base_url: Optional[str] = None):
        self.api_token = api_token or os.environ.get("STREAM_API_TOKEN")
        if not self.api_token:
            raise StreamClientError("STREAM_API_TOKEN environment variable is not set")
        
        self.base_url = base_url or STREAM_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make an authenticated request to the Stream API."""
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
            raise StreamClientError(f"Request timed out: {endpoint}")
        
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {response.status_code}: {endpoint}"
            try:
                error_data = response.json()
                if "message" in error_data:
                    error_msg = error_data["message"]
                elif "error" in error_data:
                    error_msg = error_data["error"]
            except Exception:
                pass
            raise StreamClientError(error_msg, response.status_code, response.text)
        
        except requests.exceptions.RequestException as e:
            raise StreamClientError(f"Request failed: {str(e)}")
    
    def lookup_well_by_api_number(
        self,
        api_number: str,
        limit: int = DEFAULT_PAGE_SIZE,
        page: int = 1
    ) -> List[StreamWell]:
        """
        Look up wells by API number.
        
        Endpoint: GET /v1/wells?api_number={api_number}&limit={limit}&page={page}
        
        Returns list of matching wells. For a valid pipeline, exactly 1 should match.
        """
        logger.info(f"Looking up Stream well by API number: {api_number}")
        
        params = {
            "api_number": api_number,
            "limit": limit,
            "page": page,
        }
        
        data = self._request("GET", "/v1/wells", params=params)
        
        wells = []
        
        # Handle different response structures
        if isinstance(data, dict):
            # JSON:API style response
            items = data.get("data", [])
            for item in items:
                if isinstance(item, dict):
                    # JSON:API format with attributes
                    attrs = item.get("attributes", item)
                    wells.append(StreamWell(
                        id=str(item.get("id", "")),
                        api_number=attrs.get("api_number") or attrs.get("apiNumber"),
                        name=attrs.get("name"),
                    ))
        elif isinstance(data, list):
            # Direct array response
            for item in items:
                wells.append(StreamWell(
                    id=str(item.get("id", "")),
                    api_number=item.get("api_number") or item.get("apiNumber"),
                    name=item.get("name"),
                ))
        
        logger.info(f"Found {len(wells)} Stream wells matching API number {api_number}")
        return wells
    
    def get_well_stages(
        self,
        stream_well_id: str,
        sort: str = "-stage_number",
        limit: int = DEFAULT_PAGE_SIZE,
        page: int = 1
    ) -> List[StreamStage]:
        """
        Get stages for a Stream well.
        
        Endpoint: GET /v1/stages/well/{streamWellId}?sort={sort}&page={page}&limit={limit}
        
        Default sort is -stage_number (descending) to get latest stages first.
        """
        logger.info(f"Fetching stages for Stream well {stream_well_id}")
        
        params = {
            "sort": sort,
            "limit": limit,
            "page": page,
        }
        
        data = self._request("GET", f"/v1/stages/well/{stream_well_id}", params=params)
        
        stages = []
        
        # Handle different response structures
        if isinstance(data, dict):
            # JSON:API style response
            items = data.get("data", [])
            for item in items:
                if isinstance(item, dict):
                    attrs = item.get("attributes", item)
                    stages.append(StreamStage(
                        id=str(item.get("id", "")),
                        stage_number=attrs.get("stage_number") or attrs.get("stageNumber", 0),
                        status=attrs.get("status"),
                        stage_action=attrs.get("stage_action") or attrs.get("stageAction"),
                        stage_start=attrs.get("stage_start") or attrs.get("stageStart"),
                        sb_id=attrs.get("sb_id") or attrs.get("sbId"),
                    ))
        elif isinstance(data, list):
            for item in data:
                stages.append(StreamStage(
                    id=str(item.get("id", "")),
                    stage_number=item.get("stage_number") or item.get("stageNumber", 0),
                    status=item.get("status"),
                    stage_action=item.get("stage_action") or item.get("stageAction"),
                    stage_start=item.get("stage_start") or item.get("stageStart"),
                    sb_id=item.get("sb_id") or item.get("sbId"),
                ))
        
        logger.info(f"Found {len(stages)} stages for Stream well {stream_well_id}")
        return stages
    
    def search_pads(
        self,
        search_term: str,
        status: Optional[str] = None,
        limit: int = DEFAULT_PAGE_SIZE,
        page: int = 1
    ) -> List[StreamPad]:
        """
        Search for pads by name.
        
        Endpoint: GET /v1/pads?search={search_term}&status={status}&limit={limit}&page={page}
        
        The 'search' parameter does partial name matching.
        """
        logger.info(f"Searching Stream pads with term: {search_term}")
        
        params = {
            "search": search_term,
            "limit": limit,
            "page": page,
        }
        if status:
            params["status"] = status
        
        data = self._request("GET", "/v1/pads", params=params)
        
        pads = []
        if isinstance(data, dict):
            items = data.get("data", [])
            for item in items:
                if isinstance(item, dict):
                    attrs = item.get("attributes", item)
                    rels = item.get("relationships", {})
                    
                    # Parse wells from the pad response
                    wells_data = attrs.get("wells", {}).get("data", [])
                    pad_wells = []
                    for well_item in wells_data:
                        well_attrs = well_item.get("attributes", well_item)
                        pad_wells.append(StreamPadWell(
                            id=str(well_item.get("id", "")),
                            name=well_attrs.get("name"),
                            api_number=well_attrs.get("api_number"),
                            status=well_attrs.get("status"),
                        ))
                    
                    # Parse company name from relationships
                    company_name = None
                    company_data = rels.get("company", {}).get("data", {})
                    if company_data:
                        company_attrs = company_data.get("attributes", {})
                        company_name = company_attrs.get("name")
                    
                    pads.append(StreamPad(
                        id=str(item.get("id", "")),
                        name=attrs.get("name"),
                        frac_fleet_name=attrs.get("frac_fleet_name"),
                        company_name=company_name,
                        wells=pad_wells,
                        frac_sb_id=attrs.get("frac_sb_id"),
                        wireline_sb_id=attrs.get("wireline_sb_id"),
                        pumpdown_sb_id=attrs.get("pumpdown_sb_id"),
                        status=attrs.get("status"),
                    ))
        
        logger.info(f"Found {len(pads)} Stream pads matching '{search_term}'")
        return pads
    
    def get_pad_by_id(self, pad_id: str) -> Optional[StreamPad]:
        """
        Get a specific pad by ID.
        
        Endpoint: GET /v1/pads/{padId}
        """
        logger.info(f"Fetching Stream pad by ID: {pad_id}")
        
        try:
            data = self._request("GET", f"/v1/pads/{pad_id}")
        except StreamClientError as e:
            if e.status_code == 404:
                logger.warning(f"Stream pad {pad_id} not found")
                return None
            raise
        
        if isinstance(data, dict):
            item = data.get("data", data)
            attrs = item.get("attributes", item)
            rels = item.get("relationships", {})
            
            # Parse wells from the pad response
            wells_data = attrs.get("wells", {}).get("data", [])
            pad_wells = []
            for well_item in wells_data:
                well_attrs = well_item.get("attributes", well_item)
                pad_wells.append(StreamPadWell(
                    id=str(well_item.get("id", "")),
                    name=well_attrs.get("name"),
                    api_number=well_attrs.get("api_number"),
                    status=well_attrs.get("status"),
                ))
            
            # Parse company name from relationships
            company_name = None
            company_data = rels.get("company", {}).get("data", {})
            if company_data:
                company_attrs = company_data.get("attributes", {})
                company_name = company_attrs.get("name")
            
            return StreamPad(
                id=str(item.get("id", "")),
                name=attrs.get("name"),
                frac_fleet_name=attrs.get("frac_fleet_name"),
                company_name=company_name,
                wells=pad_wells,
                frac_sb_id=attrs.get("frac_sb_id"),
                wireline_sb_id=attrs.get("wireline_sb_id"),
                pumpdown_sb_id=attrs.get("pumpdown_sb_id"),
                status=attrs.get("status"),
            )
        
        return None


# Singleton instance for reuse
_client: Optional[StreamClient] = None


def get_stream_client() -> StreamClient:
    """Get or create a Stream API client instance."""
    global _client
    if _client is None:
        _client = StreamClient()
    return _client
