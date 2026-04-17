"""
DocuMind AI — Document Processor Service
Handles extraction of text from PDF, DOCX, and TXT files,
then splits into chunks for embedding.
"""

import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from pypdf import PdfReader
from docx import Document as DocxDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


class DocumentProcessor:
    """Processes uploaded documents: extracts text + splits into chunks."""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    def extract_text_from_pdf(self, file_path: str) -> list[dict]:
        """Extract text from a PDF file, page by page."""
        pages = []
        reader = PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append({
                    "content": text.strip(),
                    "page": i + 1,
                })
        return pages

    def extract_text_from_docx(self, file_path: str) -> list[dict]:
        """Extract text from a DOCX file."""
        doc = DocxDocument(file_path)
        full_text = "\n\n".join(
            para.text for para in doc.paragraphs if para.text.strip()
        )
        return [{"content": full_text, "page": 1}] if full_text else []

    def extract_text_from_txt(self, file_path: str) -> list[dict]:
        """Extract text from a plain text file."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
        return [{"content": content, "page": 1}] if content else []

    def extract_text(self, file_path: str, file_type: str) -> list[dict]:
        """Route to the correct extractor based on file type."""
        extractors = {
            "pdf": self.extract_text_from_pdf,
            "docx": self.extract_text_from_docx,
            "txt": self.extract_text_from_txt,
        }
        extractor = extractors.get(file_type.lower())
        if not extractor:
            raise ValueError(f"Unsupported file type: {file_type}")
        return extractor(file_path)

    def chunk_document(
        self, pages: list[dict], filename: str, doc_id: str
    ) -> list[dict]:
        """Split extracted pages into smaller chunks with metadata."""
        all_chunks = []
        for page_data in pages:
            text = page_data["content"]
            page_num = page_data.get("page", 1)

            chunks = self.text_splitter.split_text(text)
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_p{page_num}_c{i}"
                all_chunks.append({
                    "content": chunk,
                    "metadata": {
                        "filename": filename,
                        "doc_id": doc_id,
                        "page": page_num,
                        "chunk_id": chunk_id,
                        "chunk_index": i,
                        "total_chunks_in_page": len(chunks),
                    },
                })
        return all_chunks

    async def process_document(
        self, file_content: bytes, filename: str, file_type: str
    ) -> dict:
        """
        Full pipeline: save file → extract text → chunk → return metadata.
        """
        doc_id = str(uuid.uuid4())[:12]

        # Save the uploaded file
        file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_{filename}")
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Extract text
        pages = self.extract_text(file_path, file_type)
        if not pages:
            raise ValueError(
                f"No text could be extracted from '{filename}'. "
                "The file may be empty or contain only images."
            )

        # Chunk the text
        chunks = self.chunk_document(pages, filename, doc_id)

        return {
            "doc_id": doc_id,
            "filename": filename,
            "file_type": file_type,
            "file_size": len(file_content),
            "file_path": file_path,
            "num_chunks": len(chunks),
            "chunks": chunks,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }


# Singleton instance
document_processor = DocumentProcessor()
