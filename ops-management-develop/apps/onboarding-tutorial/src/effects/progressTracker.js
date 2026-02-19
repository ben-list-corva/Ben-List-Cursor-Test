/**
 * Progress Tracking System for DevCenter
 * Manages quiz-based progress tracking, day unlocking, and completion status
 */

// Day to module mapping
export const DAY_MODULES = {
  1: 'introduction-to-operations',
  2: 'introduction-to-operations-day2',
  3: 'drilling-data-analyst',
  4: 'becoming-better-dda',
};

export const MODULE_TO_DAY = {
  'introduction-to-operations': 1,
  'introduction-to-operations-day2': 2,
  'drilling-data-analyst': 3,
  'becoming-better-dda': 4,
};

// Pass threshold (80%)
export const PASS_THRESHOLD = 0.80;

// localStorage key for progress
export const PROGRESS_STORAGE_KEY = 'corva_training_progress';

/**
 * Load progress from localStorage
 */
export function loadProgress() {
  try {
    const saved = localStorage.getItem(PROGRESS_STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      // Ensure viewedSections exists
      if (!parsed.viewedSections) {
        parsed.viewedSections = {};
      }
      return parsed;
    }
  } catch (error) {
    console.error('Error loading progress:', error);
  }
  
  return { quizzes: {}, viewedSections: {} };
}

/**
 * Mark a section as viewed (for sections without quizzes)
 */
export function markSectionViewed(sectionId) {
  const progress = loadProgress();
  
  if (!progress.viewedSections) {
    progress.viewedSections = {};
  }
  
  progress.viewedSections[sectionId] = true;
  saveProgress(progress);
  
  window.dispatchEvent(new CustomEvent('sectionViewed', { detail: { sectionId } }));
}

/**
 * Save progress to localStorage
 */
export function saveProgress(progress) {
  try {
    localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progress));
  } catch (error) {
    console.error('Error saving progress:', error);
  }
}

/**
 * Get quiz IDs for a specific module from the module data
 */
export function getQuizIdsFromModule(moduleData) {
  const quizIds = [];
  
  if (!moduleData?.sections) return quizIds;
  
  for (const section of moduleData.sections) {
    if (section.quiz && Array.isArray(section.quiz)) {
      for (const quiz of section.quiz) {
        if (quiz.id) {
          quizIds.push(quiz.id);
        }
      }
    }
  }
  
  return quizIds;
}

/**
 * Calculate progress for a specific day/module
 */
export function calculateDayProgress(dayNumber, quizIds, storedProgress) {
  const moduleId = DAY_MODULES[dayNumber];
  const totalQuestions = quizIds.length;
  
  let correctAnswers = 0;
  let answeredQuestions = 0;
  
  for (const quizId of quizIds) {
    const result = storedProgress.quizzes[quizId];
    if (result?.submitted) {
      answeredQuestions++;
      if (result.isCorrect) {
        correctAnswers++;
      }
    }
  }
  
  const percentage = totalQuestions > 0 
    ? (correctAnswers / totalQuestions) * 100 
    : 0;
  
  return {
    dayNumber,
    moduleId,
    totalQuestions,
    correctAnswers,
    percentage,
    passed: percentage >= PASS_THRESHOLD * 100,
    answeredQuestions,
  };
}

/**
 * Calculate section quiz statuses for a module
 * Sections without quizzes require explicit "viewed" tracking
 */
export function calculateSectionStatuses(sections, storedProgress) {
  const statuses = {};
  
  sections.forEach((section, index) => {
    // Check if section has been viewed (for sections without quizzes)
    const sectionViewed = storedProgress.viewedSections?.[section.id] === true;
    
    if (!section.quiz || section.quiz.length === 0) {
      // Sections without quizzes must be explicitly viewed to be "passed"
      statuses[section.id] = {
        sectionId: section.id,
        total: 0,
        correct: 0,
        percentage: 0,
        passed: sectionViewed,
        noQuiz: true,
      };
      return;
    }
    
    let correct = 0;
    let answered = 0;
    
    section.quiz.forEach((quiz) => {
      const saved = storedProgress.quizzes[quiz.id];
      if (saved?.submitted) {
        answered++;
        if (saved.isCorrect) correct++;
      }
    });
    
    const percentage = section.quiz.length > 0 ? (correct / section.quiz.length) * 100 : 0;
    const allAnswered = answered === section.quiz.length;
    
    statuses[section.id] = {
      sectionId: section.id,
      total: section.quiz.length,
      correct,
      percentage,
      passed: allAnswered && percentage >= PASS_THRESHOLD * 100,
    };
  });
  
  return statuses;
}

/**
 * Calculate which section the user should be on
 */
export function calculateCurrentSection(sections, storedProgress) {
  for (let i = 0; i < sections.length; i++) {
    const section = sections[i];
    
    if (!section.quiz || section.quiz.length === 0) {
      continue;
    }
    
    let correct = 0;
    let answered = 0;
    
    section.quiz.forEach((quiz) => {
      const saved = storedProgress.quizzes[quiz.id];
      if (saved?.submitted) {
        answered++;
        if (saved.isCorrect) correct++;
      }
    });
    
    const percentage = section.quiz.length > 0 ? (correct / section.quiz.length) * 100 : 0;
    const passed = percentage >= PASS_THRESHOLD * 100;
    
    if (!passed) {
      return i;
    }
  }
  
  return sections.length - 1;
}

/**
 * Reset progress for a specific day
 */
export function resetDayProgress(dayNumber, quizIds, sectionIds = []) {
  const progress = loadProgress();
  
  // Clear quiz answers
  for (const quizId of quizIds) {
    delete progress.quizzes[quizId];
  }
  
  // Clear viewed sections
  for (const sectionId of sectionIds) {
    if (progress.viewedSections) {
      delete progress.viewedSections[sectionId];
    }
  }
  
  saveProgress(progress);
  
  window.dispatchEvent(new CustomEvent('progressReset', { detail: { dayNumber } }));
}

/**
 * Record a quiz answer
 */
export function recordQuizAnswer(quizId, isCorrect, score, selected) {
  const progress = loadProgress();
  
  progress.quizzes[quizId] = {
    submitted: true,
    isCorrect,
    score,
    selected,
    attemptedAt: new Date().toISOString(),
  };
  
  saveProgress(progress);
  
  window.dispatchEvent(new CustomEvent('quizSubmitted', { detail: { quizId, isCorrect, score } }));
}

/**
 * Clear a quiz result (for retry)
 */
export function clearQuizResult(quizId) {
  const progress = loadProgress();
  
  if (progress.quizzes[quizId]) {
    delete progress.quizzes[quizId];
    saveProgress(progress);
  }
  
  window.dispatchEvent(new CustomEvent('quizSubmitted', { 
    detail: { quizId, isCorrect: false, score: 0, reset: true } 
  }));
}

export default {
  loadProgress,
  saveProgress,
  getQuizIdsFromModule,
  calculateDayProgress,
  calculateSectionStatuses,
  calculateCurrentSection,
  resetDayProgress,
  recordQuizAnswer,
  clearQuizResult,
  markSectionViewed,
  PASS_THRESHOLD,
  MODULE_TO_DAY,
  DAY_MODULES,
  PROGRESS_STORAGE_KEY,
};
