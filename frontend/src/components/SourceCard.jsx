import React, { useState } from 'react';
import { ChevronDown, FileText } from 'lucide-react';

export default function SourceCard({ sources }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!sources || sources.length === 0) return null;

  const getRelevanceClass = (score) => {
    if (score >= 0.7) return 'high';
    if (score >= 0.4) return 'medium';
    return 'low';
  };

  const getRelevanceLabel = (score) => {
    if (score >= 0.7) return 'High';
    if (score >= 0.4) return 'Medium';
    return 'Low';
  };

  return (
    <div className="sources-container">
      <button
        className={`sources-toggle ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <FileText size={13} />
        {sources.length} source{sources.length !== 1 ? 's' : ''} found
        <ChevronDown size={13} />
      </button>

      {isOpen && (
        <div className="sources-list">
          {sources.map((source, idx) => (
            <div key={idx} className="source-card">
              <div className="source-card-header">
                <span className="source-card-file">
                  <FileText size={13} />
                  {source.filename}
                  {source.page && ` • Page ${source.page}`}
                </span>
                <span
                  className={`source-card-relevance ${getRelevanceClass(source.relevance_score)}`}
                >
                  {getRelevanceLabel(source.relevance_score)}{' '}
                  ({(source.relevance_score * 100).toFixed(0)}%)
                </span>
              </div>
              <div className="source-card-text">{source.content}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
