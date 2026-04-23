# DocuMind AI

An intelligent document retrieval and question-answering system powered by Retrieval-Augmented Generation (RAG).

## Project Overview

DocuMind AI enables users to upload various document formats (PDF, DOCX, TXT) and interactively query their contents using natural language. The system processes the uploaded text, converts it into semantic embeddings, and stores it in a local vector database. When a user asks a question, the application retrieves the most relevant document chunks and uses a Large Language Model (LLM) to generate a precise answer, complete with exact source citations.

This completely free implementation relies on local embeddings for data privacy and speed, alongside the Google Gemini free tier for language generation.

## Core Features

* Multi-Format Support: Processes PDF, DOCX, and TXT files natively up to 50MB.
* Semantic Search Retrieval: Employs sentence-transformers to capture the actual meaning of documents rather than just keyword matching.
* Context-Aware Q&A: Synthesizes answers based strictly on the provided documents to mitigate hallucination risks.
* Transparent Citations: Every generated answer explicitly references the source document and page number it derived its information from.
* Private Vector Storage: Utilizes ChromaDB locally, ensuring that raw document embeddings never leave your environment unless required for a specific LLM prompt.

## Technology Stack

* Language/Framework: Python 3.11+, FastAPI (Backend)
* Frontend: React 18 with Vite, custom CSS
* AI Orchestration: LangChain
* Vector Database: ChromaDB
* Embedding Model: ONNX MiniLM-L6-v2 (Local execution)
* Generation Model: Groq Llama 3.1 or Google Gemini (Configurable via API Keys)

## System Architecture

The application is decoupled into a RESTful FastAPI backend and a React frontend. The backend manages document parsing, chunking (fixed size with overlap), vectorization, and database storage. The frontend provides a responsive chat interface and drag-and-drop document management tools.

1. Document Upload: Files are parsed and split into overlapping chunks of ~1000 characters.
2. Embedding: Each chunk is converted to a 384-dimensional vector using the all-MiniLM-L6-v2 model.
3. Storage: Vectors and their associated metadata are stored in ChromaDB.
4. Query Execution: User questions are embedded and compared against the vector store to retrieve the top-K most similar chunks.
5. Generation: The LLM processes the question alongside the retrieved context to formulate the final answer.

## How to Run Locally

### Requirements
* Python 3.11 or higher
* Node.js 18 or higher
* Gemini or Groq API Key

### Backend Setup
1. Navigate to the backend directory:
   cd backend
2. Create and activate a virtual environment:
   python -m venv venv
   source venv/Scripts/activate (Windows) or source venv/bin/activate (Unix)
3. Install dependencies:
   pip install -r requirements.txt
4. Configure the environment variables by renaming .env.example to .env and adding your API key.
5. Start the backend server:
   uvicorn app.main:app --reload --port 8000

### Frontend Setup
1. Navigate to the frontend directory:
   cd frontend
2. Install dependencies:
   npm install
3. Start the development server:
   npm run dev

The application will be available at http://localhost:5173.

## Integration & Configuration

To use the Groq Llama 3 engine instead of Gemini:
1. Obtain an API key from the Groq Developer Console.
2. Update your backend `.env` file with `GROQ_API_KEY=your_key_here`.

## API Documentation

Once the backend is running, you can explore the complete interactive API documentation (Swagger UI) by navigating to `http://localhost:8000/docs`.
