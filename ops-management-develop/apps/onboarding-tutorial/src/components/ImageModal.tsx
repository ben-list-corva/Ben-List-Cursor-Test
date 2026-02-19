import React, { useEffect, useCallback } from 'react';
import styles from './ImageModal.module.css';

interface ImageModalProps {
  isOpen: boolean;
  onClose: () => void;
  src: string;
  alt: string;
  caption?: string;
  figureNumber?: string;
}

export default function ImageModal({
  isOpen,
  onClose,
  src,
  alt,
  caption,
  figureNumber,
}: ImageModalProps) {
  // Handle escape key to close modal
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

  if (!isOpen) return null;

  return (
    <div 
      className={styles.overlay} 
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className={styles.modal}>
        <button className={styles.closeButton} onClick={onClose} aria-label="Close image">
          ×
        </button>
        <div className={styles.imageContainer}>
          <img
            src={src}
            alt={alt}
            className={styles.image}
          />
        </div>
        {(caption || figureNumber) && (
          <div className={styles.caption}>
            {figureNumber && <strong>{figureNumber}:</strong>} {caption}
          </div>
        )}
      </div>
    </div>
  );
}
