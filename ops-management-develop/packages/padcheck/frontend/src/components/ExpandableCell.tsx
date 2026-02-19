import React from 'react';
import { Box, Collapse, Typography, Chip, Stack } from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';

interface ExpandableCellProps {
  /** Main display content */
  mainContent: React.ReactNode;
  /** Expanded detail content */
  detailContent: React.ReactNode;
  /** Whether this cell is currently expanded */
  isExpanded: boolean;
  /** Callback when cell is clicked */
  onToggle: () => void;
  /** Optional status color for the dot indicator */
  statusColor?: 'green' | 'yellow' | 'red' | 'gray';
  /** Optional status text */
  statusText?: string;
}

const statusColors = {
  green: '#10b981',
  yellow: '#f59e0b',
  red: '#ef4444',
  gray: 'rgba(148, 163, 184, 0.5)',
};

export const ExpandableCell: React.FC<ExpandableCellProps> = ({
  mainContent,
  detailContent: _detailContent,
  isExpanded,
  onToggle,
  statusColor,
  statusText,
}) => {
  // Note: detailContent is part of the interface but rendered by parent via DetailPanel
  void _detailContent;
  return (
    <Box
      onClick={onToggle}
      sx={{
        cursor: 'pointer',
        '&:hover': {
          backgroundColor: 'rgba(59, 130, 246, 0.05)',
        },
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        {statusColor && (
          <Box
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: statusColors[statusColor],
              flexShrink: 0,
            }}
          />
        )}
        {statusText ? (
          <Typography
            variant="body2"
            sx={{
              color: statusColor ? statusColors[statusColor] : '#f8fafc',
              fontWeight: 500,
              fontSize: '0.8rem',
            }}
          >
            {statusText}
          </Typography>
        ) : (
          mainContent
        )}
        {isExpanded ? (
          <KeyboardArrowUpIcon sx={{ fontSize: 16, color: 'rgba(148, 163, 184, 0.5)', ml: 'auto' }} />
        ) : (
          <KeyboardArrowDownIcon sx={{ fontSize: 16, color: 'rgba(148, 163, 184, 0.5)', ml: 'auto' }} />
        )}
      </Box>
    </Box>
  );
};

/**
 * Detail panel shown when a row is expanded
 */
interface DetailPanelProps {
  children: React.ReactNode;
  colSpan: number;
  isExpanded: boolean;
}

export const DetailPanel: React.FC<DetailPanelProps> = ({ children, colSpan, isExpanded }) => {
  return (
    <tr>
      <td colSpan={colSpan} style={{ padding: 0, border: 'none' }}>
        <Collapse in={isExpanded} timeout="auto" unmountOnExit>
          <Box
            sx={{
              backgroundColor: 'rgba(30, 41, 59, 0.6)',
              borderLeft: '3px solid rgba(59, 130, 246, 0.5)',
              p: 2,
              m: 1,
              borderRadius: 1,
            }}
          >
            {children}
          </Box>
        </Collapse>
      </td>
    </tr>
  );
};

/**
 * Helper component for detail sections
 */
interface DetailSectionProps {
  title: string;
  children: React.ReactNode;
}

export const DetailSection: React.FC<DetailSectionProps> = ({ title, children }) => {
  return (
    <Box sx={{ mb: 2, '&:last-child': { mb: 0 } }}>
      <Typography
        variant="caption"
        sx={{
          color: 'rgba(148, 163, 184, 0.6)',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          fontSize: '0.65rem',
          fontWeight: 600,
          display: 'block',
          mb: 0.5,
        }}
      >
        {title}
      </Typography>
      {children}
    </Box>
  );
};

/**
 * Helper component for key-value pairs in details
 */
interface DetailItemProps {
  label: string;
  value: React.ReactNode;
}

export const DetailItem: React.FC<DetailItemProps> = ({ label, value }) => {
  return (
    <Box sx={{ display: 'flex', gap: 1, alignItems: 'baseline', mb: 0.25 }}>
      <Typography
        variant="caption"
        sx={{ color: 'rgba(148, 163, 184, 0.5)', minWidth: 100 }}
      >
        {label}:
      </Typography>
      <Typography variant="caption" sx={{ color: '#f8fafc' }}>
        {value || '-'}
      </Typography>
    </Box>
  );
};

/**
 * Helper component for app chips in stream details
 */
interface AppChipListProps {
  apps: string[];
}

export const AppChipList: React.FC<AppChipListProps> = ({ apps }) => {
  if (!apps || apps.length === 0) {
    return <Typography variant="caption" sx={{ color: 'rgba(148, 163, 184, 0.5)' }}>None</Typography>;
  }

  return (
    <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap>
      {apps.map((app, index) => (
        <Chip
          key={index}
          label={app}
          size="small"
          sx={{
            height: 20,
            fontSize: '0.65rem',
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            color: '#60a5fa',
            '& .MuiChip-label': { px: 1 },
          }}
        />
      ))}
    </Stack>
  );
};

export default ExpandableCell;
