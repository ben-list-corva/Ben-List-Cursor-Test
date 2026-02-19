import {
  Box,
  TextField,
  Tooltip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Autocomplete,
  Chip,
  FormControlLabel,
  Switch,
} from "@mui/material";

interface ConfigInputsProps {
  mode: string;
  minCoverage: number;
  maxMissingFms: number;
  onMinCoverageChange: (val: number) => void;
  onMaxMissingFmsChange: (val: number) => void;
  holeSizeTolerance: number;
  onHoleSizeToleranceChange: (val: number) => void;
  bhaType: string;
  onBhaTypeChange: (val: string) => void;
  selectedFormations: string[];
  onSelectedFormationsChange: (val: string[]) => void;
  availableFormations: string[];
  disabled: boolean;
}

export default function ConfigInputs({
  mode,
  minCoverage,
  maxMissingFms,
  onMinCoverageChange,
  onMaxMissingFmsChange,
  holeSizeTolerance,
  onHoleSizeToleranceChange,
  bhaType,
  onBhaTypeChange,
  selectedFormations,
  onSelectedFormationsChange,
  availableFormations,
  disabled,
}: ConfigInputsProps) {
  return (
    <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", alignItems: "center" }}>
      {/* Hole size tolerance toggle */}
      <Tooltip title='Allow +/- 0.25" hole size grouping (e.g. 8.5" and 8.75" together)'>
        <FormControlLabel
          control={
            <Switch
              checked={holeSizeTolerance > 0}
              onChange={(e) =>
                onHoleSizeToleranceChange(e.target.checked ? 0.25 : 0)
              }
              disabled={disabled}
              size="small"
            />
          }
          label={`Hole Size ${holeSizeTolerance > 0 ? `\u00B10.25"` : "Exact"}`}
          sx={{ mr: 1 }}
        />
      </Tooltip>

      {/* BHA type filter */}
      <Tooltip title="Filter by BHA type: RSS, Conventional, or Both">
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>BHA Type</InputLabel>
          <Select
            value={bhaType}
            label="BHA Type"
            onChange={(e) => onBhaTypeChange(e.target.value)}
            disabled={disabled}
          >
            <MenuItem value="conventional">Conventional</MenuItem>
            <MenuItem value="rss">RSS</MenuItem>
            <MenuItem value="both">Both</MenuItem>
          </Select>
        </FormControl>
      </Tooltip>

      {/* Target formation picker (lateral only) */}
      {mode === "lateral" && (
        <Tooltip title="Filter offset wells by target formation (lateral sections only)">
          <Autocomplete
            multiple
            size="small"
            options={availableFormations}
            value={selectedFormations}
            onChange={(_, val) => onSelectedFormationsChange(val)}
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
                label="Target Formations"
                placeholder={selectedFormations.length === 0 ? "All formations" : ""}
              />
            )}
            sx={{ minWidth: 260 }}
            disabled={disabled}
          />
        </Tooltip>
      )}

      {/* Vertical-specific controls */}
      {mode === "vertical" && (
        <>
          <Tooltip title="Maximum number of formations an equivalent BHA group can be missing data for and still be included">
            <TextField
              label="Max Missing Fms"
              type="number"
              value={maxMissingFms}
              onChange={(e) =>
                onMaxMissingFmsChange(parseInt(e.target.value) || 0)
              }
              inputProps={{ min: 0, max: 10, step: 1 }}
              size="small"
              sx={{ width: 160 }}
              disabled={disabled}
            />
          </Tooltip>
        </>
      )}
    </Box>
  );
}
