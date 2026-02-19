import React from 'react';
import SectionTitle from './SectionTitle';
import Paragraph from './Paragraph';
import BulletedList from './BulletedList';
import NumberedList from './NumberedList';
import Callout from './Callout';
import Figure from './Figure';
import { parseInlineFormatting } from './formatting-utils';

/**
 * Get the correct image URL for the Dev Center app
 * Prioritizes Google Docs URLs over local paths
 */
function getImageUrl(src, googleDocsUrl) {
  if (googleDocsUrl && (googleDocsUrl.startsWith('http://') || googleDocsUrl.startsWith('https://'))) {
    return googleDocsUrl;
  }
  
  if (src.startsWith('http://') || src.startsWith('https://')) {
    return src;
  }
  
  return src;
}

/**
 * Detect if text contains a callout pattern
 */
function detectCallout(text) {
  const lowerText = text.toLowerCase().trim();
  
  if (lowerText.startsWith('best practice:') || lowerText.startsWith('best practice -') || 
      lowerText.startsWith('**best practice:**') || lowerText.startsWith('tip:') || 
      lowerText.startsWith('**tip:**')) {
    const content = text.replace(/^(\*\*)?(best practice|tip)(\*\*)?:?\s*-?\s*/i, '').trim();
    return { kind: 'best_practice', content };
  }
  
  return null;
}

/**
 * Detect if text is a list (bulleted or numbered)
 */
function detectList(text) {
  const lines = text.split('\n').map(l => l.trim()).filter(l => l);
  
  if (lines.length < 2) return null;
  
  const bulletPattern = /^[-•*]\s+(.+)$/;
  const bulletMatches = lines.filter(line => bulletPattern.test(line));
  
  if (bulletMatches.length >= 2 && bulletMatches.length >= lines.length * 0.8) {
    const items = bulletMatches.map(line => {
      const match = line.match(bulletPattern);
      return match ? match[1] : line;
    });
    return { type: 'bullet', items };
  }
  
  const numberedPattern = /^\d+[.)]\s+(.+)$/;
  const numberedMatches = lines.filter(line => numberedPattern.test(line));
  
  if (numberedMatches.length >= 2 && numberedMatches.length >= lines.length * 0.8) {
    const items = numberedMatches.map(line => {
      const match = line.match(numberedPattern);
      return match ? match[1] : line;
    });
    return { type: 'numbered', items };
  }
  
  return null;
}

/**
 * Parse text block into structured content
 */
function parseTextBlock(block, images) {
  const body = block.body || '';
  if (!body) return [];
  
  const elements = [];
  
  const imageRegex = /\[IMAGE:([^\]\s]+?)(?::([^\]]+))?\]/g;
  const parts = [];
  let lastIndex = 0;
  let match;
  
  while ((match = imageRegex.exec(body)) !== null) {
    if (match.index > lastIndex) {
      parts.push({
        type: 'text',
        content: body.substring(lastIndex, match.index),
      });
    }
    parts.push({
      type: 'image',
      content: match[1],
      figure: match[2],
    });
    lastIndex = match.index + match[0].length;
  }
  
  if (lastIndex < body.length) {
    parts.push({
      type: 'text',
      content: body.substring(lastIndex),
    });
  }
  
  for (const part of parts) {
    if (part.type === 'image') {
      const imgRef = images?.find(
        (img) => img.localPath === part.content || 
                 img.localPath.endsWith(part.content.split('/').pop() || '') ||
                 (part.figure && img.figureNumber === part.figure)
      );
      
      if (imgRef) {
        elements.push(
          <Figure
            key={`img-${imgRef.id}`}
            src={imgRef.localPath}
            url={imgRef.url}
            alt={imgRef.altText || part.figure || 'Training image'}
            caption={imgRef.caption}
            figureNumber={imgRef.figureNumber}
          />
        );
      } else {
        elements.push(
          <Figure
            key={`img-direct-${String(elements.length)}`}
            src={part.content}
            alt={part.figure || 'Training image'}
          />
        );
      }
    } else {
      const text = part.content.trim();
      if (!text) continue;
      
      const callout = detectCallout(text);
      if (callout) {
        elements.push(
          <Callout key={`callout-${String(elements.length)}`} kind={callout.kind}>
            {callout.content}
          </Callout>
        );
        continue;
      }
      
      const list = detectList(text);
      if (list) {
        if (list.type === 'bullet') {
          elements.push(
            <BulletedList key={`list-${String(elements.length)}`} items={list.items} />
          );
        } else {
          elements.push(
            <NumberedList key={`list-${String(elements.length)}`} items={list.items} />
          );
        }
        continue;
      }
      
      const headingMatch = text.match(/^(#{2,4})\s+(.+)$/m);
      if (headingMatch) {
        const level = headingMatch[1].length;
        const headingText = headingMatch[2];
        const headingId = headingText
          .toLowerCase()
          .replace(/[^\w\s-]/g, '')
          .replace(/\s+/g, '-')
          .substring(0, 50);
        
        elements.push(
          <SectionTitle key={`heading-${String(elements.length)}`} level={level} id={headingId}>
            {parseInlineFormatting(headingText)}
          </SectionTitle>
        );
        
        const remainingText = text.replace(/^#{2,4}\s+.+$/m, '').trim();
        if (remainingText) {
          elements.push(
            <Paragraph key={`para-after-heading-${String(elements.length)}`}>
              {remainingText}
            </Paragraph>
          );
        }
        continue;
      }
      
      elements.push(
        <Paragraph key={`para-${String(elements.length)}`}>
          {text}
        </Paragraph>
      );
    }
  }
  
  return elements;
}

export default function RichContentRenderer({ blocks, images, sectionId }) {
  const elements = [];
  
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];
    
    switch (block.type) {
      case 'text': {
        const textElements = parseTextBlock(block, images);
        if (textElements) {
          elements.push(...textElements);
        }
        break;
      }
        
      case 'callout': {
        const calloutKind = block.kind || 'note';
        if (calloutKind === 'warning' || calloutKind === 'note') {
          continue;
        }
        elements.push(
          <Callout key={`callout-${String(i)}`} kind={calloutKind}>
            {block.body || ''}
          </Callout>
        );
        break;
      }
        
      default: {
        const fallbackText = JSON.stringify(block);
        elements.push(
          <Paragraph key={`fallback-${String(i)}`}>
            {fallbackText}
          </Paragraph>
        );
      }
    }
  }
  
  return (
    <div className="rich-content" style={{ width: '100%', maxWidth: '100%' }}>
      {elements}
    </div>
  );
}
