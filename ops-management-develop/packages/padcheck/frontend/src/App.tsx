import React, { useState, useCallback } from 'react';
import { ThemeProvider, createTheme, CssBaseline, Box, Container, Alert } from '@mui/material';
import { useAssetContext } from './hooks/useAssetContext';
import { runPipelineCheck, PipelineCheckerError } from './api/pipelineChecker';
import {
  Header,
  EmptyState,
  RunButton,
  SummaryBanner,
  WellResultsTable,
  ViewerCard,
  ViewToggle,
  PipelineTable,
} from './components';
import type { ViewMode } from './components';
import type { PadResult } from './types';

// Dark theme optimized for Corva dashboard
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3b82f6',
    },
    secondary: {
      main: '#10b981',
    },
    background: {
      default: '#0f172a',
      paper: '#1e293b',
    },
    text: {
      primary: '#f8fafc',
      secondary: '#94a3b8',
    },
  },
  typography: {
    fontFamily: '"IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    h4: {
      fontWeight: 700,
      letterSpacing: '-0.02em',
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#0f172a',
          backgroundImage: `
            radial-gradient(at 27% 37%, hsla(215, 98%, 61%, 0.08) 0px, transparent 50%),
            radial-gradient(at 97% 21%, hsla(256, 98%, 72%, 0.06) 0px, transparent 50%),
            radial-gradient(at 52% 99%, hsla(354, 98%, 61%, 0.05) 0px, transparent 50%),
            radial-gradient(at 10% 29%, hsla(170, 98%, 61%, 0.05) 0px, transparent 50%)
          `,
          minHeight: '100vh',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

/**
 * Pipeline Checker App
 * 
 * Validates completions data pipeline connectivity for a selected pad/well.
 */
const App: React.FC = () => {
  const { context, hasPadContext } = useAssetContext();
  
  // State
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState<string | null>(null);
  const [result, setResult] = useState<PadResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('table'); // Default to table view
  
  // Run pipeline check
  const handleRunCheck = useCallback(async () => {
    if (!context.padId) return;
    
    setIsLoading(true);
    setError(null);
    setLoadingStep('Doing everything all at once...');
    
    try {
      
      const checkResult = await runPipelineCheck(
        context.padId,
        context.completionWellAssetId ?? undefined
      );
      
      setResult(checkResult);
    } catch (err) {
      console.error('Pipeline check failed:', err);
      
      if (err instanceof PipelineCheckerError) {
        setError(err.message);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred while running the pipeline check.');
      }
    } finally {
      setIsLoading(false);
      setLoadingStep(null);
    }
  }, [context.padId, context.completionWellAssetId]);
  
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          padding: { xs: 2, sm: 3, md: 4 },
        }}
      >
        <Container maxWidth="lg">
          {/* Header with context display */}
          <Header context={context} />
          
          {/* Main content */}
          {!hasPadContext ? (
            // Empty state when no pad selected
            <EmptyState />
          ) : (
            <>
              {/* Run button */}
              <RunButton
                onClick={handleRunCheck}
                isLoading={isLoading}
                disabled={!hasPadContext}
                hasResults={result !== null}
                loadingStep={loadingStep}
              />
              
              {/* Error display */}
              {error && (
                <Alert
                  severity="error"
                  sx={{
                    marginBottom: 3,
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    border: '1px solid rgba(239, 68, 68, 0.3)',
                    '& .MuiAlert-icon': {
                      color: '#ef4444',
                    },
                  }}
                  onClose={() => setError(null)}
                >
                  {error}
                </Alert>
              )}
              
              {/* Summary banner */}
              <SummaryBanner
                result={result}
                isVisible={result !== null && !isLoading}
              />
              
              {/* View toggle - only show when we have results */}
              {(result || isLoading) && (
                <ViewToggle value={viewMode} onChange={setViewMode} />
              )}
              
              {/* Conditional view rendering */}
              {viewMode === 'table' ? (
                /* Table View - compact with expandable cells */
                <PipelineTable result={result} isLoading={isLoading} />
              ) : (
                /* Card View - existing detailed cards */
                <>
                  {/* Viewer cards */}
                  {result?.viewers && result.viewers.length > 0 && (
                    result.viewers.map((viewer, index) => (
                      <ViewerCard key={viewer.viewer_asset_id || index} viewer={viewer} />
                    ))
                  )}
                  
                  {/* Well results table */}
                  <WellResultsTable
                    result={result}
                    isLoading={isLoading}
                  />
                </>
              )}
              
              {/* Context info for debugging (only in dev) */}
              {import.meta.env.DEV && (
                <Box
                  sx={{
                    marginTop: 4,
                    padding: 2,
                    backgroundColor: 'rgba(30, 41, 59, 0.5)',
                    borderRadius: 1,
                    fontSize: '0.75rem',
                    fontFamily: 'monospace',
                    color: 'rgba(148, 163, 184, 0.6)',
                  }}
                >
                  <div>Debug Context:</div>
                  <pre>{JSON.stringify(context, null, 2)}</pre>
                </Box>
              )}
            </>
          )}
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default App;
