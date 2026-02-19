import React, { useState, useEffect } from 'react';
import styles from './QuizBlock.module.css';

export interface QuizOption {
  id: string;
  text: string;
  isCorrect: boolean;
  explanation?: string;
}

export interface SourceRef {
  anchorId?: string;
  locationHint?: string;
}

export interface QuizBlockProps {
  question: string;
  options: QuizOption[];
  type: 'single' | 'multi';
  quizId: string;
  moduleId?: string;
  sourceRef?: SourceRef;
  onAnswer?: (isCorrect: boolean, score: number) => void;
}

// Local storage key for quiz progress
const QUIZ_STORAGE_KEY = 'corva_training_quizzes';

interface QuizState {
  submitted: boolean;
  isCorrect: boolean;
  score: number;
  selected: string[];
}

function loadQuizState(quizId: string): QuizState | null {
  try {
    const stored = localStorage.getItem(QUIZ_STORAGE_KEY);
    if (stored) {
      const data = JSON.parse(stored);
      return data[quizId] || null;
    }
  } catch (e) {
    console.error('Failed to load quiz state:', e);
  }
  return null;
}

function saveQuizState(quizId: string, state: QuizState) {
  try {
    const stored = localStorage.getItem(QUIZ_STORAGE_KEY);
    const data = stored ? JSON.parse(stored) : {};
    data[quizId] = state;
    localStorage.setItem(QUIZ_STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    console.error('Failed to save quiz state:', e);
  }
}

function clearQuizState(quizId: string) {
  try {
    const stored = localStorage.getItem(QUIZ_STORAGE_KEY);
    if (stored) {
      const data = JSON.parse(stored);
      delete data[quizId];
      localStorage.setItem(QUIZ_STORAGE_KEY, JSON.stringify(data));
    }
  } catch (e) {
    console.error('Failed to clear quiz state:', e);
  }
}

export default function QuizBlock({ 
  question, 
  options, 
  type, 
  quizId, 
  moduleId, 
  sourceRef, 
  onAnswer 
}: QuizBlockProps) {
  const [selected, setSelected] = useState<string[]>([]);
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const handleOptionClick = (optionId: string) => {
    if (submitted) return;

    if (type === 'single') {
      setSelected([optionId]);
    } else {
      setSelected(prev => 
        prev.includes(optionId)
          ? prev.filter(id => id !== optionId)
          : [...prev, optionId]
      );
    }
  };

  const handleSubmit = () => {
    if (selected.length === 0) return;

    const correctOptions = options.filter(opt => opt.isCorrect).map(opt => opt.id);
    const isCorrect = type === 'single'
      ? selected[0] === correctOptions[0]
      : selected.length === correctOptions.length && 
        selected.every(id => correctOptions.includes(id)) &&
        correctOptions.every(id => selected.includes(id));

    const calculatedScore = isCorrect ? 100 : 0;
    setScore(calculatedScore);
    setSubmitted(true);
    
    // Save state to local storage
    saveQuizState(quizId, {
      submitted: true,
      isCorrect,
      score: calculatedScore,
      selected,
    });

    if (onAnswer) {
      onAnswer(isCorrect, calculatedScore);
    }
  };

  const handleReset = () => {
    setSelected([]);
    setSubmitted(false);
    setScore(0);
    clearQuizState(quizId);
  };

  // Load saved state on mount
  useEffect(() => {
    const savedState = loadQuizState(quizId);
    if (savedState?.submitted) {
      setSubmitted(true);
      setScore(savedState.score || 0);
      setSelected(savedState.selected || []);
    }
  }, [quizId]);

  const handleJumpToSource = () => {
    if (!sourceRef || !sourceRef.anchorId) return;
    
    const subsectionId = sourceRef.anchorId.split('__').pop() || sourceRef.anchorId;
    const element = document.getElementById(`subsection-${subsectionId}`) || 
                    document.getElementById(`section-${subsectionId}`) ||
                    document.getElementById(`subsection-${sourceRef.anchorId}`) ||
                    document.getElementById(`section-${sourceRef.anchorId}`);
    
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      element.style.transition = 'background-color 0.3s';
      element.style.backgroundColor = 'rgba(0, 188, 212, 0.2)';
      setTimeout(() => {
        element.style.backgroundColor = '';
      }, 2000);
    }
  };

  return (
    <div className={styles.quizBlock}>
      <h3 className={styles.question}>{question}</h3>
      
      {sourceRef && sourceRef.locationHint && (
        <div className={styles.sourceRef}>
          <span className={styles.sourceLabel}>Based on:</span>
          <span className={styles.sourceLocation}>{sourceRef.locationHint}</span>
          {sourceRef.anchorId && (
            <button 
              className={styles.jumpToSource}
              onClick={handleJumpToSource}
              title="Jump to source"
            >
              Jump to source →
            </button>
          )}
        </div>
      )}
      
      <div className={styles.options}>
        {options.map((option) => {
          const isSelected = selected.includes(option.id);
          const showCorrect = submitted && option.isCorrect;
          const showIncorrect = submitted && isSelected && !option.isCorrect;
          
          return (
            <div
              key={option.id}
              className={`${styles.option} ${
                isSelected ? styles.selected : ''
              } ${
                showCorrect ? styles.correct : ''
              } ${
                showIncorrect ? styles.incorrect : ''
              }`}
              onClick={() => handleOptionClick(option.id)}
            >
              <div className={styles.optionContent}>
                <span className={styles.optionText}>{option.text}</span>
                {type === 'multi' && (
                  <span className={styles.checkbox}>
                    {isSelected ? '✓' : '○'}
                  </span>
                )}
                {type === 'single' && (
                  <span className={styles.radio}>
                    {isSelected ? '●' : '○'}
                  </span>
                )}
              </div>
              {submitted && option.explanation && (
                <div className={`${styles.explanation} ${
                  option.isCorrect ? styles.explanationCorrect : ''
                }`}>
                  {option.explanation}
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {submitted && (
        <div className={styles.result}>
          <div className={`${styles.score} ${score === 100 ? styles.scoreCorrect : styles.scoreIncorrect}`}>
            {score === 100 ? '✓ Correct!' : '✗ Incorrect'}
          </div>
        </div>
      )}
      
      <div className={styles.actions}>
        {!submitted ? (
          <button 
            className={styles.submitButton} 
            onClick={handleSubmit}
            disabled={selected.length === 0}
          >
            Submit Answer
          </button>
        ) : (
          <button className={styles.resetButton} onClick={handleReset}>
            Try Again
          </button>
        )}
      </div>
    </div>
  );
}
