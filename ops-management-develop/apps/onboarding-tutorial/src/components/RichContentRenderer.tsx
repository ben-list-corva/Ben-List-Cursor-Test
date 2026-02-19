import React from 'react';
import SectionTitle from './SectionTitle';
import Paragraph from './Paragraph';
import BulletedList from './BulletedList';
import NumberedList from './NumberedList';
import Callout from './Callout';
import Figure from './Figure';
import { parseInlineFormatting } from './formatting-utils';

// Types for training content blocks
interface TrainingBlock {
  type: 'text' | 'callout' | 'checklist';
  body?: string;
  kind?: 'note' | 'warning' | 'best_practice';
  items?: Array<{ id: string; text: string }>;
  checklistId?: string;
}

interface ImageReference {
  id: string;
  localPath: string;
  altText?: string;
  caption?: string;
  figureNumber?: string;
}

interface RichContentRendererProps {
  blocks: TrainingBlock[];
  images?: ImageReference[];
  sectionId?: string;
}

/**
 * Get the correct image URL for the Dev Center app
 */
function getImageUrl(src: string): string {
  if (src.startsWith('http://') || src.startsWith('https://')) {
    return src;
  }
  if (src.startsWith('/training-assets/')) {
    return src.replace('/training-assets/', './assets/training/');
  }
  return src;
}

/**
 * Detect if text contains a callout pattern
 */
function detectCallout(text: string): { kind: 'note' | 'warning' | 'best_practice'; content: string } | null {
  const lowerText = text.toLowerCase().trim();
  
  // Best practice patterns only (notes and warnings disabled per user request)
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
function detectList(text: string): { type: 'bullet' | 'numbered'; items: string[] } | null {
  const lines = text.split('\n').map(l => l.trim()).filter(l => l);
  
  if (lines.length < 2) return null;
  
  // Check for bullet list (starts with -, •, or *)
  const bulletPattern = /^[-•*]\s+(.+)$/;
  const bulletMatches = lines.filter(line => bulletPattern.test(line));
  
  if (bulletMatches.length >= 2 && bulletMatches.length >= lines.length * 0.8) {
    const items = bulletMatches.map(line => {
      const match = line.match(bulletPattern);
      return match ? match[1] : line;
    });
    return { type: 'bullet', items };
  }
  
  // Check for numbered list (starts with number.)
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
function parseTextBlock(block: TrainingBlock, images?: ImageReference[]): React.ReactNode[] {
  const body = block.body || '';
  if (!body) return [];
  
  const elements: React.ReactNode[] = [];
  
  // Check for image references - supports both [IMAGE:path] and [IMAGE:path:figureNumber]
  const imageRegex = /\[IMAGE:([^\]\s]+?)(?::([^\]]+))?\]/g;
  const parts: Array<{ type: 'text' | 'image'; content: string; figure?: string }> = [];
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
  
  // Process each part
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
            src={getImageUrl(imgRef.localPath)}
            alt={imgRef.altText || part.figure || 'Training image'}
            caption={imgRef.caption}
            figureNumber={imgRef.figureNumber}
          />
        );
      } else {
        elements.push(
          <Figure
            key={`img-direct-${String(elements.length)}`}
            src={getImageUrl(part.content)}
            alt={part.figure || 'Training image'}
          />
        );
      }
    } else {
      const text = part.content.trim();
      if (!text) continue;
      
      // Check for callout
      const callout = detectCallout(text);
      if (callout) {
        elements.push(
          <Callout key={`callout-${String(elements.length)}`} kind={callout.kind}>
            {callout.content}
          </Callout>
        );
        continue;
      }
      
      // Check for list
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
      
      // Check for heading (starts with ##, ###, ####)
      const headingMatch = text.match(/^(#{2,4})\s+(.+)$/m);
      if (headingMatch) {
        const level = headingMatch[1].length as 2 | 3 | 4;
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
      
      // Regular paragraph
      elements.push(
        <Paragraph key={`para-${String(elements.length)}`}>
          {text}
        </Paragraph>
      );
    }
  }
  
  return elements;
}

export default function RichContentRenderer({ blocks, images, sectionId }: RichContentRendererProps) {
  const elements: React.ReactNode[] = [];
  
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
        // Skip warning and note callouts per user request
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
        // Fallback: render as text
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
