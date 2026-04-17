import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Brain, User, Shield } from 'lucide-react';
import SourceCard from './SourceCard';

export default function MessageBubble({ message }) {
  const { role, content, sources, confidence } = message;
  const isUser = role === 'user';

  const getConfidenceClass = (score) => {
    if (score >= 0.7) return 'high';
    if (score >= 0.4) return 'medium';
    return 'low';
  };

  const getConfidenceLabel = (score) => {
    if (score >= 0.7) return 'High confidence';
    if (score >= 0.4) return 'Medium confidence';
    return 'Low confidence';
  };

  return (
    <div className={`message ${role}`}>
      <div className="message-avatar">
        {isUser ? <User size={16} /> : <Brain size={16} />}
      </div>
      <div className="message-body">
        <div className="message-content">
          {isUser ? (
            content
          ) : (
            <ReactMarkdown>{content}</ReactMarkdown>
          )}
        </div>

        {/* Confidence badge for assistant messages */}
        {!isUser && confidence !== undefined && confidence !== null && (
          <span className={`confidence-badge ${getConfidenceClass(confidence)}`}>
            <Shield size={11} />
            {getConfidenceLabel(confidence)} ({(confidence * 100).toFixed(0)}%)
          </span>
        )}

        {/* Source citations */}
        {!isUser && sources && sources.length > 0 && (
          <SourceCard sources={sources} />
        )}
      </div>
    </div>
  );
}
