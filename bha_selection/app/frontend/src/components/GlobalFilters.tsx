import { useEffect } from "react";
import {
  Box,
  Paper,
  Typography,
  Autocomplete,
  TextField,
  Chip,
  CircularProgress,
} from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { getOffsetFilterOptions } from "../api/client";

interface GlobalFiltersProps {
  assetId: string;
  selectedBasins: string[];
  onBasinsChange: (basins: string[]) => void;
}

export default function GlobalFilters({
  assetId,
  selectedBasins,
  onBasinsChange,
}: GlobalFiltersProps) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["offset-filters", assetId],
    queryFn: () => getOffsetFilterOptions(assetId),
    enabled: !!assetId,
  });

  const availableBasins = data?.basins ?? [];

  useEffect(() => {
    if (availableBasins.length > 0 && selectedBasins.length === 0) {
      onBasinsChange(availableBasins);
    }
  }, [availableBasins, selectedBasins.length, onBasinsChange]);

  return (
    <Paper sx={{ p: 2, bgcolor: "background.paper" }}>
      <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
        Global Filters
      </Typography>
      <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", alignItems: "center" }}>
        <Autocomplete
          multiple
          size="small"
          options={availableBasins}
          value={selectedBasins}
          onChange={(_, val) => onBasinsChange(val)}
          disableCloseOnSelect
          renderTags={(value, getTagProps) =>
            value.map((opt, idx) => (
              <Chip
                label={opt}
                size="small"
                {...getTagProps({ index: idx })}
                key={opt}
              />
            ))
          }
          renderInput={(params) => (
            <TextField
              {...params}
              label="Basin Filter"
              placeholder="All basins"
            />
          )}
          sx={{ minWidth: 300 }}
        />
        {isLoading && assetId && (
          <CircularProgress size={18} />
        )}
        {isError && assetId && (
          <Typography variant="caption" color="warning.main">
            Basin options unavailable. Confirm backend API is reachable.
          </Typography>
        )}
        {!isLoading && !isError && assetId && availableBasins.length === 0 && (
          <Typography variant="caption" color="warning.main">
            No basin values were found for this analysis run.
          </Typography>
        )}
        <Typography variant="caption" color="text.secondary">
          {selectedBasins.length === availableBasins.length || selectedBasins.length === 0
            ? "All basins included"
            : `${selectedBasins.length} of ${availableBasins.length} basins selected`}
        </Typography>
      </Box>
    </Paper>
  );
}
