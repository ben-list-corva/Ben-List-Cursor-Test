import React from 'react';
import { parseInlineFormatting } from './formatting-utils';
import styles from './NumberedList.module.css';

interface NumberedListProps {
  items: string[];
  className?: string;
}

export default function NumberedList({ items, className }: NumberedListProps) {
  if (items.length === 0) return null;

  return (
    <ol className={`${styles.list} ${className || ''}`}>
      {items.map((item, index) => (
        <li key={index} className={styles.listItem}>
          {parseInlineFormatting(item)}
        </li>
      ))}
    </ol>
  );
}
