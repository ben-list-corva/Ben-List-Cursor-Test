import React, { useState, useEffect, useRef, useCallback } from 'react';
import { AppContainer, AppHeader } from '@corva/ui/componentsV2';
import { useAppCommons } from '@corva/ui/effects';

import { DEFAULT_SETTINGS } from './constants';
import styles from './App.module.css';
import corvaLogo from './assets/corva-logo.png';

// Import image registry for bundled training assets
import getImageUrl from './imageRegistry.js';

// Import components
import QuizBlock from './components/QuizBlock.jsx';
import RichContentRenderer from './components/RichContentRenderer.jsx';
import SectionHeader from './components/SectionHeader.jsx';
import SectionNav from './components/SectionNav.jsx';

// Import progress tracking
import {
  loadProgress,
  getQuizIdsFromModule,
  calculateDayProgress,
  calculateSectionStatuses,
  calculateCurrentSection,
  resetDayProgress,
  markSectionViewed,
  MODULE_TO_DAY,
  PASS_THRESHOLD,
} from './effects/progressTracker.js';

// Import module content directly (bundled with the app)
import introToOpsSections from './content/modules/introduction-to-operations-sections.json';
import introToOpsDay2Sections from './content/modules/introduction-to-operations-day2-sections.json';
import drillingDataAnalystSections from './content/modules/drilling-data-analyst-sections.json';
import becomingBetterDdaSections from './content/modules/becoming-better-dda-sections.json';

// Module content map
const MODULE_CONTENT = {
  'introduction-to-operations': introToOpsSections,
  'introduction-to-operations-day2': introToOpsDay2Sections,
  'drilling-data-analyst': drillingDataAnalystSections,
  'becoming-better-dda': becomingBetterDdaSections,
};

// Training module index
const MODULE_INDEX = [
  {
    moduleSlug: 'introduction-to-operations',
    title: 'Introduction to Operations',
    description: 'Learn the fundamentals of drilling operations',
    day: 1,
  },
  {
    moduleSlug: 'introduction-to-operations-day2',
    title: 'Introduction to Operations - Day 2',
    description: 'Continue your operations training journey',
    day: 2,
  },
  {
    moduleSlug: 'drilling-data-analyst',
    title: 'How to be a Drilling Data Analyst',
    description: 'Master the skills of a drilling data analyst',
    day: 3,
  },
  {
    moduleSlug: 'becoming-better-dda',
    title: 'Becoming a Better DDA',
    description: 'Advanced techniques for drilling data analysts',
    day: 4,
  },
];

// Inline SVG logos for Tech Stack tools
const SlackLogo = () => (
  <svg width="32" height="32" viewBox="0 0 127 127" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M27.2 80c0 7.3-5.9 13.2-13.2 13.2S.8 87.3.8 80s5.9-13.2 13.2-13.2h13.2V80zm6.6 0c0-7.3 5.9-13.2 13.2-13.2s13.2 5.9 13.2 13.2v33c0 7.3-5.9 13.2-13.2 13.2s-13.2-5.9-13.2-13.2V80z" fill="#E01E5A"/>
    <path d="M47 27c-7.3 0-13.2-5.9-13.2-13.2S39.7.6 47 .6s13.2 5.9 13.2 13.2V27H47zm0 6.7c7.3 0 13.2 5.9 13.2 13.2s-5.9 13.2-13.2 13.2H14c-7.3 0-13.2-5.9-13.2-13.2S6.7 33.7 14 33.7h33z" fill="#36C5F0"/>
    <path d="M99.9 46.9c0-7.3 5.9-13.2 13.2-13.2s13.2 5.9 13.2 13.2-5.9 13.2-13.2 13.2H99.9V46.9zm-6.6 0c0 7.3-5.9 13.2-13.2 13.2s-13.2-5.9-13.2-13.2V14c0-7.3 5.9-13.2 13.2-13.2s13.2 5.9 13.2 13.2v32.9z" fill="#2EB67D"/>
    <path d="M80.1 99.8c7.3 0 13.2 5.9 13.2 13.2s-5.9 13.2-13.2 13.2-13.2-5.9-13.2-13.2V99.8h13.2zm0-6.6c-7.3 0-13.2-5.9-13.2-13.2s5.9-13.2 13.2-13.2h33c7.3 0 13.2 5.9 13.2 13.2s-5.9 13.2-13.2 13.2h-33z" fill="#ECB22E"/>
  </svg>
);

