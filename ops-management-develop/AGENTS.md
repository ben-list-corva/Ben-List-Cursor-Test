# Corva Frontend Monorepo - AI Agent Instructions

## Architecture Overview

This is an **Nx monorepo** for Corva's DevCenter frontend applications. Apps are individually deployable microfrontends that run within the Corva platform, consuming shared dependencies from the platform runtime rather than bundling them.

**Key concepts:**

- **Apps in `apps/`**: Each app is a standalone React 17 microfrontend with its own `manifest.json` (platform metadata) and build output
- **Custom Nx plugin (`@corva/cca`)**: Located in `tools/cca/`, provides generators for creating/importing apps and a deploy executor
- **Shared vite config (`@corva/vite-config`)**: Located in `tools/vite-config/`, configures external dependencies via `CORVA_GLOBAL_DEPENDENCIES` from `@corva/dc-platform-shared`
- **External dependencies**: React, Material-UI, Highcharts, etc. are NOT bundled—they're provided by the platform runtime as globals

## Creating New Apps

Use the custom generator (never create apps manually):

```bash
# Create new app with default Corva provider
npx nx generate @corva/cca:create "App Name"

# Create app with custom provider
npx nx generate @corva/cca:create "App Name" --provider custom-provider

# Import existing app from git repository
npx nx generate @corva/cca:import --repository git@github.com:corva-ai/corva-dc-fe-*.git
```

**What the generator does:**

- Clones/generates app source into `apps/app-name/`
- Creates `manifest.json` with app metadata (key, segment, category)
- Configures `vite.config.ts` that imports from `@corva/vite-config`
- Sets up tsconfig with paths and reference to `tools/vite-config`
- Adds project to `.release-please-manifest.json` for versioning
- Infers `deploy` target via the `@corva/cca` Nx plugin

## Build Configuration

Apps use a **specialized Vite config** (`tools/vite-config/src/lib/vite-config.ts`) that:

- Builds as IIFE format with externalized dependencies
- Reads `manifest.json` to determine app key and generate versioned identifiers
- Excludes `CORVA_GLOBAL_DEPENDENCIES` from bundle via Rollup externals
- Generates `this["@material-ui/core"]` style global accessors
- Copies `manifest.json` and `package.json` to build output
- Uses versioning logic from `get-version.ts` (respects git tags like `app-name@v1.2.3`)

**Never bundle these (they're platform externals):**

- `react`, `react-dom`, `@material-ui/*`, `highcharts`, `lodash`, `moment`, etc.

## Development Workflow

```bash
# Install dependencies
npm i

# Serve app in dev mode (uses local Corva platform dev environment)
npx nx serve app-name

# Build app
npx nx build app-name

# Build only affected apps (uses Nx affected logic)
npx nx affected -t build

# Deploy (currently a stub executor, logs manifest)
npx nx deploy app-name
```

**Dev server specifics:**

- Uses `devApp.js` and `isolatedApp.js` entry points
- Loads from `public/DevCenterAppPage.html` and `public/DevCenterIsolatedAppPage.html`
- Connects to Corva API via `CORVA_API_ENV` environment variable (defaults to `production`)

## Project Structure Patterns

Each app MUST have:

- `manifest.json` - Corva platform metadata (app key, segment, category)
- `package.json` - Version and dependencies (version synced with `.release-please-manifest.json`)
- `vite.config.ts` - Imports `createViteConfig` from `@corva/vite-config`
- `src/` - App source code
- `tsconfig.app.json` - Extends base config with paths
- `project.json` - Optional (Nx infers targets from plugins)

**The `@corva/cca` plugin** (`tools/cca/src/index.ts`) infers `deploy` target by:

1. Finding `package.json` files
2. Checking for sibling `project.json` and `manifest.json`
3. Adding deploy target that depends on build

## Testing

- **Unit tests**: Vitest (see `vitest.workspace.ts`)
- **E2E tests**: Playwright (configured via `@nx/playwright` plugin)
- Tests run via `npx nx test app-name` or `npx nx affected -t test`

## CI/CD

**Workflows** (`.github/workflows/`):

- `deploy.yml` - Builds affected apps on PR/push, creates artifacts with `manifest.json,package.json,build/**`
- `release-please.yml` - Manages versioning via release-please
- `semantic-pr.yml` - Validates PR titles

**Key deployment detail**: Apps are zipped with `manifest.json` + `package.json` + `build/**` for platform deployment.

## Patches

**Critical patches** in `patches/`:

- `@corva+create-app+0.111.1.patch` - Updates Node runtime to v22
- `@corva+ui+3.15.0-9.patch` - UI library modifications
- Applied via `patch-package` in postinstall

## Common Pitfalls

1. **Don't add platform externals to dependencies** - Check `CORVA_GLOBAL_DEPENDENCIES` first
2. **Never edit generated vite configs directly** - Modify `tools/vite-config/src/lib/vite-config.ts`
3. **Respect manifest.json structure** - Platform relies on `application.key` format (`provider.app-name`)
4. **Build outputs must include manifest/package.json** - Deployment expects this structure

## Key Files to Reference

- [tools/cca/src/index.ts](tools/cca/src/index.ts) - Nx plugin that infers deploy targets
- [tools/vite-config/src/lib/vite-config.ts](tools/vite-config/src/lib/vite-config.ts) - Shared build config
- [tools/cca/generators/lib/application-generator/create-app.ts](tools/cca/generators/lib/application-generator/create-app.ts) - App generation logic
- [nx.json](nx.json) - Nx plugin configuration and target defaults
