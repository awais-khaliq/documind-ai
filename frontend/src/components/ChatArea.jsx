import React, { useRef, useEffect, useState } from 'react';
import {
  Send,
  Brain,
  Upload,
  Search,
  FileText,
  Menu,
} from 'lucide-react';
import MessageBubble from './MessageBubble';

export default function ChatArea({
  messages,
  isLoading,
  onSendMessage,
  hasDocuments,
  onToggleSidebar,
}) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height =
        Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  }, [input]);

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    onSendMessage(trimmed);
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const showWelcome = messages.length === 0 && !isLoading;

  return (
    <div className="main-content">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-header-left">
          <button
            className="mobile-menu-btn"
            onClick={onToggleSidebar}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              padding: 4,
            }}
          >
            <Menu size={20} />
          </button>
          <div>
            <div className="chat-header-title">DocuMind AI Chat</div>
            <div className="chat-header-status">
              <span className="status-dot" />
              {hasDocuments ? 'Ready — Ask anything about your documents' : 'Upload a document to get started'}
            </div>
          </div>
        </div>
        <div className="chat-header-badge">
          ✨ Powered by Groq
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {showWelcome ? (
          <div className="welcome-screen">
            <div className="welcome-icon">
              <Brain size={36} />
            </div>
            <h2 className="welcome-title">Welcome to DocuMind AI</h2>
            <p className="welcome-subtitle">
              Upload your documents and ask questions in natural language. 
              Get instant, accurate answers with source citations.
            </p>
            <div className="welcome-features">
              <div className="welcome-feature">
                <div className="welcome-feature-icon">
                  <Upload size={18} />
                </div>
                <h3>Upload Documents</h3>
                <p>PDF, DOCX, TXT files up to 50MB</p>
              </div>
              <div className="welcome-feature">
                <div className="welcome-feature-icon">
                  <Search size={18} />
                </div>
                <h3>Ask Questions</h3>
                <p>Natural language queries about your docs</p>
              </div>
              <div className="welcome-feature">
                <div className="welcome-feature-icon">
                  <FileText size={18} />
                </div>
                <h3>Source Citations</h3>
                <p>Every answer backed by document references</p>
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <MessageBubble key={idx} message={msg} />
            ))}

            {/* Typing indicator */}
            {isLoading && (
              <div className="typing-indicator">
                <div className="message-avatar" style={{
                  background: 'var(--gradient-brand)',
                  width: 34,
                  height: 34,
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}>
                  <Brain size={16} color="white" />
                </div>
                <div className="typing-dots">
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            ref={textareaRef}
            className="chat-input-field"
            placeholder={
              hasDocuments
                ? 'Ask a question about your documents...'
                : 'Upload a document first, then ask questions...'
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={!hasDocuments || isLoading}
          />
          <button
            className="chat-send-btn"
            onClick={handleSubmit}
            disabled={!input.trim() || isLoading || !hasDocuments}
            title="Send message"
          >
            <Send size={18} />
          </button>
        </div>
        <div className="chat-input-hint">
          DocuMind answers based only on your uploaded documents • Press Enter to send
        </div>
      </div>
    </div>
  );
}
