import React from 'react';
import { parseInlineFormatting } from './formatting-utils';
import styles from './BulletedList.module.css';

interface BulletedListProps {
  items: string[];
  className?: string;
}

export default function BulletedList({ items, className }: BulletedListProps) {
  if (items.length === 0) return null;

  return (
    <ul className={`${styles.list} ${className || ''}`}>
      {items.map((item, index) => (
        <li key={index} className={styles.listItem}>
          {parseInlineFormatting(item)}
        </li>
      ))}
    </ul>
  );
}
