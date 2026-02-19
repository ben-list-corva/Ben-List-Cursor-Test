/**
 * Pipeline Checker Types
 * Defines the data structures for pipeline validation results
 */

// Status types
export type CheckStatus = 'PASS' | 'WARN' | 'FAIL';
export type StreamType = 'frac' | 'wireline' | 'pumpdown';
export type StreamStatus = 'active' | 'idle' | 'missing' | 'unknown';
export type PadConfigType = 'zipper' | 'simulfrac' | 'unknown';

// Source App IDs mapping
export const SOURCE_APP_IDS: Record<StreamType, number> = {
  frac: 169,
  wireline: 170,
  pumpdown: 599,
};

// Source App Names mapping
export const SOURCE_APP_NAMES: Record<number, string> = {
  169: 'Stream Frac Source App',
  170: 'Stream Wireline Source App',
  599: 'Stream Pumpdown Source App',
};

/**
 * Settings from the Source App connection
 */
export interface StreamSettings {
  api_number: string | null;
  force_start_from: string | null;
  stream_api_root_url: string | null;
  stream_api_log_path: string | null;
  stream_api_key_masked: string | null;
}

/**
 * Source App information from app_connections
 */
export interface SourceAppInfo {
  app_id: number;
  app_name: string;
  status: 'active' | 'idle' | 'unknown' | 'missing';
  settings: StreamSettings | null;
  check_status: CheckStatus;
  failures: string[];
  warnings: string[];
  is_manual_pumpdown: boolean;  // True if pumpdown is routed through frac streambox
}

/**
 * Result for a single stream (Frac/Wireline/Pumpdown)
 */
export interface StreamResult {
  stream_id: number | null;
  stream_type: StreamType;
  stream_name: string | null;
  stream_status: StreamStatus;
  connected_app_ids: number[];
  connected_app_names: string[];
  source_app: SourceAppInfo | null;
  check_status: CheckStatus;
  failures: string[];
  warnings: string[];
}

/**
 * Stage information from Stream platform
 */
export interface StageInfo {
  stage_number: number;
  stage_action: string;
  stage_start: string;
  sb_id: string | null;
  status: string;
}

/**
 * Stage status summary
 */
export interface StageStatus {
  has_stages: boolean;
  has_active_stage: boolean;
  active_stage_number: number | null;
  active_stage_action: string | null;
  sb_id: string | null;
  stage_start: string | null;
  check_status: CheckStatus;
  failures: string[];
  warnings: string[];
}

/**
 * Pumping schedule check results (informational only)
 */
export interface ScheduleCheck {
  stage_1_has_schedule: boolean | null;
  last_stage_number: number | null;
  last_stage_has_schedule: boolean | null;
}

/**
 * Result for a single well
 */
export interface WellResult {
  corva_well_asset_id: number;
  well_id: number | null;
  well_name: string;
  api_number: string | null;
  color: string | null;  // Wellhead color from custom_properties
  line_assignment: string | null;  // For SimulFrac: "Line A", "Line B", etc.
  corva_streams: {
    frac: StreamResult | null;
    wireline: StreamResult | null;
    pumpdown: StreamResult | null;
  };
  stream_platform_well_id: string | null;
  stream_platform_well_name: string | null;
  stream_platform_check: {
    check_status: CheckStatus;
    failures: string[];
    warnings: string[];
  };
  stage_status: StageStatus | null;
  schedule_check: ScheduleCheck | null;  // Pumping schedule check (informational)
  overall_status: CheckStatus;
  failures: string[];
  warnings: string[];
}

/**
 * Viewer stream result
 */
export interface ViewerStreamResult {
  stream_id: number | null;
  stream_type: StreamType;
  stream_name: string | null;
  stream_status: StreamStatus;
  connected_app_ids: number[];
  connected_app_names: string[];
  source_app: SourceAppInfo | null;
  check_status: CheckStatus;
  failures: string[];
  warnings: string[];
}

/**
 * Result for the viewer asset check
 */
