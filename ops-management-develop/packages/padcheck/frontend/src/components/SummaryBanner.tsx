import React, { useState, useMemo } from 'react';
import { Box, Typography, Paper, Collapse, IconButton, Divider } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import type { CheckStatus, PadResult } from '../types';

interface SummaryBannerProps {
  result: PadResult | null;
  isVisible: boolean;
}

interface IssueItem {
  type: 'failure' | 'warning';
  location: string;
  message: string;
}

const statusConfig: Record<CheckStatus, {
  icon: React.ReactNode;
  title: string;
  description: string;
  bgColor: string;
  borderColor: string;
  iconColor: string;
}> = {
  PASS: {
    icon: <CheckCircleIcon sx={{ fontSize: 32 }} />,
    title: 'Pipeline Healthy',
    description: 'All checks passed. The completions data pipeline is correctly wired.',
    bgColor: 'rgba(16, 185, 129, 0.1)',
    borderColor: 'rgba(16, 185, 129, 0.4)',
    iconColor: '#10b981',
  },
  WARN: {
    icon: <WarningIcon sx={{ fontSize: 32 }} />,
    title: 'Pipeline Has Warnings',
    description: 'Some non-blocking issues were found. Click to see details.',
    bgColor: 'rgba(245, 158, 11, 0.1)',
    borderColor: 'rgba(245, 158, 11, 0.4)',
    iconColor: '#f59e0b',
  },
  FAIL: {
    icon: <ErrorIcon sx={{ fontSize: 32 }} />,
    title: 'Pipeline Issues Detected',
    description: 'Critical issues found. Click to see details.',
    bgColor: 'rgba(239, 68, 68, 0.1)',
    borderColor: 'rgba(239, 68, 68, 0.4)',
    iconColor: '#ef4444',
  },
};

/**
 * Collect all issues from the result with clear location context
 */
