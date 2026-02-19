import { useState } from "react";
import { Box, Container, Typography } from "@mui/material";
import WellInput from "./components/WellInput";
import GlobalFilters from "./components/GlobalFilters";
import SectionTabs from "./components/SectionTabs";
import type { AnalyzeWellResponse } from "./types";

export default function App() {
  const [wellData, setWellData] = useState<AnalyzeWellResponse | null>(null);
  const [selectedBasins, setSelectedBasins] = useState<string[]>([]);

  const handleAnalyzed = (data: AnalyzeWellResponse) => {
    setWellData(data);
    setSelectedBasins([]);
  };

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
      <Container maxWidth="xl" sx={{ py: 3 }}>
        <Typography
          variant="h4"
          sx={{ mb: 3, fontWeight: 700, color: "primary.main" }}
        >
          BHA Selection Tool
        </Typography>

        <WellInput onAnalyzed={handleAnalyzed} />

        {wellData && (
          <Box sx={{ mt: 3 }}>
            <Box sx={{ display: "flex", alignItems: "baseline", gap: 1.5, mb: 1 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: "text.primary" }}>
                {wellData.well_name}
              </Typography>
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                (Asset {wellData.target_asset_id})
              </Typography>
            </Box>

            <GlobalFilters
              assetId={wellData.target_asset_id}
              selectedBasins={selectedBasins}
              onBasinsChange={setSelectedBasins}
            />

            <Box sx={{ mt: 2 }}>
              <SectionTabs
                sections={wellData.sections}
                assetId={wellData.target_asset_id}
                basinFilter={selectedBasins}
              />
            </Box>
          </Box>
        )}
      </Container>
    </Box>
  );
}
