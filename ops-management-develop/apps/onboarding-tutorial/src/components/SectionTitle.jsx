import React from 'react';
import styles from './SectionTitle.module.css';

export default function SectionTitle({ level = 2, id, children }) {
  const Tag = `h${level}`;
  const className = styles[`h${level}`] || styles.h2;
  
  return (
    <Tag id={id} className={className}>
      {children}
    </Tag>
  );
}