const IntercomLogo = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="32" height="32" rx="8" fill="#1F8DED"/>
    <path d="M24 21.5c0 .3-.2.5-.5.5h-1c-.3 0-.5-.2-.5-.5v-7c0-.3.2-.5.5-.5h1c.3 0 .5.2.5.5v7zm-4 1.5c0 .3-.2.5-.5.5h-1c-.3 0-.5-.2-.5-.5v-10c0-.3.2-.5.5-.5h1c.3 0 .5.2.5.5v10zm-4 0c0 .3-.2.5-.5.5h-1c-.3 0-.5-.2-.5-.5v-10c0-.3.2-.5.5-.5h1c.3 0 .5.2.5.5v10zm-4-1.5c0 .3-.2.5-.5.5h-1c-.3 0-.5-.2-.5-.5v-7c0-.3.2-.5.5-.5h1c.3 0 .5.2.5.5v7zm-4-2c0 .3-.2.5-.5.5h-1c-.3 0-.5-.2-.5-.5v-3c0-.3.2-.5.5-.5h1c.3 0 .5.2.5.5v3z" fill="white"/>
  </svg>
);

const TrelloLogo = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="32" height="32" rx="6" fill="#0079BF"/>
    <rect x="6" y="6" width="8" height="14" rx="1.5" fill="white"/>
    <rect x="18" y="6" width="8" height="9" rx="1.5" fill="white"/>
  </svg>
);

// Get tech stack logo component for subsection title
function getTechStackLogo(title) {
  const titleLower = title.toLowerCase();
  if (titleLower.includes('slack')) return <SlackLogo />;
  if (titleLower.includes('intercom')) return <IntercomLogo />;
  if (titleLower.includes('trello')) return <TrelloLogo />;
  return null;
}

