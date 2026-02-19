import React, { useState } from 'react';
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Collapse,
  Chip,
  Skeleton,
} from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import type {
  PadResult,
  WellResult,
  ViewerResult,
  StreamResult,
  ViewerStreamResult,
  CheckStatus,
  StreamStatus,
  StageStatus,
  ScheduleCheck,
} from '../types';
import { DetailSection, DetailItem, AppChipList } from './ExpandableCell';

interface PipelineTableProps {
  result: PadResult | null;
  isLoading: boolean;
}

// Status color mapping
const getStatusColor = (status: StreamStatus | CheckStatus | string | null): 'green' | 'yellow' | 'red' | 'gray' => {
  if (!status) return 'gray';
  const s = status.toLowerCase();
  if (s === 'active' || s === 'pass' || s === 'good') return 'green';
  if (s === 'idle' || s === 'warn' || s === 'warning') return 'yellow';
  if (s === 'fail' || s === 'missing' || s === 'error') return 'red';
  return 'gray';
};

const statusColors = {
  green: '#10b981',
  yellow: '#f59e0b',
  red: '#ef4444',
  gray: 'rgba(148, 163, 184, 0.5)',
};

// Get stream status text
const getStreamStatusText = (stream: StreamResult | ViewerStreamResult | null): string => {
  if (!stream) return 'Missing';
  return stream.stream_status === 'active' ? 'Active' : 
         stream.stream_status === 'idle' ? 'Idle' : 
         stream.stream_status === 'missing' ? 'Missing' : 'Unknown';
};

// Get stream platform status
const getStreamPlatformStatus = (check: { check_status: CheckStatus } | null): { text: string; color: 'green' | 'yellow' | 'red' | 'gray' } => {
  if (!check) return { text: '-', color: 'gray' };
  return {
    text: check.check_status === 'PASS' ? 'good' : check.check_status === 'WARN' ? 'warn' : 'fail',
    color: getStatusColor(check.check_status),
  };
};

// Get stage status
const getStageStatusDisplay = (stage: StageStatus | null): { text: string; color: 'green' | 'yellow' | 'red' | 'gray' } => {
  if (!stage) return { text: '-', color: 'gray' };
  if (stage.has_active_stage) return { text: 'good', color: 'green' };
  if (stage.has_stages) return { text: 'warn', color: 'yellow' };
  return { text: 'fail', color: 'red' };
};

// Get schedule status
const getScheduleStatus = (schedule: ScheduleCheck | null): { text: string; color: 'green' | 'yellow' | 'red' | 'gray' } => {
  if (!schedule) return { text: '-', color: 'gray' };
  const hasStage1 = schedule.stage_1_has_schedule;
  const hasLast = schedule.last_stage_has_schedule;
  if (hasStage1 && hasLast) return { text: 'yes', color: 'green' };
  if (hasStage1 || hasLast) return { text: 'partial', color: 'yellow' };
  if (hasStage1 === false && hasLast === false) return { text: 'no', color: 'red' };
  return { text: '-', color: 'gray' };
};

// Status cell component
interface StatusCellProps {
  text: string;
  color: 'green' | 'yellow' | 'red' | 'gray';
  onClick?: () => void;
  isExpanded?: boolean;
  hasWarning?: boolean;  // Show warning icon for issues
  warningTooltip?: string;
  hasVerification?: boolean;  // Show exclamation icon for verification items
  verificationTooltip?: string;
}

const StatusCell: React.FC<StatusCellProps> = ({ text, color, onClick, isExpanded, hasWarning, warningTooltip, hasVerification, verificationTooltip }) => (
  <TableCell
    onClick={onClick}
    sx={{
      cursor: onClick ? 'pointer' : 'default',
      '&:hover': onClick ? { backgroundColor: 'rgba(59, 130, 246, 0.05)' } : {},
      py: 1,
    }}
  >
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <Box
        sx={{
          width: 8,
          height: 8,
          borderRadius: '50%',
          backgroundColor: statusColors[color],
          flexShrink: 0,
        }}
      />
      <Typography
        variant="body2"
        sx={{
          color: statusColors[color],
          fontWeight: 500,
          fontSize: '0.8rem',
        }}
      >
        {text}
      </Typography>
      {hasWarning && (
        <Box
          component="span"
          title={warningTooltip || 'Check stream configuration'}
          sx={{
            color: '#f59e0b',
            display: 'flex',
            alignItems: 'center',
            animation: 'pulse 2s infinite',
            '@keyframes pulse': {
              '0%, 100%': { opacity: 1 },
              '50%': { opacity: 0.5 },
            },
          }}
        >
          ⚠️
        </Box>
      )}
      {hasVerification && !hasWarning && (
        <Box
          component="span"
          title={verificationTooltip || 'Verify configuration'}
          sx={{
            color: '#60a5fa',
            display: 'flex',
            alignItems: 'center',
            fontSize: '0.9rem',
          }}
        >
          ❗
        </Box>
      )}
      {onClick && (
        isExpanded ? (
          <KeyboardArrowDownIcon sx={{ fontSize: 16, color: 'rgba(148, 163, 184, 0.5)', ml: 'auto' }} />
        ) : (
          <KeyboardArrowRightIcon sx={{ fontSize: 16, color: 'rgba(148, 163, 184, 0.5)', ml: 'auto' }} />
        )
      )}
    </Box>
  </TableCell>
);

// Expanded detail row for wells
interface WellDetailRowProps {
  well: WellResult;
  expandedColumn: string | null;
  colSpan: number;
}

