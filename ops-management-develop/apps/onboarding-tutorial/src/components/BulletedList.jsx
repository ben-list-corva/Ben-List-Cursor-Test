import React from 'react';
import styles from './BulletedList.module.css';
import { parseInlineFormatting } from './formatting-utils';

export default function BulletedList({ items }) {
  return (
    <ul className={styles.list}>
      {items.map((item, index) => (
        <li key={index} className={styles.item}>
          {typeof item === 'string' ? parseInlineFormatting(item) : item}
        </li>
      ))}
    </ul>
  );
}