export interface ViewerResult {
  viewer_asset_id: number | null;
  viewer_name: string | null;
  viewer_status: string | null;
  viewer_pad_id: number | null;
  frac_fleet_id: string | null;
  frac_fleet_name: string | null;
  line_name: string | null;  // For SimulFrac: "Line A", "Line B", etc.
  api_number: string | null;
  streams: {
    frac: ViewerStreamResult | null;
    wireline: ViewerStreamResult | null;
    pumpdown: ViewerStreamResult | null;
  };
  stream_platform_well_id: string | null;
  stream_platform_well_name: string | null;
  stream_platform_check: {
    check_status: CheckStatus;
    failures: string[];
    warnings: string[];
  } | null;
  stage_status: StageStatus | null;
  check_status: CheckStatus;
  failures: string[];
  warnings: string[];
}

/**
 * Frac fleet line for SimulFrac pads
 */
export interface FracFleetLine {
  line_id: number;
  name: string;
  well_ids: number[];
  viewer_well_id: number | null;
}

/**
 * Pad frac configuration (Zipper vs SimulFrac)
 */
export interface PadConfiguration {
  config_type: PadConfigType;
  frac_fleet_id: number | null;
  frac_fleet_name: string | null;
  lines: FracFleetLine[];
}

/**
 * Single Stream Platform pad info
 */
export interface StreamPadInfo {
  stream_pad_id: string;
  pad_name: string;
  pad_type: 'well' | 'viewer';
  active_wells: string[];
  company_name: string | null;
  frac_fleet_name: string | null;
  frac_sb_id: string | null;
  wireline_sb_id: string | null;
  pumpdown_sb_id: string | null;
  status: string | null;
  wells_match_corva_pad: boolean;
  active_job_warning: string | null;
}

/**
 * Stream Platform pad check result
 */
export interface StreamPadCheck {
  pads: StreamPadInfo[];
  total_pads_found: number;
  well_pads_found: number;
  viewer_pads_found: number;
  check_status: CheckStatus;
  failures: string[];
  warnings: string[];
}

/**
 * Result for the entire pad
 */
export interface PadResult {
  pad_id: number;
  pad_name: string;
  configuration: PadConfiguration | null;
  viewers: ViewerResult[];  // Can be multiple for SimulFrac pads
  wells: WellResult[];
  stream_pad_check: StreamPadCheck | null;  // Stream Platform pad check
  overall_status: CheckStatus;
  total_failures: number;
  total_warnings: number;
  checked_at: string;
}

/**
 * Asset context from Corva dashboard chips
 */
export interface AssetContext {
  padId: number | null;
  padName: string | null;
  completionWellAssetId: number | null;
  wellName: string | null;
  fracFleetId: number | null;
}

/**
 * API request payload
 */
export interface PipelineCheckRequest {
  pad_id: number;
  well_asset_id?: number;
}

/**
 * API response wrapper
 */
export interface PipelineCheckResponse {
  success: boolean;
  data: PadResult | null;
  error: string | null;
}

/**
 * Loading states for the UI
 */
export interface LoadingState {
  isLoading: boolean;
  currentStep: string | null;
  progress: number;
}

/**
 * Helper function to get status color
 */
export function getStatusColor(status: CheckStatus): string {
  switch (status) {
    case 'PASS':
      return '#4caf50'; // Green
    case 'WARN':
      return '#ff9800'; // Orange
    case 'FAIL':
      return '#f44336'; // Red
    default:
      return '#9e9e9e'; // Gray
  }
}

/**
 * Helper function to get status icon
 */
export function getStatusIcon(status: CheckStatus): string {
  switch (status) {
    case 'PASS':
      return '✅';
    case 'WARN':
      return '⚠️';
    case 'FAIL':
      return '❌';
    default:
      return '❓';
  }
}

/**
 * Helper function to get app name from ID
 */
export function getAppName(appId: number): string {
  return SOURCE_APP_NAMES[appId] || `App ${appId}`;
}
