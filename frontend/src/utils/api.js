/**
 * DocuMind AI — API Utility Functions
 */

const API_BASE = '/api';

/**
 * Upload a document file to the backend.
 */
export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Failed to upload document');
  }
  return res.json();
}

/**
 * Get list of all uploaded documents.
 */
export async function getDocuments() {
  const res = await fetch(`${API_BASE}/documents`);
  if (!res.ok) throw new Error('Failed to fetch documents');
  return res.json();
}

/**
 * Delete a document by ID.
 */
export async function deleteDocument(docId) {
  const res = await fetch(`${API_BASE}/documents/${docId}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete document');
  return res.json();
}

/**
 * Send a chat question and get a RAG response.
 */
export async function sendMessage(question, conversationId = null) {
  const body = { question };
  if (conversationId) body.conversation_id = conversationId;

  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Failed to get response');
  }
  return res.json();
}

/**
 * Get all conversation summaries.
 */
export async function getConversations() {
  const res = await fetch(`${API_BASE}/chat/conversations`);
  if (!res.ok) throw new Error('Failed to fetch conversations');
  return res.json();
}

/**
 * Get chat history for a specific conversation.
 */
export async function getChatHistory(conversationId) {
  const res = await fetch(`${API_BASE}/chat/history/${conversationId}`);
  if (!res.ok) throw new Error('Failed to fetch chat history');
  return res.json();
}

/**
 * Health check.
 */
export async function healthCheck() {
  const res = await fetch('/health');
  if (!res.ok) throw new Error('API not available');
  return res.json();
}
