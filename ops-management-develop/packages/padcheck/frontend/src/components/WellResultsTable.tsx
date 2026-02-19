import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Collapse,
  IconButton,
  Chip,
  Stack,
  Divider,
  Skeleton,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import OilBarrelIcon from '@mui/icons-material/OilBarrel';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';
import StorageIcon from '@mui/icons-material/Storage';
import LayersIcon from '@mui/icons-material/Layers';
import EventNoteIcon from '@mui/icons-material/EventNote';
import type { PadResult, WellResult, CheckStatus, PadConfiguration } from '../types';
import StreamCheckRow from './StreamCheckRow';

interface WellResultsTableProps {
  result: PadResult | null;
  isLoading: boolean;
}

interface WellCardProps {
  well: WellResult;
  defaultExpanded?: boolean;
}

const StatusBadge: React.FC<{ status: CheckStatus }> = ({ status }) => {
  const config = {
    PASS: { icon: <CheckCircleIcon sx={{ fontSize: 16 }} />, color: '#10b981', bg: 'rgba(16, 185, 129, 0.15)' },
    WARN: { icon: <WarningIcon sx={{ fontSize: 16 }} />, color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)' },
    FAIL: { icon: <ErrorIcon sx={{ fontSize: 16 }} />, color: '#ef4444', bg: 'rgba(239, 68, 68, 0.15)' },
  }[status];
  
  return (
    <Chip
      icon={config.icon}
      label={status}
      size="small"
      sx={{
        backgroundColor: config.bg,
        color: config.color,
        fontWeight: 600,
        '& .MuiChip-icon': { color: config.color },
      }}
    />
  );
};

