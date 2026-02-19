import React, { createElement } from 'react';
import styles from './SectionTitle.module.css';

interface SectionTitleProps {
  level: 2 | 3 | 4;
  children: React.ReactNode;
  id?: string;
}

export default function SectionTitle({ level, children, id }: SectionTitleProps) {
  return createElement(
    `h${level}`,
    {
      id,
      className: `${styles.sectionTitle} ${styles[`level${level}`]}`,
    },
    children
  );
}
