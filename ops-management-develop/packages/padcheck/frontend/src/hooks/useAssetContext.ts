import { useState, useEffect, useCallback } from 'react';
import type { AssetContext } from '../types';

/**
 * Hook to retrieve asset chip context from Corva Dev Center runtime.
 * 
 * Priority:
 * 1. Dev Center runtime context (window.__CORVA_CONTEXT__)
 * 2. URL query parameters (fallback)
 * 
 * Expected context fields:
 * - padId: Corva pad asset ID
 * - padName: Pad name for display
 * - completionWellAssetId: Optional specific well selection
 * - wellName: Well name for display
 * - fracFleetId: Optional frac fleet ID (informational only)
 */

// Type for Dev Center runtime context
interface CorvaRuntimeContext {
  asset?: {
    id?: number;
    name?: string;
    type?: string;
  };
  pad?: {
    id?: number;
    name?: string;
  };
  well?: {
    id?: number;
    name?: string;
    assetId?: number;
  };
  completionWell?: {
    assetId?: number;
    name?: string;
  };
  fracFleet?: {
    id?: number;
    name?: string;
  };
  // Additional context fields that may be available
  [key: string]: unknown;
}

// Extend window to include Corva context
declare global {
  interface Window {
    __CORVA_CONTEXT__?: CorvaRuntimeContext;
    // Alternative context injection methods
    corvaContext?: CorvaRuntimeContext;
  }
}

/**
 * Parse URL query parameters for asset context
 */
function parseQueryParams(): Partial<AssetContext> {
  if (typeof window === 'undefined') return {};
  
  const params = new URLSearchParams(window.location.search);
  
  const padId = params.get('padId') || params.get('pad_id');
  const padName = params.get('padName') || params.get('pad_name');
  const wellAssetId = params.get('completionWellAssetId') || params.get('well_asset_id') || params.get('wellId');
  const wellName = params.get('wellName') || params.get('well_name');
  const fracFleetId = params.get('fracFleetId') || params.get('frac_fleet_id');
  
  return {
    padId: padId ? parseInt(padId, 10) : null,
    padName: padName || null,
    completionWellAssetId: wellAssetId ? parseInt(wellAssetId, 10) : null,
    wellName: wellName || null,
    fracFleetId: fracFleetId ? parseInt(fracFleetId, 10) : null,
  };
}

/**
 * Extract asset context from Dev Center runtime
 */
function extractRuntimeContext(): Partial<AssetContext> {
  if (typeof window === 'undefined') return {};
  
  // Try different possible context injection points
  const runtimeContext = window.__CORVA_CONTEXT__ || window.corvaContext;
  
  if (!runtimeContext) return {};
  
  // Extract pad context
  let padId: number | null = null;
  let padName: string | null = null;
  
  if (runtimeContext.pad) {
    padId = runtimeContext.pad.id ?? null;
    padName = runtimeContext.pad.name ?? null;
  } else if (runtimeContext.asset?.type === 'pad') {
    padId = runtimeContext.asset.id ?? null;
    padName = runtimeContext.asset.name ?? null;
  }
  
  // Extract well context
  let completionWellAssetId: number | null = null;
  let wellName: string | null = null;
  
  if (runtimeContext.completionWell) {
    completionWellAssetId = runtimeContext.completionWell.assetId ?? null;
    wellName = runtimeContext.completionWell.name ?? null;
  } else if (runtimeContext.well) {
    completionWellAssetId = runtimeContext.well.assetId ?? runtimeContext.well.id ?? null;
    wellName = runtimeContext.well.name ?? null;
  }
  
  // Extract frac fleet context (informational)
  let fracFleetId: number | null = null;
  if (runtimeContext.fracFleet) {
    fracFleetId = runtimeContext.fracFleet.id ?? null;
  }
  
  return {
    padId,
    padName,
    completionWellAssetId,
    wellName,
    fracFleetId,
  };
}

/**
 * Merge context sources with priority: runtime > query params
 */
function mergeContexts(
  runtime: Partial<AssetContext>,
  queryParams: Partial<AssetContext>
): AssetContext {
  return {
    padId: runtime.padId ?? queryParams.padId ?? null,
    padName: runtime.padName ?? queryParams.padName ?? null,
    completionWellAssetId: runtime.completionWellAssetId ?? queryParams.completionWellAssetId ?? null,
    wellName: runtime.wellName ?? queryParams.wellName ?? null,
    fracFleetId: runtime.fracFleetId ?? queryParams.fracFleetId ?? null,
  };
}

/**
 * Custom hook to access Corva asset chip context
 */
export function useAssetContext(): {
  context: AssetContext;
  isContextAvailable: boolean;
  hasPadContext: boolean;
  hasWellContext: boolean;
  refresh: () => void;
} {
  const [context, setContext] = useState<AssetContext>({
    padId: null,
    padName: null,
    completionWellAssetId: null,
    wellName: null,
    fracFleetId: null,
  });
  
  const loadContext = useCallback(() => {
    const runtimeContext = extractRuntimeContext();
    const queryParams = parseQueryParams();
    const merged = mergeContexts(runtimeContext, queryParams);
    setContext(merged);
  }, []);
  
  useEffect(() => {
    // Initial load
    loadContext();
    
    // Listen for context updates (Dev Center may emit events)
    const handleContextUpdate = () => {
      loadContext();
    };
    
    // Listen for custom Corva context events
    window.addEventListener('corva-context-update', handleContextUpdate);
    
    // Also listen for URL changes (in case of navigation)
    window.addEventListener('popstate', handleContextUpdate);
    
    return () => {
      window.removeEventListener('corva-context-update', handleContextUpdate);
      window.removeEventListener('popstate', handleContextUpdate);
    };
  }, [loadContext]);
  
  const isContextAvailable = context.padId !== null;
  const hasPadContext = context.padId !== null;
  const hasWellContext = context.completionWellAssetId !== null;
  
  return {
    context,
    isContextAvailable,
    hasPadContext,
    hasWellContext,
    refresh: loadContext,
  };
}

export default useAssetContext;
