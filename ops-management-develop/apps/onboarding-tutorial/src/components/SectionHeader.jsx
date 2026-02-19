import React from 'react';

/**
 * SectionHeader - Reusable header component for all sections
 * Contains:
 * - Back navigation link
 * - Section title with decorative background
 * - Optional subtitle
 * 
 * The decorative rectangle is contained within this header only,
 * never overlapping content below.
 */
export default function SectionHeader({ 
  title, 
  subtitle,
  backLabel, 
  onBackClick,
}) {
  const headerContainerStyle = {
    position: 'relative',
    marginBottom: '2rem',
    zIndex: 10, // Header always above content
  };

  const backButtonStyle = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5rem',
    background: 'transparent',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    borderRadius: '6px',
    padding: '0.5rem 1rem',
    color: 'rgba(255, 255, 255, 0.7)',
    fontSize: '0.9375rem',
    cursor: 'pointer',
    transition: 'all 0.2s',
    marginBottom: '1.5rem',
  };

  const titleContainerStyle = {
    position: 'relative',
    padding: '1.5rem 2rem',
    background: '#161b22',
    borderRadius: '12px',
    border: '1px solid rgba(0, 188, 212, 0.3)',
  };

  const titleStyle = {
    fontSize: '1.75rem',
    fontWeight: 700,
    color: '#00bcd4',
    margin: 0,
    position: 'relative',
    zIndex: 2,
  };

  const subtitleStyle = {
    fontSize: '1rem',
    color: 'rgba(255, 255, 255, 0.6)',
    marginTop: '0.5rem',
    position: 'relative',
    zIndex: 2,
  };

  return (
    <header style={headerContainerStyle}>
      {backLabel && onBackClick && (
        <button 
          style={backButtonStyle}
          onClick={onBackClick}
          onMouseEnter={(e) => {
            e.target.style.borderColor = '#00bcd4';
            e.target.style.color = '#00bcd4';
          }}
          onMouseLeave={(e) => {
            e.target.style.borderColor = 'rgba(255, 255, 255, 0.2)';
            e.target.style.color = 'rgba(255, 255, 255, 0.7)';
          }}
        >
          ← {backLabel}
        </button>
      )}
      
      <div style={titleContainerStyle}>
        <h1 style={titleStyle}>{title}</h1>
        {subtitle && <p style={subtitleStyle}>{subtitle}</p>}
      </div>
    </header>
  );
}
