"""
DocuMind AI — Chat Routes
Handles Q&A conversations with the RAG pipeline.
"""

from fastapi import APIRouter, HTTPException

from app.models import (
    ChatRequest,
    ChatResponse,
    SourceDocument,
    ConversationSummary,
    ChatMessage,
)
from app.services.rag_pipeline import rag_pipeline
from app.services.vector_store import vector_store

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Ask a question about your uploaded documents.
    Returns an AI-generated answer with source citations and confidence score.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Check if any documents are loaded
    if vector_store.get_total_chunks() == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet. Please upload at least one document first.",
        )

    try:
        result = await rag_pipeline.ask(
            question=request.question,
            conversation_id=request.conversation_id,
        )

        sources = [
            SourceDocument(
                content=s["content"],
                filename=s["filename"],
                page=s.get("page"),
                chunk_id=s["chunk_id"],
                relevance_score=s["relevance_score"],
            )
            for s in result["sources"]
        ]

        return ChatResponse(
            answer=result["answer"],
            sources=sources,
            confidence=result["confidence"],
            conversation_id=result["conversation_id"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}",
        )


@router.get("/conversations", response_model=list[ConversationSummary])
async def get_conversations():
    """Get a list of all conversation summaries."""
    convos = rag_pipeline.get_all_conversations()
    return [
        ConversationSummary(**c) for c in convos
    ]


@router.get("/history/{conversation_id}", response_model=list[ChatMessage])
async def get_chat_history(conversation_id: str):
    """Get the full chat history for a conversation."""
    history = rag_pipeline.get_conversation_history(conversation_id)
    if not history:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    return [
        ChatMessage(
            role=m["role"],
            content=m["content"],
            sources=[SourceDocument(**s) for s in m.get("sources", [])] if m.get("sources") else None,
            confidence=m.get("confidence"),
            timestamp=m["timestamp"],
        )
        for m in history
    ]


@router.delete("/history/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a specific conversation history."""
    success = rag_pipeline.clear_conversation(conversation_id)
    if success:
        return {"success": True, "message": "Conversation cleared."}
    raise HTTPException(status_code=404, detail="Conversation not found.")
