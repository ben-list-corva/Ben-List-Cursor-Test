import React from 'react';
import styles from './Callout.module.css';
import { parseInlineFormatting } from './formatting-utils';

export default function Callout({ kind = 'note', children }) {
  const kindClass = styles[kind] || styles.note;
  
  const content = typeof children === 'string' ? parseInlineFormatting(children) : children;
  
  return (
    <div className={`${styles.callout} ${kindClass}`}>
      <div className={styles.content}>
        {content}
      </div>
    </div>
  );
}