const WellCard: React.FC<WellCardProps> = ({ well, defaultExpanded = false }) => {
  const [expanded, setExpanded] = React.useState(defaultExpanded || well.overall_status !== 'PASS');
  
  const borderColor = {
    PASS: 'rgba(16, 185, 129, 0.3)',
    WARN: 'rgba(245, 158, 11, 0.3)',
    FAIL: 'rgba(239, 68, 68, 0.3)',
  }[well.overall_status];
  
  return (
    <Paper
      elevation={0}
      sx={{
        backgroundColor: 'rgba(30, 41, 59, 0.4)',
        border: `1px solid ${borderColor}`,
        borderRadius: 2,
        overflow: 'hidden',
        marginBottom: 2,
      }}
    >
      {/* Well Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          padding: 2,
          cursor: 'pointer',
          '&:hover': {
            backgroundColor: 'rgba(30, 41, 59, 0.6)',
          },
        }}
        onClick={() => setExpanded(!expanded)}
      >
        {/* Wellhead color indicator (if available) */}
        {well.color ? (
          <Box
            sx={{
              width: 24,
              height: 24,
              borderRadius: '50%',
              backgroundColor: well.color,
              border: '2px solid rgba(255, 255, 255, 0.3)',
              boxShadow: `0 0 8px ${well.color}40`,
              flexShrink: 0,
            }}
            title={`Wellhead color: ${well.color}`}
          />
        ) : (
          <OilBarrelIcon sx={{ color: 'rgba(148, 163, 184, 0.6)', fontSize: 24 }} />
        )}
        
        <Box sx={{ flex: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography
              variant="subtitle1"
              sx={{
                color: '#f8fafc',
                fontWeight: 600,
              }}
            >
              {well.well_name}
            </Typography>
            {/* Line assignment badge for SimulFrac */}
            {well.line_assignment && (
              <Chip
                label={well.line_assignment}
                size="small"
                sx={{
                  backgroundColor: 'rgba(59, 130, 246, 0.2)',
                  color: '#60a5fa',
                  fontWeight: 600,
                  fontSize: '0.65rem',
                  height: 20,
                  '& .MuiChip-label': { px: 1 },
                }}
              />
            )}
          </Box>
          <Typography
            variant="caption"
            sx={{ color: 'rgba(148, 163, 184, 0.6)' }}
          >
            Asset ID: {well.corva_well_asset_id}
            {well.api_number && ` • API: ${well.api_number}`}
          </Typography>
        </Box>
        
        <StatusBadge status={well.overall_status} />
        
        <IconButton size="small" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>
          {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </IconButton>
      </Box>
      
      {/* Expanded Content */}
      <Collapse in={expanded}>
        <Box sx={{ padding: 2, paddingTop: 0 }}>
          <Divider sx={{ marginBottom: 2, borderColor: 'rgba(148, 163, 184, 0.1)' }} />
          
          {/* Stream Checks Section */}
          <Typography
            variant="subtitle2"
            sx={{
              color: 'rgba(148, 163, 184, 0.7)',
              marginBottom: 1.5,
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              fontSize: '0.7rem',
            }}
          >
            Corva Streams
          </Typography>
          
          <Stack spacing={1} sx={{ marginBottom: 3 }}>
            <StreamCheckRow
              streamType="frac"
              result={well.corva_streams.frac}
              isRequired={true}
            />
            <StreamCheckRow
              streamType="wireline"
              result={well.corva_streams.wireline}
              isRequired={false}
            />
            <StreamCheckRow
              streamType="pumpdown"
              result={well.corva_streams.pumpdown}
              isRequired={false}
            />
          </Stack>
          
          {/* Stream Platform Check */}
          <Typography
            variant="subtitle2"
            sx={{
              color: 'rgba(148, 163, 184, 0.7)',
              marginBottom: 1.5,
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              fontSize: '0.7rem',
            }}
          >
            Stream Platform Link
          </Typography>
          
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 2,
              padding: 2,
              backgroundColor: 'rgba(30, 41, 59, 0.3)',
              borderRadius: 1,
              border: '1px solid rgba(148, 163, 184, 0.1)',
              marginBottom: 3,
            }}
          >
            <StorageIcon sx={{ color: 'rgba(148, 163, 184, 0.5)' }} />
            
            <Box sx={{ flex: 1 }}>
              {well.stream_platform_well_id ? (
                <>
                  <Typography
                    variant="body2"
                    sx={{ color: '#10b981', fontWeight: 500 }}
                  >
                    ✓ Well found in Stream Platform
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{ color: 'rgba(148, 163, 184, 0.8)', display: 'block' }}
                  >
                    {well.stream_platform_well_name || 'Unknown Well'}
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{ color: 'rgba(148, 163, 184, 0.5)', fontFamily: 'monospace', fontSize: '0.7rem' }}
                  >
                    ID: {well.stream_platform_well_id}
                  </Typography>
                </>
              ) : (
                <>
                  <Typography
                    variant="body2"
                    sx={{ color: '#ef4444', fontWeight: 500 }}
                  >
                    ✗ Well not found in Stream Platform
                  </Typography>
                  {well.stream_platform_check.failures.map((f, i) => (
                    <Typography
                      key={i}
                      variant="caption"
                      sx={{ color: 'rgba(239, 68, 68, 0.8)', display: 'block' }}
                    >
                      {f}
                    </Typography>
                  ))}
                </>
              )}
            </Box>
            
            <StatusBadge status={well.stream_platform_check.check_status} />
          </Box>
          
          {/* Stage Status */}
          {well.stage_status && (
            <>
              <Typography
                variant="subtitle2"
                sx={{
                  color: 'rgba(148, 163, 184, 0.7)',
                  marginBottom: 1.5,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  fontSize: '0.7rem',
                }}
              >
                Stage Status
              </Typography>
              
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                  padding: 2,
                  backgroundColor: 'rgba(30, 41, 59, 0.3)',
                  borderRadius: 1,
                  border: '1px solid rgba(148, 163, 184, 0.1)',
                  marginBottom: 3,
                }}
              >
                <LayersIcon sx={{ color: 'rgba(148, 163, 184, 0.5)' }} />
                
                <Box sx={{ flex: 1 }}>
                  {well.stage_status.has_active_stage ? (
                    <>
                      <Typography
                        variant="body2"
                        sx={{ color: '#10b981', fontWeight: 500 }}
                      >
                        ✓ Active stage found
                      </Typography>
                      <Typography
                        variant="caption"
                        sx={{ color: 'rgba(148, 163, 184, 0.6)' }}
                      >
                        Stage #{well.stage_status.active_stage_number}
                        {well.stage_status.active_stage_action && ` (${well.stage_status.active_stage_action})`}
                        {well.stage_status.sb_id && ` • Streambox: ${well.stage_status.sb_id}`}
                      </Typography>
                    </>
                  ) : well.stage_status.has_stages ? (
                    <>
                      <Typography
                        variant="body2"
                        sx={{ color: '#f59e0b', fontWeight: 500 }}
                      >
                        ⚠ Stages exist but none active
                      </Typography>
                      {well.stage_status.warnings.map((w, i) => (
                        <Typography
                          key={i}
                          variant="caption"
                          sx={{ color: 'rgba(245, 158, 11, 0.8)', display: 'block' }}
                        >
                          {w}
                        </Typography>
                      ))}
                    </>
                  ) : (
                    <>
                      <Typography
                        variant="body2"
                        sx={{ color: '#ef4444', fontWeight: 500 }}
                      >
                        ✗ No stages found
                      </Typography>
                      {well.stage_status.failures.map((f, i) => (
                        <Typography
                          key={i}
                          variant="caption"
                          sx={{ color: 'rgba(239, 68, 68, 0.8)', display: 'block' }}
                        >
                          {f}
                        </Typography>
                      ))}
                    </>
                  )}
                </Box>
                
                <StatusBadge status={well.stage_status.check_status} />
              </Box>
            </>
          )}
          
          {/* Pumping Schedule Check (Informational) */}
          {well.schedule_check && (
            <>
              <Typography
                variant="subtitle2"
                sx={{
                  color: 'rgba(148, 163, 184, 0.7)',
                  marginBottom: 1.5,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  fontSize: '0.7rem',
                }}
              >
                Pumping Schedules
              </Typography>
              
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                  padding: 2,
                  backgroundColor: 'rgba(30, 41, 59, 0.3)',
                  borderRadius: 1,
                  border: '1px solid rgba(148, 163, 184, 0.1)',
                }}
              >
                <EventNoteIcon sx={{ color: 'rgba(148, 163, 184, 0.5)' }} />
                
                <Box sx={{ flex: 1 }}>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                    {/* Stage 1 Schedule */}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography
                        variant="body2"
                        sx={{ 
                          color: well.schedule_check.stage_1_has_schedule 
                            ? '#10b981' 
                            : 'rgba(148, 163, 184, 0.8)',
                          fontWeight: 500,
                          minWidth: 120,
                        }}
                      >
                        {well.schedule_check.stage_1_has_schedule ? '✓' : '○'} Stage 1:
                      </Typography>
                      <Typography
                        variant="caption"
                        sx={{ 
                          color: well.schedule_check.stage_1_has_schedule 
                            ? '#10b981' 
                            : 'rgba(148, 163, 184, 0.5)',
                        }}
                      >
                        {well.schedule_check.stage_1_has_schedule === null 
                          ? 'Checking...' 
                          : well.schedule_check.stage_1_has_schedule 
                            ? 'Schedule uploaded' 
                            : 'No schedule'}
                      </Typography>
                    </Box>
                    
                    {/* Last Stage Schedule */}
                    {well.schedule_check.last_stage_number && well.schedule_check.last_stage_number !== 1 && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography
                          variant="body2"
                          sx={{ 
                            color: well.schedule_check.last_stage_has_schedule 
                              ? '#10b981' 
                              : 'rgba(148, 163, 184, 0.8)',
                            fontWeight: 500,
                            minWidth: 120,
                          }}
                        >
                          {well.schedule_check.last_stage_has_schedule ? '✓' : '○'} Stage {well.schedule_check.last_stage_number}:
                        </Typography>
                        <Typography
                          variant="caption"
                          sx={{ 
                            color: well.schedule_check.last_stage_has_schedule 
                              ? '#10b981' 
                              : 'rgba(148, 163, 184, 0.5)',
                          }}
                        >
                          {well.schedule_check.last_stage_has_schedule === null 
                            ? 'Checking...' 
                            : well.schedule_check.last_stage_has_schedule 
                              ? 'Schedule uploaded' 
                              : 'No schedule'}
                        </Typography>
                      </Box>
                    )}
                  </Box>
                </Box>
                
                {/* Info badge - schedule check is informational only */}
                <Chip
                  label="INFO"
                  size="small"
                  sx={{
                    backgroundColor: 'rgba(59, 130, 246, 0.15)',
                    color: '#3b82f6',
                    fontWeight: 600,
                    fontSize: '0.65rem',
                  }}
                />
              </Box>
            </>
          )}
        </Box>
      </Collapse>
    </Paper>
  );
};

