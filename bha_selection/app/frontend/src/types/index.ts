export interface WellSection {
  name: string;
  hole_size: number | null;
  mode: "vertical" | "lateral";
  top_md: number;
  bottom_md: number;
  section_length_md: number;
  formations_in_section: string[];
  start_formation: string | null;
  end_formation: string | null;
  top_tvd?: number | null;
  bottom_tvd?: number | null;
}

export interface AnalyzeWellResponse {
  target_asset_id: string;
  well_name: string;
  sections: WellSection[];
}

export interface OffsetWell {
  asset_id: string;
  well_name: string;
  operator: string;
  distance_miles: string;
  runs: number;
  bha_number: string;
  bit_size: string;
  run_length: string;
  formation_coverage: string;
}

export interface OffsetWellsResponse {
  total: number;
  filtered: number;
  wells: OffsetWell[];
}

export interface RunSectionRequest {
  asset_id: string;
  section_name: string;
  mode: string;
  hole_size: number | null;
  min_coverage: number;
  max_missing_formations: number;
  section_length: number;
  target_formations?: string[];
  basin_filter?: string[];
  hole_size_tolerance: number;
  bha_type: string;
}

export interface OffsetFilterOptions {
  basins: string[];
  target_formations: string[];
  target_asset_formation?: string | null;
}

export interface JobStatus {
  job_id: string;
  status: "pending" | "running" | "completed" | "failed";
  progress: string;
  step: number;
  total_steps: number;
  error: string | null;
}

export interface ChartInfo {
  name: string;
  url: string;
}

export interface TTDBucket {
  label: string;
  length_ft: number;
  rotary_rop: number;
  rotary_time: number;
  slide_rop: number;
  slide_time: number;
  total_time: number;
}

export interface MotorSummary {
  motor_diam: string;
  rotor_lobes: string;
  stator_lobes: string;
  stages: string;
  label: string;
}

export interface BitTTDEntry {
  bit_manufacturer: string;
  bit_model: string;
  num_runs: number;
  ttd_hours: number;
  ttd_days: number;
}

export interface TTDEntry {
  group_key: string;
  num_runs: number;
  num_wells: number;
  ttd_hours: number;
  ttd_days: number;
  actual_slide_pct: number;
  is_rss: boolean;
  common_motor: MotorSummary;
  bit_ttd_by_mfg_model: BitTTDEntry[];
  fastest_bit?: BitTTDEntry | null;
  buckets: TTDBucket[];
}

export interface GroupInfo {
  group_key: string;
  num_runs: number;
  num_wells: number;
}

export interface SectionResults {
  section_name: string;
  hole_size: number | null;
  mode: string;
  charts: ChartInfo[];
  ttd_ranking: TTDEntry[];
  groups: GroupInfo[];
  filtered_runs: number;
  runs_with_data: number;
  runs_in_curves: number;
  analyzed_runs: number;
}

export interface CanonicalFormation {
  canonical_name: string;
  order: number;
  tvd_top: number | null;
  tvd_bottom: number | null;
  sub_formations: string[];
}

export interface CanonicalFormationsResponse {
  formations: CanonicalFormation[];
  total_canonical: number;
  total_raw: number;
}
