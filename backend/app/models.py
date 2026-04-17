"""
DocuMind AI — Pydantic Models / Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── Chat ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Incoming chat question."""
    question: str
    conversation_id: Optional[str] = None


class SourceDocument(BaseModel):
    """A source chunk used to answer a question."""
    content: str
    filename: str
    page: Optional[int] = None
    chunk_id: str
    relevance_score: float


class ChatResponse(BaseModel):
    """Response to a chat question."""
    answer: str
    sources: list[SourceDocument]
    confidence: float
    conversation_id: str


# ── Documents ─────────────────────────────────────────

class DocumentInfo(BaseModel):
    """Metadata about an uploaded document."""
    id: str
    filename: str
    file_type: str
    file_size: int
    num_chunks: int
    uploaded_at: str


class DocumentListResponse(BaseModel):
    """List of uploaded documents."""
    documents: list[DocumentInfo]
    total: int


class DeleteResponse(BaseModel):
    """Response after deleting a document."""
    success: bool
    message: str


# ── Chat History ──────────────────────────────────────

class ChatMessage(BaseModel):
    """A single chat message."""
    role: str  # "user" or "assistant"
    content: str
    sources: Optional[list[SourceDocument]] = None
    confidence: Optional[float] = None
    timestamp: str


class ConversationSummary(BaseModel):
    """Summary of a conversation."""
    conversation_id: str
    title: str
    message_count: int
    created_at: str
    last_message_at: str


# ── Health ────────────────────────────────────────────

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    documents_loaded: int
    model: str
