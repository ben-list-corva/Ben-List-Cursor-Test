import type {
  PipelineCheckRequest,
  PipelineCheckResponse,
  PadResult,
} from '../types';

/**
 * API client for Pipeline Checker backend
 * 
 * In production, this calls the Corva Dev Center backend Lambda.
 * For local development, it can proxy through Vite to a local server.
 */

// API endpoint configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

/**
 * Custom error class for API errors
 */
export class PipelineCheckerError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public details?: unknown
  ) {
    super(message);
    this.name = 'PipelineCheckerError';
  }
}

/**
 * Make an authenticated request to the backend
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  // In Dev Center, the auth is handled automatically
  // If running locally, you may need to add CORVA_API_KEY
  const apiKey = import.meta.env.VITE_CORVA_API_KEY;
  if (apiKey) {
    defaultHeaders['Authorization'] = `API ${apiKey}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    let errorMessage = `API request failed: ${response.status} ${response.statusText}`;
    let errorDetails: unknown = null;
    
    try {
      const errorData = await response.json();
      if (errorData.error) {
        errorMessage = errorData.error;
      }
      errorDetails = errorData;
    } catch {
      // Ignore JSON parse errors
    }
    
    throw new PipelineCheckerError(errorMessage, response.status, errorDetails);
  }
  
  return response.json();
}

/**
 * Run pipeline checks for a pad (and optionally a specific well)
 */
export async function runPipelineCheck(
  padId: number,
  wellAssetId?: number
): Promise<PadResult> {
  const request: PipelineCheckRequest = {
    pad_id: padId,
  };
  
  if (wellAssetId) {
    request.well_asset_id = wellAssetId;
  }
  
  const response = await apiRequest<PipelineCheckResponse>(
    '/pipeline-check',
    {
      method: 'POST',
      body: JSON.stringify(request),
    }
  );
  
  if (!response.success || !response.data) {
    throw new PipelineCheckerError(
      response.error || 'Pipeline check failed with unknown error'
    );
  }
  
  return response.data;
}

/**
 * Get pad information (for display purposes)
 */
export async function getPadInfo(padId: number): Promise<{
  id: number;
  name: string;
  well_count: number;
}> {
  return apiRequest(`/pads/${padId}`);
}

/**
 * Health check endpoint
 */
export async function healthCheck(): Promise<{ status: string; timestamp: string }> {
  return apiRequest('/health');
}

export default {
  runPipelineCheck,
  getPadInfo,
  healthCheck,
};
