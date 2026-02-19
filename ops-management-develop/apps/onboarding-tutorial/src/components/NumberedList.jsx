import React from 'react';
import styles from './NumberedList.module.css';
import { parseInlineFormatting } from './formatting-utils';

export default function NumberedList({ items }) {
  return (
    <ol className={styles.list}>
      {items.map((item, index) => (
        <li key={index} className={styles.item}>
          {typeof item === 'string' ? parseInlineFormatting(item) : item}
        </li>
      ))}
    </ol>
  );
}
