import React from 'react';

/**
 * Parse inline formatting like **bold**, *italic*, and [links](url)
 */
export function parseInlineFormatting(text) {
  if (!text || typeof text !== 'string') return text;
  
  const parts = [];
  const remaining = text;
  let keyIndex = 0;
  
  // Simple regex-based parsing
  const patterns = [
    // Bold: **text**
    { regex: /\*\*([^*]+)\*\*/g, render: (match, p1) => <strong key={keyIndex++}>{p1}</strong> },
    // Italic: *text*
    { regex: /\*([^*]+)\*/g, render: (match, p1) => <em key={keyIndex++}>{p1}</em> },
    // Links: [text](url)
    { regex: /\[([^\]]+)\]\(([^)]+)\)/g, render: (match, p1, p2) => <a key={keyIndex++} href={p2} target="_blank" rel="noopener noreferrer">{p1}</a> },
  ];
  
  // For simplicity, just handle basic cases
  // This could be made more sophisticated with a proper parser
  
  // Check for links
  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let linkMatch;
  let lastIndex = 0;
  const result = [];
  
  while ((linkMatch = linkRegex.exec(text)) !== null) {
    if (linkMatch.index > lastIndex) {
      result.push(text.substring(lastIndex, linkMatch.index));
    }
    result.push(
      <a key={keyIndex++} href={linkMatch[2]} target="_blank" rel="noopener noreferrer">
        {linkMatch[1]}
      </a>
    );
    lastIndex = linkMatch.index + linkMatch[0].length;
  }
  
  if (lastIndex < text.length) {
    result.push(text.substring(lastIndex));
  }
  
  if (result.length === 0) {
    return text;
  }
  
  return result;
}

export default { parseInlineFormatting };
