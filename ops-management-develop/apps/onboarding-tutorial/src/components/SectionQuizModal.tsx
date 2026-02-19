import React, { useState, useEffect, useCallback } from 'react';
import styles from './SectionQuizModal.module.css';

export interface QuizOption {
  id: string;
  text: string;
  isCorrect: boolean;
  explanation?: string;
}

export interface QuizQuestion {
  id: string;
  question: string;
  type: 'single' | 'multi';
  options: QuizOption[];
  explanation?: string;
}

interface SectionQuizModalProps {
  isOpen: boolean;
  onClose: () => void;
  sectionTitle: string;
  quizzes: QuizQuestion[];
  onQuizComplete?: (passed: boolean, percentage: number) => void;
}

export default function SectionQuizModal({
  isOpen,
  onClose,
  sectionTitle,
  quizzes,
  onQuizComplete,
}: SectionQuizModalProps) {
  const [currentQuizIndex, setCurrentQuizIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string[]>>({});
  const [submittedQuizzes, setSubmittedQuizzes] = useState<Set<string>>(new Set());
  const [quizResults, setQuizResults] = useState<Record<string, boolean>>({});

  // Reset state when modal opens
  useEffect(() => {
    if (isOpen) {
      setCurrentQuizIndex(0);
      setSelectedAnswers({});
      setSubmittedQuizzes(new Set());
      setQuizResults({});
    }
  }, [isOpen]);

  // Handle escape key
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
  }, [onClose]);

  useEffect(() => {
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, handleKeyDown]);

  if (!isOpen || quizzes.length === 0) return null;

  const currentQuiz = quizzes[currentQuizIndex];
  const isCurrentSubmitted = submittedQuizzes.has(currentQuiz.id);

  const handleOptionSelect = (quizId: string, optionId: string, isMulti: boolean) => {
    if (submittedQuizzes.has(quizId)) return;

    setSelectedAnswers(prev => {
      const current = prev[quizId] || [];
      if (isMulti) {
        if (current.includes(optionId)) {
          return { ...prev, [quizId]: current.filter(id => id !== optionId) };
        }
        return { ...prev, [quizId]: [...current, optionId] };
      }
      return { ...prev, [quizId]: [optionId] };
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

    setSubmittedQuizzes(prev => new Set([...prev, currentQuiz.id]));
    setQuizResults(prev => ({ ...prev, [currentQuiz.id]: isCorrect }));
  };

  const handleNext = () => {
    if (currentQuizIndex < quizzes.length - 1) {
      setCurrentQuizIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuizIndex > 0) {
      setCurrentQuizIndex(prev => prev - 1);
    }
  };

  const handleFinish = () => {
    const correctCount = Object.values(quizResults).filter(r => r).length;
    const totalCount = quizzes.length;
    const percentage = totalCount > 0 ? (correctCount / totalCount) * 100 : 0;
    const passed = percentage >= 70;

    if (onQuizComplete) {
      onQuizComplete(passed, percentage);
    }

    onClose();
  };

  const allAnswered = quizzes.every(q => submittedQuizzes.has(q.id));
  const correctCount = Object.values(quizResults).filter(r => r).length;
  const percentage = quizzes.length > 0 ? Math.round((correctCount / quizzes.length) * 100) : 0;

  // Find the explanation for current quiz
  const currentExplanation = currentQuiz.explanation || 
    currentQuiz.options.find(opt => opt.isCorrect)?.explanation || '';

  return (
    <div 
      className={styles.overlay} 
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className={styles.modal}>
        <div className={styles.header}>
          <h2>Test Your Knowledge</h2>
          <p className={styles.sectionName}>{sectionTitle}</p>
          <button className={styles.closeButton} onClick={onClose}>×</button>
        </div>

        <div className={styles.progress}>
          <div className={styles.progressInfo}>
            Question {currentQuizIndex + 1} of {quizzes.length}
            {allAnswered && (
              <span className={styles.score}>
                Score: {correctCount}/{quizzes.length} ({percentage}%)
              </span>
            )}
          </div>
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill}
              style={{ width: `${((currentQuizIndex + 1) / quizzes.length) * 100}%` }}
            />
          </div>
          <div className={styles.questionDots}>
            {quizzes.map((quiz, idx) => (
              <button
                key={quiz.id}
                className={`${styles.dot} ${idx === currentQuizIndex ? styles.dotActive : ''} ${
                  submittedQuizzes.has(quiz.id) 
                    ? quizResults[quiz.id] 
                      ? styles.dotCorrect 
                      : styles.dotIncorrect
                    : ''
                }`}
                onClick={() => setCurrentQuizIndex(idx)}
                title={`Question ${idx + 1}`}
              />
            ))}
          </div>
        </div>

        <div className={styles.content}>
          <h3 className={styles.question}>{currentQuiz.question}</h3>
          
          {currentQuiz.type === 'multi' && (
            <p className={styles.hint}>Select all that apply</p>
          )}

          <div className={styles.options}>
            {currentQuiz.options.map((option) => {
              const isSelected = (selectedAnswers[currentQuiz.id] || []).includes(option.id);
              const showCorrect = isCurrentSubmitted && option.isCorrect;
              const showIncorrect = isCurrentSubmitted && isSelected && !option.isCorrect;

              return (
                <button
                  key={option.id}
                  className={`${styles.option} ${isSelected ? styles.optionSelected : ''} ${
                    showCorrect ? styles.optionCorrect : ''
                  } ${showIncorrect ? styles.optionIncorrect : ''}`}
                  onClick={() => handleOptionSelect(currentQuiz.id, option.id, currentQuiz.type === 'multi')}
                  disabled={isCurrentSubmitted}
                >
                  <span className={styles.optionIndicator}>
                    {currentQuiz.type === 'multi' 
                      ? (isSelected ? '☑' : '☐')
                      : (isSelected ? '●' : '○')
                    }
                  </span>
                  <span className={styles.optionText}>{option.text}</span>
                </button>
              );
            })}
          </div>

          {isCurrentSubmitted && (
            <div className={`${styles.feedback} ${quizResults[currentQuiz.id] ? styles.feedbackCorrect : styles.feedbackIncorrect}`}>
              <p className={styles.feedbackTitle}>
                {quizResults[currentQuiz.id] ? '✓ Correct!' : '✗ Incorrect'}
              </p>
              {currentExplanation && (
                <p className={styles.feedbackExplanation}>{currentExplanation}</p>
              )}
            </div>
          )}
        </div>

        <div className={styles.actions}>
          <button
            className={`${styles.button} ${styles.buttonSecondary}`}
            onClick={handlePrevious}
            disabled={currentQuizIndex === 0}
          >
            ← Previous
          </button>

          {!isCurrentSubmitted ? (
            <button
              className={`${styles.button} ${styles.buttonPrimary}`}
              onClick={handleSubmitAnswer}
              disabled={(selectedAnswers[currentQuiz.id] || []).length === 0}
            >
              Submit Answer
            </button>
          ) : currentQuizIndex < quizzes.length - 1 ? (
            <button
              className={`${styles.button} ${styles.buttonPrimary}`}
              onClick={handleNext}
            >
              Next →
            </button>
          ) : (
            <button
              className={`${styles.button} ${styles.buttonPrimary}`}
              onClick={handleFinish}
            >
              Finish Quiz
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
