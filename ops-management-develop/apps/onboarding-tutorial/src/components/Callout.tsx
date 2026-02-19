import React from 'react';
import { parseInlineFormatting } from './formatting-utils';
import styles from './Callout.module.css';

interface CalloutProps {
  kind: 'note' | 'warning' | 'best_practice';
  children: React.ReactNode;
  title?: string;
}

const kindConfig = {
  note: {
    icon: 'ℹ️',
    title: 'Note',
    className: styles.note
  },
  warning: {
    icon: '⚠️',
    title: 'Warning',
    className: styles.warning
  },
  best_practice: {
    icon: '✓',
    title: 'Best Practice',
    className: styles.bestPractice
  }
};

export default function Callout({ kind, children, title }: CalloutProps) {
  const config = kindConfig[kind];
  const displayTitle = title || config.title;

  return (
    <div className={`${styles.callout} ${config.className}`}>
      <div className={styles.header}>
        <span className={styles.icon}>{config.icon}</span>
        <span className={styles.title}>{displayTitle}</span>
      </div>
      <div className={styles.content}>
        {typeof children === 'string' ? parseInlineFormatting(children) : children}
      </div>
    </div>
  );
}
