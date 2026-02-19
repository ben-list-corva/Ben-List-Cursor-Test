import React, { useState, useEffect } from 'react';
import { AppContainer, AppHeader } from '@corva/ui/componentsV2';
import { useAppCommons } from '@corva/ui/effects';

import { DEFAULT_SETTINGS } from './constants';
import { RichContentRenderer, SectionQuizModal } from './components';
import type { QuizQuestion as QuizModalQuestion } from './components/SectionQuizModal';
import type { 
  TrainingModule, 
  TrainingSection,
  AppProps,
  QuizQuestion,
  QuizChoice
} from './types';

import styles from './App.module.css';

// Tech Stack logo mapping
const TECH_STACK_LOGOS: Record<string, string> = {
  'slack': './assets/logos/slack-logo.svg',
  'intercom': './assets/logos/intercom-logo.svg',
  'trello': './assets/logos/trello-logo.svg',
};

// Training module index data (loaded from bundled content)
const MODULE_INDEX = [
  {
    moduleSlug: 'introduction-to-operations',
    title: 'Introduction to Operations',
    description: 'Learn the fundamentals of drilling operations',
  },
  {
    moduleSlug: 'introduction-to-operations-day2',
    title: 'Introduction to Operations - Day 2',
    description: 'Continue your operations training journey',
  },
  {
    moduleSlug: 'drilling-data-analyst',
    title: 'How to be a Drilling Data Analyst',
    description: 'Master the skills of a drilling data analyst',
  },
  {
    moduleSlug: 'becoming-better-dda',
    title: 'Becoming a Better DDA',
    description: 'Advanced techniques for drilling data analysts',
  },
];

// Views for navigation
type ViewState = 
  | { type: 'home' }
  | { type: 'module'; moduleSlug: string }
  | { type: 'section'; moduleSlug: string; sectionId: string };

interface AppComponentProps {
  isExampleCheckboxChecked?: boolean;
  rig?: { name: string };
  well?: { name: string };
  currentUser?: { id: number; first_name: string; last_name: string };
}

