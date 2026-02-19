import React from 'react';

/**
 * Parse inline formatting (bold, italic, links) from text
 * Adapted for Corva Dev Center app
 */
export function parseInlineFormatting(text: string): React.ReactNode[] {
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  
  // Match bold **text**, italic *text*, and links [text](url)
  const regex = /(\*\*([^*]+)\*\*|\*([^*]+)\*|\[([^\]]+)\]\(([^)]+)\))/g;
  let match;
  
  while ((match = regex.exec(text)) !== null) {
    // Add text before match
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }
    
    // Add formatted content
    if (match[1].startsWith('**')) {
      // Bold
      parts.push(<strong key={match.index}>{match[2]}</strong>);
    } else if (match[1].startsWith('*') && !match[1].startsWith('**')) {
      // Italic
      parts.push(<em key={match.index}>{match[3]}</em>);
    } else if (match[1].startsWith('[')) {
      // Link
      parts.push(
        <a 
          key={match.index} 
          href={match[5]} 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ color: '#00bcd4', textDecoration: 'underline' }}
        >
          {match[4]}
        </a>
      );
    }
    
    lastIndex = match.index + match[0].length;
  }
  
  // Add remaining text
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }
  
  return parts.length > 0 ? parts : [text];
}
