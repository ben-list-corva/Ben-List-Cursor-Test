import React from 'react';
import { Button, CircularProgress, Box, Typography } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import RefreshIcon from '@mui/icons-material/Refresh';

interface RunButtonProps {
  onClick: () => void;
  isLoading: boolean;
  disabled: boolean;
  hasResults?: boolean;
  loadingStep?: string | null;
}

/**
 * Primary action button to run pipeline checks
 */
export const RunButton: React.FC<RunButtonProps> = ({
  onClick,
  isLoading,
  disabled,
  hasResults = false,
  loadingStep = null,
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 1.5,
        marginBottom: 4,
      }}
    >
      <Button
        variant="contained"
        size="large"
        onClick={onClick}
        disabled={disabled || isLoading}
        startIcon={
          isLoading ? (
            <CircularProgress size={20} sx={{ color: 'inherit' }} />
          ) : hasResults ? (
            <RefreshIcon />
          ) : (
            <PlayArrowIcon />
          )
        }
        sx={{
          minWidth: 280,
          height: 56,
          fontSize: '1rem',
          fontWeight: 600,
          textTransform: 'none',
          borderRadius: 2,
          background: disabled
            ? 'rgba(148, 163, 184, 0.2)'
            : 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
          boxShadow: disabled
            ? 'none'
            : '0 4px 14px 0 rgba(59, 130, 246, 0.39)',
          transition: 'all 0.2s ease-in-out',
          '&:hover': {
            background: disabled
              ? 'rgba(148, 163, 184, 0.2)'
              : 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
            transform: disabled ? 'none' : 'translateY(-1px)',
            boxShadow: disabled
              ? 'none'
              : '0 6px 20px 0 rgba(59, 130, 246, 0.45)',
          },
          '&:active': {
            transform: 'translateY(0)',
          },
          '&.Mui-disabled': {
            color: 'rgba(148, 163, 184, 0.5)',
          },
        }}
      >
        {isLoading
          ? 'Running Checks...'
          : hasResults
          ? 'Re-run Pipeline Check'
          : 'Run Pipeline Check'}
      </Button>
      
      {isLoading && loadingStep && (
        <Typography
          variant="body2"
          sx={{
            color: 'rgba(148, 163, 184, 0.7)',
            fontSize: '0.85rem',
            animation: 'pulse 1.5s ease-in-out infinite',
            '@keyframes pulse': {
              '0%, 100%': { opacity: 0.7 },
              '50%': { opacity: 1 },
            },
          }}
        >
          {loadingStep}
        </Typography>
      )}
    </Box>
  );
};

export default RunButton;
