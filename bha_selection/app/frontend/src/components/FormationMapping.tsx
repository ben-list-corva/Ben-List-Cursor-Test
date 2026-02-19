import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Box,
  Chip,
  List,
  ListItem,
  ListItemText,
  Typography,
  Skeleton,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import LayersIcon from "@mui/icons-material/Layers";
import { useQuery } from "@tanstack/react-query";
import { getCanonicalFormations } from "../api/client";
import type { CanonicalFormation } from "../types";

interface FormationMappingProps {
  tvdTop?: number | null;
  tvdBottom?: number | null;
}

function FormationRow({ fm }: { fm: CanonicalFormation }) {
  const hasSubs = fm.sub_formations.length > 1 ||
    (fm.sub_formations.length === 1 &&
      fm.sub_formations[0] !== fm.canonical_name);

  const tvdLabel =
    fm.tvd_top != null && fm.tvd_bottom != null
      ? `${fm.tvd_top.toLocaleString()}' - ${fm.tvd_bottom.toLocaleString()}' TVD`
      : "";

  if (!hasSubs) {
    return (
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          py: 0.75,
          px: 2,
          borderBottom: 1,
          borderColor: "divider",
        }}
      >
        <Typography variant="body2" sx={{ fontWeight: 500 }}>
          {fm.canonical_name}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {tvdLabel}
        </Typography>
      </Box>
    );
  }

  return (
    <Accordion
      disableGutters
      elevation={0}
      sx={{
        "&:before": { display: "none" },
        borderBottom: 1,
        borderColor: "divider",
        bgcolor: "transparent",
      }}
    >
      <AccordionSummary
        expandIcon={<ExpandMoreIcon sx={{ fontSize: "1rem" }} />}
        sx={{ minHeight: 40, px: 2, "& .MuiAccordionSummary-content": { my: 0.5 } }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            width: "100%",
            pr: 1,
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              {fm.canonical_name}
            </Typography>
            <Chip
              label={`${fm.sub_formations.length} names`}
              size="small"
              variant="outlined"
              sx={{ height: 18, fontSize: "0.65rem" }}
            />
          </Box>
          <Typography variant="caption" color="text.secondary">
            {tvdLabel}
          </Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails sx={{ pt: 0, pb: 1, px: 2, pl: 4 }}>
        <List dense disablePadding>
          {fm.sub_formations.map((sub, idx) => (
            <ListItem key={idx} disablePadding sx={{ py: 0 }}>
              <ListItemText
                primary={sub}
                primaryTypographyProps={{
                  variant: "caption",
                  color: "text.secondary",
                  sx: { pl: 1, borderLeft: 2, borderColor: "primary.main" },
                }}
              />
            </ListItem>
          ))}
        </List>
      </AccordionDetails>
    </Accordion>
  );
}

export default function FormationMapping({
  tvdTop,
  tvdBottom,
}: FormationMappingProps) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["canonical-formations", tvdTop, tvdBottom],
    queryFn: () => getCanonicalFormations(tvdTop, tvdBottom),
  });

  if (isLoading) {
    return <Skeleton variant="rectangular" height={80} />;
  }

  if (error) {
    return (
      <Typography variant="body2" color="error">
        Failed to load formation mapping.
      </Typography>
    );
  }

  if (!data || data.formations.length === 0) {
    return (
      <Typography variant="body2" color="text.secondary">
        No canonical formation data available.
      </Typography>
    );
  }

  return (
    <Box>
      <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
        <LayersIcon fontSize="small" color="secondary" />
        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
          FORMATIONS
        </Typography>
        <Typography variant="caption" color="text.secondary">
          ({data.total_canonical} canonical from {data.total_raw} raw names)
        </Typography>
      </Box>
      <Box
        sx={{
          border: 1,
          borderColor: "divider",
          borderRadius: 1,
          overflow: "hidden",
        }}
      >
        {data.formations.map((fm) => (
          <FormationRow key={fm.canonical_name} fm={fm} />
        ))}
      </Box>
    </Box>
  );
}