/**
 * Loading skeleton for well results
 */
const LoadingSkeleton: React.FC = () => (
  <Box>
    {[1, 2, 3].map((i) => (
      <Paper
        key={i}
        elevation={0}
        sx={{
          backgroundColor: 'rgba(30, 41, 59, 0.4)',
          border: '1px solid rgba(148, 163, 184, 0.1)',
          borderRadius: 2,
          padding: 2,
          marginBottom: 2,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Skeleton variant="circular" width={24} height={24} sx={{ bgcolor: 'rgba(148, 163, 184, 0.1)' }} />
          <Box sx={{ flex: 1 }}>
            <Skeleton variant="text" width="60%" sx={{ bgcolor: 'rgba(148, 163, 184, 0.1)' }} />
            <Skeleton variant="text" width="40%" sx={{ bgcolor: 'rgba(148, 163, 184, 0.1)' }} />
          </Box>
          <Skeleton variant="rounded" width={60} height={24} sx={{ bgcolor: 'rgba(148, 163, 184, 0.1)' }} />
        </Box>
      </Paper>
    ))}
  </Box>
);

/**
 * Configuration badge component
 */
const ConfigBadge: React.FC<{ config: PadConfiguration | null }> = ({ config }) => {
  if (!config) return null;
  
  const isSimulfrac = config.config_type === 'simulfrac';
  const label = isSimulfrac ? 'SIMULFRAC' : config.config_type === 'zipper' ? 'ZIPPER' : 'UNKNOWN';
  const color = isSimulfrac ? '#a855f7' : '#3b82f6';
  const bg = isSimulfrac ? 'rgba(168, 85, 247, 0.15)' : 'rgba(59, 130, 246, 0.15)';
  
  return (
    <Chip
      label={label}
      size="small"
      sx={{
        backgroundColor: bg,
        color: color,
        fontWeight: 700,
        fontSize: '0.7rem',
        letterSpacing: '0.05em',
        border: `1px solid ${color}40`,
      }}
    />
  );
};

/**
 * Table component for displaying well results
 */
export const WellResultsTable: React.FC<WellResultsTableProps> = ({ result, isLoading }) => {
  if (isLoading) {
    return <LoadingSkeleton />;
  }
  
  if (!result || result.wells.length === 0) {
    return null;
  }
  
  // Group wells by line assignment for SimulFrac display
  const isSimulfrac = result.configuration?.config_type === 'simulfrac';
  const lineGroups: Map<string, WellResult[]> = new Map();
  
  if (isSimulfrac && result.configuration?.lines) {
    // Initialize line groups in order
    for (const line of result.configuration.lines) {
      lineGroups.set(line.name, []);
    }
    lineGroups.set('Unassigned', []);
    
    // Assign wells to groups
    for (const well of result.wells) {
      const lineName = well.line_assignment || 'Unassigned';
      const group = lineGroups.get(lineName) || lineGroups.get('Unassigned')!;
      group.push(well);
    }
    
    // Remove empty groups
    for (const [key, value] of lineGroups.entries()) {
      if (value.length === 0) lineGroups.delete(key);
    }
  }
  
  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, marginBottom: 2 }}>
        <Typography
          variant="h6"
          sx={{
            color: '#f8fafc',
            fontWeight: 600,
          }}
        >
          Well Results ({result.wells.length})
        </Typography>
        <ConfigBadge config={result.configuration} />
        {result.configuration?.frac_fleet_name && (
          <Typography
            variant="caption"
            sx={{ color: 'rgba(148, 163, 184, 0.6)' }}
          >
            Fleet: {result.configuration.frac_fleet_name}
          </Typography>
        )}
      </Box>
      
      {isSimulfrac ? (
        // SimulFrac: Group wells by line
        Array.from(lineGroups.entries()).map(([lineName, wells]) => (
          <Box key={lineName} sx={{ marginBottom: 3 }}>
            <Typography
              variant="subtitle2"
              sx={{
                color: '#a855f7',
                fontWeight: 600,
                marginBottom: 1.5,
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                fontSize: '0.75rem',
                display: 'flex',
                alignItems: 'center',
                gap: 1,
              }}
            >
              <Box
                sx={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  backgroundColor: '#a855f7',
                }}
              />
              {lineName} ({wells.length} wells)
            </Typography>
            {wells.map((well, index) => (
              <WellCard
                key={well.corva_well_asset_id}
                well={well}
                defaultExpanded={index === 0}
              />
            ))}
          </Box>
        ))
      ) : (
        // Zipper: Show all wells
        result.wells.map((well, index) => (
          <WellCard
            key={well.corva_well_asset_id}
            well={well}
            defaultExpanded={index === 0}
          />
        ))
      )}
    </Box>
  );
};

export default WellResultsTable;
