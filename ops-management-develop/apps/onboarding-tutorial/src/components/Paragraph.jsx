import React from 'react';
import styles from './Paragraph.module.css';
import { parseInlineFormatting } from './formatting-utils';

export default function Paragraph({ children }) {
  const content = typeof children === 'string' ? parseInlineFormatting(children) : children;
  
  return (
    <p className={styles.paragraph}>
      {content}
    </p>
  );
}
