import { Button, CircularProgress, Typography, Box } from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { useMutation } from "@tanstack/react-query";
import { runSection } from "../api/client";
import type { WellSection } from "../types";

interface RunButtonProps {
  assetId: string;
  section: WellSection;
  minCoverage: number;
  maxMissingFms: number;
  holeSizeTolerance: number;
  bhaType: string;
  targetFormations?: string[];
  basinFilter?: string[];
  onJobStarted: (jobId: string) => void;
  disabled: boolean;
}

async function runSectionWithRetry(
  ...args: Parameters<typeof runSection>
): ReturnType<typeof runSection> {
  const maxRetries = 3;
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await runSection(...args);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      const isTransient = msg.startsWith("422") || msg.startsWith("502") || msg.startsWith("503");
      if (isTransient && attempt < maxRetries - 1) {
        await new Promise((r) => setTimeout(r, 1000 * (attempt + 1)));
        continue;
      }
      throw err;
    }
  }
  throw new Error("Unexpected: exhausted retries");
}

export default function RunButton({
  assetId,
  section,
  minCoverage,
  maxMissingFms,
  holeSizeTolerance,
  bhaType,
  targetFormations,
  basinFilter,
  onJobStarted,
  disabled,
}: RunButtonProps) {
  const mutation = useMutation({
    mutationFn: () =>
      runSectionWithRetry({
        asset_id: assetId,
        section_name: section.name,
        mode: section.mode,
        hole_size: section.hole_size,
        min_coverage: minCoverage,
        max_missing_formations: maxMissingFms,
        section_length: section.section_length_md,
        hole_size_tolerance: holeSizeTolerance,
        bha_type: bhaType,
        target_formations:
          targetFormations && targetFormations.length > 0
            ? targetFormations
            : undefined,
        basin_filter:
          basinFilter && basinFilter.length > 0 ? basinFilter : undefined,
      }),
    onSuccess: (data) => onJobStarted(data.job_id),
  });

  return (
    <Box>
      <Button
        variant="contained"
        color="primary"
        size="large"
        startIcon={
          mutation.isPending ? (
            <CircularProgress size={20} color="inherit" />
          ) : (
            <PlayArrowIcon />
          )
        }
        onClick={() => mutation.mutate()}
        disabled={disabled || mutation.isPending}
      >
        {mutation.isPending ? "Starting..." : "Run Analysis"}
      </Button>
      {mutation.isError && (
        <Typography color="error" variant="body2" sx={{ mt: 1 }}>
          Failed to start: {mutation.error?.message ?? "Unknown error"}
        </Typography>
      )}
    </Box>
  );
}
