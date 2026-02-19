import React, { useState, useEffect } from 'react';
import { loadProgress, recordQuizAnswer, clearQuizResult } from '../effects/progressTracker';
import styles from './QuizBlock.module.css';

export default function QuizBlock({ 
  question, 
  options, 
  type, 
  quizId, 
  moduleId, 
  sourceRef, 
  onAnswer 
}) {
  const [selected, setSelected] = useState([]);
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const handleOptionClick = (optionId) => {
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
    
    recordQuizAnswer(quizId, isCorrect, calculatedScore, selected);

    if (onAnswer) {
      onAnswer(isCorrect, calculatedScore);
    }
  };

  const handleReset = () => {
    setSelected([]);
    setSubmitted(false);
    setScore(0);
    clearQuizResult(quizId);
  };

  useEffect(() => {
    const progress = loadProgress();
    const savedState = progress.quizzes[quizId];
    
    if (savedState?.submitted) {
      setSubmitted(true);
      setScore(savedState.score || 0);
      setSelected(savedState.selected || []);
    }
  }, [quizId]);

  useEffect(() => {
    const handleProgressReset = () => {
      setSelected([]);
      setSubmitted(false);
      setScore(0);
    };

    window.addEventListener('progressReset', handleProgressReset);
    return () => {
      window.removeEventListener('progressReset', handleProgressReset);
    };
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
