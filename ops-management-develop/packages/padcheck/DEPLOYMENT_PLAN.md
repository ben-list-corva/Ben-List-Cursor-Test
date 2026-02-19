# PadCheck Deployment Plan

**Status:** ⏸️ PAUSED - Awaiting developer input on architecture questions

**Last Updated:** January 22, 2026

---

## Executive Summary

PadCheck is a pipeline validation tool that checks Corva completions data connectivity. The app currently works locally but needs restructuring to deploy to Corva Dev Center.

### What's Done
- ✅ Backend deployed to Dev Center (draft status)
- ✅ `STREAM_API_TOKEN` configured as secret in Dev Center
- ✅ Code pushed to GitHub (`ops-management/packages/padcheck/`)

### What's Blocked
- ❌ Frontend deployment failing due to format mismatch
- ❓ Architecture questions about frontend ↔ backend communication

---

## Architecture Question for Developer

### The Problem

PadCheck's current architecture:
```
Frontend (React) ──HTTP Request──> Backend (Lambda) ──Returns JSON──> Frontend displays
```

Corva's Task App architecture (per documentation):
```
Frontend ──POST /v2/tasks──> Task App ──Writes to Dataset──> Frontend polls/subscribes
```

**Key insight from docs:** "The task app does not return data to the frontend app. The task app can communicate processed data by posting the values in a dataset."

### What PadCheck Does

1. **Calls Corva API** - Gets pad info, wells, streams, app_connections (existing datasets)
2. **Calls Stream API** - External API requiring bearer token (stored in backend)
3. **Returns aggregated results** - Validation status for each well/stream

### Questions for Developer

1. **How do we get results back?**
   - Do we need to create a custom dataset (e.g., `{company}.padcheck-results`) and have frontend poll it?
   - Or is there a way for task apps to return data directly?

2. **Can some logic move to frontend?**
   - Corva API calls could potentially use `corvaDataAPI` from frontend
   - But Stream API calls need the bearer token - should stay in backend

3. **Alternative approach?**
   - Could frontend make direct Corva API calls and only invoke backend for Stream API checks?

---

## Current State vs Corva Required Format

| Aspect | Current PadCheck | Corva Required |
|--------|------------------|----------------|
| Bundler | Vite | Webpack via `@corva/dc-platform-shared` |
| React | 18.x | 17.x |
| Entry | `src/index.tsx` | `src/index.js` exporting `{ component, settings }` |
| Context | URL params via custom hook | Props from Corva (`props.padId`, `props.wells`) |
| Styling | Inline MUI sx | CSS Modules recommended |
| Package manager | npm | Yarn 1.x (Classic) |

---

## Frontend Restructure Plan

### Required File Structure
```
frontend/
├── src/
│   ├── index.js              # NEW: exports { component: App, settings: AppSettings }
│   ├── App.tsx               # MODIFY: receive props from Corva
│   ├── AppSettings.tsx       # NEW: settings panel (can be minimal)
│   ├── types.ts              # UPDATE: add Corva AppProps interface
│   ├── custom.d.ts           # NEW: CSS module declarations
│   ├── components/           # KEEP: existing components
│   └── effects/              # KEEP: existing hooks
├── manifest.json             # UPDATE: Corva UI schema
├── config-overrides.js       # NEW: Webpack config
└── package.json              # UPDATE: Corva dependencies
```

### Context Access Change

**Before (current - reads URL params):**
```typescript
const { context } = useAssetContext();
const padId = context.padId;
```

**After (Corva props):**
```typescript
function App({ padId, fracFleetId, wells, well }: AppProps) {
  // Props passed directly by Corva platform
}
```

### Required manifest.json
```json
{
  "format": 1,
  "license": { "type": "MIT", "url": "https://example.com/license/" },
  "developer": {
    "name": "Your Company",
    "identifier": "yourcompany",
    "authors": []
  },
  "application": {
    "type": "ui",
    "key": "yourcompany.padcheck.ui",
    "visibility": "private",
    "name": "PadCheck",
    "description": "Pipeline connectivity validation for completions",
    "category": "analytics",
    "segments": ["completion"],
    "ui": {
      "initial_size": { "w": 6, "h": 12 },
      "multi_rig": false,
      "full_screen_report": false,
      "use_app_header_v3": true
    }
  },
  "settings": {
    "entrypoint": { "file": "src/index.js", "function": "handler" },
    "environment": {},
    "runtime": "ui",
    "app": { "log_type": "time" }
  },
  "datasets": {}
}
```