const WellDetailRow: React.FC<WellDetailRowProps> = ({ well, expandedColumn, colSpan }) => {
  if (!expandedColumn) return null;

  const renderDetails = () => {
    switch (expandedColumn) {
      case 'name':
        return (
          <Box>
            <DetailItem label="Well Name" value={well.well_name} />
            <DetailItem label="Asset ID" value={well.corva_well_asset_id} />
            <DetailItem label="Well ID" value={well.well_id} />
            <DetailItem label="API Number" value={well.api_number || '(not set)'} />
            {well.color && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)', minWidth: 100 }}>Color:</Typography>
                <Box sx={{ width: 16, height: 16, borderRadius: '50%', backgroundColor: well.color, border: '1px solid rgba(255,255,255,0.2)' }} />
                <Typography variant="caption" sx={{ color: '#f8fafc' }}>{well.color}</Typography>
              </Box>
            )}
            {well.line_assignment && <DetailItem label="Line" value={well.line_assignment} />}
            
            {/* Well Failures */}
            {well.failures && well.failures.length > 0 && (
              <Box sx={{ mt: 1 }}>
                {well.failures.map((f, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ {f}</Typography>
                ))}
              </Box>
            )}
            
            {/* Well Warnings */}
            {well.warnings && well.warnings.length > 0 && (
              <Box sx={{ mt: 0.5 }}>
                {well.warnings.map((w, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ {w}</Typography>
                ))}
              </Box>
            )}
          </Box>
        );
      
      case 'frac':
      case 'wireline':
      case 'pumpdown': {
        const stream = well.corva_streams[expandedColumn];
        if (!stream) return <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>No stream data</Typography>;
        return (
          <Box>
            <DetailSection title="Stream Info">
              <DetailItem label="Stream ID" value={stream.stream_id} />
              <DetailItem label="Stream Name" value={stream.stream_name} />
              <DetailItem label="Status" value={stream.stream_status} />
            </DetailSection>
            
            {/* Stream Failures */}
            {stream.failures && stream.failures.length > 0 && (
              <DetailSection title="Stream Failures">
                {stream.failures.map((f, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ {f}</Typography>
                ))}
              </DetailSection>
            )}
            
            {/* Stream Warnings */}
            {stream.warnings && stream.warnings.length > 0 && (
              <DetailSection title="Stream Warnings">
                {stream.warnings.map((w, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ {w}</Typography>
                ))}
              </DetailSection>
            )}
            
            <DetailSection title="Connected Apps">
              <AppChipList apps={stream.connected_app_names} />
            </DetailSection>
            
            {stream.source_app && (
              <DetailSection title="Source App">
                <DetailItem label="App" value={`${stream.source_app.app_name} (ID: ${stream.source_app.app_id})`} />
                <DetailItem label="Status" value={stream.source_app.status} />
                {stream.source_app.settings && (
                  <>
                    <Box sx={{ mt: 1, mb: 0.5 }}>
                      <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)', fontStyle: 'italic' }}>Settings:</Typography>
                    </Box>
                    <DetailItem label="API Number" value={
                      <Typography variant="caption" sx={{ color: stream.source_app.settings.api_number ? '#10b981' : '#f59e0b' }}>
                        {stream.source_app.settings.api_number || '(not set)'}
                      </Typography>
                    } />
                    <DetailItem label="Stream API URL" value={stream.source_app.settings.stream_api_root_url || '(not set)'} />
                    <DetailItem label="Log Path" value={stream.source_app.settings.stream_api_log_path || '(not set)'} />
                    <DetailItem label="Force Start From" value={stream.source_app.settings.force_start_from || '(not set)'} />
                    <DetailItem label="API Key" value={stream.source_app.settings.stream_api_key_masked || '(not set)'} />
                  </>
                )}
                
                {/* Source App Failures */}
                {stream.source_app.failures && stream.source_app.failures.length > 0 && (
                  <Box sx={{ mt: 1 }}>
                    {stream.source_app.failures.map((f, i) => (
                      <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ Source: {f}</Typography>
                    ))}
                  </Box>
                )}
                
                {/* Source App Warnings */}
                {stream.source_app.warnings && stream.source_app.warnings.length > 0 && (
                  <Box sx={{ mt: 0.5 }}>
                    {stream.source_app.warnings.map((w, i) => (
                      <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ Source: {w}</Typography>
                    ))}
                  </Box>
                )}
              </DetailSection>
            )}
          </Box>
        );
      }
      
      case 'stream_platform':
        return (
          <Box>
            <DetailItem label="Stream Well ID" value={well.stream_platform_well_id || '(not found)'} />
            <DetailItem label="Stream Well Name" value={well.stream_platform_well_name || '(not found)'} />
            <DetailItem label="Status" value={well.stream_platform_check?.check_status || 'Unknown'} />
            
            {/* Stream Platform Failures */}
            {well.stream_platform_check?.failures && well.stream_platform_check.failures.length > 0 && (
              <Box sx={{ mt: 1 }}>
                {well.stream_platform_check.failures.map((f, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ {f}</Typography>
                ))}
              </Box>
            )}
            
            {/* Stream Platform Warnings */}
            {well.stream_platform_check?.warnings && well.stream_platform_check.warnings.length > 0 && (
              <Box sx={{ mt: 0.5 }}>
                {well.stream_platform_check.warnings.map((w, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ {w}</Typography>
                ))}
              </Box>
            )}
          </Box>
        );
      
      case 'stage':
        if (!well.stage_status) return <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>No stage data</Typography>;
        return (
          <Box>
            <DetailItem label="Has Stages" value={well.stage_status.has_stages ? 'Yes' : 'No'} />
            <DetailItem label="Active Stage" value={well.stage_status.has_active_stage ? `#${well.stage_status.active_stage_number}` : 'None'} />
            <DetailItem label="Stage Action" value={well.stage_status.active_stage_action || 'N/A'} />
            <DetailItem label="Streambox ID" value={well.stage_status.sb_id || 'N/A'} />
            
            {/* Stage Failures */}
            {well.stage_status.failures && well.stage_status.failures.length > 0 && (
              <Box sx={{ mt: 1 }}>
                {well.stage_status.failures.map((f, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ {f}</Typography>
                ))}
              </Box>
            )}
            
            {/* Stage Warnings */}
            {well.stage_status.warnings && well.stage_status.warnings.length > 0 && (
              <Box sx={{ mt: 0.5 }}>
                {well.stage_status.warnings.map((w, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ {w}</Typography>
                ))}
              </Box>
            )}
          </Box>
        );
      
      case 'schedule':
        if (!well.schedule_check) return <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>No schedule data</Typography>;
        return (
          <Box>
            <DetailItem label="Stage 1" value={well.schedule_check.stage_1_has_schedule ? 'Schedule uploaded' : 'No schedule'} />
            {well.schedule_check.last_stage_number && (
              <DetailItem 
                label={`Stage ${well.schedule_check.last_stage_number}`} 
                value={well.schedule_check.last_stage_has_schedule ? 'Schedule uploaded' : 'No schedule'} 
              />
            )}
          </Box>
        );
      
      default:
        return null;
    }
  };

  return (
    <TableRow>
      <TableCell colSpan={colSpan} sx={{ p: 0, borderBottom: 'none' }}>
        <Collapse in={!!expandedColumn} timeout="auto" unmountOnExit>
          <Box
            sx={{
              backgroundColor: 'rgba(30, 41, 59, 0.6)',
              borderLeft: '3px solid rgba(59, 130, 246, 0.5)',
              p: 2,
              mx: 1,
              my: 0.5,
              borderRadius: 1,
            }}
          >
            {renderDetails()}
          </Box>
        </Collapse>
      </TableCell>
    </TableRow>
  );
};

