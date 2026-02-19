import { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Paper,
  CircularProgress,
  Alert,
  Chip,
  InputAdornment,
  Tooltip,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { useMutation } from "@tanstack/react-query";
import { analyzeWell } from "../api/client";
import type { AnalyzeWellResponse } from "../types";

type DatePreset = "1m" | "3m" | "1y" | "custom" | "all";

function getDateCutoff(preset: DatePreset, customDate: string): string | null {
  if (preset === "all") return null;
  if (preset === "custom") return customDate || null;

  const now = new Date();
  if (preset === "1m") now.setMonth(now.getMonth() - 1);
  else if (preset === "3m") now.setMonth(now.getMonth() - 3);
  else if (preset === "1y") now.setFullYear(now.getFullYear() - 1);

  return now.toISOString().split("T")[0];
}

interface WellInputProps {
  onAnalyzed: (data: AnalyzeWellResponse) => void;
}

export default function WellInput({ onAnalyzed }: WellInputProps) {
  const [assetId, setAssetId] = useState("");
  const [searchRadius, setSearchRadius] = useState(15);
  const [datePreset, setDatePreset] = useState<DatePreset>("1y");
  const [customDate, setCustomDate] = useState("");

  const mutation = useMutation({
    mutationFn: ({
      id,
      radius,
      dateCutoff,
    }: {
      id: string;
      radius: number;
      dateCutoff: string | null;
    }) => analyzeWell(id, radius, dateCutoff),
    onSuccess: (data) => onAnalyzed(data),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (assetId.trim()) {
      const dateCutoff = getDateCutoff(datePreset, customDate);
      mutation.mutate({
        id: assetId.trim(),
        radius: searchRadius,
        dateCutoff,
      });
    }
  };

  return (
    <Paper sx={{ p: 3, bgcolor: "background.paper" }}>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 2,
          flexWrap: "wrap",
        }}
      >
        <TextField
          label="Target Well Asset ID"
          value={assetId}
          onChange={(e) => setAssetId(e.target.value)}
          placeholder="e.g. 82512872"
          size="small"
          sx={{ minWidth: 220 }}
          disabled={mutation.isPending}
        />

        <Tooltip title="Radius in miles to search for offset wells">
          <TextField
            label="Search Radius (mi)"
            type="number"
            value={searchRadius}
            onChange={(e) =>
              setSearchRadius(Math.max(1, parseFloat(e.target.value) || 15))
            }
            inputProps={{ min: 1, max: 500, step: 1 }}
            size="small"
            sx={{ width: 140 }}
            disabled={mutation.isPending}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">mi</InputAdornment>
              ),
            }}
          />
        </Tooltip>

        <Tooltip title="Only include offset wells spudded after this date">
          <FormControl size="small" sx={{ minWidth: 160 }}>
            <InputLabel>Spud Date Filter</InputLabel>
            <Select
              value={datePreset}
              label="Spud Date Filter"
              onChange={(e) => setDatePreset(e.target.value as DatePreset)}
              disabled={mutation.isPending}
            >
              <MenuItem value="1m">Last Month</MenuItem>
              <MenuItem value="3m">Last 3 Months</MenuItem>
              <MenuItem value="1y">Last Year</MenuItem>
              <MenuItem value="custom">Custom Date</MenuItem>
              <MenuItem value="all">All Time</MenuItem>
            </Select>
          </FormControl>
        </Tooltip>

        {datePreset === "custom" && (
          <TextField
            label="Cutoff Date"
            type="date"
            value={customDate}
            onChange={(e) => setCustomDate(e.target.value)}
            size="small"
            sx={{ width: 160 }}
            disabled={mutation.isPending}
            InputLabelProps={{ shrink: true }}
          />
        )}

        <Button
          type="submit"
          variant="contained"
          startIcon={
            mutation.isPending ? (
              <CircularProgress size={18} color="inherit" />
            ) : (
              <SearchIcon />
            )
          }
          disabled={!assetId.trim() || mutation.isPending}
        >
          {mutation.isPending ? "Pulling..." : "Pull Offsets"}
        </Button>

        {mutation.data && (
          <Chip
            label={`${mutation.data.sections.length} sections found`}
            color="success"
            variant="outlined"
          />
        )}
      </Box>

      {mutation.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {(mutation.error as Error).message}
        </Alert>
      )}
    </Paper>
  );
}
