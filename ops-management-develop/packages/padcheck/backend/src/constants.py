"""
Constants for Pipeline Checker.

Contains Source App ID mappings, App ID Library, and API configuration.
"""

from typing import Dict, Optional

# =============================================================================
# APP ID LIBRARY
# =============================================================================
# Mapping of Corva app IDs to display names for connected apps on streams.
# These apps don't change often, so we maintain a static library.
# Last updated: 2026-01-19
#
# Format: app_id: {"name": "Short Display Name", "category": "type"}
# Keep names SHORT for clean UI display (ideally < 25 chars)
# =============================================================================

APP_LIBRARY: Dict[int, Dict[str, str]] = {
    # -------------------------------------------------------------------------
    # FRAC STREAM APPS
    # -------------------------------------------------------------------------
    169: {"name": "Frac Source", "category": "source", "stream_type": "frac"},
    141: {"name": "Column Mapper", "category": "enrichment"},
    142: {"name": "Engineering App", "category": "engineering"},
    291: {"name": "Pad Metrics Scheduler", "category": "scheduler"},
    770: {"name": "Activity Tracker", "category": "other"},
    1128: {"name": "Metrics Scheduler", "category": "other"},
    4642: {"name": "Guided Frac Insights", "category": "other"},
    5033: {"name": "Schedule Adherence", "category": "other"},
    2209: {"name": "Python Alerts", "category": "other"},
    5074: {"name": "Pump Insights", "category": "other"},
    2937: {"name": "Stage Rerun Trigger", "category": "other"},
    596: {"name": "WELLness", "category": "other"},
    2049: {"name": "Stage Target", "category": "other"},
    
    # -------------------------------------------------------------------------
    # WIRELINE STREAM APPS
    # -------------------------------------------------------------------------
    170: {"name": "Wireline Source", "category": "source", "stream_type": "wireline"},
    173: {"name": "WL Activity Detector", "category": "enrichment"},
    172: {"name": "WL Column Mapper", "category": "enrichment"},
    171: {"name": "WL Enrichment", "category": "enrichment"},
    174: {"name": "WL Stage Times", "category": "stream"},
    222: {"name": "WL Wits Summary", "category": "stream"},
    4622: {"name": "CCL Anomaly Model", "category": "other"},
    4621: {"name": "CCL Anomaly Summary", "category": "other"},
    4620: {"name": "CCL Anomaly Enricher", "category": "other"},
    5052: {"name": "WL Predictions", "category": "other"},
    
    # -------------------------------------------------------------------------
    # PUMPDOWN STREAM APPS
    # -------------------------------------------------------------------------
    599: {"name": "Pumpdown Source", "category": "source", "stream_type": "pumpdown"},
    781: {"name": "PD Wits Summary", "category": "stream"},
    673: {"name": "PD Enrichment", "category": "enrichment"},
    
    # -------------------------------------------------------------------------
    # VIEWER STREAM APPS
    # -------------------------------------------------------------------------
    4643: {"name": "FracVision Test Frac", "category": "other"},
    1774: {"name": "Viewer Engineering", "category": "engineering"},
    5110: {"name": "Redzone Backend", "category": "other"},
    4698: {"name": "FracVision Test WL", "category": "other"},
}

# Source App IDs for each stream type (subset of APP_LIBRARY)
SOURCE_APP_IDS: Dict[str, int] = {
    "frac": 169,
    "wireline": 170,
    "pumpdown": 599,
    "drillout": 596,
}

# Reverse mapping: app_id -> stream type (for source apps only)
APP_ID_TO_STREAM_TYPE: Dict[int, str] = {
    app_id: info["stream_type"]
    for app_id, info in APP_LIBRARY.items()
    if info.get("stream_type")
}

# Legacy alias for backward compatibility
SOURCE_APP_NAMES: Dict[int, str] = {
    app_id: info["name"]
    for app_id, info in APP_LIBRARY.items()
}

# Expected Stream API root URL
EXPECTED_STREAM_API_ROOT_URL = "https://api.stream.corva.ai"

# Corva API base URL
CORVA_API_BASE_URL = "https://api.corva.ai"

# Corva Data API base URL (separate from standard API)
CORVA_DATA_API_BASE_URL = "https://data.corva.ai"

# Stream Platform API base URL
STREAM_API_BASE_URL = "https://api.stream.corva.ai"

# Required stream types (at least one must exist for PASS)
REQUIRED_STREAM_TYPES = ["frac"]  # Only frac is required per user spec

# Optional stream types (WARN if missing, not FAIL)
OPTIONAL_STREAM_TYPES = ["wireline"]  # Wireline is optional but expected

# Silent stream types (no warning if missing - truly optional)
SILENT_STREAM_TYPES = ["pumpdown"]  # Pumpdown may not be monitored

# API timeout in seconds
API_TIMEOUT = 30

# Pagination defaults
DEFAULT_PAGE_SIZE = 50


def get_app_name(app_id: int) -> str:
    """Get the display name for an app ID."""
    return SOURCE_APP_NAMES.get(app_id, f"App {app_id}")


def get_stream_type_for_app(app_id: int) -> str | None:
    """Get the stream type for a source app ID."""
    return APP_ID_TO_STREAM_TYPE.get(app_id)


def is_source_app(app_id: int) -> bool:
    """Check if an app ID is a known source app."""
    return app_id in SOURCE_APP_IDS.values()