function App({ 
  isExampleCheckboxChecked = DEFAULT_SETTINGS.isExampleCheckboxChecked, 
  rig, 
  well,
  currentUser 
}: AppComponentProps) {
  const { appKey } = useAppCommons();
  const [view, setView] = useState<ViewState>({ type: 'home' });
  const [moduleData, setModuleData] = useState<TrainingModule | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load module data when viewing a module
  useEffect(() => {
    if (view.type === 'module' || view.type === 'section') {
      loadModule(view.moduleSlug);
    }
  }, [view.type === 'module' || view.type === 'section' ? view.moduleSlug : null]);

  const loadModule = async (moduleSlug: string) => {
    setLoading(true);
    setError(null);
    
    try {
      // In production, this would load from bundled content or fetch from API
      // For now, we'll load from the bundled JSON files
      const response = await fetch(`./content/modules/${moduleSlug}-sections.json`);
      if (!response.ok) {
        throw new Error(`Failed to load module: ${response.statusText}`);
      }
      const data = await response.json();
      setModuleData(data);
    } catch (err) {
      console.error('Failed to load module:', err);
      setError(err instanceof Error ? err.message : 'Failed to load module');
    } finally {
      setLoading(false);
    }
  };

  const [isQuizModalOpen, setIsQuizModalOpen] = useState(false);
  const [currentQuizSection, setCurrentQuizSection] = useState<TrainingSection | null>(null);

  const handleQuizAnswer = (quizId: string, isCorrect: boolean, score: number) => {
    console.log(`Quiz ${quizId}: ${isCorrect ? 'Correct' : 'Incorrect'} (${score}%)`);
    // In production, this would save to Corva datasets
  };

  // Convert quiz question to modal format
  const convertQuizToModalFormat = (quiz: QuizQuestion): QuizModalQuestion => {
    return {
      id: quiz.id,
      question: quiz.question,
      type: quiz.type,
      explanation: quiz.explanation,
      options: quiz.choices.map((choice: QuizChoice) => ({
        id: choice.id,
        text: choice.text,
        isCorrect: quiz.type === 'single' 
          ? choice.id === quiz.correctAnswer
          : (quiz.correctAnswers || []).includes(choice.id),
        explanation: choice.id === quiz.correctAnswer || (quiz.correctAnswers || []).includes(choice.id)
          ? quiz.explanation
          : undefined
      }))
    };
  };

  // Get tech stack logo for subsection title
  const getTechStackLogo = (title: string): string | null => {
    const titleLower = title.toLowerCase();
    const matchedTool = Object.keys(TECH_STACK_LOGOS).find(tool => titleLower.includes(tool));
    return matchedTool ? TECH_STACK_LOGOS[matchedTool] : null;
  };

  // Render home view with module list
  const renderHome = () => (
    <div className={styles.homeContainer}>
      <div className={styles.header}>
        <h1 className={styles.title}>Operations Training</h1>
        <p className={styles.subtitle}>
          Welcome{currentUser ? `, ${currentUser.first_name}` : ''}! Select a training module to begin.
        </p>
      </div>

      <div className={styles.moduleGrid}>
        {MODULE_INDEX.map((module) => (
          <div 
            key={module.moduleSlug}
            className={styles.moduleCard}
            onClick={() => setView({ type: 'module', moduleSlug: module.moduleSlug })}
          >
            <h3 className={styles.moduleTitle}>{module.title}</h3>
            <p className={styles.moduleDescription}>{module.description}</p>
            <span className={styles.moduleArrow}>→</span>
          </div>
        ))}
      </div>
    </div>
  );

  // Render module view with section list
  const renderModule = () => {
    if (loading) {
      return <div className={styles.loading}>Loading module...</div>;
    }

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

    return (
      <div className={styles.moduleContainer}>
        <button 
          className={styles.backButton}
          onClick={() => setView({ type: 'home' })}
        >
          ← Back to Modules
        </button>

        <h1 className={styles.moduleHeading}>{moduleData.title}</h1>

        <div className={styles.sectionList}>
          {moduleData.sections.map((section, index) => (
            <div 
              key={section.id}
              className={styles.sectionCard}
              onClick={() => setView({ 
                type: 'section', 
                moduleSlug: view.type !== 'home' ? view.moduleSlug : '',
                sectionId: section.id 
              })}
            >
              <span className={styles.sectionNumber}>{index + 1}</span>
              <div className={styles.sectionInfo}>
                <h4 className={styles.sectionTitle}>{section.title}</h4>
                {section.quiz && section.quiz.length > 0 && (
                  <span className={styles.quizBadge}>
                    {section.quiz.length} Quiz Question{section.quiz.length > 1 ? 's' : ''}
                  </span>
                )}
              </div>
              <span className={styles.sectionArrow}>→</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Render section view with content and quiz
  const renderSection = () => {
    if (loading || !moduleData) {
      return <div className={styles.loading}>Loading...</div>;
    }

    const sectionId = view.type === 'section' ? view.sectionId : '';
    const section = moduleData.sections.find(s => s.id === sectionId);

    if (!section) {
      return (
        <div className={styles.error}>
          <p>Section not found</p>
          <button 
            className={styles.backButton}
            onClick={() => setView({ type: 'module', moduleSlug: view.type !== 'home' ? view.moduleSlug : '' })}
          >
            ← Back to Module
          </button>
        </div>
      );
    }

    const currentIndex = moduleData.sections.findIndex(s => s.id === sectionId);
    const prevSection = currentIndex > 0 ? moduleData.sections[currentIndex - 1] : null;
    const nextSection = currentIndex < moduleData.sections.length - 1 ? moduleData.sections[currentIndex + 1] : null;

    return (
      <div className={styles.sectionContainer}>
        <button 
          className={styles.backButton}
          onClick={() => setView({ type: 'module', moduleSlug: view.type !== 'home' ? view.moduleSlug : '' })}
        >
          ← Back to {moduleData.title}
        </button>

        <h1 className={styles.sectionHeading}>{section.title}</h1>

        <div className={styles.sectionContent}>
          <RichContentRenderer 
            blocks={section.content as any[]}
            images={section.images as any[]}
            sectionId={section.id}
          />

          {/* Render subsections if any */}
          {section.subsections && section.subsections.map((subsection) => {
            const logoSrc = getTechStackLogo(subsection.title);
            return (
              <div key={subsection.id} id={`subsection-${subsection.id}`} className={styles.subsection}>
                <div className={styles.subsectionHeader}>
                  {logoSrc && (
                    <img
                      src={logoSrc}
                      alt={`${subsection.title} logo`}
                      className={styles.subsectionLogo}
                    />
                  )}
                  <h2 className={styles.subsectionTitle}>{subsection.title}</h2>
                </div>
                <RichContentRenderer 
                  blocks={subsection.content as any[]}
                  images={subsection.images as any[]}
                  sectionId={subsection.id}
                />
              </div>
            );
          })}

          {/* Quiz Button - opens modal */}
          {section.quiz && section.quiz.length > 0 && (
            <div className={styles.quizSection}>
              <button
                className={styles.quizButton}
                onClick={() => {
                  setCurrentQuizSection(section);
                  setIsQuizModalOpen(true);
                }}
              >
                Test your knowledge on {section.title}
              </button>
            </div>
          )}
        </div>

        {/* Navigation buttons */}
        <div className={styles.sectionNav}>
          {prevSection && (
            <button 
              className={styles.navButton}
              onClick={() => setView({ 
                type: 'section', 
                moduleSlug: view.type !== 'home' ? view.moduleSlug : '',
                sectionId: prevSection.id 
              })}
            >
              ← {prevSection.title}
            </button>
          )}
          {nextSection && (
            <button 
              className={`${styles.navButton} ${styles.navButtonNext}`}
              onClick={() => setView({ 
                type: 'section', 
                moduleSlug: view.type !== 'home' ? view.moduleSlug : '',
                sectionId: nextSection.id 
              })}
            >
              {nextSection.title} →
            </button>
          )}
        </div>
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
      <div className={styles.appContainer}>
        {renderContent()}
      </div>
      
      {/* Quiz Modal */}
      {currentQuizSection && currentQuizSection.quiz && (
        <SectionQuizModal
          isOpen={isQuizModalOpen}
          onClose={() => {
            setIsQuizModalOpen(false);
            setCurrentQuizSection(null);
          }}
          sectionTitle={currentQuizSection.title}
          quizzes={currentQuizSection.quiz.map(convertQuizToModalFormat)}
          onQuizComplete={(passed, percentage) => {
            console.log(`Quiz complete: ${passed ? 'Passed' : 'Failed'} with ${percentage}%`);
          }}
        />
      )}
    </AppContainer>
  );
}

// Important: Do not change root component default export (App.js). Use it as container
// for your App. It's required to make build and zip scripts work as expected;
export default App;
