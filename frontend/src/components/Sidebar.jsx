import React from 'react';
import {
  Brain,
  Plus,
  FileText,
  Trash2,
  File,
  MessageSquare,
  FolderOpen,
} from 'lucide-react';
import DocumentUpload from './DocumentUpload';

export default function Sidebar({
  documents,
  conversations,
  onUpload,
  onDeleteDoc,
  onNewChat,
  onSelectConversation,
  activeConversation,
}) {
  const getFileIcon = (type) => {
    const classes = {
      pdf: 'pdf',
      docx: 'docx',
      txt: 'txt',
    };
    return classes[type] || 'txt';
  };

  const formatSize = (bytes) => {
    if (!bytes) return '';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <aside className="sidebar">
      {/* Header */}
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">
            <Brain size={22} />
          </div>
          <h1>DocuMind AI</h1>
        </div>
        <p className="sidebar-logo-subtitle">Document Intelligence</p>

        <button className="new-chat-btn" onClick={onNewChat}>
          <Plus size={16} />
          New Conversation
        </button>
      </div>

      {/* Documents Section */}
      <div className="sidebar-section">
        <div className="sidebar-section-title">
          📄 Documents ({documents.length})
        </div>
      </div>

      <div className="sidebar-documents">
        {documents.length === 0 ? (
          <div className="empty-state">
            <FolderOpen size={28} />
            <p>No documents uploaded yet</p>
          </div>
        ) : (
          documents.map((doc) => (
            <div key={doc.id} className="doc-card">
              <div className="doc-card-header">
                <div className="doc-card-info">
                  <div className={`doc-card-icon ${getFileIcon(doc.file_type)}`}>
                    <FileText size={16} />
                  </div>
                  <div>
                    <div className="doc-card-name" title={doc.filename}>
                      {doc.filename}
                    </div>
                    <div className="doc-card-meta">
                      {doc.num_chunks} chunks
                      {doc.file_size ? ` • ${formatSize(doc.file_size)}` : ''}
                    </div>
                  </div>
                </div>
                <button
                  className="doc-card-delete"
                  onClick={() => onDeleteDoc(doc.id)}
                  title="Delete document"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Conversations Section */}
      {conversations.length > 0 && (
        <>
          <div className="sidebar-section">
            <div className="sidebar-section-title">
              💬 Recent Chats
            </div>
          </div>
          <div className="sidebar-documents" style={{ flex: 'none', maxHeight: '200px' }}>
            {conversations.map((conv) => (
              <div
                key={conv.conversation_id}
                className="doc-card"
                style={{
                  cursor: 'pointer',
                  borderColor:
                    activeConversation === conv.conversation_id
                      ? 'var(--border-accent)'
                      : undefined,
                }}
                onClick={() => onSelectConversation(conv.conversation_id)}
              >
                <div className="doc-card-header">
                  <div className="doc-card-info">
                    <div
                      className="doc-card-icon"
                      style={{
                        background: 'rgba(108, 92, 231, 0.15)',
                        color: '#6c5ce7',
                      }}
                    >
                      <MessageSquare size={16} />
                    </div>
                    <div>
                      <div className="doc-card-name">{conv.title}</div>
                      <div className="doc-card-meta">
                        {conv.message_count} messages
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Upload Zone */}
      <DocumentUpload onUpload={onUpload} />
    </aside>
  );
}
