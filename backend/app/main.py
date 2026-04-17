"""
DocuMind AI — FastAPI Application Entry Point
A RAG-based Document Intelligence System powered by Google Gemini (Free Tier).
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import HealthResponse
from app.routes import documents, chat
from app.services.vector_store import vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    print("=" * 60)
    print("  DocuMind AI -- Starting Up")
    print("=" * 60)
    print(f"  Model:      {settings.GROQ_MODEL}")
    print(f"  Embeddings: {settings.EMBEDDING_MODEL}")
    print(f"  ChromaDB:   {settings.CHROMA_PERSIST_DIR}")
    print("=" * 60)

    # Create required directories
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)

    # Validate API key
    if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your_groq_api_key_here":
        print("\n  WARNING: GROQ_API_KEY not set!")
        print("   Get your FREE key at: https://console.groq.com/keys")
        print("   Then set it in backend/.env\n")

    yield

    # Shutdown
    print("\n  DocuMind AI -- Shutting Down")


# ── Create FastAPI App ────────────────────────────────

app = FastAPI(
    title="DocuMind AI",
    description=(
        "🧠 AI-Powered Document Intelligence System — "
        "Upload documents, ask questions, get answers with source citations. "
        "Powered by Groq (Free) + ChromaDB + Sentence Transformers."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS Middleware ───────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount Routes ──────────────────────────────────────

app.include_router(documents.router)
app.include_router(chat.router)


# ── Health Check ──────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint — API info."""
    return {
        "name": "DocuMind AI",
        "version": "1.0.0",
        "description": "AI-Powered Document Intelligence System",
        "docs": "/docs",
        "endpoints": {
            "upload": "POST /api/documents/upload",
            "documents": "GET /api/documents",
            "chat": "POST /api/chat",
            "history": "GET /api/chat/conversations",
        },
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        documents_loaded=vector_store.get_document_count(),
        model=settings.GROQ_MODEL,
    )