// Expanded detail row for viewers
interface ViewerDetailRowProps {
  viewer: ViewerResult;
  expandedColumn: string | null;
  colSpan: number;
}

const ViewerDetailRow: React.FC<ViewerDetailRowProps> = ({ viewer, expandedColumn, colSpan }) => {
  if (!expandedColumn) return null;

  const renderDetails = () => {
    switch (expandedColumn) {
      case 'name':
        return (
          <Box>
            <DetailItem label="Viewer Name" value={viewer.viewer_name} />
            <DetailItem label="Asset ID" value={viewer.viewer_asset_id} />
            <DetailItem label="API Number" value={viewer.api_number || '(not set)'} />
            <DetailItem label="Status" value={viewer.viewer_status} />
            <DetailItem label="Frac Fleet" value={viewer.frac_fleet_name} />
            {viewer.line_name && <DetailItem label="Line" value={viewer.line_name} />}
            
            {/* Viewer Failures */}
            {viewer.failures && viewer.failures.length > 0 && (
              <Box sx={{ mt: 1 }}>
                {viewer.failures.map((f, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ {f}</Typography>
                ))}
              </Box>
            )}
            
            {/* Viewer Warnings */}
            {viewer.warnings && viewer.warnings.length > 0 && (
              <Box sx={{ mt: 0.5 }}>
                {viewer.warnings.map((w, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ {w}</Typography>
                ))}
              </Box>
            )}
          </Box>
        );
      
      case 'frac':
      case 'wireline':
      case 'pumpdown': {
        const viewerStream = viewer.streams[expandedColumn];
        if (!viewerStream) return <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>No stream data</Typography>;
        return (
          <Box>
            <DetailSection title="Stream Info">
              <DetailItem label="Stream ID" value={viewerStream.stream_id} />
              <DetailItem label="Stream Name" value={viewerStream.stream_name} />
              <DetailItem label="Status" value={viewerStream.stream_status} />
            </DetailSection>
            
            {/* Stream Failures */}
            {viewerStream.failures && viewerStream.failures.length > 0 && (
              <DetailSection title="Stream Failures">
                {viewerStream.failures.map((f, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ {f}</Typography>
                ))}
              </DetailSection>
            )}
            
            {/* Stream Warnings */}
            {viewerStream.warnings && viewerStream.warnings.length > 0 && (
              <DetailSection title="Stream Warnings">
                {viewerStream.warnings.map((w, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ {w}</Typography>
                ))}
              </DetailSection>
            )}
            
            <DetailSection title="Connected Apps">
              <AppChipList apps={viewerStream.connected_app_names} />
            </DetailSection>
            
            {viewerStream.source_app && (
              <DetailSection title="Source App">
                <DetailItem label="App" value={`${viewerStream.source_app.app_name} (ID: ${viewerStream.source_app.app_id})`} />
                <DetailItem label="Status" value={viewerStream.source_app.status} />
                {viewerStream.source_app.settings && (
                  <>
                    <Box sx={{ mt: 1, mb: 0.5 }}>
                      <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)', fontStyle: 'italic' }}>Settings:</Typography>
                    </Box>
                    <DetailItem label="API Number" value={
                      <Typography variant="caption" sx={{ color: viewerStream.source_app.settings.api_number ? '#10b981' : '#f59e0b' }}>
                        {viewerStream.source_app.settings.api_number || '(not set)'}
                      </Typography>
                    } />
                    <DetailItem label="Stream API URL" value={viewerStream.source_app.settings.stream_api_root_url || '(not set)'} />
                    <DetailItem label="Log Path" value={viewerStream.source_app.settings.stream_api_log_path || '(not set)'} />
                    <DetailItem label="Force Start From" value={viewerStream.source_app.settings.force_start_from || '(not set)'} />
                    <DetailItem label="API Key" value={viewerStream.source_app.settings.stream_api_key_masked || '(not set)'} />
                  </>
                )}
                
                {/* Source App Failures */}
                {viewerStream.source_app.failures && viewerStream.source_app.failures.length > 0 && (
                  <Box sx={{ mt: 1 }}>
                    {viewerStream.source_app.failures.map((f, i) => (
                      <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ Source: {f}</Typography>
                    ))}
                  </Box>
                )}
                
                {/* Source App Warnings */}
                {viewerStream.source_app.warnings && viewerStream.source_app.warnings.length > 0 && (
                  <Box sx={{ mt: 0.5 }}>
                    {viewerStream.source_app.warnings.map((w, i) => (
                      <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ Source: {w}</Typography>
                    ))}
                  </Box>
                )}
              </DetailSection>
            )}
          </Box>
        );
      }
      
      case 'stream_platform':
        if (!viewer.stream_platform_check) return <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>No data</Typography>;
        return (
          <Box>
            <DetailItem label="Stream Well ID" value={viewer.stream_platform_well_id || '(not found)'} />
            <DetailItem label="Stream Well Name" value={viewer.stream_platform_well_name || '(not found)'} />
            <DetailItem label="Status" value={viewer.stream_platform_check.check_status} />
            
            {/* Stream Platform Failures */}
            {viewer.stream_platform_check.failures && viewer.stream_platform_check.failures.length > 0 && (
              <Box sx={{ mt: 1 }}>
                {viewer.stream_platform_check.failures.map((f, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ {f}</Typography>
                ))}
              </Box>
            )}
            
            {/* Stream Platform Warnings */}
            {viewer.stream_platform_check.warnings && viewer.stream_platform_check.warnings.length > 0 && (
              <Box sx={{ mt: 0.5 }}>
                {viewer.stream_platform_check.warnings.map((w, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ {w}</Typography>
                ))}
              </Box>
            )}
          </Box>
        );
      
      case 'stage':
        if (!viewer.stage_status) return <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>No stage data</Typography>;
        return (
          <Box>
            <DetailItem label="Has Stages" value={viewer.stage_status.has_stages ? 'Yes' : 'No'} />
            <DetailItem label="Active Stage" value={viewer.stage_status.has_active_stage ? `#${viewer.stage_status.active_stage_number}` : 'None'} />
            <DetailItem label="Stage Action" value={viewer.stage_status.active_stage_action || 'N/A'} />
            <DetailItem label="Streambox ID" value={viewer.stage_status.sb_id || 'N/A'} />
            
            {/* Stage Failures */}
            {viewer.stage_status.failures && viewer.stage_status.failures.length > 0 && (
              <Box sx={{ mt: 1 }}>
                {viewer.stage_status.failures.map((f, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>⚠ {f}</Typography>
                ))}
              </Box>
            )}
            
            {/* Stage Warnings */}
            {viewer.stage_status.warnings && viewer.stage_status.warnings.length > 0 && (
              <Box sx={{ mt: 0.5 }}>
                {viewer.stage_status.warnings.map((w, i) => (
                  <Typography key={i} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>⚠ {w}</Typography>
                ))}
              </Box>
            )}
          </Box>
        );
      
      default:
        return null;
    }
  };

  return (
    <TableRow>
      <TableCell colSpan={colSpan} sx={{ p: 0, borderBottom: 'none' }}>
        <Collapse in={!!expandedColumn} timeout="auto" unmountOnExit>
          <Box
            sx={{
              backgroundColor: 'rgba(30, 41, 59, 0.6)',
              borderLeft: '3px solid rgba(168, 85, 247, 0.5)',
              p: 2,
              mx: 1,
              my: 0.5,
              borderRadius: 1,
            }}
          >
            {renderDetails()}
          </Box>
        </Collapse>
      </TableCell>
    </TableRow>
  );
};

