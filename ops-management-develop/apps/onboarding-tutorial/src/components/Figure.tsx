import React, { useState } from 'react';
import ImageModal from './ImageModal';
import styles from './Figure.module.css';

interface FigureProps {
  src: string;
  alt: string;
  caption?: string;
  figureNumber?: string;
  className?: string;
}

/**
 * Get the correct image URL for the Dev Center app
 * Images are bundled in src/assets/training/
 */
function getImageUrl(src: string): string {
  // If already a full URL, return as-is
  if (src.startsWith('http://') || src.startsWith('https://')) {
    return src;
  }
  
  // For local paths, resolve from assets folder
  // The build process will copy images from shared/assets/training-images/
  if (src.startsWith('/training-assets/')) {
    return src.replace('/training-assets/', './assets/training/');
  }
  
  return src;
}

export default function Figure({ src, alt, caption, figureNumber, className }: FigureProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const isPlaceholder = src.includes('placeholder-');
  const imageUrl = getImageUrl(src);

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
              const target = e.target as HTMLImageElement;
              target.style.display = 'none';
              const placeholder = document.createElement('div');
              placeholder.className = styles.placeholder;
              placeholder.innerHTML = `<p><strong>${figureNumber || 'Figure'}</strong></p><p class="${styles.placeholderText}">Image unavailable</p>`;
              target.parentElement?.appendChild(placeholder);
            }}
          />
          <div className={styles.expandHint}>
            <span>Click to expand</span>
          </div>
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
        src={imageUrl}
        alt={alt}
        caption={caption}
        figureNumber={figureNumber}
      />
    </>
  );
}
