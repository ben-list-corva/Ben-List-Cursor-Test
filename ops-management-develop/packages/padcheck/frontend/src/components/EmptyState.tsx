import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import SearchOffIcon from '@mui/icons-material/SearchOff';

interface EmptyStateProps {
  title?: string;
  message?: string;
}

/**
 * Empty state component shown when no pad context is available
 */
export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No Pad Selected',
  message = 'Select a Pad using the dashboard asset chips to begin pipeline validation.',
}) => {
  return (
    <Paper
      elevation={0}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 6,
        backgroundColor: 'rgba(30, 41, 59, 0.5)',
        borderRadius: 2,
        border: '1px dashed rgba(148, 163, 184, 0.3)',
        minHeight: 300,
      }}
    >
      <Box
        sx={{
          width: 80,
          height: 80,
          borderRadius: '50%',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: 3,
        }}
      >
        <SearchOffIcon
          sx={{
            fontSize: 40,
            color: 'rgba(148, 163, 184, 0.6)',
          }}
        />
      </Box>
      
      <Typography
        variant="h6"
        sx={{
          color: '#e2e8f0',
          fontWeight: 600,
          marginBottom: 1,
          textAlign: 'center',
        }}
      >
        {title}
      </Typography>
      
      <Typography
        variant="body1"
        sx={{
          color: 'rgba(148, 163, 184, 0.8)',
          textAlign: 'center',
          maxWidth: 400,
          lineHeight: 1.6,
        }}
      >
        {message}
      </Typography>
      
      <Box
        sx={{
          marginTop: 4,
          padding: 2,
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderRadius: 1,
          border: '1px solid rgba(59, 130, 246, 0.2)',
        }}
      >
        <Typography
          variant="body2"
          sx={{
            color: 'rgba(147, 197, 253, 0.9)',
            fontSize: '0.85rem',
          }}
        >
          💡 Tip: Use the asset selector in the Corva dashboard header to choose a pad.
        </Typography>
      </Box>
    </Paper>
  );
};

export default EmptyState;
