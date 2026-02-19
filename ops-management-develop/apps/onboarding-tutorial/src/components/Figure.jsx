import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import styles from './Figure.module.css';
import { getImageUrl as getBundledImageUrl } from '../imageRegistry';

/**
 * Get the correct image URL for the Dev Center app
 * Prioritizes LOCAL BUNDLED images over Google Docs URLs for reliability
 */
function getImageUrl(src, googleDocsUrl) {
  // First try to get the local bundled image (most reliable)
  if (src) {
    const bundledUrl = getBundledImageUrl(src);
    if (bundledUrl) {
      return bundledUrl;
    }
  }
  
  // Fall back to Google Docs URL if local image not found
  if (googleDocsUrl && (googleDocsUrl.startsWith('http://') || googleDocsUrl.startsWith('https://'))) {
    return googleDocsUrl;
  }
  
  // Fall back to src if it's a full URL
  if (src && src.startsWith && (src.startsWith('http://') || src.startsWith('https://'))) {
    return src;
  }
  
  return src;
}

// Image Modal for expanded view - uses Portal to render to document body
function ImageModal({ isOpen, onClose, imageUrl, altText, caption, figureNumber }) {
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

  if (!isOpen) return null;

  // Use React Portal to render modal to document body, escaping any stacking context
  return ReactDOM.createPortal(
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.85)',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 2147483647, // Maximum z-index value
        padding: '1rem',
        cursor: 'zoom-out',
      }}
      onClick={onClose}
    >
      <div style={{ position: 'relative', maxWidth: '95vw', maxHeight: '95vh' }}>
        <button 
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '-40px',
            right: 0,
            background: 'transparent',
            border: 'none',
            fontSize: '36px',
            color: 'white',
            cursor: 'pointer',
            padding: 0,
            lineHeight: 1,
          }}
        >×</button>
        <img
          src={imageUrl}
          alt={altText}
          style={{ 
            maxWidth: '95vw', 
            maxHeight: '85vh', 
            width: 'auto',
            height: 'auto',
            objectFit: 'contain',
            borderRadius: '8px',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
          }}
          onClick={(e) => e.stopPropagation()}
        />
        {(caption || figureNumber) && (
          <div style={{
            marginTop: '1rem',
            padding: '0.5rem 1.5rem',
            background: 'rgba(0, 0, 0, 0.7)',
            borderRadius: '8px',
            color: 'white',
            fontSize: '0.875rem',
            textAlign: 'center',
          }}>
            {figureNumber && <strong>{figureNumber}: </strong>}{caption}
          </div>
        )}
      </div>
    </div>,
    document.body
  );
}

export default function Figure({ src, alt, caption, figureNumber, className, url }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const isPlaceholder = src && src.includes && src.includes('placeholder-');
  const imageUrl = getImageUrl(src, url);

  if (isPlaceholder) {
    return (
      <div className={`${styles.container} ${className || ''}`}>
        <div className={styles.placeholder}>
          <p><strong>{figureNumber || 'Figure'}</strong></p>
          <p className={styles.placeholderText}>Image placeholder</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <figure className={`${styles.container} ${className || ''}`}>
        <div 
          className={styles.imageWrapper}
          onClick={() => setIsModalOpen(true)}
          style={{ cursor: 'zoom-in' }}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              setIsModalOpen(true);
            }
          }}
        >
          <img
            src={imageUrl}
            alt={alt}
            className={styles.image}
            onError={(e) => {
              const target = e.target;
              target.style.display = 'none';
              const placeholder = document.createElement('div');
              placeholder.className = styles.placeholder;
              placeholder.innerHTML = `<p><strong>${figureNumber || 'Figure'}</strong></p><p class="${styles.placeholderText}">Image unavailable</p>`;
              target.parentElement?.appendChild(placeholder);
            }}
          />
          <div className={styles.expandHint}>Click to expand</div>
        </div>
        {(caption || figureNumber) && (
          <figcaption className={styles.caption}>
            {figureNumber && <strong>{figureNumber}:</strong>} {caption}
          </figcaption>
        )}
      </figure>
      
      <ImageModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        imageUrl={imageUrl}
        altText={alt}
        caption={caption}
        figureNumber={figureNumber}
      />
    </>
  );
}