### Required package.json Updates
```json
{
  "dependencies": {
    "@corva/ui": "latest",
    "@material-ui/core": "4.11.2",
    "@material-ui/icons": "4.9.1",
    "react": "17.0.1",
    "react-dom": "17.0.1"
  },
  "devDependencies": {
    "@corva/dc-platform-shared": "latest"
  },
  "scripts": {
    "build": "webpack --config=./config-overrides.js --mode production",
    "start": "webpack-dev-server --config=./config-overrides.js --mode development",
    "zip": "create-corva-app zip .",
    "release": "create-corva-app release ."
  },
  "engines": { "node": "^20", "yarn": "*" }
}
```

---

## Backend Task App Pattern (from Corva docs)

### How to Invoke a Task App
```javascript
// Frontend POSTs to Corva tasks API
fetch('https://api.corva.ai/v2/tasks', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer {user_token}',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    task: {
      provider: 'yourcompany',
      app_key: 'yourcompany.padcheck',
      asset_id: padId,
      properties: {
        padId: 11048,
        fracFleetId: 1993
      }
    }
  })
});
```

### Task App Receives Event
```python
@task
def lambda_handler(event: TaskEvent, api: Api):
    pad_id = event.properties["padId"]
    # ... run checks ...
    
    # Write results to dataset (task apps can't return data directly)
    api.post("/api/v1/data/yourcompany/padcheck-results/", data=[results])
```

### Frontend Gets Results
```javascript
// Option 1: Poll the dataset
const results = await corvaDataAPI.get('/api/v1/data/yourcompany/padcheck-results/', {
  query: JSON.stringify({ asset_id: padId }),
  sort: JSON.stringify({ timestamp: -1 }),
  limit: 1
});

// Option 2: Subscribe to real-time updates
socketClient.subscribe(
  { provider: 'yourcompany', dataset: 'padcheck-results', assetId: padId },
  { onDataReceive: (event) => setResults(event.data) }
);
```

---

## Implementation TODOs

### Phase 1: Create Corva-Compatible Structure
- [ ] Create `frontend/src/index.js` - entry point
- [ ] Create `frontend/src/AppSettings.tsx` - minimal settings
- [ ] Create `frontend/config-overrides.js` - webpack config
- [ ] Update `frontend/manifest.json` with Corva schema

### Phase 2: Adapt Components to Props
- [ ] Update `App.tsx` to receive Corva props instead of URL params
- [ ] Add Corva `AppProps` interface to types

### Phase 3: Update Dependencies
- [ ] Update `package.json` with Corva dependencies
- [ ] Delete `package-lock.json`
- [ ] Install with Yarn 1.x (Classic)

### Phase 4: Build and Deploy
- [ ] Run `yarn build` to verify webpack works
- [ ] Run `yarn zip` to create deployment package
- [ ] Upload zip to Dev Center

### Phase 5: Backend Integration (needs developer input)
- [ ] Determine how frontend calls backend and receives results
- [ ] Possibly create results dataset
- [ ] Update backend to write to dataset instead of returning JSON

---

## Reference Documents

- **Corva FE Rules:** `CORVA_FE_RULES.md` (in this project)
- **Dev Center Docs:** https://dc-docs.corva.ai/docs/intro
- **Component Library:** https://storybook.dev.corva.ai/
- **Example Drilling App:** https://github.com/corva-ai/example-frontend-app-drilling-wits

---

## Notes from Development

1. The Dev Center upload was failing because we were uploading a **built bundle** (`dist/`) but Corva expects **source code** that it builds itself using their webpack config.

2. Corva uses **React 17**, not React 18. Need to downgrade.

3. Corva uses **Yarn 1.x (Classic)**, not npm or newer Yarn versions.

4. App receives context via **props** (like `props.padId`, `props.wells`), not via URL parameters.

5. The chip selectors at the top of Corva dashboards (Frac Fleet > Pad > Well) automatically pass these values as props to apps.
