import type {
  AnalyzeWellResponse,
  OffsetWellsResponse,
  OffsetFilterOptions,
  RunSectionRequest,
  JobStatus,
  SectionResults,
  CanonicalFormationsResponse,
} from "../types";

const BASE = "";

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status}: ${text}`);
  }
  return res.json();
}

export async function analyzeWell(
  assetId: string,
  searchRadiusMiles: number = 15,
  spudDateFilter?: string | null
): Promise<AnalyzeWellResponse> {
  const body: Record<string, unknown> = {
    asset_id: assetId,
    search_radius_miles: searchRadiusMiles,
  };
  if (spudDateFilter) {
    body.spud_date_filter = spudDateFilter;
  }
  return fetchJSON("/api/analyze-well", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function getOffsetWells(
  sectionName: string,
  holeSize: number,
  assetId?: string
): Promise<OffsetWellsResponse> {
  const params = new URLSearchParams({
    section_name: sectionName,
    hole_size: String(holeSize),
  });
  if (assetId) params.set("asset_id", assetId);
  return fetchJSON(`/api/offset-wells?${params}`);
}

export async function getOffsetFilterOptions(
  assetId?: string
): Promise<OffsetFilterOptions> {
  const params = new URLSearchParams();
  if (assetId) params.set("asset_id", assetId);
  return fetchJSON(`/api/offset-filters?${params}`);
}

export async function runSection(
  req: RunSectionRequest
): Promise<{ job_id: string }> {
  return fetchJSON("/api/run-section", {
    method: "POST",
    body: JSON.stringify(req),
  });
}

export async function getJobStatus(jobId: string): Promise<JobStatus> {
  return fetchJSON(`/api/job/${jobId}/status`);
}

export async function getSectionResults(
  sectionName: string,
  assetId?: string
): Promise<SectionResults> {
  const params = new URLSearchParams();
  if (assetId) params.set("asset_id", assetId);
  const qs = params.toString();
  return fetchJSON(`/api/results/${sectionName}${qs ? `?${qs}` : ""}`);
}

export async function getCanonicalFormations(
  tvdTop?: number | null,
  tvdBottom?: number | null
): Promise<CanonicalFormationsResponse> {
  const params = new URLSearchParams();
  if (tvdTop != null) params.set("tvd_top", String(tvdTop));
  if (tvdBottom != null) params.set("tvd_bottom", String(tvdBottom));
  const qs = params.toString();
  return fetchJSON(`/api/canonical-formations${qs ? `?${qs}` : ""}`);
}
