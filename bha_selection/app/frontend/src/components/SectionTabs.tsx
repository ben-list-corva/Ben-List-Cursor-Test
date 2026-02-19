import { useState } from "react";
import { Box, Tab, Tabs, Chip } from "@mui/material";
import SectionPanel from "./SectionPanel";
import type { WellSection } from "../types";

interface SectionTabsProps {
  sections: WellSection[];
  assetId: string;
  basinFilter: string[];
}

export default function SectionTabs({ sections, assetId, basinFilter }: SectionTabsProps) {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <Box>
      <Tabs
        value={activeTab}
        onChange={(_, v) => setActiveTab(v)}
        variant="scrollable"
        scrollButtons="auto"
        sx={{
          borderBottom: 1,
          borderColor: "divider",
          "& .MuiTab-root": { textTransform: "none", fontWeight: 600 },
        }}
      >
        {sections.map((sec, idx) => (
          <Tab
            key={idx}
            label={
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                {sec.name}
                {sec.hole_size && (
                  <Chip
                    label={`${sec.hole_size}"`}
                    size="small"
                    variant="outlined"
                    sx={{ height: 20, fontSize: "0.7rem" }}
                  />
                )}
                <Chip
                  label={sec.mode}
                  size="small"
                  color={sec.mode === "lateral" ? "primary" : "secondary"}
                  sx={{ height: 20, fontSize: "0.7rem" }}
                />
              </Box>
            }
          />
        ))}
      </Tabs>

      {sections.map((sec, idx) => (
        <Box
          key={idx}
          role="tabpanel"
          hidden={activeTab !== idx}
          sx={{ pt: 2 }}
        >
          {activeTab === idx && (
            <SectionPanel section={sec} assetId={assetId} basinFilter={basinFilter} />
          )}
        </Box>
      ))}
    </Box>
  );
}
