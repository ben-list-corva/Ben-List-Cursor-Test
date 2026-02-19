import { useState } from "react";
import {
  Box,
  Typography,
  Card,
  CardMedia,
  CardActionArea,
  Dialog,
  IconButton,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import type { ChartInfo } from "../types";

interface ChartGridProps {
  charts: ChartInfo[];
}

function formatChartName(name: string): string {
  return name
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function ChartGrid({ charts }: ChartGridProps) {
  const [expanded, setExpanded] = useState<ChartInfo | null>(null);

  if (charts.length === 0) {
    return (
      <Typography variant="body2" color="text.secondary">
        No charts available yet. Run analysis to generate charts.
      </Typography>
    );
  }

  return (
    <>
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: {
            xs: "1fr",
            sm: "1fr 1fr",
            lg: "1fr 1fr 1fr",
          },
          gap: 2,
        }}
      >
        {charts.map((chart) => (
          <Card key={chart.name} sx={{ bgcolor: "background.default" }}>
            <CardActionArea onClick={() => setExpanded(chart)}>
              <CardMedia
                component="img"
                image={chart.url}
                alt={chart.name}
                sx={{ objectFit: "contain", maxHeight: 260, p: 1 }}
              />
              <Typography
                variant="caption"
                sx={{
                  display: "block",
                  textAlign: "center",
                  pb: 1,
                  color: "text.secondary",
                }}
              >
                {formatChartName(chart.name)}
              </Typography>
            </CardActionArea>
          </Card>
        ))}
      </Box>

      <Dialog
        open={!!expanded}
        onClose={() => setExpanded(null)}
        maxWidth="xl"
        fullWidth
      >
        {expanded && (
          <Box sx={{ position: "relative", bgcolor: "#000", p: 1 }}>
            <IconButton
              onClick={() => setExpanded(null)}
              sx={{
                position: "absolute",
                right: 8,
                top: 8,
                color: "white",
                bgcolor: "rgba(0,0,0,0.5)",
              }}
            >
              <CloseIcon />
            </IconButton>
            <img
              src={expanded.url}
              alt={expanded.name}
              style={{
                width: "100%",
                height: "auto",
                maxHeight: "90vh",
                objectFit: "contain",
              }}
            />
            <Typography
              variant="body2"
              sx={{ textAlign: "center", color: "white", py: 1 }}
            >
              {formatChartName(expanded.name)}
            </Typography>
          </Box>
        )}
      </Dialog>
    </>
  );
}