function collectAllIssues(result: PadResult): IssueItem[] {
  const issues: IssueItem[] = [];

  // Collect viewer issues
  if (result.viewers) {
    for (const viewer of result.viewers) {
      const viewerName = viewer.viewer_name || `Viewer ${viewer.viewer_asset_id}`;
      
      // Viewer-level failures
      for (const failure of viewer.failures || []) {
        issues.push({
          type: 'failure',
          location: `Viewer: ${viewerName}`,
          message: failure,
        });
      }
      
      // Viewer-level warnings
      for (const warning of viewer.warnings || []) {
        issues.push({
          type: 'warning',
          location: `Viewer: ${viewerName}`,
          message: warning,
        });
      }

      // Viewer stream issues
      if (viewer.streams) {
        for (const [streamType, stream] of Object.entries(viewer.streams)) {
          if (stream) {
            for (const failure of stream.failures || []) {
              issues.push({
                type: 'failure',
                location: `Viewer: ${viewerName} → ${streamType.toUpperCase()} Stream`,
                message: failure,
              });
            }
            for (const warning of stream.warnings || []) {
              issues.push({
                type: 'warning',
                location: `Viewer: ${viewerName} → ${streamType.toUpperCase()} Stream`,
                message: warning,
              });
            }
          }
        }
      }
    }
  }

  // Collect well issues
  for (const well of result.wells || []) {
    const wellName = well.well_name || `Well ${well.corva_well_asset_id}`;
    
    // Well-level failures
    for (const failure of well.failures || []) {
      // Skip duplicates that are already captured at stream level
      if (!failure.includes('stream not found') && !failure.includes('Source App')) {
        issues.push({
          type: 'failure',
          location: `Well: ${wellName}`,
          message: failure,
        });
      }
    }
    
    // Well-level warnings
    for (const warning of well.warnings || []) {
      // Skip duplicates that are already captured at stream level
      if (!warning.includes('stream is idle') && !warning.includes('No active stage')) {
        issues.push({
          type: 'warning',
          location: `Well: ${wellName}`,
          message: warning,
        });
      }
    }

    // Well stream issues
    if (well.corva_streams) {
      for (const [streamType, stream] of Object.entries(well.corva_streams)) {
        if (stream) {
          for (const failure of stream.failures || []) {
            issues.push({
              type: 'failure',
              location: `Well: ${wellName} → ${streamType.toUpperCase()} Stream`,
              message: failure,
            });
          }
          for (const warning of stream.warnings || []) {
            issues.push({
              type: 'warning',
              location: `Well: ${wellName} → ${streamType.toUpperCase()} Stream`,
              message: warning,
            });
          }
        }
      }
    }

    // Stream platform issues
    if (well.stream_platform_check) {
      for (const failure of well.stream_platform_check.failures || []) {
        issues.push({
          type: 'failure',
          location: `Well: ${wellName} → Stream Platform`,
          message: failure,
        });
      }
      for (const warning of well.stream_platform_check.warnings || []) {
        issues.push({
          type: 'warning',
          location: `Well: ${wellName} → Stream Platform`,
          message: warning,
        });
      }
    }

    // Stage status issues
    if (well.stage_status) {
      for (const failure of well.stage_status.failures || []) {
        issues.push({
          type: 'failure',
          location: `Well: ${wellName} → Stages`,
          message: failure,
        });
      }
      for (const warning of well.stage_status.warnings || []) {
        issues.push({
          type: 'warning',
          location: `Well: ${wellName} → Stages`,
          message: warning,
        });
      }
    }
  }

  // Collect Stream Platform pad issues
  if (result.stream_pad_check) {
    for (const failure of result.stream_pad_check.failures || []) {
      issues.push({
        type: 'failure',
        location: 'Stream Platform Pads',
        message: failure,
      });
    }
    for (const warning of result.stream_pad_check.warnings || []) {
      issues.push({
        type: 'warning',
        location: 'Stream Platform Pads',
        message: warning,
      });
    }

    // Individual pad issues
    for (const pad of result.stream_pad_check.pads || []) {
      if (pad.active_job_warning) {
        issues.push({
          type: 'warning',
          location: `Stream Pad: ${pad.pad_name}`,
          message: pad.active_job_warning,
        });
      }
    }
  }

  // Remove duplicates and filter out noisy warnings
  const seen = new Set<string>();
  const noisyPatterns = [
    /idle/i,                          // Idle status is normal
    /not actively streaming/i,        // Same as idle
    /no active stage/i,               // Normal for inactive pads
    /no stages found.*may not be active/i,  // Normal for new pads
    /pumpdown stream not configured/i,  // Pumpdown is optional
    /pumpdown stream not found/i,       // Pumpdown is optional
    /manual pumpdown/i,               // Manual pumpdown is verification, not warning
  ];
  
  return issues.filter(issue => {
    // Skip noisy warnings (but keep failures)
    if (issue.type === 'warning') {
      for (const pattern of noisyPatterns) {
        if (pattern.test(issue.message)) {
          return false;
        }
      }
    }
    
    // Remove duplicates
    const key = `${issue.type}:${issue.location}:${issue.message}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/**
 * Summary banner showing overall pipeline check status with expandable issue list
 */
export const SummaryBanner: React.FC<SummaryBannerProps> = ({ result, isVisible }) => {
  const [expanded, setExpanded] = useState(false);
  
  const allIssues = useMemo(() => {
    if (!result) return [];
    return collectAllIssues(result);
  }, [result]);

  const failures = allIssues.filter(i => i.type === 'failure');
  const warnings = allIssues.filter(i => i.type === 'warning');
  const hasIssues = failures.length > 0 || warnings.length > 0;

  if (!result) return null;
  
  const config = statusConfig[result.overall_status];
  
  return (
    <Collapse in={isVisible}>
      <Paper
        elevation={0}
        sx={{
          marginBottom: 4,
          backgroundColor: config.bgColor,
          border: `1px solid ${config.borderColor}`,
          borderRadius: 2,
          overflow: 'hidden',
        }}
      >
        {/* Main Banner - Clickable */}
        <Box
          onClick={() => hasIssues && setExpanded(!expanded)}
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 3,
            padding: 3,
            cursor: hasIssues ? 'pointer' : 'default',
            '&:hover': hasIssues ? {
              backgroundColor: 'rgba(255, 255, 255, 0.03)',
            } : {},
          }}
        >
          {/* Status Icon */}
          <Box
            sx={{
              color: config.iconColor,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {config.icon}
          </Box>
          
          {/* Status Text */}
          <Box sx={{ flex: 1 }}>
            <Typography
              variant="h6"
              sx={{
                color: '#f8fafc',
                fontWeight: 600,
                marginBottom: 0.5,
              }}
            >
              {config.title}
            </Typography>
            <Typography
              variant="body2"
              sx={{
                color: 'rgba(148, 163, 184, 0.9)',
              }}
            >
              {config.description}
            </Typography>
          </Box>
          
          {/* Stats */}
          <Box
            sx={{
              display: 'flex',
              gap: 3,
              paddingLeft: 3,
              borderLeft: '1px solid rgba(148, 163, 184, 0.2)',
            }}
          >
            <Box sx={{ textAlign: 'center' }}>
              <Typography
                variant="h5"
                sx={{
                  color: '#f8fafc',
                  fontWeight: 700,
                }}
              >
                {result.wells.length}
              </Typography>
              <Typography
                variant="caption"
                sx={{
                  color: 'rgba(148, 163, 184, 0.7)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                }}
              >
                Wells
              </Typography>
            </Box>
            
            {failures.length > 0 && (
              <Box sx={{ textAlign: 'center' }}>
                <Typography
                  variant="h5"
                  sx={{
                    color: '#ef4444',
                    fontWeight: 700,
                  }}
                >
                  {failures.length}
                </Typography>
                <Typography
                  variant="caption"
                  sx={{
                    color: 'rgba(148, 163, 184, 0.7)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                  }}
                >
                  Failures
                </Typography>
              </Box>
            )}
            
            {warnings.length > 0 && (
              <Box sx={{ textAlign: 'center' }}>
                <Typography
                  variant="h5"
                  sx={{
                    color: '#f59e0b',
                    fontWeight: 700,
                  }}
                >
                  {warnings.length}
                </Typography>
                <Typography
                  variant="caption"
                  sx={{
                    color: 'rgba(148, 163, 184, 0.7)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                  }}
                >
                  Warnings
                </Typography>
              </Box>
            )}
          </Box>
          
          {/* Timestamp */}
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 0.5,
              color: 'rgba(148, 163, 184, 0.6)',
            }}
          >
            <AccessTimeIcon sx={{ fontSize: 14 }} />
            <Typography variant="caption">
              {new Date(result.checked_at).toLocaleTimeString()}
            </Typography>
          </Box>

          {/* Expand/Collapse Button */}
          {hasIssues && (
            <IconButton
              size="small"
              sx={{ color: 'rgba(148, 163, 184, 0.7)' }}
            >
              {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </IconButton>
          )}
        </Box>

        {/* Expandable Issues List */}
        <Collapse in={expanded}>
          <Divider sx={{ borderColor: 'rgba(148, 163, 184, 0.15)' }} />
          <Box sx={{ p: 2, maxHeight: 400, overflow: 'auto' }}>
            {/* Failures Section */}
            {failures.length > 0 && (
              <Box sx={{ mb: warnings.length > 0 ? 2 : 0 }}>
                <Typography
                  variant="subtitle2"
                  sx={{
                    color: '#ef4444',
                    fontWeight: 600,
                    mb: 1,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 0.5,
                  }}
                >
                  <ErrorIcon sx={{ fontSize: 16 }} /> Failures ({failures.length})
                </Typography>
                {failures.map((issue, idx) => (
                  <Box
                    key={`fail-${idx}`}
                    sx={{
                      display: 'flex',
                      gap: 1,
                      mb: 1,
                      p: 1.5,
                      backgroundColor: 'rgba(239, 68, 68, 0.1)',
                      borderRadius: 1,
                      borderLeft: '3px solid #ef4444',
                    }}
                  >
                    <Box sx={{ flex: 1 }}>
                      <Typography
                        variant="caption"
                        sx={{
                          color: '#ef4444',
                          fontWeight: 600,
                          display: 'block',
                          mb: 0.5,
                        }}
                      >
                        {issue.location}
                      </Typography>
                      <Typography
                        variant="body2"
                        sx={{ color: 'rgba(248, 250, 252, 0.9)', fontSize: '0.8rem' }}
                      >
                        {issue.message}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            )}

            {/* Warnings Section */}
            {warnings.length > 0 && (
              <Box>
                <Typography
                  variant="subtitle2"
                  sx={{
                    color: '#f59e0b',
                    fontWeight: 600,
                    mb: 1,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 0.5,
                  }}
                >
                  <WarningIcon sx={{ fontSize: 16 }} /> Warnings ({warnings.length})
                </Typography>
                {warnings.map((issue, idx) => (
                  <Box
                    key={`warn-${idx}`}
                    sx={{
                      display: 'flex',
                      gap: 1,
                      mb: 1,
                      p: 1.5,
                      backgroundColor: 'rgba(245, 158, 11, 0.1)',
                      borderRadius: 1,
                      borderLeft: '3px solid #f59e0b',
                    }}
                  >
                    <Box sx={{ flex: 1 }}>
                      <Typography
                        variant="caption"
                        sx={{
                          color: '#f59e0b',
                          fontWeight: 600,
                          display: 'block',
                          mb: 0.5,
                        }}
                      >
                        {issue.location}
                      </Typography>
                      <Typography
                        variant="body2"
                        sx={{ color: 'rgba(248, 250, 252, 0.9)', fontSize: '0.8rem' }}
                      >
                        {issue.message}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            )}
          </Box>
        </Collapse>
      </Paper>
    </Collapse>
  );
};

export default SummaryBanner;
