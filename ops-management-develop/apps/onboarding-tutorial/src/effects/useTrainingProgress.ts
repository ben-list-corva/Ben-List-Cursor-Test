/**
 * useTrainingProgress Hook
 * 
 * Manages user training progress using Corva datasets
 */

import { useState, useEffect, useCallback } from 'react';
import { corvaDataAPI } from '@corva/ui/clients';
import type { TrainingProgressRecord } from '../types';

const DATASET_PROVIDER = 'corva';
const DATASET_NAME = 'training_progress';

interface UseTrainingProgressProps {
  userId: number | undefined;
}

interface UseTrainingProgressResult {
  progress: TrainingProgressRecord[];
  loading: boolean;
  error: string | null;
  fetchProgress: () => Promise<void>;
  saveProgress: (record: Omit<TrainingProgressRecord, '_id' | 'timestamp'>) => Promise<void>;
  getModuleProgress: (moduleSlug: string) => TrainingProgressRecord[];
  getSectionProgress: (moduleSlug: string, sectionId: string) => TrainingProgressRecord | undefined;
  isModuleComplete: (moduleSlug: string, totalSections: number) => boolean;
}

export function useTrainingProgress({ userId }: UseTrainingProgressProps): UseTrainingProgressResult {
  const [progress, setProgress] = useState<TrainingProgressRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch progress from Corva dataset
  const fetchProgress = useCallback(async () => {
    if (!userId) {
      setProgress([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await corvaDataAPI.get<TrainingProgressRecord[]>(
        `/api/v1/data/${DATASET_PROVIDER}/${DATASET_NAME}/`,
        {
          query: JSON.stringify({ user_id: userId }),
          sort: JSON.stringify({ timestamp: -1 }),
          limit: 1000,
        }
      );

      setProgress(response || []);
    } catch (err) {
      console.error('Error fetching training progress:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch progress');
      setProgress([]);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Save progress to Corva dataset
  const saveProgress = useCallback(async (
    record: Omit<TrainingProgressRecord, '_id' | 'timestamp'>
  ) => {
    if (!userId) {
      throw new Error('User ID is required to save progress');
    }

    try {
      const progressRecord: TrainingProgressRecord = {
        ...record,
        user_id: userId,
        timestamp: Math.floor(Date.now() / 1000), // Unix timestamp in seconds
        completed_at: new Date().toISOString(),
      };

      await corvaDataAPI.post(
        `/api/v1/data/${DATASET_PROVIDER}/${DATASET_NAME}/`,
        progressRecord
      );

      // Refresh progress after saving
      await fetchProgress();
    } catch (err) {
      console.error('Error saving training progress:', err);
      throw err;
    }
  }, [userId, fetchProgress]);

  // Get progress for a specific module
  const getModuleProgress = useCallback((moduleSlug: string): TrainingProgressRecord[] => {
    return progress.filter(p => p.module_slug === moduleSlug);
  }, [progress]);

  // Get progress for a specific section
  const getSectionProgress = useCallback((
    moduleSlug: string,
    sectionId: string
  ): TrainingProgressRecord | undefined => {
    return progress.find(
      p => p.module_slug === moduleSlug && p.section_id === sectionId
    );
  }, [progress]);

  // Check if a module is complete
  const isModuleComplete = useCallback((
    moduleSlug: string,
    totalSections: number
  ): boolean => {
    const moduleProgress = getModuleProgress(moduleSlug);
    const completedSections = moduleProgress.filter(p => p.completed).length;
    return completedSections >= totalSections;
  }, [getModuleProgress]);

  // Fetch progress on mount and when userId changes
  useEffect(() => {
    fetchProgress();
  }, [fetchProgress]);

  return {
    progress,
    loading,
    error,
    fetchProgress,
    saveProgress,
    getModuleProgress,
    getSectionProgress,
    isModuleComplete,
  };
}

export default useTrainingProgress;
