# PadCheck - Corva Dev Center Dashboard App

A Corva Dev Center dashboard application that validates completions data pipeline connectivity end-to-end for a selected pad or well.

## Overview

PadCheck provides a fast "is it wired correctly?" yes/no answer for management and field-facing teams without needing to log into app.stream or dig through Control Center.

**Target Users:**
- Management
- Front-line tech sales / field-facing teams

**Core Goal:**
Validate that the pipeline is connected and producing data, NOT validating enrichment quality.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React/TypeScript)              │
│  - Asset chip context detection                             │
│  - Pipeline check trigger                                   │
│  - Results visualization                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Python Lambda)                  │
│  - Corva Platform API integration                           │
│  - Stream Platform API integration                          │
│  - Validation engine                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  Corva Platform  │    │ Stream Platform  │
│       API        │    │      API         │
└──────────────────┘    └──────────────────┘
```

## Project Structure

```
pipeline-checker/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/       # UI components
│   │   ├── hooks/            # React hooks (useAssetContext)
│   │   ├── api/              # Backend API client
│   │   ├── types/            # TypeScript type definitions
│   │   ├── App.tsx           # Main application
│   │   └── index.tsx         # Entry point
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # Python Lambda backend
│   ├── src/
│   │   ├── api/              # API clients (Corva, Stream)
│   │   ├── validators/       # Validation logic
│   │   ├── models/           # Pydantic data models
│   │   ├── constants.py      # Configuration constants
│   │   └── lambda_handler.py # Main Lambda handler
│   ├── requirements.txt
│   └── manifest.json
└── README.md
```

## Environment Variables

### Backend (Required)

| Variable | Description |
|----------|-------------|
| `CORVA_API_KEY` | Corva Platform API key (auto-provided in Dev Center) |
| `STREAM_API_TOKEN` | Bearer token for Stream Platform API |

### Frontend (Optional, for local development)

| Variable | Description |
|----------|-------------|
| `VITE_API_BASE_URL` | Backend API URL (defaults to `/api`) |
| `VITE_CORVA_API_KEY` | Corva API key for local testing |

## Asset Chip Context

The app uses Corva dashboard asset chips for input. No manual text entry is required.

**Required Context:**
- `padId` - Corva pad asset ID

**Optional Context:**
- `completionWellAssetId` - Specific well to check (if not provided, checks all wells on pad)
- `fracFleetId` - Informational only

**How Context is Retrieved:**
1. **Primary**: Dev Center runtime context (`window.__CORVA_CONTEXT__`)
2. **Fallback**: URL query parameters (`?padId=123&completionWellAssetId=456`)

**Behavior:**
- If `padId` is missing → Shows empty state: "Select a Pad using the dashboard asset chips"
- Once pad context exists → Shows "Run Pipeline Check" button
- Checks only run after clicking the button

## Pipeline Checks

The app runs automated checks (A-H) across Corva and Stream platforms:

### Viewer Checks (F-H)

Before checking individual wells, the app validates the **Viewer Asset** - the central collection point for raw data that gets tagged and routed to pad wells.

### Check F: Viewer Asset Discovery
**Purpose:** Find the viewer asset for the pad

**Discovery Method:**
- Search for assets matching `{Pad Name} * Viewer` pattern
- Score candidates by name similarity
- Validate viewer name matches pad name (>70% similarity required)

**Status:**
- FAIL: Viewer found but name doesn't match pad (may be wrong viewer)
- WARN: No viewer asset found for pad
- PASS: Viewer found and name matches

### Check G: Viewer Stream Validation
**Purpose:** Validate viewer's Frac/WL/PD streams and Source Apps

**Validates:**
- Viewer streams exist (Frac, Wireline, Pumpdown)
- Source apps configured with api_number

### Check H: Viewer → Stream Platform Link
**Purpose:** Confirm viewer's api_number resolves in Stream Platform

**Note:** The viewer's api_number is the link to raw data in Stream Platform. If misconfigured, no data flows to the pad.

---

### Well Checks (A-E)

### Check A: Pad → Wells Enumeration
**Purpose:** Build list of wells on the pad

**API:** `GET /v2/pads/{padId}/wells`

**Outputs:**
- Well asset_id
- Well name
- API number (link key to Stream)

**Status:**
- FAIL: No wells found
- PASS: At least one well found

### Check B: Well → Completion Streams
**Purpose:** Verify completion streams exist for each well

**API:** `GET /v1/app_streams?asset_id={wellId}&segment=completion`

**Validates:**
- Frac stream (REQUIRED)
- Wireline stream (optional)
- Pumpdown stream (optional)

**Status:**
- FAIL: Required stream (Frac) missing
- WARN: Optional stream missing or stream is idle
- PASS: Stream exists and is active

### Check C: Stream → Source App Settings
**Purpose:** Validate Source App configuration (bridge to Stream platform)

**Source App IDs:**
- Frac: 169
- Wireline: 170
- Pumpdown: 599

**Validates:**
- Source app connected to stream
- Source app status is active
- `settings.api_number` matches well API number
- `stream_api_root_url` is present
- `stream_api_log_path` is present
- `force_start_from` is present

**Status:**
- FAIL: Source app missing, or API number mismatch
- WARN: Source app inactive, or missing optional settings
- PASS: All settings correct and active

### Check D: Stream Platform → Well Lookup
**Purpose:** Confirm API number resolves to exactly one Stream well

**API:** `GET /v1/wells?api_number={api_number}`

**Status:**
- FAIL: 0 results (well not found) or >1 results (ambiguous)
- PASS: Exactly 1 matching well

### Check E: Stream Platform → Stages Check
**Purpose:** Confirm stages exist and an active stage is running

**API:** `GET /v1/stages/well/{streamWellId}?sort=-stage_number`

**Status:**
- FAIL: No stages found
- WARN: Stages exist but none active
- PASS: Active stage exists

## Status Indicators

| Status | Icon | Meaning |
|--------|------|---------|
| PASS | ✅ | Check passed, pipeline is healthy |
| WARN | ⚠️ | Non-blocking issue, review recommended |
| FAIL | ❌ | Critical issue, pipeline may not work |

**Overall Status Logic:**
- If ANY check is FAIL → Overall FAIL
- Else if ANY check is WARN → Overall WARN
- Else → Overall PASS

## Local Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will start on http://localhost:3000

### Backend

```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export CORVA_API_KEY="your-api-key"
export STREAM_API_TOKEN="your-stream-token"

