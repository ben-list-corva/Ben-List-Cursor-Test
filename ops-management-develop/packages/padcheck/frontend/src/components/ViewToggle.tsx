import React from 'react';
import { ToggleButton, ToggleButtonGroup, Box } from '@mui/material';
import ViewModuleIcon from '@mui/icons-material/ViewModule';
import TableChartIcon from '@mui/icons-material/TableChart';

export type ViewMode = 'card' | 'table';

interface ViewToggleProps {
  value: ViewMode;
  onChange: (value: ViewMode) => void;
}

export const ViewToggle: React.FC<ViewToggleProps> = ({ value, onChange }) => {
  const handleChange = (_event: React.MouseEvent<HTMLElement>, newValue: ViewMode | null) => {
    if (newValue !== null) {
      onChange(newValue);
    }
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
      <ToggleButtonGroup
        value={value}
        exclusive
        onChange={handleChange}
        size="small"
        sx={{
          backgroundColor: 'rgba(30, 41, 59, 0.6)',
          borderRadius: 1,
          '& .MuiToggleButton-root': {
            color: 'rgba(148, 163, 184, 0.7)',
            borderColor: 'rgba(148, 163, 184, 0.2)',
            px: 2,
            py: 0.75,
            '&:hover': {
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
            },
            '&.Mui-selected': {
              backgroundColor: 'rgba(59, 130, 246, 0.2)',
              color: '#60a5fa',
              '&:hover': {
                backgroundColor: 'rgba(59, 130, 246, 0.3)',
              },
            },
          },
        }}
      >
        <ToggleButton value="card" aria-label="card view">
          <ViewModuleIcon sx={{ mr: 0.75, fontSize: 18 }} />
          Card View
        </ToggleButton>
        <ToggleButton value="table" aria-label="table view">
          <TableChartIcon sx={{ mr: 0.75, fontSize: 18 }} />
          Table View
        </ToggleButton>
      </ToggleButtonGroup>
    </Box>
  );
};

export default ViewToggle;
