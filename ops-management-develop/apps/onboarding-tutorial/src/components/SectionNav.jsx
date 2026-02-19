import React from 'react';

/**
 * SectionNav - Navigation between sections (prev/next)
 * Always appears at the bottom of section content.
 * Has explicit z-index to ensure it's never covered by images.
 */
export default function SectionNav({ 
  prevSection, 
  nextSection, 
  nextSectionUnlocked,
  onNavigate,
}) {
  const navContainerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '1rem',
    marginTop: '3rem',
    padding: '1.5rem 0',
    borderTop: '2px solid rgba(0, 188, 212, 0.2)',
    position: 'relative',
    zIndex: 5, // Above images but below header
    background: 'transparent',
  };

  const buttonBaseStyle = {
    background: '#161b22',
    border: '1px solid rgba(0, 188, 212, 0.3)',
    borderRadius: '8px',
    padding: '1rem 1.5rem',
    color: '#e0e0e0',
    fontSize: '0.9375rem',
    cursor: 'pointer',
    transition: 'all 0.2s',
    maxWidth: '45%',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  };

  const lockedButtonStyle = {
    ...buttonBaseStyle,
    opacity: 0.6,
    cursor: 'not-allowed',
    borderColor: 'rgba(255, 255, 255, 0.12)',
    color: 'rgba(255, 255, 255, 0.5)',
  };

  const handleHover = (e, isHover) => {
    if (e.target.disabled) return;
    e.target.style.borderColor = isHover ? '#00bcd4' : 'rgba(0, 188, 212, 0.3)';
    e.target.style.background = isHover ? 'rgba(0, 188, 212, 0.1)' : '#161b22';
  };

  return (
    <nav style={navContainerStyle}>
      {prevSection ? (
        <button 
          style={buttonBaseStyle}
          onClick={() => onNavigate(prevSection.id)}
          onMouseEnter={(e) => handleHover(e, true)}
          onMouseLeave={(e) => handleHover(e, false)}
        >
          ← {prevSection.title}
        </button>
      ) : (
        <div /> // Spacer to maintain flex layout
      )}
      
      {nextSection && (
        <button 
          style={nextSectionUnlocked ? { ...buttonBaseStyle, marginLeft: 'auto' } : { ...lockedButtonStyle, marginLeft: 'auto' }}
          onClick={() => nextSectionUnlocked && onNavigate(nextSection.id)}
          disabled={!nextSectionUnlocked}
          onMouseEnter={(e) => nextSectionUnlocked && handleHover(e, true)}
          onMouseLeave={(e) => nextSectionUnlocked && handleHover(e, false)}
        >
          {nextSectionUnlocked ? (
            <>{nextSection.title} →</>
          ) : (
            <>🔒 Complete quiz to unlock</>
          )}
        </button>
      )}
    </nav>
  );
}
