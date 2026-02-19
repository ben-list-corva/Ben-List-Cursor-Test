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
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import VisibilityIcon from '@mui/icons-material/Visibility';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';
import StorageIcon from '@mui/icons-material/Storage';
import LayersIcon from '@mui/icons-material/Layers';
import StreamIcon from '@mui/icons-material/Stream';
import type { ViewerResult, CheckStatus, ViewerStreamResult } from '../types';

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

const StreamCheckItem: React.FC<{
  streamType: string;
  result: ViewerStreamResult | null;
}> = ({ streamType, result }) => {
  const [expanded, setExpanded] = React.useState(false);
  
  const label = {
    frac: 'Frac',
    wireline: 'Wireline',
    pumpdown: 'Pumpdown',
  }[streamType] || streamType;
  
  if (!result) {
    return (
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          padding: 1.5,
          backgroundColor: 'rgba(30, 41, 59, 0.3)',
          borderRadius: 1,
          border: '1px solid rgba(148, 163, 184, 0.1)',
        }}
      >
        <StreamIcon sx={{ color: 'rgba(148, 163, 184, 0.3)', fontSize: 20 }} />
        <Box sx={{ flex: 1 }}>
          <Typography variant="body2" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>
            {label} Stream
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.4)' }}>
            Not found
          </Typography>
        </Box>
        <Chip
          label="N/A"
          size="small"
          sx={{
            backgroundColor: 'rgba(148, 163, 184, 0.1)',
            color: 'rgba(148, 163, 184, 0.5)',
            fontWeight: 500,
          }}
        />
      </Box>
    );
  }
  
  const statusColor = {
    PASS: '#10b981',
    WARN: '#f59e0b',
    FAIL: '#ef4444',
  }[result.check_status];
  
  const hasDetails = result.connected_app_ids?.length > 0 || result.source_app;
  
  return (
    <Box
      sx={{
        backgroundColor: 'rgba(30, 41, 59, 0.3)',
        borderRadius: 1,
        border: '1px solid rgba(148, 163, 184, 0.1)',
        overflow: 'hidden',
      }}
    >
      {/* Main Row */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          padding: 1.5,
          cursor: hasDetails ? 'pointer' : 'default',
          '&:hover': {
            backgroundColor: hasDetails ? 'rgba(30, 41, 59, 0.5)' : 'transparent',
          },
        }}
        onClick={() => hasDetails && setExpanded(!expanded)}
      >
        <StreamIcon sx={{ color: statusColor, fontSize: 20 }} />
        <Box sx={{ flex: 1 }}>
          <Typography variant="body2" sx={{ color: '#f8fafc', fontWeight: 500 }}>
            {label} Stream
            <Chip
              label={result.stream_status}
              size="small"
              sx={{
                ml: 1,
                height: 18,
                fontSize: '0.65rem',
                fontWeight: 600,
                backgroundColor: result.stream_status === 'active' 
                  ? 'rgba(16, 185, 129, 0.2)' 
                  : 'rgba(245, 158, 11, 0.2)',
                color: result.stream_status === 'active' 
                  ? '#10b981' 
                  : '#f59e0b',
                '& .MuiChip-label': { px: 0.75 },
              }}
            />
          </Typography>
          {result.source_app ? (
            <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.6)' }}>
              Source: {result.source_app.app_name}
              {result.source_app.settings?.api_number && (
                <> • API: {result.source_app.settings.api_number}</>
              )}
            </Typography>
          ) : (
            <Typography variant="caption" sx={{ color: 'rgba(239, 68, 68, 0.8)' }}>
              No source app configured
            </Typography>
          )}
        </Box>
        <StatusBadge status={result.check_status} />
        {hasDetails && (
          <IconButton size="small" sx={{ color: 'rgba(148, 163, 184, 0.5)', padding: 0.5 }}>
            {expanded ? <ExpandLessIcon fontSize="small" /> : <ExpandMoreIcon fontSize="small" />}
          </IconButton>
        )}
      </Box>
      
      {/* Expanded Details */}
      <Collapse in={expanded}>
        <Box
          sx={{
            padding: 1.5,
            paddingTop: 0,
            borderTop: '1px solid rgba(148, 163, 184, 0.1)',
          }}
        >
          {/* Connected Apps */}
          {result.connected_app_ids && result.connected_app_ids.length > 0 && (
            <Box sx={{ marginBottom: 1.5, marginTop: 1 }}>
              <Typography
                variant="caption"
                sx={{ 
                  color: 'rgba(148, 163, 184, 0.6)', 
                  display: 'block', 
                  marginBottom: 0.5,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  fontSize: '0.6rem',
                }}
              >
                Connected Apps ({result.connected_app_ids.length})
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {result.connected_app_ids.map((appId, idx) => (
                  <Chip
                    key={appId}
                    label={result.connected_app_names?.[idx] || `App ${appId}`}
                    size="small"
                    sx={{
                      backgroundColor: 'rgba(59, 130, 246, 0.1)',
                      color: 'rgba(148, 163, 184, 0.9)',
                      fontSize: '0.65rem',
                      height: 20,
                    }}
                  />
                ))}
              </Box>
            </Box>
          )}
          
          {/* Source App Settings */}
          {result.source_app && (
            <Box
              sx={{
                padding: 1,
                backgroundColor: 'rgba(15, 23, 42, 0.5)',
                borderRadius: 1,
                fontSize: '0.7rem',
                fontFamily: '"IBM Plex Mono", monospace',
              }}
            >
              <Typography
                variant="caption"
                sx={{ 
                  color: 'rgba(148, 163, 184, 0.7)', 
                  display: 'block', 
                  marginBottom: 0.5,
                  fontWeight: 600,
                  fontFamily: '"IBM Plex Sans", sans-serif',
                  fontSize: '0.65rem',
                }}
              >
                Source: {result.source_app.app_name} (ID: {result.source_app.app_id})
              </Typography>
              <Box sx={{ color: 'rgba(148, 163, 184, 0.8)', lineHeight: 1.6, fontSize: '0.65rem' }}>
                <div><span style={{ color: '#94a3b8' }}>api_number:</span> <span style={{ color: result.source_app.settings?.api_number ? '#10b981' : '#f59e0b' }}>{result.source_app.settings?.api_number || '(not set)'}</span></div>
                <div><span style={{ color: '#94a3b8' }}>stream_api_root_url:</span> {result.source_app.settings?.stream_api_root_url || '(not set)'}</div>
                <div><span style={{ color: '#94a3b8' }}>stream_api_log_path:</span> {result.source_app.settings?.stream_api_log_path || '(not set)'}</div>
                <div><span style={{ color: '#94a3b8' }}>force_start_from:</span> {result.source_app.settings?.force_start_from || '(not set)'}</div>
              </Box>
            </Box>
          )}
        </Box>
      </Collapse>
    </Box>
  );
};

