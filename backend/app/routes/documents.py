"""
DocuMind AI — Document Routes
Handles document upload, listing, and deletion.
"""

import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models import DocumentInfo, DocumentListResponse, DeleteResponse
from app.services.document_processor import document_processor
from app.services.vector_store import vector_store

router = APIRouter(prefix="/api/documents", tags=["Documents"])

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def get_file_extension(filename: str) -> str:
    """Extract and validate file extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext


@router.post("/upload", response_model=DocumentInfo)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, DOCX, or TXT) for processing.
    The document is extracted, chunked, embedded, and stored in the vector DB.
    """
    # Validate file type
    file_ext = get_file_extension(file.filename)
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{file_ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Read file content
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty.")

    # Check file size (50MB limit)
    max_size = 50 * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is 50MB.",
        )

    try:
        # Process document: extract text + chunk
        doc_info = await document_processor.process_document(
            file_content=content,
            filename=file.filename,
            file_type=file_ext,
        )

        # Add chunks to vector store
        num_added = await vector_store.add_document(doc_info["chunks"])

        return DocumentInfo(
            id=doc_info["doc_id"],
            filename=doc_info["filename"],
            file_type=doc_info["file_type"],
            file_size=doc_info["file_size"],
            num_chunks=num_added,
            uploaded_at=doc_info["uploaded_at"],
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}",
        )


@router.get("", response_model=DocumentListResponse)
async def list_documents():
    """Get a list of all uploaded documents."""
    docs = vector_store.get_all_documents()
    document_list = []
    for doc in docs:
        document_list.append(
            DocumentInfo(
                id=doc["doc_id"],
                filename=doc["filename"],
                file_type=doc["filename"].rsplit(".", 1)[-1] if "." in doc["filename"] else "unknown",
                file_size=0,
                num_chunks=doc["num_chunks"],
                uploaded_at="",
            )
        )
    return DocumentListResponse(documents=document_list, total=len(document_list))


@router.delete("/{doc_id}", response_model=DeleteResponse)
async def delete_document(doc_id: str):
    """Delete a document and all its chunks from the vector store."""
    success = await vector_store.delete_document(doc_id)
    if success:
        return DeleteResponse(success=True, message="Document deleted successfully.")
    raise HTTPException(status_code=404, detail="Document not found.")
