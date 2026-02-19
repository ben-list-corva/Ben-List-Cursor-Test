import React from 'react';
import {
  Box,
  Typography,
  Chip,
  Tooltip,
  Collapse,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import LinkIcon from '@mui/icons-material/Link';
import SettingsIcon from '@mui/icons-material/Settings';
import type { StreamResult, CheckStatus } from '../types';

interface StreamCheckRowProps {
  streamType: 'frac' | 'wireline' | 'pumpdown';
  result: StreamResult | null;
  isRequired: boolean;
}

const streamTypeLabels: Record<string, { label: string; color: string }> = {
  frac: { label: 'Frac', color: '#ef4444' },
  wireline: { label: 'Wireline', color: '#8b5cf6' },
  pumpdown: { label: 'Pumpdown', color: '#06b6d4' },
};

const StatusIcon: React.FC<{ status: CheckStatus; size?: number }> = ({ status, size = 18 }) => {
  switch (status) {
    case 'PASS':
      return <CheckCircleOutlineIcon sx={{ fontSize: size, color: '#10b981' }} />;
    case 'WARN':
      return <WarningAmberIcon sx={{ fontSize: size, color: '#f59e0b' }} />;
    case 'FAIL':
      return <ErrorOutlineIcon sx={{ fontSize: size, color: '#ef4444' }} />;
    default:
      return null;
  }
};

/**
 * Row component for displaying stream check results
 */
export const StreamCheckRow: React.FC<StreamCheckRowProps> = ({
  streamType,
  result,
  isRequired,
}) => {
  const [expanded, setExpanded] = React.useState(false);
  
  const typeConfig = streamTypeLabels[streamType];
  const hasDetails = result && (result.connected_app_ids?.length > 0 || result.source_app);
  
  // If stream doesn't exist
  if (!result || result.stream_status === 'missing') {
    return (
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
        <Chip
          label={typeConfig.label}
          size="small"
          sx={{
            backgroundColor: `${typeConfig.color}20`,
            color: typeConfig.color,
            fontWeight: 600,
            minWidth: 80,
          }}
        />
        
        <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
          <StatusIcon status={isRequired ? 'FAIL' : 'WARN'} />
          <Typography
            variant="body2"
            sx={{ color: 'rgba(148, 163, 184, 0.7)' }}
          >
            Stream not found
          </Typography>
        </Box>
        
        <Chip
          label={isRequired ? 'Required' : 'Optional'}
          size="small"
          sx={{
            backgroundColor: isRequired ? 'rgba(239, 68, 68, 0.1)' : 'rgba(148, 163, 184, 0.1)',
            color: isRequired ? '#ef4444' : 'rgba(148, 163, 184, 0.7)',
            fontSize: '0.7rem',
          }}
        />
      </Box>
    );
  }
  
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
          padding: 2,
          cursor: hasDetails ? 'pointer' : 'default',
          '&:hover': {
            backgroundColor: hasDetails ? 'rgba(30, 41, 59, 0.5)' : 'transparent',
          },
        }}
        onClick={() => hasDetails && setExpanded(!expanded)}
      >
        {/* Stream Type Badge */}
        <Chip
          label={typeConfig.label}
          size="small"
          sx={{
            backgroundColor: `${typeConfig.color}20`,
            color: typeConfig.color,
            fontWeight: 600,
            minWidth: 80,
          }}
        />
        
        {/* Overall Status */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 100 }}>
          <StatusIcon status={result.check_status} />
          <Typography
            variant="body2"
            sx={{
              color: result.check_status === 'PASS' ? '#10b981' :
                     result.check_status === 'WARN' ? '#f59e0b' : '#ef4444',
              fontWeight: 500,
            }}
          >
            {result.check_status}
          </Typography>
        </Box>
        
        {/* Stream Status */}
        <Tooltip title="Stream Status">
          <Chip
            icon={<LinkIcon sx={{ fontSize: 14 }} />}
            label={result.stream_status}
            size="small"
            sx={{
              backgroundColor: result.stream_status === 'active' 
                ? 'rgba(16, 185, 129, 0.1)' 
                : 'rgba(245, 158, 11, 0.1)',
              color: result.stream_status === 'active' ? '#10b981' : '#f59e0b',
              fontSize: '0.75rem',
              '& .MuiChip-icon': {
                color: 'inherit',
              },
            }}
          />
        </Tooltip>
        
        {/* Source App Status */}
        {result.source_app && (
          <Tooltip title={`Source App: ${result.source_app.app_name}`}>
            <Chip
              icon={<SettingsIcon sx={{ fontSize: 14 }} />}
              label={`Source: ${result.source_app.status}`}
              size="small"
              sx={{
                backgroundColor: result.source_app.status === 'active'
                  ? 'rgba(16, 185, 129, 0.1)'
                  : 'rgba(245, 158, 11, 0.1)',
                color: result.source_app.status === 'active' ? '#10b981' : '#f59e0b',
                fontSize: '0.75rem',
                '& .MuiChip-icon': {
                  color: 'inherit',
                },
              }}
            />
          </Tooltip>
        )}
        
        {/* Stream ID */}
        {result.stream_id && (
          <Typography
            variant="caption"
            sx={{ color: 'rgba(148, 163, 184, 0.5)', marginLeft: 'auto' }}
          >
            Stream ID: {result.stream_id}
          </Typography>
        )}
        
        {/* Expand Button */}
        {hasDetails && (
          <IconButton
            size="small"
            sx={{ color: 'rgba(148, 163, 184, 0.5)' }}
          >
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        )}
      </Box>
      
      {/* Expanded Details */}
      <Collapse in={expanded}>
        <Box
          sx={{
            padding: 2,
            paddingTop: 1,
            borderTop: '1px solid rgba(148, 163, 184, 0.1)',
          }}
        >
          {/* App Connections */}
          {result.connected_app_ids && result.connected_app_ids.length > 0 && (
            <Box sx={{ marginBottom: 2 }}>
              <Typography
                variant="caption"
                sx={{ 
                  color: 'rgba(148, 163, 184, 0.6)', 
                  display: 'block', 
                  marginBottom: 0.5,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  fontSize: '0.65rem',
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
                      fontSize: '0.7rem',
                      height: 22,
                    }}
                  />
                ))}
              </Box>
            </Box>
          )}
          
          {/* Stream Failures */}
          {result.failures.length > 0 && (
            <List dense disablePadding sx={{ marginBottom: 1 }}>
              {result.failures.map((failure, idx) => (
                <ListItem key={`fail-${idx}`} sx={{ paddingLeft: 0 }}>
                  <ListItemIcon sx={{ minWidth: 28 }}>
                    <ErrorOutlineIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                  </ListItemIcon>
                  <ListItemText
                    primary={failure}
                    primaryTypographyProps={{
                      variant: 'body2',
                      sx: { color: 'rgba(239, 68, 68, 0.9)', fontSize: '0.85rem' },
                    }}
                  />
                </ListItem>
              ))}
            </List>
          )}
          
          {/* Stream Warnings */}
          {result.warnings.length > 0 && (
            <List dense disablePadding sx={{ marginBottom: 1 }}>
              {result.warnings.map((warning, idx) => (
                <ListItem key={`warn-${idx}`} sx={{ paddingLeft: 0 }}>
                  <ListItemIcon sx={{ minWidth: 28 }}>
                    <WarningAmberIcon sx={{ fontSize: 16, color: '#f59e0b' }} />
                  </ListItemIcon>
                  <ListItemText
                    primary={warning}
                    primaryTypographyProps={{
                      variant: 'body2',
                      sx: { color: 'rgba(245, 158, 11, 0.9)', fontSize: '0.85rem' },
                    }}
                  />
                </ListItem>
              ))}
            </List>
          )}
          
          {/* Source App Issues */}
          {result.source_app && (result.source_app.failures.length > 0 || result.source_app.warnings.length > 0) && (
            <List dense disablePadding sx={{ marginBottom: 1 }}>
              {result.source_app.failures.map((failure, idx) => (
                <ListItem key={`src-fail-${idx}`} sx={{ paddingLeft: 0 }}>
                  <ListItemIcon sx={{ minWidth: 28 }}>
                    <ErrorOutlineIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                  </ListItemIcon>
                  <ListItemText
                    primary={`Source App: ${failure}`}
                    primaryTypographyProps={{
                      variant: 'body2',
                      sx: { color: 'rgba(239, 68, 68, 0.9)', fontSize: '0.85rem' },
                    }}
                  />
                </ListItem>
              ))}
              {result.source_app.warnings.map((warning, idx) => (
                <ListItem key={`src-warn-${idx}`} sx={{ paddingLeft: 0 }}>
                  <ListItemIcon sx={{ minWidth: 28 }}>
                    <WarningAmberIcon sx={{ fontSize: 16, color: '#f59e0b' }} />
                  </ListItemIcon>
                  <ListItemText
                    primary={`Source App: ${warning}`}
                    primaryTypographyProps={{
                      variant: 'body2',
                      sx: { color: 'rgba(245, 158, 11, 0.9)', fontSize: '0.85rem' },
                    }}
                  />
                </ListItem>
              ))}
            </List>
          )}
          
          {/* Source App Settings */}
          {result.source_app && (
            <Box
              sx={{
                padding: 1.5,
                backgroundColor: 'rgba(15, 23, 42, 0.5)',
                borderRadius: 1,
                fontSize: '0.75rem',
                fontFamily: '"IBM Plex Mono", monospace',
              }}
            >
              <Typography
                variant="caption"
                sx={{ 
                  color: 'rgba(148, 163, 184, 0.7)', 
                  display: 'block', 
                  marginBottom: 1,
                  fontWeight: 600,
                  fontFamily: '"IBM Plex Sans", sans-serif',
                }}
              >
                Source App: {result.source_app.app_name} (ID: {result.source_app.app_id})
              </Typography>
              <Box sx={{ color: 'rgba(148, 163, 184, 0.8)', lineHeight: 1.8 }}>
                <div><span style={{ color: '#94a3b8' }}>api_number:</span> <span style={{ color: result.source_app.settings?.api_number ? '#10b981' : '#f59e0b' }}>{result.source_app.settings?.api_number || '(not set)'}</span></div>
                <div><span style={{ color: '#94a3b8' }}>stream_api_root_url:</span> <span style={{ color: result.source_app.settings?.stream_api_root_url ? '#94a3b8' : '#f59e0b' }}>{result.source_app.settings?.stream_api_root_url || '(not set)'}</span></div>
                <div><span style={{ color: '#94a3b8' }}>stream_api_log_path:</span> <span style={{ color: result.source_app.settings?.stream_api_log_path ? '#94a3b8' : '#f59e0b' }}>{result.source_app.settings?.stream_api_log_path || '(not set)'}</span></div>
                <div><span style={{ color: '#94a3b8' }}>force_start_from:</span> <span style={{ color: result.source_app.settings?.force_start_from ? '#94a3b8' : '#f59e0b' }}>{result.source_app.settings?.force_start_from || '(not set)'}</span></div>
                <div><span style={{ color: '#94a3b8' }}>stream_api_key:</span> {result.source_app.settings?.stream_api_key_masked || '(not set)'}</div>
              </Box>
            </Box>
          )}
        </Box>
      </Collapse>
    </Box>
  );
};

export default StreamCheckRow;
