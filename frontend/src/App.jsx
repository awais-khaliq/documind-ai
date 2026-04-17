import React, { useState, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import {
  uploadDocument,
  deleteDocument,
  sendMessage,
  getConversations,
  getChatHistory,
} from './utils/api';

export default function App() {
  // State
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Clear error after 5 seconds
  const showError = (msg) => {
    setError(msg);
    setTimeout(() => setError(null), 5000);
  };

  // Upload document
  const handleUpload = useCallback(async (file) => {
    try {
      const result = await uploadDocument(file);
      setDocuments((prev) => [...prev, result]);
    } catch (err) {
      showError(err.message);
      throw err;
    }
  }, []);

  // Delete document
  const handleDeleteDoc = useCallback(async (docId) => {
    try {
      await deleteDocument(docId);
      setDocuments((prev) => prev.filter((d) => d.id !== docId));
    } catch (err) {
      showError(err.message);
    }
  }, []);

  // Send message
  const handleSendMessage = useCallback(
    async (question) => {
      // Add user message immediately
      const userMsg = { role: 'user', content: question };
      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);

      try {
        const result = await sendMessage(question, activeConversation);

        // Set active conversation
        if (!activeConversation) {
          setActiveConversation(result.conversation_id);
        }

        // Add assistant message
        const assistantMsg = {
          role: 'assistant',
          content: result.answer,
          sources: result.sources,
          confidence: result.confidence,
        };
        setMessages((prev) => [...prev, assistantMsg]);

        // Refresh conversations list
        try {
          const convos = await getConversations();
          setConversations(convos);
        } catch {
          // Ignore conversation list errors
        }
      } catch (err) {
        showError(err.message);
        // Add error message
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `❌ **Error:** ${err.message}\n\nPlease make sure the backend is running and your API key is configured.`,
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [activeConversation]
  );

  // New chat
  const handleNewChat = useCallback(() => {
    setMessages([]);
    setActiveConversation(null);
  }, []);

  // Select existing conversation
  const handleSelectConversation = useCallback(async (convId) => {
    try {
      const history = await getChatHistory(convId);
      setMessages(
        history.map((m) => ({
          role: m.role,
          content: m.content,
          sources: m.sources || undefined,
          confidence: m.confidence || undefined,
        }))
      );
      setActiveConversation(convId);
    } catch (err) {
      showError(err.message);
    }
  }, []);

  return (
    <div className="app-layout">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <Sidebar
        documents={documents}
        conversations={conversations}
        onUpload={handleUpload}
        onDeleteDoc={handleDeleteDoc}
        onNewChat={handleNewChat}
        onSelectConversation={handleSelectConversation}
        activeConversation={activeConversation}
      />

      <ChatArea
        messages={messages}
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
        hasDocuments={documents.length > 0}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
      />

      {/* Error toast */}
      {error && <div className="error-toast">⚠️ {error}</div>}
    </div>
  );
}