interface ViewerCardProps {
  viewer: ViewerResult;
}

/**
 * Card component for displaying viewer asset check results
 */
export const ViewerCard: React.FC<ViewerCardProps> = ({ viewer }) => {
  const [expanded, setExpanded] = React.useState(viewer.check_status !== 'PASS');
  
  const borderColor = {
    PASS: 'rgba(59, 130, 246, 0.3)',  // Blue for viewer
    WARN: 'rgba(245, 158, 11, 0.3)',
    FAIL: 'rgba(239, 68, 68, 0.3)',
  }[viewer.check_status];
  
  // If no viewer found
  if (!viewer.viewer_asset_id) {
    return (
      <Paper
        elevation={0}
        sx={{
          backgroundColor: 'rgba(30, 41, 59, 0.4)',
          border: '1px solid rgba(245, 158, 11, 0.3)',
          borderRadius: 2,
          padding: 2,
          marginBottom: 3,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <VisibilityIcon sx={{ color: 'rgba(245, 158, 11, 0.6)', fontSize: 28 }} />
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle1" sx={{ color: '#f8fafc', fontWeight: 600 }}>
              Viewer Asset
            </Typography>
            <Typography variant="body2" sx={{ color: 'rgba(245, 158, 11, 0.8)' }}>
              ⚠ No viewer asset found for this pad
            </Typography>
            {viewer.warnings.map((w, i) => (
              <Typography
                key={i}
                variant="caption"
                sx={{ color: 'rgba(148, 163, 184, 0.6)', display: 'block' }}
              >
                {w}
              </Typography>
            ))}
          </Box>
          <StatusBadge status="WARN" />
        </Box>
      </Paper>
    );
  }
  
  return (
    <Paper
      elevation={0}
      sx={{
        backgroundColor: 'rgba(30, 41, 59, 0.4)',
        border: `1px solid ${borderColor}`,
        borderRadius: 2,
        overflow: 'hidden',
        marginBottom: 3,
      }}
    >
      {/* Viewer Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          padding: 2,
          cursor: 'pointer',
          background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(59, 130, 246, 0.02) 100%)',
          '&:hover': {
            backgroundColor: 'rgba(30, 41, 59, 0.6)',
          },
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <VisibilityIcon sx={{ color: '#3b82f6', fontSize: 28 }} />
        
        <Box sx={{ flex: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography
              variant="subtitle1"
              sx={{
                color: '#f8fafc',
                fontWeight: 600,
              }}
            >
              {viewer.viewer_name || 'Viewer Asset'}
            </Typography>
            {/* Line badge for SimulFrac */}
            {viewer.line_name && (
              <Chip
                label={viewer.line_name}
                size="small"
                sx={{
                  backgroundColor: 'rgba(168, 85, 247, 0.2)',
                  color: '#c084fc',
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
            Asset ID: {viewer.viewer_asset_id}
            {viewer.frac_fleet_name && ` • Fleet: ${viewer.frac_fleet_name}`}
            {viewer.api_number && ` • API: ${viewer.api_number}`}
          </Typography>
        </Box>
        
        <StatusBadge status={viewer.check_status} />
        
        <IconButton size="small" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>
          {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </IconButton>
      </Box>
      
      {/* Expanded Content */}
      <Collapse in={expanded}>
        <Box sx={{ padding: 2, paddingTop: 0 }}>
          <Divider sx={{ marginBottom: 2, borderColor: 'rgba(148, 163, 184, 0.1)' }} />
          
          {/* Viewer Streams Section */}
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
            Viewer Streams (Raw Data Ingestion)
          </Typography>
          
          <Stack spacing={1} sx={{ marginBottom: 3 }}>
            <StreamCheckItem streamType="frac" result={viewer.streams.frac} />
            <StreamCheckItem streamType="wireline" result={viewer.streams.wireline} />
            <StreamCheckItem streamType="pumpdown" result={viewer.streams.pumpdown} />
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
              {viewer.stream_platform_well_id ? (
                <>
                  <Typography
                    variant="body2"
                    sx={{ color: '#10b981', fontWeight: 500 }}
                  >
                    ✓ Viewer found in Stream Platform
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{ color: 'rgba(148, 163, 184, 0.8)', display: 'block' }}
                  >
                    {viewer.stream_platform_well_name || 'Unknown Well'}
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{ color: 'rgba(148, 163, 184, 0.5)', fontFamily: 'monospace', fontSize: '0.7rem' }}
                  >
                    ID: {viewer.stream_platform_well_id}
                  </Typography>
                </>
              ) : (
                <>
                  <Typography
                    variant="body2"
                    sx={{ color: '#ef4444', fontWeight: 500 }}
                  >
                    ✗ Viewer not found in Stream Platform
                  </Typography>
                  {viewer.stream_platform_check?.failures.map((f, i) => (
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
            
            <StatusBadge status={viewer.stream_platform_check?.check_status || 'FAIL'} />
          </Box>
          
          {/* Stage Status */}
          {viewer.stage_status && (
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
                Viewer Stage Status
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
                <LayersIcon sx={{ color: 'rgba(148, 163, 184, 0.5)' }} />
                
                <Box sx={{ flex: 1 }}>
                  {viewer.stage_status.has_active_stage ? (
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
                        Stage #{viewer.stage_status.active_stage_number}
                        {viewer.stage_status.active_stage_action && ` (${viewer.stage_status.active_stage_action})`}
                        {viewer.stage_status.sb_id && ` • Streambox: ${viewer.stage_status.sb_id}`}
                      </Typography>
                    </>
                  ) : viewer.stage_status.has_stages ? (
                    <>
                      <Typography
                        variant="body2"
                        sx={{ color: '#f59e0b', fontWeight: 500 }}
                      >
                        ⚠ Stages exist but none active
                      </Typography>
                      {viewer.stage_status.warnings.map((w, i) => (
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
                      {viewer.stage_status.failures.map((f, i) => (
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
                
                <StatusBadge status={viewer.stage_status.check_status} />
              </Box>
            </>
          )}
          
          {/* Failures and Warnings Summary */}
          {(viewer.failures.length > 0 || viewer.warnings.length > 0) && (
            <Box sx={{ marginTop: 2 }}>
              {viewer.failures.length > 0 && (
                <Box sx={{ marginBottom: 1 }}>
                  {viewer.failures.map((f, i) => (
                    <Typography
                      key={i}
                      variant="caption"
                      sx={{ color: 'rgba(239, 68, 68, 0.8)', display: 'block' }}
                    >
                      ❌ {f}
                    </Typography>
                  ))}
                </Box>
              )}
              {viewer.warnings.length > 0 && (
                <Box>
                  {viewer.warnings.map((w, i) => (
                    <Typography
                      key={i}
                      variant="caption"
                      sx={{ color: 'rgba(245, 158, 11, 0.8)', display: 'block' }}
                    >
                      ⚠️ {w}
                    </Typography>
                  ))}
                </Box>
              )}
            </Box>
          )}
        </Box>
      </Collapse>
    </Paper>
  );
};

export default ViewerCard;
