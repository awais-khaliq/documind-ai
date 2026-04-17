"""
DocuMind AI — RAG Pipeline Service
Retrieval-Augmented Generation using Google Gemini (FREE tier)
with semantic search from ChromaDB.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config import settings
from app.services.vector_store import vector_store


# ── System Prompt ─────────────────────────────────────

RAG_SYSTEM_PROMPT = """You are DocuMind AI, an intelligent document analysis assistant. 
Your job is to answer questions based ONLY on the provided context from uploaded documents.

RULES:
1. Answer ONLY based on the provided context. Do not use external knowledge.
2. If the context doesn't contain enough information, say "I couldn't find enough information in your documents to answer this question."
3. Be concise but thorough. Use bullet points for lists.
4. When referencing information, mention which document it came from.
5. If the question is ambiguous, address the most likely interpretation.
6. Format your answers in clean markdown for readability.

CONTEXT FROM DOCUMENTS:
{context}

Remember: Only use the above context to answer. Do not make up information."""

RAG_USER_PROMPT = """{question}"""


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""

    def __init__(self):
        self._llm = None
        self._chain = None
        self._conversations: dict[str, list[dict]] = {}

    def _get_llm(self) -> ChatGroq:
        """Lazy-load the Groq LLM."""
        if self._llm is None:
            self._llm = ChatGroq(
                model_name=settings.GROQ_MODEL,
                groq_api_key=settings.GROQ_API_KEY,
                temperature=settings.TEMPERATURE,
            )
        return self._llm

    def _build_context(self, search_results: list[dict]) -> str:
        """Format search results into a context string for the LLM."""
        if not search_results:
            return "No relevant documents found."

        context_parts = []
        for i, result in enumerate(search_results, 1):
            filename = result["metadata"].get("filename", "Unknown")
            page = result["metadata"].get("page", "N/A")
            score = result["relevance_score"]

            context_parts.append(
                f"[Source {i}] (File: {filename}, Page: {page}, Relevance: {score:.0%})\n"
                f"{result['content']}"
            )

        return "\n\n---\n\n".join(context_parts)

    def _calculate_confidence(self, search_results: list[dict]) -> float:
        """
        Calculate overall confidence based on relevance scores.
        Higher scores = more confident the answer is grounded in documents.
        """
        if not search_results:
            return 0.0

        scores = [r["relevance_score"] for r in search_results]
        top_score = max(scores)
        avg_score = sum(scores) / len(scores)

        # Weighted: 60% top result, 40% average
        confidence = (0.6 * top_score) + (0.4 * avg_score)
        return round(min(confidence, 1.0), 4)

    async def ask(
        self,
        question: str,
        conversation_id: Optional[str] = None,
    ) -> dict:
        """
        Full RAG pipeline:
        1. Retrieve relevant chunks from vector store
        2. Build context
        3. Generate answer with Gemini
        4. Return answer + sources + confidence
        """
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())[:12]

        # Step 1: Retrieve relevant chunks
        search_results = await vector_store.search(
            query=question,
            top_k=settings.TOP_K_RESULTS,
        )

        # Step 2: Build context
        context = self._build_context(search_results)

        # Step 3: Generate answer
        llm = self._get_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", RAG_SYSTEM_PROMPT),
            ("human", RAG_USER_PROMPT),
        ])

        chain = prompt | llm | StrOutputParser()

        answer = await chain.ainvoke({
            "context": context,
            "question": question,
        })

        # Step 4: Calculate confidence
        confidence = self._calculate_confidence(search_results)

        # Step 5: Format sources
        sources = []
        for result in search_results:
            sources.append({
                "content": result["content"][:300] + ("..." if len(result["content"]) > 300 else ""),
                "filename": result["metadata"].get("filename", "Unknown"),
                "page": result["metadata"].get("page"),
                "chunk_id": result["metadata"].get("chunk_id", ""),
                "relevance_score": result["relevance_score"],
            })

        # Step 6: Store in conversation history
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = []

        self._conversations[conversation_id].append({
            "role": "user",
            "content": question,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self._conversations[conversation_id].append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "conversation_id": conversation_id,
        }

    def get_conversation_history(self, conversation_id: str) -> list[dict]:
        """Get chat history for a conversation."""
        return self._conversations.get(conversation_id, [])

    def get_all_conversations(self) -> list[dict]:
        """Get summaries of all conversations."""
        summaries = []
        for conv_id, messages in self._conversations.items():
            if not messages:
                continue
            user_messages = [m for m in messages if m["role"] == "user"]
            title = user_messages[0]["content"][:60] + "..." if user_messages else "New Chat"
            summaries.append({
                "conversation_id": conv_id,
                "title": title,
                "message_count": len(messages),
                "created_at": messages[0]["timestamp"],
                "last_message_at": messages[-1]["timestamp"],
            })
        return summaries

    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a specific conversation."""
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False


# Singleton instance
rag_pipeline = RAGPipeline()