# Run local development server
python -m src.lambda_handler 8000
```

The backend will start on http://localhost:8000

### Testing with Context

To test locally, append query parameters to the URL:

```
http://localhost:3000?padId=12345
http://localhost:3000?padId=12345&completionWellAssetId=67890
```

## Deployment

### Dev Center Deployment

1. **Frontend:**
   - Build: `cd frontend && npm run build`
   - Deploy the `dist/` folder as a Dev Center frontend app

2. **Backend:**
   - Package the `backend/` folder
   - Deploy as a Dev Center task app
   - Configure environment variables in Dev Center settings

### Environment Configuration

In Dev Center app settings, configure:

```
STREAM_API_TOKEN=<your-stream-platform-bearer-token>
```

The `CORVA_API_KEY` is automatically provided by the Dev Center runtime.

## UI Components

The frontend uses `@corva/ui` and Material-UI components:

- **Header**: Shows app title and current context (Pad, Well, Fleet)
- **EmptyState**: Displayed when no pad is selected
- **RunButton**: Primary action to trigger pipeline checks
- **SummaryBanner**: Overall PASS/WARN/FAIL status with counts
- **WellResultsTable**: Expandable cards showing per-well results
- **StreamCheckRow**: Individual stream check results with details

## Troubleshooting

### "Select a Pad using the dashboard asset chips"
The app needs pad context to run. Select a pad from the Corva dashboard asset selector.

### "Stream Platform validation skipped"
The `STREAM_API_TOKEN` environment variable is not configured. Configure it in the Dev Center backend settings.

### API Number Mismatch
The Source App settings have a different API number than the Corva well. This usually indicates a configuration error in the stream setup.

### No Stages Found
The well exists in Stream Platform but has no stage data. This could mean:
- The well hasn't been started yet
- Stage data isn't being transmitted
- Wrong well was linked

## API Reference

### Backend Endpoints

**POST /api/pipeline-check**

Request:
```json
{
  "pad_id": 12345,
  "well_asset_id": 67890  // optional
}
```

Response:
```json
{
  "success": true,
  "data": {
    "pad_id": 12345,
    "pad_name": "Example Pad",
    "wells": [...],
    "overall_status": "PASS",
    "total_failures": 0,
    "total_warnings": 2,
    "checked_at": "2025-01-19T12:00:00Z"
  },
  "error": null
}
```

**GET /api/health**

Response:
```json
{
  "status": "ok",
  "timestamp": "2025-01-19T12:00:00Z"
}
```

## Contributing

1. Follow the existing code style and patterns
2. Add appropriate error handling
3. Update this README if adding new checks or features
4. Test with various pad/well configurations

## Known Issues / TODOs

### UI Styling - Corva Design System

**Priority:** Address before deploying to Dev Center

The current UI uses a custom dark theme built with Material-UI. Before production deployment, the UI should be updated to match the official Corva design system used in apps like Red Zone:

**Items to address:**
1. **Color scheme** - Match Corva's official dark theme colors
2. **Typography** - Use Corva's standard fonts and sizing
3. **Component styling** - Use `@corva/ui` components where available
4. **Layout patterns** - Match table/card layouts used in Red Zone and other Corva apps
5. **Asset chips header** - Match the blue/purple chip styling seen in Red Zone
6. **Status indicators** - Align with Corva's standard status color palette

**Reference:** See Red Zone app for target styling
- Blue/purple asset chips in header
- Green status indicators (e.g., "FR", "WR", "PD" badges)
- Dark background with subtle gradients
- Fleet/Pad/Well hierarchy display

### Future Enhancements

1. **Historical Stream Validation** - Currently only notes historical streams, could add validation
2. **Latency monitoring** - Show data latency like Red Zone does
3. **Auto-refresh** - Periodic background checks
4. **Batch operations** - Check multiple pads at once
5. **Export results** - Download check results as PDF/CSV

## License

Internal Corva application - not for external distribution.