// Well row component
interface WellRowProps {
  well: WellResult;
}

const WellRow: React.FC<WellRowProps> = ({ well }) => {
  const [expandedColumn, setExpandedColumn] = useState<string | null>(null);

  const toggleColumn = (column: string) => {
    setExpandedColumn(expandedColumn === column ? null : column);
  };

  const fracStatus = getStreamStatusText(well.corva_streams.frac);
  const wlStatus = getStreamStatusText(well.corva_streams.wireline);
  const pdStatus = getStreamStatusText(well.corva_streams.pumpdown);
  const streamPlatform = getStreamPlatformStatus(well.stream_platform_check);
  const stageStatus = getStageStatusDisplay(well.stage_status);
  const scheduleStatus = getScheduleStatus(well.schedule_check);

  return (
    <>
      <TableRow
        sx={{
          '&:hover': { backgroundColor: 'rgba(30, 41, 59, 0.4)' },
          backgroundColor: expandedColumn ? 'rgba(30, 41, 59, 0.3)' : 'transparent',
        }}
      >
        {/* Well Name */}
        <TableCell
          onClick={() => toggleColumn('name')}
          sx={{ cursor: 'pointer', '&:hover': { backgroundColor: 'rgba(59, 130, 246, 0.05)' }, py: 1 }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {well.color && (
              <Box
                sx={{
                  width: 10,
                  height: 10,
                  borderRadius: '50%',
                  backgroundColor: well.color,
                  flexShrink: 0,
                  border: '1px solid rgba(255,255,255,0.2)',
                }}
              />
            )}
            <Typography variant="body2" sx={{ color: '#f8fafc', fontWeight: 500, fontSize: '0.85rem' }}>
              {well.well_name}
            </Typography>
            {expandedColumn === 'name' ? (
              <KeyboardArrowDownIcon sx={{ fontSize: 16, color: 'rgba(148, 163, 184, 0.5)', ml: 'auto' }} />
            ) : (
              <KeyboardArrowRightIcon sx={{ fontSize: 16, color: 'rgba(148, 163, 184, 0.5)', ml: 'auto' }} />
            )}
          </Box>
        </TableCell>

        {/* Type */}
        <TableCell sx={{ py: 1 }}>
          <Chip
            label="Well"
            size="small"
            sx={{
              height: 20,
              fontSize: '0.7rem',
              backgroundColor: 'rgba(59, 130, 246, 0.15)',
              color: '#60a5fa',
            }}
          />
        </TableCell>

        {/* Frac */}
        <StatusCell
          text={fracStatus}
          color={getStatusColor(well.corva_streams.frac?.stream_status || null)}
          onClick={() => toggleColumn('frac')}
          isExpanded={expandedColumn === 'frac'}
          hasWarning={(well.corva_streams.frac?.warnings?.filter(w => !w.toLowerCase().includes('idle'))?.length || 0) > 0 || (well.corva_streams.frac?.failures?.length || 0) > 0}
          warningTooltip={[...(well.corva_streams.frac?.failures || []), ...(well.corva_streams.frac?.warnings?.filter(w => !w.toLowerCase().includes('idle')) || [])].join(', ')}
        />

        {/* Wireline */}
        <StatusCell
          text={wlStatus}
          color={getStatusColor(well.corva_streams.wireline?.stream_status || null)}
          onClick={() => toggleColumn('wireline')}
          isExpanded={expandedColumn === 'wireline'}
          hasWarning={(well.corva_streams.wireline?.warnings?.filter(w => !w.toLowerCase().includes('idle'))?.length || 0) > 0 || (well.corva_streams.wireline?.failures?.length || 0) > 0}
          warningTooltip={[...(well.corva_streams.wireline?.failures || []), ...(well.corva_streams.wireline?.warnings?.filter(w => !w.toLowerCase().includes('idle')) || [])].join(', ')}
        />

        {/* Pumpdown */}
        <StatusCell
          text={pdStatus}
          color={getStatusColor(well.corva_streams.pumpdown?.stream_status || null)}
          onClick={() => toggleColumn('pumpdown')}
          isExpanded={expandedColumn === 'pumpdown'}
          hasWarning={(well.corva_streams.pumpdown?.warnings?.filter(w => !w.toLowerCase().includes('idle') && !w.toLowerCase().includes('manual pumpdown'))?.length || 0) > 0 || (well.corva_streams.pumpdown?.failures?.length || 0) > 0}
          warningTooltip={[...(well.corva_streams.pumpdown?.failures || []), ...(well.corva_streams.pumpdown?.warnings?.filter(w => !w.toLowerCase().includes('idle') && !w.toLowerCase().includes('manual pumpdown')) || [])].join(', ')}
          hasVerification={well.corva_streams.pumpdown?.source_app?.is_manual_pumpdown || false}
          verificationTooltip="Manual pumpdown - verify data flows through frac streambox"
        />

        {/* Stream Platform */}
        <StatusCell
          text={streamPlatform.text}
          color={streamPlatform.color}
          onClick={() => toggleColumn('stream_platform')}
          isExpanded={expandedColumn === 'stream_platform'}
        />

        {/* Stage */}
        <StatusCell
          text={stageStatus.text}
          color={stageStatus.color}
          onClick={() => toggleColumn('stage')}
          isExpanded={expandedColumn === 'stage'}
        />

        {/* Schedule */}
        <StatusCell
          text={scheduleStatus.text}
          color={scheduleStatus.color}
          onClick={() => toggleColumn('schedule')}
          isExpanded={expandedColumn === 'schedule'}
        />
      </TableRow>

      <WellDetailRow well={well} expandedColumn={expandedColumn} colSpan={8} />
    </>
  );
};

// Viewer row component
interface ViewerRowProps {
  viewer: ViewerResult;
}

const ViewerRow: React.FC<ViewerRowProps> = ({ viewer }) => {
  const [expandedColumn, setExpandedColumn] = useState<string | null>(null);

  const toggleColumn = (column: string) => {
    setExpandedColumn(expandedColumn === column ? null : column);
  };

  const fracStatus = getStreamStatusText(viewer.streams.frac);
  const wlStatus = getStreamStatusText(viewer.streams.wireline);
  const pdStatus = getStreamStatusText(viewer.streams.pumpdown);
  const streamPlatform = getStreamPlatformStatus(viewer.stream_platform_check);
  const stageStatus = getStageStatusDisplay(viewer.stage_status);

  // Use full viewer name
  const displayName = viewer.viewer_name || 'Viewer';

  return (
    <>
      <TableRow
        sx={{
          '&:hover': { backgroundColor: 'rgba(168, 85, 247, 0.1)' },
          backgroundColor: expandedColumn ? 'rgba(168, 85, 247, 0.08)' : 'rgba(168, 85, 247, 0.05)',
        }}
      >
        {/* Viewer Name */}
        <TableCell
          onClick={() => toggleColumn('name')}
          sx={{ cursor: 'pointer', '&:hover': { backgroundColor: 'rgba(168, 85, 247, 0.1)' }, py: 1 }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Box
              sx={{
                width: 10,
                height: 10,
                borderRadius: '50%',
                backgroundColor: '#a855f7',
                flexShrink: 0,
              }}
            />
            <Typography variant="body2" sx={{ color: '#c4b5fd', fontWeight: 500, fontSize: '0.85rem' }}>
              {displayName}
            </Typography>
            {expandedColumn === 'name' ? (
              <KeyboardArrowDownIcon sx={{ fontSize: 16, color: 'rgba(148, 163, 184, 0.5)', ml: 'auto' }} />
            ) : (
              <KeyboardArrowRightIcon sx={{ fontSize: 16, color: 'rgba(148, 163, 184, 0.5)', ml: 'auto' }} />
            )}
          </Box>
        </TableCell>

        {/* Type */}
        <TableCell sx={{ py: 1 }}>
          <Chip
            label="Viewer"
            size="small"
            sx={{
              height: 20,
              fontSize: '0.7rem',
              backgroundColor: 'rgba(168, 85, 247, 0.2)',
              color: '#c4b5fd',
            }}
          />
        </TableCell>

        {/* Frac */}
        <StatusCell
          text={fracStatus}
          color={getStatusColor(viewer.streams.frac?.stream_status || null)}
          onClick={() => toggleColumn('frac')}
          isExpanded={expandedColumn === 'frac'}
          hasWarning={(viewer.streams.frac?.warnings?.filter(w => !w.toLowerCase().includes('idle'))?.length || 0) > 0 || (viewer.streams.frac?.failures?.length || 0) > 0}
          warningTooltip={[...(viewer.streams.frac?.failures || []), ...(viewer.streams.frac?.warnings?.filter(w => !w.toLowerCase().includes('idle')) || [])].join(', ')}
        />

        {/* Wireline */}
        <StatusCell
          text={wlStatus}
          color={getStatusColor(viewer.streams.wireline?.stream_status || null)}
          onClick={() => toggleColumn('wireline')}
          isExpanded={expandedColumn === 'wireline'}
          hasWarning={(viewer.streams.wireline?.warnings?.filter(w => !w.toLowerCase().includes('idle'))?.length || 0) > 0 || (viewer.streams.wireline?.failures?.length || 0) > 0}
          warningTooltip={[...(viewer.streams.wireline?.failures || []), ...(viewer.streams.wireline?.warnings?.filter(w => !w.toLowerCase().includes('idle')) || [])].join(', ')}
        />

        {/* Pumpdown */}
        <StatusCell
          text={pdStatus}
          color={getStatusColor(viewer.streams.pumpdown?.stream_status || null)}
          onClick={() => toggleColumn('pumpdown')}
          isExpanded={expandedColumn === 'pumpdown'}
          hasWarning={(viewer.streams.pumpdown?.warnings?.filter(w => !w.toLowerCase().includes('idle') && !w.toLowerCase().includes('manual pumpdown'))?.length || 0) > 0 || (viewer.streams.pumpdown?.failures?.length || 0) > 0}
          warningTooltip={[...(viewer.streams.pumpdown?.failures || []), ...(viewer.streams.pumpdown?.warnings?.filter(w => !w.toLowerCase().includes('idle') && !w.toLowerCase().includes('manual pumpdown')) || [])].join(', ')}
          hasVerification={viewer.streams.pumpdown?.source_app?.is_manual_pumpdown || false}
          verificationTooltip="Manual pumpdown - verify data flows through frac streambox"
        />

        {/* Stream Platform */}
        <StatusCell
          text={streamPlatform.text}
          color={streamPlatform.color}
          onClick={() => toggleColumn('stream_platform')}
          isExpanded={expandedColumn === 'stream_platform'}
        />

        {/* Stage */}
        <StatusCell
          text={stageStatus.text}
          color={stageStatus.color}
          onClick={() => toggleColumn('stage')}
          isExpanded={expandedColumn === 'stage'}
        />

        {/* Schedule - N/A for viewers */}
        <TableCell sx={{ py: 1 }}>
          <Typography variant="body2" sx={{ color: 'rgba(148, 163, 184, 0.4)', fontSize: '0.8rem' }}>
            -
          </Typography>
        </TableCell>
      </TableRow>

      <ViewerDetailRow viewer={viewer} expandedColumn={expandedColumn} colSpan={8} />
    </>
  );
};

// Loading skeleton
const LoadingSkeleton: React.FC = () => (
  <TableBody>
    {[1, 2, 3, 4].map((i) => (
      <TableRow key={i}>
        {[1, 2, 3, 4, 5, 6, 7, 8].map((j) => (
          <TableCell key={j} sx={{ py: 1.5 }}>
            <Skeleton variant="text" sx={{ bgcolor: 'rgba(148, 163, 184, 0.1)' }} />
          </TableCell>
        ))}
      </TableRow>
    ))}
  </TableBody>
);

// Main component
export const PipelineTable: React.FC<PipelineTableProps> = ({ result, isLoading }) => {
  if (!result && !isLoading) return null;

  return (
    <Box>
      {/* Config badge */}
      {result?.configuration && (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Chip
            label={result.configuration.config_type.toUpperCase()}
            size="small"
            sx={{
              backgroundColor: result.configuration.config_type === 'simulfrac' 
                ? 'rgba(168, 85, 247, 0.15)' 
                : 'rgba(59, 130, 246, 0.15)',
              color: result.configuration.config_type === 'simulfrac' ? '#a855f7' : '#3b82f6',
              fontWeight: 700,
              fontSize: '0.7rem',
            }}
          />
          {result.configuration.frac_fleet_name && (
            <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.6)' }}>
              Fleet: {result.configuration.frac_fleet_name}
            </Typography>
          )}
        </Box>
      )}

      {/* Stream Platform Pads Table */}
      {result?.stream_pad_check && result.stream_pad_check.pads.length > 0 && (
        <Box sx={{ mb: 3 }}>
          {/* Header */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1.5 }}>
            <Typography
              variant="subtitle2"
              sx={{
                color: '#f8fafc',
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                fontSize: '0.75rem',
              }}
            >
              Stream Platform Pads
            </Typography>
            <Chip
              label={result.stream_pad_check.check_status}
              size="small"
              sx={{
                backgroundColor: result.stream_pad_check.check_status === 'PASS' ? 'rgba(16, 185, 129, 0.15)' :
                  result.stream_pad_check.check_status === 'WARN' ? 'rgba(245, 158, 11, 0.15)' :
                  'rgba(239, 68, 68, 0.15)',
                color: result.stream_pad_check.check_status === 'PASS' ? '#10b981' :
                  result.stream_pad_check.check_status === 'WARN' ? '#f59e0b' : '#ef4444',
                fontWeight: 700,
                fontSize: '0.65rem',
              }}
            />
            <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>
              {result.stream_pad_check.total_pads_found} pads found ({result.stream_pad_check.well_pads_found} well, {result.stream_pad_check.viewer_pads_found} viewer)
            </Typography>
          </Box>
          
          {/* Failures and Warnings */}
          {(result.stream_pad_check.failures.length > 0 || result.stream_pad_check.warnings.length > 0) && (
            <Box sx={{ mb: 1.5 }}>
              {result.stream_pad_check.failures.map((f, i) => (
                <Typography key={`fail-${i}`} variant="caption" sx={{ color: '#ef4444', display: 'block', mb: 0.25 }}>
                  ⚠ {f}
                </Typography>
              ))}
              {result.stream_pad_check.warnings.map((w, i) => (
                <Typography key={`warn-${i}`} variant="caption" sx={{ color: '#f59e0b', display: 'block', mb: 0.25 }}>
                  ⚠ {w}
                </Typography>
              ))}
            </Box>
          )}

          {/* Pads Table */}
          <TableContainer
            component={Paper}
            sx={{
              backgroundColor: 'rgba(15, 23, 42, 0.6)',
              borderRadius: 2,
              border: '1px solid rgba(148, 163, 184, 0.1)',
              overflow: 'auto',
            }}
          >
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell
                    sx={{
                      backgroundColor: 'rgba(30, 41, 59, 0.95)',
                      color: 'rgba(148, 163, 184, 0.8)',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                      minWidth: 200,
                    }}
                  >
                    Pad Name
                  </TableCell>
                  <TableCell
                    sx={{
                      backgroundColor: 'rgba(30, 41, 59, 0.95)',
                      color: 'rgba(148, 163, 184, 0.8)',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                      minWidth: 70,
                    }}
                  >
                    Status
                  </TableCell>
                  <TableCell
                    sx={{
                      backgroundColor: 'rgba(30, 41, 59, 0.95)',
                      color: 'rgba(148, 163, 184, 0.8)',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                      minWidth: 150,
                    }}
                  >
                    Active Wells
                  </TableCell>
                  <TableCell
                    sx={{
                      backgroundColor: 'rgba(30, 41, 59, 0.95)',
                      color: 'rgba(148, 163, 184, 0.8)',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                      minWidth: 120,
                    }}
                  >
                    Company
                  </TableCell>
                  <TableCell
                    sx={{
                      backgroundColor: 'rgba(30, 41, 59, 0.95)',
                      color: 'rgba(148, 163, 184, 0.8)',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                      minWidth: 100,
                    }}
                  >
                    Frac Fleet
                  </TableCell>
                  <TableCell
                    sx={{
                      backgroundColor: 'rgba(30, 41, 59, 0.95)',
                      color: 'rgba(148, 163, 184, 0.8)',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                      minWidth: 90,
                    }}
                  >
                    Frac SB
                  </TableCell>
                  <TableCell
                    sx={{
                      backgroundColor: 'rgba(30, 41, 59, 0.95)',
                      color: 'rgba(148, 163, 184, 0.8)',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                      minWidth: 90,
                    }}
                  >
                    WL SB
                  </TableCell>
                  <TableCell
                    sx={{
                      backgroundColor: 'rgba(30, 41, 59, 0.95)',
                      color: 'rgba(148, 163, 184, 0.8)',
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                      minWidth: 90,
                    }}
                  >
                    PD SB
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {result.stream_pad_check.pads.map((pad) => (
                  <TableRow
                    key={pad.stream_pad_id}
                    sx={{
                      '&:hover': { backgroundColor: 'rgba(30, 41, 59, 0.4)' },
                      backgroundColor: pad.pad_type === 'viewer' ? 'rgba(168, 85, 247, 0.05)' : 'transparent',
                    }}
                  >
                    {/* Pad Name */}
                    <TableCell sx={{ py: 1.5 }}>
                      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                        <Box
                          sx={{
                            width: 8,
                            height: 8,
                            borderRadius: '50%',
                            backgroundColor: pad.pad_type === 'viewer' ? '#a855f7' : '#3b82f6',
                            flexShrink: 0,
                            mt: 0.5,
                          }}
                        />
                        <Box>
                          <Typography variant="body2" sx={{ color: '#f8fafc', fontWeight: 500, fontSize: '0.8rem' }}>
                            {pad.pad_name}
                          </Typography>
                          <Chip
                            label={pad.pad_type}
                            size="small"
                            sx={{
                              height: 16,
                              fontSize: '0.6rem',
                              mt: 0.5,
                              backgroundColor: pad.pad_type === 'viewer' ? 'rgba(168, 85, 247, 0.2)' : 'rgba(59, 130, 246, 0.2)',
                              color: pad.pad_type === 'viewer' ? '#c4b5fd' : '#93c5fd',
                            }}
                          />
                        </Box>
                      </Box>
                    </TableCell>

                    {/* Status */}
                    <TableCell sx={{ py: 1.5 }}>
                      <Chip
                        label={pad.status || 'unknown'}
                        size="small"
                        sx={{
                          height: 18,
                          fontSize: '0.65rem',
                          fontWeight: 600,
                          textTransform: 'capitalize',
                          backgroundColor: pad.status === 'active' ? 'rgba(16, 185, 129, 0.15)' :
                            pad.status === 'inactive' ? 'rgba(148, 163, 184, 0.15)' :
                            'rgba(245, 158, 11, 0.15)',
                          color: pad.status === 'active' ? '#10b981' :
                            pad.status === 'inactive' ? '#94a3b8' :
                            '#f59e0b',
                        }}
                      />
                    </TableCell>

                    {/* Active Wells */}
                    <TableCell sx={{ py: 1.5 }}>
                      {pad.active_wells.length > 0 ? (
                        <Box>
                          {pad.active_wells.map((wellName, idx) => (
                            <Typography
                              key={idx}
                              variant="caption"
                              sx={{ 
                                color: pad.wells_match_corva_pad === false ? '#f59e0b' : 'rgba(148, 163, 184, 0.8)', 
                                display: 'block', 
                                fontSize: '0.7rem', 
                                mb: 0.25 
                              }}
                            >
                              {wellName}
                            </Typography>
                          ))}
                          {pad.active_job_warning && (
                            <Typography
                              variant="caption"
                              sx={{ 
                                color: '#f59e0b', 
                                display: 'block', 
                                fontSize: '0.65rem', 
                                mt: 0.5,
                                fontStyle: 'italic',
                              }}
                            >
                              ⚠ {pad.active_job_warning}
                            </Typography>
                          )}
                        </Box>
                      ) : (
                        <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.4)', fontStyle: 'italic' }}>
                          No wells
                        </Typography>
                      )}
                    </TableCell>

                    {/* Company */}
                    <TableCell sx={{ py: 1.5 }}>
                      <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.8)', fontSize: '0.75rem' }}>
                        {pad.company_name || '-'}
                      </Typography>
                    </TableCell>

                    {/* Frac Fleet */}
                    <TableCell sx={{ py: 1.5 }}>
                      <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.8)', fontSize: '0.75rem' }}>
                        {pad.frac_fleet_name || '-'}
                      </Typography>
                    </TableCell>

                    {/* Frac SB */}
                    <TableCell sx={{ py: 1.5 }}>
                      <Typography
                        variant="caption"
                        sx={{
                          color: pad.frac_sb_id ? '#10b981' : 'rgba(148, 163, 184, 0.4)',
                          fontSize: '0.75rem',
                          fontWeight: pad.frac_sb_id ? 500 : 400,
                        }}
                      >
                        {pad.frac_sb_id || '-'}
                      </Typography>
                    </TableCell>

                    {/* WL SB */}
                    <TableCell sx={{ py: 1.5 }}>
                      <Typography
                        variant="caption"
                        sx={{
                          color: pad.wireline_sb_id ? '#10b981' : 'rgba(148, 163, 184, 0.4)',
                          fontSize: '0.75rem',
                          fontWeight: pad.wireline_sb_id ? 500 : 400,
                        }}
                      >
                        {pad.wireline_sb_id || '-'}
                      </Typography>
                    </TableCell>

                    {/* PD SB */}
                    <TableCell sx={{ py: 1.5 }}>
                      <Typography
                        variant="caption"
                        sx={{
                          color: pad.pumpdown_sb_id ? '#10b981' : 'rgba(148, 163, 184, 0.4)',
                          fontSize: '0.75rem',
                          fontWeight: pad.pumpdown_sb_id ? 500 : 400,
                        }}
                      >
                        {pad.pumpdown_sb_id || '-'}
                      </Typography>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}
      
      {/* No Stream Pads Found */}
      {result?.stream_pad_check && result.stream_pad_check.pads.length === 0 && (
        <Box
          sx={{
            mb: 2,
            p: 2,
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            borderRadius: 2,
            border: '1px solid rgba(239, 68, 68, 0.3)',
          }}
        >
          <Typography variant="body2" sx={{ color: '#ef4444' }}>
            ⚠ No Stream Platform pads found for "{result.pad_name}"
          </Typography>
          {result.stream_pad_check.failures.map((f, i) => (
            <Typography key={i} variant="caption" sx={{ color: '#ef4444', display: 'block', mt: 0.5 }}>
              {f}
            </Typography>
          ))}
        </Box>
      )}

      <TableContainer
        component={Paper}
        sx={{
          backgroundColor: 'rgba(15, 23, 42, 0.6)',
          borderRadius: 2,
          border: '1px solid rgba(148, 163, 184, 0.1)',
          maxHeight: 'calc(100vh - 300px)',
          overflow: 'auto',
        }}
      >
        <Table stickyHeader size="small">
          <TableHead>
            <TableRow>
              <TableCell
                sx={{
                  backgroundColor: 'rgba(30, 41, 59, 0.95)',
                  color: 'rgba(148, 163, 184, 0.8)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                  minWidth: 180,
                }}
              >
                Well Name
              </TableCell>
              <TableCell
                sx={{
                  backgroundColor: 'rgba(30, 41, 59, 0.95)',
                  color: 'rgba(148, 163, 184, 0.8)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                  minWidth: 80,
                }}
              >
                Type
              </TableCell>
              <TableCell
                sx={{
                  backgroundColor: 'rgba(30, 41, 59, 0.95)',
                  color: 'rgba(148, 163, 184, 0.8)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                  minWidth: 100,
                }}
              >
                Frac
              </TableCell>
              <TableCell
                sx={{
                  backgroundColor: 'rgba(30, 41, 59, 0.95)',
                  color: 'rgba(148, 163, 184, 0.8)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                  minWidth: 100,
                }}
              >
                Wireline
              </TableCell>
              <TableCell
                sx={{
                  backgroundColor: 'rgba(30, 41, 59, 0.95)',
                  color: 'rgba(148, 163, 184, 0.8)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                  minWidth: 100,
                }}
              >
                Pumpdown
              </TableCell>
              <TableCell
                sx={{
                  backgroundColor: 'rgba(30, 41, 59, 0.95)',
                  color: 'rgba(148, 163, 184, 0.8)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                  minWidth: 120,
                }}
              >
                Stream Link
              </TableCell>
              <TableCell
                sx={{
                  backgroundColor: 'rgba(30, 41, 59, 0.95)',
                  color: 'rgba(148, 163, 184, 0.8)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                  minWidth: 80,
                }}
              >
                Stage
              </TableCell>
              <TableCell
                sx={{
                  backgroundColor: 'rgba(30, 41, 59, 0.95)',
                  color: 'rgba(148, 163, 184, 0.8)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  borderBottom: '2px solid rgba(148, 163, 184, 0.2)',
                  minWidth: 80,
                }}
              >
                Sched
              </TableCell>
            </TableRow>
          </TableHead>

          {isLoading ? (
            <LoadingSkeleton />
          ) : (
            <TableBody>
              {/* Viewer rows first */}
              {result?.viewers.map((viewer) => (
                <ViewerRow key={viewer.viewer_asset_id} viewer={viewer} />
              ))}

              {/* Separator if there are viewers */}
              {result && result.viewers.length > 0 && result.wells.length > 0 && (
                <TableRow>
                  <TableCell
                    colSpan={8}
                    sx={{
                      py: 0.5,
                      backgroundColor: 'rgba(148, 163, 184, 0.05)',
                      borderBottom: '1px solid rgba(148, 163, 184, 0.1)',
                    }}
                  />
                </TableRow>
              )}

              {/* Well rows */}
              {result?.wells.map((well) => (
                <WellRow key={well.corva_well_asset_id} well={well} />
              ))}
            </TableBody>
          )}
        </Table>
      </TableContainer>
    </Box>
  );
};

export default PipelineTable;
