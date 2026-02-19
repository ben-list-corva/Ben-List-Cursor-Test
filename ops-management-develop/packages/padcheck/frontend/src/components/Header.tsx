import React from 'react';
import { Box, Typography, Chip, Stack } from '@mui/material';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import OilBarrelIcon from '@mui/icons-material/OilBarrel';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import type { AssetContext } from '../types';

interface HeaderProps {
  context: AssetContext;
}

/**
 * Header component displaying app title and current context
 */
export const Header: React.FC<HeaderProps> = ({ context }) => {
  const { padId, padName, completionWellAssetId, wellName, fracFleetId } = context;
  
  return (
    <Box
      sx={{
        marginBottom: 4,
        paddingBottom: 3,
        borderBottom: '1px solid rgba(148, 163, 184, 0.2)',
      }}
    >
      {/* Title */}
      <Typography
        variant="h4"
        sx={{
          color: '#f8fafc',
          fontWeight: 700,
          marginBottom: 1,
          letterSpacing: '-0.02em',
        }}
      >
        PadCheck
      </Typography>
      
      <Typography
        variant="body1"
        sx={{
          color: 'rgba(148, 163, 184, 0.8)',
          marginBottom: 3,
        }}
      >
        Validate completions data pipeline connectivity
      </Typography>
      
      {/* Context Chips */}
      {padId && (
        <Stack direction="row" spacing={1.5} flexWrap="wrap" useFlexGap>
          {/* Pad Chip */}
          <Chip
            icon={<LocationOnIcon sx={{ fontSize: 18 }} />}
            label={
              <Box component="span">
                <Typography
                  component="span"
                  sx={{ 
                    fontWeight: 600, 
                    color: '#e2e8f0',
                    fontSize: '0.85rem',
                  }}
                >
                  Pad:
                </Typography>
                {' '}
                <Typography
                  component="span"
                  sx={{ 
                    color: 'rgba(148, 163, 184, 0.9)',
                    fontSize: '0.85rem',
                  }}
                >
                  {padName || `ID ${padId}`}
                </Typography>
                <Typography
                  component="span"
                  sx={{ 
                    color: 'rgba(148, 163, 184, 0.6)',
                    fontSize: '0.75rem',
                    marginLeft: 0.5,
                  }}
                >
                  ({padId})
                </Typography>
              </Box>
            }
            sx={{
              backgroundColor: 'rgba(59, 130, 246, 0.15)',
              border: '1px solid rgba(59, 130, 246, 0.3)',
              borderRadius: 1,
              height: 36,
              '& .MuiChip-icon': {
                color: '#3b82f6',
              },
            }}
          />
          
          {/* Well Chip (if selected) */}
          {completionWellAssetId && (
            <Chip
              icon={<OilBarrelIcon sx={{ fontSize: 18 }} />}
              label={
                <Box component="span">
                  <Typography
                    component="span"
                    sx={{ 
                      fontWeight: 600, 
                      color: '#e2e8f0',
                      fontSize: '0.85rem',
                    }}
                  >
                    Well:
                  </Typography>
                  {' '}
                  <Typography
                    component="span"
                    sx={{ 
                      color: 'rgba(148, 163, 184, 0.9)',
                      fontSize: '0.85rem',
                    }}
                  >
                    {wellName || `ID ${completionWellAssetId}`}
                  </Typography>
                  <Typography
                    component="span"
                    sx={{ 
                      color: 'rgba(148, 163, 184, 0.6)',
                      fontSize: '0.75rem',
                      marginLeft: 0.5,
                    }}
                  >
                    ({completionWellAssetId})
                  </Typography>
                </Box>
              }
              sx={{
                backgroundColor: 'rgba(16, 185, 129, 0.15)',
                border: '1px solid rgba(16, 185, 129, 0.3)',
                borderRadius: 1,
                height: 36,
                '& .MuiChip-icon': {
                  color: '#10b981',
                },
              }}
            />
          )}
          
          {/* Frac Fleet Chip (informational) */}
          {fracFleetId && (
            <Chip
              icon={<LocalShippingIcon sx={{ fontSize: 18 }} />}
              label={
                <Box component="span">
                  <Typography
                    component="span"
                    sx={{ 
                      fontWeight: 600, 
                      color: '#e2e8f0',
                      fontSize: '0.85rem',
                    }}
                  >
                    Fleet:
                  </Typography>
                  {' '}
                  <Typography
                    component="span"
                    sx={{ 
                      color: 'rgba(148, 163, 184, 0.6)',
                      fontSize: '0.85rem',
                    }}
                  >
                    {fracFleetId}
                  </Typography>
                </Box>
              }
              sx={{
                backgroundColor: 'rgba(148, 163, 184, 0.1)',
                border: '1px solid rgba(148, 163, 184, 0.2)',
                borderRadius: 1,
                height: 36,
                '& .MuiChip-icon': {
                  color: 'rgba(148, 163, 184, 0.7)',
                },
              }}
            />
          )}
        </Stack>
      )}
    </Box>
  );
};

export default Header;