// Quiz Modal Component
function QuizModal({ isOpen, onClose, sectionTitle, quizzes, onQuizComplete }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [submittedQuizzes, setSubmittedQuizzes] = useState(new Set());
  const [quizResults, setQuizResults] = useState({});

  // Reset state when modal opens
  useEffect(() => {
    if (isOpen) {
      setCurrentIndex(0);
      setSelectedAnswers({});
      setSubmittedQuizzes(new Set());
      setQuizResults({});
    }
  }, [isOpen]);

  // Handle escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen || !quizzes || quizzes.length === 0) return null;

  const currentQuiz = quizzes[currentIndex];
  const isCurrentSubmitted = submittedQuizzes.has(currentQuiz.id);

  const handleOptionSelect = (optionId) => {
    if (submittedQuizzes.has(currentQuiz.id)) return;
    const isMulti = currentQuiz.type === 'multi';
    
    setSelectedAnswers(prev => {
      const current = prev[currentQuiz.id] || [];
      if (isMulti) {
        if (current.includes(optionId)) {
          return { ...prev, [currentQuiz.id]: current.filter(id => id !== optionId) };
        }
        return { ...prev, [currentQuiz.id]: [...current, optionId] };
      }
      return { ...prev, [currentQuiz.id]: [optionId] };
    });
  };

  const handleSubmitAnswer = () => {
    const selected = selectedAnswers[currentQuiz.id] || [];
    if (selected.length === 0) return;

    const correctOptions = currentQuiz.options.filter(opt => opt.isCorrect).map(opt => opt.id);
    const isCorrect = currentQuiz.type === 'single'
      ? selected[0] === correctOptions[0]
      : selected.length === correctOptions.length &&
        selected.every(id => correctOptions.includes(id)) &&
        correctOptions.every(id => selected.includes(id));

    // Save to localStorage
    const progress = loadProgress();
    progress.quizzes[currentQuiz.id] = {
      submitted: true,
      isCorrect,
      score: isCorrect ? 100 : 0,
      selected,
      attemptedAt: new Date().toISOString(),
    };
    localStorage.setItem('corva_training_progress', JSON.stringify(progress));

    setSubmittedQuizzes(prev => new Set([...prev, currentQuiz.id]));
    setQuizResults(prev => ({ ...prev, [currentQuiz.id]: isCorrect }));

    // Dispatch event for progress tracking
    window.dispatchEvent(new CustomEvent('quizSubmitted', {
      detail: { quizId: currentQuiz.id, isCorrect, score: isCorrect ? 100 : 0 }
    }));
  };

  const handleNext = () => {
    if (currentIndex < quizzes.length - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  };

  const handleFinish = () => {
    const correctCount = Object.values(quizResults).filter(r => r).length;
    const percentage = quizzes.length > 0 ? (correctCount / quizzes.length) * 100 : 0;
    const passed = percentage >= PASS_THRESHOLD * 100;

    if (onQuizComplete) {
      onQuizComplete(passed, percentage);
    }
    onClose();
  };

  const correctCount = Object.values(quizResults).filter(r => r).length;
  const explanation = currentQuiz.explanation || 
    currentQuiz.options.find(opt => opt.isCorrect)?.explanation || '';

  return (
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.85)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '1rem',
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div style={{
        background: '#0d1117',
        borderRadius: '12px',
        maxWidth: '700px',
        width: '100%',
        maxHeight: '90vh',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        border: '1px solid rgba(0, 188, 212, 0.3)',
      }}>
        {/* Header */}
        <div style={{
          padding: '1.5rem',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          position: 'relative',
        }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#e0e0e0', margin: 0 }}>
            Test Your Knowledge
          </h2>
          <p style={{ fontSize: '1rem', color: '#00bcd4', margin: '0.25rem 0 0' }}>{sectionTitle}</p>
          <button 
            onClick={onClose}
            style={{
              position: 'absolute',
              top: '1rem',
              right: '1rem',
              background: 'transparent',
              border: 'none',
              fontSize: '28px',
              color: 'rgba(255, 255, 255, 0.6)',
              cursor: 'pointer',
              padding: 0,
              lineHeight: 1,
            }}
          >×</button>
        </div>

        {/* Progress */}
        <div style={{
          padding: '1rem 1.5rem',
          background: '#161b22',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.875rem', color: 'rgba(255,255,255,0.6)' }}>
              Question {currentIndex + 1} of {quizzes.length}
            </span>
            <span style={{ fontSize: '0.875rem', color: '#00bcd4', fontWeight: 600 }}>
              Score: {correctCount}/{quizzes.length}
            </span>
          </div>
          <div style={{
            width: '100%',
            height: '4px',
            background: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '2px',
            overflow: 'hidden',
          }}>
            <div style={{
              height: '100%',
              width: `${((currentIndex + 1) / quizzes.length) * 100}%`,
              background: '#00bcd4',
              borderRadius: '2px',
              transition: 'width 0.2s ease',
            }} />
          </div>
        </div>

        {/* Content */}
        <div style={{ padding: '1.5rem', overflowY: 'auto', flex: 1 }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#e0e0e0', margin: '0 0 1rem', lineHeight: 1.4 }}>
            {currentQuiz.question}
          </h3>
          
          {currentQuiz.type === 'multi' && (
            <p style={{ fontSize: '0.875rem', color: '#00bcd4', margin: '-0.5rem 0 1rem', fontStyle: 'italic' }}>
              Select all that apply
            </p>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {currentQuiz.options.map((option) => {
              const isSelected = (selectedAnswers[currentQuiz.id] || []).includes(option.id);
              const showCorrect = isCurrentSubmitted && option.isCorrect;
              const showIncorrect = isCurrentSubmitted && isSelected && !option.isCorrect;

              return (
                <button
                  key={option.id}
                  onClick={() => handleOptionSelect(option.id)}
                  disabled={isCurrentSubmitted}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '0.75rem',
                    padding: '1rem',
                    background: showCorrect ? 'rgba(76, 175, 80, 0.2)' : showIncorrect ? 'rgba(244, 67, 54, 0.2)' : isSelected ? 'rgba(0, 188, 212, 0.15)' : '#161b22',
                    border: `2px solid ${showCorrect ? '#4caf50' : showIncorrect ? '#f44336' : isSelected ? '#00bcd4' : 'rgba(255, 255, 255, 0.12)'}`,
                    borderRadius: '8px',
                    cursor: isCurrentSubmitted ? 'default' : 'pointer',
                    textAlign: 'left',
                    transition: 'all 0.2s ease',
                    color: '#e0e0e0',
                    fontSize: '1rem',
                  }}
                >
                  <span style={{ fontSize: '1.125rem', color: '#00bcd4', flexShrink: 0, width: '24px' }}>
                    {currentQuiz.type === 'multi' 
                      ? (isSelected ? '☑' : '☐')
                      : (isSelected ? '●' : '○')
                    }
                  </span>
                  <span style={{ flex: 1, lineHeight: 1.5 }}>{option.text}</span>
                </button>
              );
            })}
          </div>

          {isCurrentSubmitted && (
            <div style={{
              marginTop: '1.5rem',
              padding: '1rem',
              borderRadius: '8px',
              background: quizResults[currentQuiz.id] ? 'rgba(76, 175, 80, 0.15)' : 'rgba(244, 67, 54, 0.15)',
              border: `1px solid ${quizResults[currentQuiz.id] ? '#4caf50' : '#f44336'}`,
            }}>
              <p style={{ 
                fontSize: '1.125rem', 
                fontWeight: 700, 
                margin: '0 0 0.5rem',
                color: quizResults[currentQuiz.id] ? '#4caf50' : '#f44336',
              }}>
                {quizResults[currentQuiz.id] ? '✓ Correct!' : '✗ Incorrect'}
              </p>
              {explanation && (
                <p style={{ fontSize: '1rem', color: 'rgba(255, 255, 255, 0.7)', margin: 0, lineHeight: 1.5 }}>
                  {explanation}
                </p>
              )}
            </div>
          )}
        </div>

        {/* Actions */}
        <div style={{
          padding: '1rem 1.5rem',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          gap: '1rem',
        }}>
          <button
            onClick={handlePrevious}
            disabled={currentIndex === 0}
            style={{
              padding: '0.75rem 1.5rem',
              borderRadius: '8px',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: currentIndex === 0 ? 'not-allowed' : 'pointer',
              opacity: currentIndex === 0 ? 0.5 : 1,
              background: 'transparent',
              color: 'rgba(255, 255, 255, 0.7)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
            }}
          >
            ← Previous
          </button>

          {!isCurrentSubmitted ? (
            <button
              onClick={handleSubmitAnswer}
              disabled={(selectedAnswers[currentQuiz.id] || []).length === 0}
              style={{
                padding: '0.75rem 1.5rem',
                borderRadius: '8px',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: (selectedAnswers[currentQuiz.id] || []).length === 0 ? 'not-allowed' : 'pointer',
                opacity: (selectedAnswers[currentQuiz.id] || []).length === 0 ? 0.5 : 1,
                background: '#00bcd4',
                color: '#0d1117',
                border: 'none',
              }}
            >
              Submit Answer
            </button>
          ) : currentIndex < quizzes.length - 1 ? (
            <button
              onClick={handleNext}
              style={{
                padding: '0.75rem 1.5rem',
                borderRadius: '8px',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'pointer',
                background: '#00bcd4',
                color: '#0d1117',
                border: 'none',
              }}
            >
              Next →
            </button>
          ) : (
            <button
              onClick={handleFinish}
              style={{
                padding: '0.75rem 1.5rem',
                borderRadius: '8px',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'pointer',
                background: '#00bcd4',
                color: '#0d1117',
                border: 'none',
              }}
            >
              Finish Quiz
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// Note: Content rendering now uses RichContentRenderer from ./components/RichContentRenderer.jsx
// which uses Figure from ./components/Figure.jsx (with click-to-expand functionality)

function App({ 
  isExampleCheckboxChecked = DEFAULT_SETTINGS.isExampleCheckboxChecked, 
  rig, 
  well,
  currentUser 
}) {
  const { appKey } = useAppCommons();
  const [view, setView] = useState({ type: 'home' });
  const [moduleData, setModuleData] = useState(null);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);
  
  // Progress tracking state
  const [dayProgress, setDayProgress] = useState(null);
  const [sectionQuizStatuses, setSectionQuizStatuses] = useState({});
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [quizIds, setQuizIds] = useState([]);
  
  // Quiz modal state
  const [quizModal, setQuizModal] = useState({ isOpen: false, sectionTitle: '', quizzes: [] });

  const dayNumber = view.moduleSlug ? MODULE_TO_DAY[view.moduleSlug] : null;

  // Update section statuses
  const updateSectionStatuses = useCallback((sections) => {
    const progress = loadProgress();
    const statuses = calculateSectionStatuses(sections, progress);
    setSectionQuizStatuses(statuses);
    
    // Update current section index
    const newCurrentIndex = calculateCurrentSection(sections, progress);
    setCurrentSectionIndex(newCurrentIndex);
  }, []);

  // Update overall progress
  const updateProgress = useCallback(() => {
    if (quizIds.length > 0 && dayNumber) {
      const progress = loadProgress();
      const dayProg = calculateDayProgress(dayNumber, quizIds, progress);
      setDayProgress(dayProg);
    }
    
    if (moduleData?.sections) {
      updateSectionStatuses(moduleData.sections);
    }
  }, [dayNumber, quizIds, moduleData, updateSectionStatuses]);

  // Load module data when viewing a module
  useEffect(() => {
    if (view.type === 'module' || view.type === 'section') {
      const content = MODULE_CONTENT[view.moduleSlug];
      if (content) {
        setModuleData(content);
        setError(null);
        
        // Extract quiz IDs for progress tracking
        const ids = getQuizIdsFromModule(content);
        setQuizIds(ids);
        
        // Calculate initial progress
        const progress = loadProgress();
        const day = MODULE_TO_DAY[view.moduleSlug];
        const dayProg = calculateDayProgress(day, ids, progress);
        setDayProgress(dayProg);
        
        // Calculate section statuses
        updateSectionStatuses(content.sections);
      } else {
        setError('Module not found');
        setModuleData(null);
      }
    }
    // Scroll to top on view change
    if (scrollRef.current) {
      scrollRef.current.scrollTop = 0;
    }
  }, [view, updateSectionStatuses]);

  // Update progress when quizzes are submitted or sections are viewed
  useEffect(() => {
    const handleQuizSubmitted = () => {
      updateProgress();
    };
    
    const handleSectionViewed = () => {
      updateProgress();
    };

    window.addEventListener('quizSubmitted', handleQuizSubmitted);
    window.addEventListener('sectionViewed', handleSectionViewed);
    return () => {
      window.removeEventListener('quizSubmitted', handleQuizSubmitted);
      window.removeEventListener('sectionViewed', handleSectionViewed);
    };
  }, [updateProgress]);

  // Handle restart day
  const handleRestartDay = () => {
    if (window.confirm(`Are you sure you want to restart Day ${dayNumber}? This will reset all quiz answers for this day.`)) {
      const sectionIds = moduleData?.sections?.map(s => s.id) || [];
      resetDayProgress(dayNumber, quizIds, sectionIds);
      setCurrentSectionIndex(0);
      setSectionQuizStatuses({});
      setDayProgress(null);
      // Force refresh
      if (moduleData?.sections) {
        updateSectionStatuses(moduleData.sections);
      }
    }
  };

  // Mark section as viewed when user enters it
  useEffect(() => {
    if (view.type === 'section' && view.sectionId && moduleData) {
      const section = moduleData.sections.find(s => s.id === view.sectionId);
      // Mark section as viewed (especially for sections without quizzes)
      if (section && (!section.quiz || section.quiz.length === 0)) {
        markSectionViewed(view.sectionId);
        updateProgress();
      }
    }
  }, [view.type, view.sectionId, moduleData, updateProgress]);

  // Calculate overall progress across all modules
  const calculateOverallProgress = () => {
    const progress = loadProgress();
    let totalQuestions = 0;
    let correctAnswers = 0;
    let totalSections = 0;
    let completedSections = 0;

    MODULE_INDEX.forEach((module) => {
      const content = MODULE_CONTENT[module.moduleSlug];
      if (content?.sections) {
        totalSections += content.sections.length;
        
        content.sections.forEach((section) => {
          // Check if section is viewed (for no-quiz sections)
          if (!section.quiz || section.quiz.length === 0) {
            if (progress.viewedSections?.[section.id]) {
              completedSections++;
            }
          } else {
            // For sections with quizzes
            let sectionCorrect = 0;
            let sectionAnswered = 0;
            section.quiz.forEach((quiz) => {
              totalQuestions++;
              const saved = progress.quizzes[quiz.id];
              if (saved?.submitted) {
                sectionAnswered++;
                if (saved.isCorrect) {
                  correctAnswers++;
                  sectionCorrect++;
                }
              }
            });
            // Section is complete if all quizzes answered and >= 80% correct
            if (sectionAnswered === section.quiz.length && 
                (sectionCorrect / section.quiz.length) >= PASS_THRESHOLD) {
              completedSections++;
            }
          }
        });
      }
    });

    const percentage = totalQuestions > 0 ? (correctAnswers / totalQuestions) * 100 : 0;
    return {
      totalQuestions,
      correctAnswers,
      percentage,
      totalSections,
      completedSections,
      passed: percentage >= PASS_THRESHOLD * 100,
    };
  };

  // Render home view with module list
  const renderHome = () => {
    const overallProgress = calculateOverallProgress();
    
    return (
      <div className={styles.homeContainer}>
        {/* Corva Logo */}
        <div className={styles.logoContainer}>
          <img src={corvaLogo} alt="Corva" className={styles.corvaLogo} />
        </div>

        <div className={styles.header}>
          <h1 className={styles.title}>Operations Training</h1>
          <p className={styles.subtitle}>
            Welcome{currentUser ? `, ${currentUser.first_name}` : ''}! Select a training module to begin.
          </p>
        </div>

        {/* Overall Progress Bar - NUCLEAR FIX with inline styles */}
        <div className={styles.overallProgress}>
          <div className={styles.overallProgressHeader}>
            <span className={styles.overallProgressLabel}>Overall Training Progress</span>
            <span className={styles.overallProgressStats}>
              {overallProgress.completedSections}/{overallProgress.totalSections} sections completed
            </span>
          </div>
          <div style={{
            position: 'relative',
            height: '8px',
            background: '#21262d',
            borderRadius: '4px',
            marginBottom: '0.5rem',
            overflow: 'hidden',
          }}>
            {/* Progress Fill - only show if > 0 */}
            {overallProgress.percentage > 0 && (
              <div style={{
                position: 'absolute',
                left: 0,
                top: 0,
                height: '100%',
                width: `${overallProgress.percentage}%`,
                background: overallProgress.passed 
                  ? 'linear-gradient(90deg, #4caf50, #66bb6a)' 
                  : 'linear-gradient(90deg, #00bcd4, #00acc1)',
                borderRadius: '4px',
              }} />
            )}
          </div>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: '0.875rem',
          }}>
            <span style={{ color: 'rgba(255,255,255,0.7)' }}>
              {overallProgress.correctAnswers}/{overallProgress.totalQuestions} questions correct ({Math.round(overallProgress.percentage)}%)
            </span>
            <span style={{ color: '#ff9800', fontSize: '0.75rem' }}>
              {overallProgress.passed ? '✓ Training Complete' : '80% required to pass'}
            </span>
          </div>
        </div>

        {/* Module List - Horizontal Stack */}
        <div className={styles.moduleList}>
          {MODULE_INDEX.map((module) => {
            // Calculate day progress for this module
            const content = MODULE_CONTENT[module.moduleSlug];
            const progress = loadProgress();
            let dayCorrect = 0;
            let dayTotal = 0;
            
            if (content?.sections) {
              content.sections.forEach((section) => {
                if (section.quiz) {
                  section.quiz.forEach((quiz) => {
                    dayTotal++;
                    const saved = progress.quizzes[quiz.id];
                    if (saved?.submitted && saved.isCorrect) {
                      dayCorrect++;
                    }
                  });
                }
              });
            }
            
            const dayPercentage = dayTotal > 0 ? Math.round((dayCorrect / dayTotal) * 100) : 0;
            const dayPassed = dayPercentage >= PASS_THRESHOLD * 100;
            
            return (
              <div 
                key={module.moduleSlug}
                className={`${styles.moduleCardWide} ${dayPassed ? styles.moduleCardPassed : ''}`}
                onClick={() => setView({ type: 'module', moduleSlug: module.moduleSlug })}
              >
                <div className={styles.moduleCardLeft}>
                  <span className={styles.dayBadgeLarge}>Day {module.day}</span>
                </div>
                <div className={styles.moduleCardCenter}>
                  <h3 className={styles.moduleTitle}>{module.title}</h3>
                  <p className={styles.moduleDescription}>{module.description}</p>
                  <div className={styles.moduleProgressMini}>
                    <div style={{
                      flex: 1,
                      maxWidth: '200px',
                      height: '6px',
                      background: '#21262d',
                      borderRadius: '3px',
                      overflow: 'hidden',
                      position: 'relative',
                    }}>
                      {dayPercentage > 0 && (
                        <div style={{
                          position: 'absolute',
                          left: 0,
                          top: 0,
                          height: '100%',
                          width: `${dayPercentage}%`,
                          background: dayPassed 
                            ? 'linear-gradient(90deg, #4caf50, #66bb6a)' 
                            : 'linear-gradient(90deg, #00bcd4, #00acc1)',
                          borderRadius: '3px',
                        }} />
                      )}
                    </div>
                    <span className={styles.moduleProgressTextMini}>
                      {dayCorrect}/{dayTotal} ({dayPercentage}%)
                    </span>
                  </div>
                </div>
                <div className={styles.moduleCardRight}>
                  {dayPassed ? (
                    <span className={styles.moduleCheckmark}>✓</span>
                  ) : (
                    <span className={styles.moduleArrowLarge}>→</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  // Render module view with section list
  const renderModule = () => {
    if (error) {
      return (
        <div className={styles.error}>
          <p>{error}</p>
          <button 
            className={styles.backButton}
            onClick={() => setView({ type: 'home' })}
          >
            ← Back to Home
          </button>
        </div>
      );
    }

    if (!moduleData) {
      return <div className={styles.loading}>Loading...</div>;
    }

    const totalSections = moduleData.sections.length;
    const completedSections = Object.values(sectionQuizStatuses).filter(s => s.passed).length;

    return (
      <div className={styles.moduleContainer}>
        <button 
          className={styles.backButton}
          onClick={() => setView({ type: 'home' })}
        >
          ← Back to Modules
        </button>

        <div className={styles.moduleHeader}>
          <div className={styles.moduleHeaderTop}>
            <div>
              <h1 className={styles.moduleHeading}>{moduleData.title}</h1>
              <p className={styles.moduleMeta}>
                Day {dayNumber} • Section {Math.min(currentSectionIndex + 1, totalSections)} of {totalSections}
              </p>
            </div>
            <button 
              className={styles.restartButton}
              onClick={handleRestartDay}
              title="Restart this day's progress"
            >
              ↺ Restart Day
            </button>
          </div>

          {/* Progress Bar - Clean display matching percentage */}
          {dayProgress && (
            <div className={styles.progressSummary}>
              <div style={{
                position: 'relative',
                height: '8px',
                background: '#21262d',
                borderRadius: '4px',
                marginBottom: '0.5rem',
                overflow: 'hidden',
              }}>
                {/* Progress Fill - only show if > 0 */}
                {dayProgress.percentage > 0 && (
                  <div style={{
                    position: 'absolute',
                    left: 0,
                    top: 0,
                    height: '100%',
                    width: `${dayProgress.percentage}%`,
                    background: dayProgress.passed 
                      ? 'linear-gradient(90deg, #4caf50, #66bb6a)' 
                      : 'linear-gradient(90deg, #00bcd4, #00acc1)',
                    borderRadius: '4px',
                  }} />
                )}
              </div>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontSize: '0.875rem',
              }}>
                <span style={{ color: 'rgba(255,255,255,0.7)' }}>
                  {dayProgress.correctAnswers}/{dayProgress.totalQuestions} questions correct ({Math.round(dayProgress.percentage)}%)
                </span>
                <span style={{ color: dayProgress.passed ? '#4caf50' : '#ff9800', fontSize: '0.75rem' }}>
                  {dayProgress.passed ? '✓ Day Passed' : '80% required to pass'}
                </span>
              </div>
            </div>
          )}

          {/* Section Progress Dots */}
          <div className={styles.sectionProgress}>
            <div className={styles.sectionDots}>
              {moduleData.sections.map((section, index) => {
                const status = sectionQuizStatuses[section.id];
                const isActive = index === currentSectionIndex;
                const isPassed = status?.passed;
                const isLocked = index > currentSectionIndex + 1;
                
                return (
                  <div
                    key={section.id}
                    className={`${styles.sectionDot} ${isActive ? styles.sectionDotActive : ''} ${isPassed ? styles.sectionDotPassed : ''} ${isLocked ? styles.sectionDotLocked : ''}`}
                    title={section.title}
                  />
                );
              })}
            </div>
            <p className={styles.sectionProgressText}>
              {completedSections} of {totalSections} sections completed
            </p>
          </div>
        </div>

        <div className={styles.sectionList}>
          {moduleData.sections.map((section, index) => {
            const status = sectionQuizStatuses[section.id];
            const isLocked = index > 0 && !sectionQuizStatuses[moduleData.sections[index - 1]?.id]?.passed;
            const isUnlocked = index === 0 || sectionQuizStatuses[moduleData.sections[index - 1]?.id]?.passed;
            
            // Only show unlocked sections + next one
            if (index > currentSectionIndex + 1) {
              return null;
            }

            return (
              <div 
                key={section.id}
                className={`${styles.sectionCard} ${isLocked ? styles.sectionLocked : ''} ${status?.passed ? styles.sectionPassed : ''}`}
                onClick={() => {
                  if (!isLocked) {
                    setView({ 
                      type: 'section', 
                      moduleSlug: view.moduleSlug,
                      sectionId: section.id 
                    });
                  }
                }}
              >
                <span className={`${styles.sectionNumber} ${status?.passed ? styles.sectionNumberPassed : ''}`}>
                  {status?.passed ? '✓' : index + 1}
                </span>
                <div className={styles.sectionInfo}>
                  <h4 className={styles.sectionTitle}>{section.title}</h4>
                  {section.quiz && section.quiz.length > 0 && (
                    <span className={styles.quizBadge}>
                      {status?.correct || 0}/{section.quiz.length} Quiz Question{section.quiz.length > 1 ? 's' : ''}
                    </span>
                  )}
                </div>
                {isLocked ? (
                  <span className={styles.lockIcon}>🔒</span>
                ) : (
                  <span className={styles.sectionArrow}>→</span>
                )}
              </div>
            );
          })}
          
          {/* Locked sections indicator */}
          {currentSectionIndex + 2 < totalSections && (
            <div className={styles.lockedSectionsIndicator}>
              <span className={styles.lockIcon}>🔒</span>
              <p>{totalSections - currentSectionIndex - 2} more section{totalSections - currentSectionIndex - 2 > 1 ? 's' : ''} available after completing current section</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Render section view with content
  // Uses shared SectionHeader and SectionNav components for consistent layout across ALL sections
  const renderSection = () => {
    if (!moduleData) {
      return <div className={styles.loading}>Loading...</div>;
    }

    const section = moduleData.sections.find(s => s.id === view.sectionId);

    if (!section) {
      return (
        <div className={styles.error}>
          <p>Section not found</p>
          <button 
            className={styles.backButton}
            onClick={() => setView({ type: 'module', moduleSlug: view.moduleSlug })}
          >
            ← Back to Module
          </button>
        </div>
      );
    }

    const currentIndex = moduleData.sections.findIndex(s => s.id === view.sectionId);
    const prevSection = currentIndex > 0 ? moduleData.sections[currentIndex - 1] : null;
    const nextSection = currentIndex < moduleData.sections.length - 1 ? moduleData.sections[currentIndex + 1] : null;
    const nextSectionUnlocked = nextSection && sectionQuizStatuses[section.id]?.passed;

    // Collect all images from section and subsections
    const allImages = [
      ...(section.images || []),
      ...(section.subsections?.flatMap(sub => sub.images || []) || [])
    ];

    // Container style - normal document flow
    const containerStyle = {
      display: 'block',
      width: '100%',
      maxWidth: '1000px',
      margin: '0 auto',
      position: 'relative',
    };

    // Content area style - NO decorative background (moved to SectionHeader)
    const contentStyle = {
      display: 'block',
      width: '100%',
      boxSizing: 'border-box',
      position: 'relative',
      zIndex: 1,
    };

    // Subsection container style
    const subsectionStyle = (index, hasMainContent) => ({
      marginTop: index === 0 && !hasMainContent ? 0 : '3rem',
      paddingTop: index === 0 && !hasMainContent ? 0 : '2rem',
      borderTop: index === 0 && !hasMainContent ? 'none' : '1px solid rgba(255, 255, 255, 0.1)',
      position: 'relative',
      zIndex: 1,
    });

    // Subsection header style
    const subsectionHeaderStyle = {
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem',
      marginBottom: '1.5rem',
      padding: '1rem 1.5rem',
      background: '#161b22',
      borderRadius: '8px',
      border: '1px solid rgba(0, 188, 212, 0.2)',
      position: 'relative',
      zIndex: 2,
    };

    // Quiz section style
    const quizSectionStyle = {
      marginTop: '3rem',
      paddingTop: '2rem',
      borderTop: '2px solid rgba(0, 188, 212, 0.3)',
      position: 'relative',
      zIndex: 5, // Above images
    };

    const handleNavigate = (sectionId) => {
      setView({ 
        type: 'section', 
        moduleSlug: view.moduleSlug,
        sectionId 
      });
    };

    return (
      <div style={containerStyle}>
        {/* SECTION HEADER - Decorative rectangle is contained here */}
        <SectionHeader
          title={section.title}
          backLabel={`Back to ${moduleData.title}`}
          onBackClick={() => setView({ type: 'module', moduleSlug: view.moduleSlug })}
        />

        {/* CONTENT AREA - Normal document flow, no decorative elements */}
        <div style={contentStyle}>
          {/* Main section content */}
          {section.content && section.content.length > 0 && (
            <div style={{ marginBottom: section.subsections?.length > 0 ? '2rem' : 0 }}>
              <RichContentRenderer blocks={section.content} images={allImages} sectionId={section.id} />
            </div>
          )}

          {/* Subsections */}
          {section.subsections && section.subsections.map((subsection, index) => {
            const logo = getTechStackLogo(subsection.title);
            const hasMainContent = section.content && section.content.length > 0;
            
            return (
              <div 
                key={subsection.id} 
                id={`subsection-${subsection.id}`}
                style={subsectionStyle(index, hasMainContent)}
              >
                {/* Subsection header with decorative background */}
                <div style={subsectionHeaderStyle}>
                  {logo && (
                    <span style={{ width: '32px', height: '32px', flexShrink: 0 }}>
                      {logo}
                    </span>
                  )}
                  <h2 style={{ 
                    fontSize: '1.375rem', 
                    fontWeight: 600, 
                    color: '#00bcd4', 
                    margin: 0,
                  }}>
                    {subsection.title}
                  </h2>
                </div>
                
                {/* Subsection content - images will have proper spacing */}
                <div style={{ position: 'relative', zIndex: 1 }}>
                  <RichContentRenderer blocks={subsection.content} images={subsection.images} sectionId={subsection.id} />
                </div>
              </div>
            );
          })}

          {/* Quiz Button - Always above images */}
          {section.quiz && section.quiz.length > 0 && (
            <div style={quizSectionStyle}>
              <button
                className={styles.quizButton}
                onClick={() => setQuizModal({
                  isOpen: true,
                  sectionTitle: section.title,
                  quizzes: section.quiz
                })}
              >
                Test your knowledge on {section.title}
              </button>
            </div>
          )}
        </div>

        {/* SECTION NAVIGATION - Uses shared component, always at bottom */}
        <SectionNav
          prevSection={prevSection}
          nextSection={nextSection}
          nextSectionUnlocked={nextSectionUnlocked}
          onNavigate={handleNavigate}
        />
      </div>
    );
  };

  // Render current view
  const renderContent = () => {
    switch (view.type) {
      case 'home':
        return renderHome();
      case 'module':
        return renderModule();
      case 'section':
        return renderSection();
      default:
        return renderHome();
    }
  };

  return (
    <AppContainer header={<AppHeader />} testId={appKey}>
      <div ref={scrollRef} className={styles.appContainer}>
        {renderContent()}
      </div>
      
      {/* Quiz Modal */}
      <QuizModal
        isOpen={quizModal.isOpen}
        onClose={() => setQuizModal({ isOpen: false, sectionTitle: '', quizzes: [] })}
        sectionTitle={quizModal.sectionTitle}
        quizzes={quizModal.quizzes}
        onQuizComplete={(passed, percentage) => {
          updateProgress();
        }}
      />
    </AppContainer>
  );
}

export default App;
