"""
DocuMind AI — Vector Store Service
Manages ChromaDB for storing and querying document embeddings.
Uses Chroma DB's lightweight default ONNX runtime for FREE local embeddings (no PyTorch required).
"""

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import settings


class VectorStore:
    """ChromaDB vector store with ONNX default embeddings."""

    def __init__(self):
        self._client = None
        self._collection = None
        self._doc_registry: dict[str, dict] = {}

    def _get_client(self) -> chromadb.ClientAPI:
        """Lazy-load the ChromaDB client."""
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
        return self._client

    def _get_collection(self) -> chromadb.Collection:
        """Get or create the ChromaDB collection."""
        if self._collection is None:
            client = self._get_client()
            self._collection = client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    async def add_document(self, chunks: list[dict]) -> int:
        """
        Add document chunks to the vector store.
        Returns the number of chunks added.
        """
        if not chunks:
            return 0

        collection = self._get_collection()

        texts = [c["content"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [c["metadata"]["chunk_id"] for c in chunks]

        # Add to ChromaDB (It automatically generates embeddings using ONNX DefaultEmbeddingFunction!)
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )

        # Register document
        doc_id = chunks[0]["metadata"]["doc_id"]
        self._doc_registry[doc_id] = {
            "filename": chunks[0]["metadata"]["filename"],
            "doc_id": doc_id,
            "num_chunks": len(chunks),
            "chunk_ids": ids,
        }

        return len(chunks)

    async def search(
        self, query: str, top_k: int = None
    ) -> list[dict]:
        """
        Search for similar chunks. Returns list of results with scores.
        """
        if top_k is None:
            top_k = settings.TOP_K_RESULTS

        collection = self._get_collection()

        # Check if collection has documents
        if collection.count() == 0:
            return []

        # Query ChromaDB (It automatically embeds the query!)
        results = collection.query(
            query_texts=[query],
            n_results=min(top_k, collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        search_results = []
        if results and results["documents"]:
            for i in range(len(results["documents"][0])):
                distance = results["distances"][0][i]
                # Convert cosine distance to similarity score (0-1)
                similarity = 1 - distance

                search_results.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "relevance_score": round(similarity, 4),
                })

        # Sort by relevance (highest first)
        search_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return search_results

    async def delete_document(self, doc_id: str) -> bool:
        """Delete all chunks belonging to a document."""
        collection = self._get_collection()

        if doc_id in self._doc_registry:
            chunk_ids = self._doc_registry[doc_id]["chunk_ids"]
            collection.delete(ids=chunk_ids)
            del self._doc_registry[doc_id]
            return True

        # Fallback: search by metadata
        try:
            results = collection.get(
                where={"doc_id": doc_id},
                include=["metadatas"],
            )
            if results and results["ids"]:
                collection.delete(ids=results["ids"])
                return True
        except Exception:
            pass

        return False

    def get_document_count(self) -> int:
        """Get total number of documents (unique doc_ids)."""
        return len(self._doc_registry)

    def get_all_documents(self) -> list[dict]:
        """Get info about all registered documents."""
        return list(self._doc_registry.values())

    def get_total_chunks(self) -> int:
        """Get total chunks in the vector store."""
        try:
            return self._get_collection().count()
        except Exception:
            return 0


# Singleton instance
vector_store = VectorStore()
