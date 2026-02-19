import { useState, useEffect, useCallback, useRef } from "react";
import {
  Box,
  Paper,
  Typography,
  Divider,
  Alert,
  LinearProgress,
} from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import {
  getOffsetWells,
  getOffsetFilterOptions,
  getJobStatus,
  getSectionResults,
} from "../api/client";
import OffsetWellsTable from "./OffsetWellsTable";
import ConfigInputs from "./ConfigInputs";
import RunButton from "./RunButton";
import ChartGrid from "./ChartGrid";
import TTDRanking from "./TTDRanking";
import FormationMapping from "./FormationMapping";
import type { WellSection, JobStatus, SectionResults } from "../types";

interface SectionPanelProps {
  section: WellSection;
  assetId: string;
  basinFilter: string[];
}

export default function SectionPanel({ section, assetId, basinFilter }: SectionPanelProps) {
  const [minCoverage, setMinCoverage] = useState(0.5);
  const [maxMissingFms, setMaxMissingFms] = useState(1);
  const [holeSizeTolerance, setHoleSizeTolerance] = useState(0.0);
  const [bhaType, setBhaType] = useState("conventional");
  const [selectedFormations, setSelectedFormations] = useState<string[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null);
  const [results, setResults] = useState<SectionResults | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const offsetQuery = useQuery({
    queryKey: ["offsets", section.name, section.hole_size, assetId],
    queryFn: () => getOffsetWells(section.name, section.hole_size ?? 0, assetId),
    enabled: !!section.hole_size,
  });

  const filterOptsQuery = useQuery({
    queryKey: ["offset-filters", assetId],
    queryFn: () => getOffsetFilterOptions(assetId),
    enabled: !!assetId,
  });

  const availableFormations = filterOptsQuery.data?.target_formations ?? [];
  const targetAssetFormation = filterOptsQuery.data?.target_asset_formation ?? null;

  const safeName = section.name.replace(/ /g, "_").replace(/\//g, "-");

  const stopPolling = useCallback(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }, []);

  const loadResultsWithRetry = useCallback(async () => {
    let lastError = "";
    for (let attempt = 1; attempt <= 5; attempt++) {
      try {
        const res = await getSectionResults(safeName, assetId);
        if (res.charts.length > 0 || res.ttd_ranking.length > 0) {
          setResults(res);
          return true;
        }
        if (res.analyzed_runs === 0 && (res.filtered_runs > 0 || res.runs_with_data > 0)) {
          setResults(res);
          return true;
        }
      } catch (err) {
        lastError = err instanceof Error ? err.message : String(err);
      }
      await new Promise((resolve) => setTimeout(resolve, attempt * 1000));
    }

    setJobStatus((prev) =>
      prev
        ? {
            ...prev,
            status: "failed",
            error:
              lastError ||
              "Analysis completed but result files were not available yet.",
          }
        : prev
    );
    return false;
  }, [safeName, assetId]);

  const startPolling = useCallback(
    (jid: string) => {
      stopPolling();
      pollRef.current = setInterval(async () => {
        try {
          const status = await getJobStatus(jid);
          setJobStatus(status);
          if (status.status === "completed" || status.status === "failed") {
            stopPolling();
            if (status.status === "completed") {
              const loaded = await loadResultsWithRetry();
              if (loaded) {
                // Refresh offset wells to get updated BHA run counts
                offsetQuery.refetch();
              }
            }
          }
        } catch (err) {
          stopPolling();
          const msg = err instanceof Error ? err.message : String(err);
          setJobStatus((prev) =>
            prev
              ? {
                  ...prev,
                  status: "failed",
                  error: `Polling failed: ${msg}`,
                }
              : prev
          );
        }
      }, 2000);
    },
    [stopPolling, loadResultsWithRetry, offsetQuery]
  );

  useEffect(() => {
    return () => stopPolling();
  }, [stopPolling]);

  const handleJobStarted = (jid: string) => {
    setJobId(jid);
    setJobStatus({
      job_id: jid,
      status: "pending",
      progress: "Starting...",
      step: 0,
      total_steps: 8,
      error: null,
    });
    setResults(null);
    startPolling(jid);
  };

  // Clear results when asset changes
  useEffect(() => {
    setResults(null);
    setJobId(null);
    setJobStatus(null);
    setSelectedFormations([]);
  }, [assetId]);

  // Default target formation for lateral sections when none selected.
  useEffect(() => {
    if (section.mode !== "lateral") return;
    if (selectedFormations.length > 0) return;
    if (!targetAssetFormation) return;
    if (!availableFormations.includes(targetAssetFormation)) return;
    setSelectedFormations([targetAssetFormation]);
  }, [
    section.mode,
    selectedFormations.length,
    targetAssetFormation,
    availableFormations,
  ]);

  // Try to load existing results on mount or asset change
  useEffect(() => {
    getSectionResults(safeName, assetId)
      .then((res) => {
        if (res.charts.length > 0 || res.ttd_ranking.length > 0) {
          setResults(res);
        }
      })
      .catch(() => {});
  }, [safeName, assetId]);

  const isRunning =
    jobStatus?.status === "pending" || jobStatus?.status === "running";
  const progressPct = jobStatus
    ? (jobStatus.step / jobStatus.total_steps) * 100
    : 0;

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
      {/* Section Info Header */}
      <Paper sx={{ p: 2, bgcolor: "background.paper" }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
          {section.name}
          {section.hole_size && ` (${section.hole_size}")`}
          {" - "}
          <Typography
            component="span"
            sx={{
              color:
                section.mode === "lateral" ? "primary.main" : "secondary.main",
            }}
          >
            {section.mode}
          </Typography>
        </Typography>
        <Typography variant="body2" color="text.secondary">
          MD: {section.top_md.toLocaleString()}' -{" "}
          {section.bottom_md.toLocaleString()}' (
          {section.section_length_md.toLocaleString()}' total)
          {section.formations_in_section.length > 0 && (
            <>
              {" | "}
              Formations: {section.formations_in_section.join(", ")}
            </>
          )}
        </Typography>
      </Paper>

      {/* Canonical Formation Mapping -- show for vertical sections */}
      {section.mode === "vertical" && (
        <Paper sx={{ p: 2, bgcolor: "background.paper" }}>
          <FormationMapping
            tvdTop={section.top_tvd}
            tvdBottom={section.bottom_tvd}
          />
        </Paper>
      )}

      {/* Offset Wells */}
      <Paper sx={{ p: 2, bgcolor: "background.paper" }}>
        <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
          OFFSET WELLS
          {offsetQuery.data && (
            <Typography component="span" color="text.secondary" sx={{ ml: 1 }}>
              ({offsetQuery.data.total} runs from {offsetQuery.data.filtered}{" "}
              wells)
            </Typography>
          )}
        </Typography>
        {offsetQuery.isLoading && <LinearProgress />}
        {offsetQuery.data && (
          <>
            <OffsetWellsTable wells={offsetQuery.data.wells} />
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ mt: 1, display: "block" }}
            >
              BHA Runs reflects runs matched to this section; values remain 0 until section filtering completes.
            </Typography>
          </>
        )}
      </Paper>

      {/* Configuration + Run */}
      <Paper sx={{ p: 2, bgcolor: "background.paper" }}>
        <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
          CONFIGURATION
        </Typography>
        <ConfigInputs
          mode={section.mode}
          minCoverage={minCoverage}
          maxMissingFms={maxMissingFms}
          onMinCoverageChange={setMinCoverage}
          onMaxMissingFmsChange={setMaxMissingFms}
          holeSizeTolerance={holeSizeTolerance}
          onHoleSizeToleranceChange={setHoleSizeTolerance}
          bhaType={bhaType}
          onBhaTypeChange={setBhaType}
          selectedFormations={selectedFormations}
          onSelectedFormationsChange={setSelectedFormations}
          availableFormations={availableFormations}
          disabled={isRunning}
        />
        {section.mode === "lateral" && filterOptsQuery.isError && (
          <Typography variant="caption" color="warning.main" sx={{ mt: 1, display: "block" }}>
            Target formation options failed to load. Check backend connectivity.
          </Typography>
        )}
        {section.mode === "lateral" &&
          !filterOptsQuery.isLoading &&
          !filterOptsQuery.isError &&
          availableFormations.length === 0 && (
            <Typography variant="caption" color="warning.main" sx={{ mt: 1, display: "block" }}>
              No target formation values were found for this analysis run.
            </Typography>
          )}
        <Divider sx={{ my: 2 }} />
        <RunButton
          assetId={assetId}
          section={section}
          minCoverage={minCoverage}
          maxMissingFms={maxMissingFms}
          holeSizeTolerance={holeSizeTolerance}
          bhaType={bhaType}
          targetFormations={section.mode === "lateral" ? selectedFormations : undefined}
          basinFilter={basinFilter}
          onJobStarted={handleJobStarted}
          disabled={isRunning}
        />
        {isRunning && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress variant="determinate" value={progressPct} />
            <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: "block" }}>
              Step {jobStatus!.step}/{jobStatus!.total_steps}:{" "}
              {jobStatus!.progress}
            </Typography>
          </Box>
        )}
        {jobStatus?.status === "failed" && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {jobStatus.error || "Pipeline failed"}
          </Alert>
        )}
        {jobStatus?.status === "completed" && !results && (
          <Alert severity="success" sx={{ mt: 2 }}>
            Analysis complete! Loading results...
          </Alert>
        )}
      </Paper>

      {/* Results */}
      {results && (
        <Paper sx={{ p: 2, bgcolor: "background.paper" }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
            RESULTS
          </Typography>
          {(results.filtered_runs > 0 || results.analyzed_runs > 0) && (
            <Box sx={{ mb: 2, display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap" }}>
              {results.filtered_runs > 0 && (
                <Typography variant="body2" color="text.secondary">
                  {results.filtered_runs} section-filtered
                </Typography>
              )}
              {results.runs_with_data > 0 && (
                <>
                  <Typography variant="body2" color="text.secondary">→</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {results.runs_with_data} with WITS data
                  </Typography>
                </>
              )}
              {results.runs_in_curves > 0 && (
                <>
                  <Typography variant="body2" color="text.secondary">→</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {results.runs_in_curves} with formation coverage
                  </Typography>
                </>
              )}
              {results.analyzed_runs > 0 && (
                <>
                  <Typography variant="body2" color="text.secondary">→</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {results.analyzed_runs} in qualifying BHA groups
                  </Typography>
                </>
              )}
            </Box>
          )}
          {results.charts.length === 0 && results.ttd_ranking.length === 0 ? (
            <Alert severity="info">
              Analysis completed, but no qualifying runs remained to build curves/charts for this section with current filters.
            </Alert>
          ) : (
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", md: "1fr 2fr" },
                gap: 2,
              }}
            >
              <Box>
                <TTDRanking entries={results.ttd_ranking} />
              </Box>
              <Box>
                <ChartGrid charts={results.charts} />
              </Box>
            </Box>
          )}
        </Paper>
      )}
    </Box>
  );
}
