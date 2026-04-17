<div align="center">

# 🧠 DocuMind AI

### AI-Powered Document Intelligence System

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Gemini](https://img.shields.io/badge/Google_Gemini-Free-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Upload documents. Ask questions. Get instant answers with source citations.**

*Built with Retrieval-Augmented Generation (RAG) — 100% Free to run*

---

</div>

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Multi-Format Upload** | Support for PDF, DOCX, and TXT files up to 50MB |
| 🔍 **Semantic Search** | Intelligent document retrieval using sentence-transformer embeddings |
| 💬 **Natural Language Q&A** | Ask questions in plain English and get accurate answers |
| 📑 **Source Citations** | Every answer includes clickable source references with page numbers |
| 🎯 **Confidence Scoring** | AI confidence indicator shows how well-grounded each answer is |
| 💾 **Persistent Storage** | Documents and embeddings stored locally with ChromaDB |
| 🆓 **100% Free** | Uses Google Gemini free tier + local embeddings (no paid APIs!) |
| 🎨 **Premium UI** | Dark-themed glassmorphism design with smooth animations |
| 📱 **Responsive** | Works on desktop and mobile devices |
| 🐳 **Docker Ready** | One-command deployment with Docker Compose |

## 🏗️ Architecture

```
┌──────────────┐     REST API      ┌──────────────────┐
│              │ ◄────────────────► │                  │
│  React + Vite│                   │  FastAPI Backend  │
│  Frontend    │                   │                   │
│              │                   │  ┌──────────────┐ │
└──────────────┘                   │  │ Document     │ │
                                   │  │ Processor    │ │
                                   │  │ (PDF/DOCX/   │ │
                                   │  │  TXT)        │ │
                                   │  └──────┬───────┘ │
                                   │         │         │
                                   │  ┌──────▼───────┐ │
                                   │  │ Text         │ │
                                   │  │ Splitter     │ │
                                   │  │ (1000 chars) │ │
                                   │  └──────┬───────┘ │
                                   │         │         │
                                   │  ┌──────▼───────┐ │
                                   │  │ Sentence     │ │
                                   │  │ Transformers │ │
                                   │  │ (Local)      │ │
                                   │  └──────┬───────┘ │
                                   │         │         │
                                   │  ┌──────▼───────┐ │
                                   │  │ ChromaDB     │ │
                                   │  │ Vector Store │ │
                                   │  └──────┬───────┘ │
                                   │         │         │
                                   │  ┌──────▼───────┐ │
                                   │  │ RAG Pipeline │ │
                                   │  │ + Gemini LLM │ │
                                   │  └──────────────┘ │
                                   └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** — [Download](https://python.org/downloads)
- **Node.js 18+** — [Download](https://nodejs.org)
- **Google Gemini API Key** (FREE) — [Get yours here](https://aistudio.google.com/apikey)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/documind-ai.git
cd documind-ai
```

### 2. Set Up Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
copy .env.example .env
# Edit .env and add your FREE Gemini API key
```

### 3. Set Up Frontend

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install
```

### 4. Run the Application

```bash
# Terminal 1 — Start backend (from /backend directory)
uvicorn app.main:app --reload --port 8000

# Terminal 2 — Start frontend (from /frontend directory)
npm run dev
```

Open **http://localhost:5173** in your browser 🎉

### 🐳 Docker (Alternative)

```bash
docker-compose up --build
```

## 🔑 Getting Your Free Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click **"Create API Key"**
3. Copy the key
4. Paste it in `backend/.env` as `GOOGLE_API_KEY=your_key_here`

> **Note:** The free tier gives you **15 requests/minute** and **1 million tokens/day** — more than enough for personal use!

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/documents/upload` | Upload a document (PDF/DOCX/TXT) |
| `GET` | `/api/documents` | List all uploaded documents |
| `DELETE` | `/api/documents/{id}` | Delete a document |
| `POST` | `/api/chat` | Ask a question about your documents |
| `GET` | `/api/chat/conversations` | List all conversations |
| `GET` | `/api/chat/history/{id}` | Get conversation history |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Interactive API docs (Swagger) |

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **LLM** | Google Gemini 2.0 Flash | Answer generation (FREE tier) |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | Semantic search (runs locally) |
| **Vector DB** | ChromaDB | Document storage & retrieval |
| **Framework** | LangChain | RAG pipeline orchestration |
| **Backend** | FastAPI + Uvicorn | REST API server |
| **Frontend** | React 18 + Vite | User interface |
| **Styling** | Custom CSS | Premium dark glassmorphism theme |
| **Icons** | Lucide React | Beautiful SVG icons |

## 📁 Project Structure

```
documind-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application
│   │   ├── config.py                  # Environment configuration
│   │   ├── models.py                  # Pydantic schemas
│   │   ├── services/
│   │   │   ├── document_processor.py  # Text extraction & chunking
│   │   │   ├── vector_store.py        # ChromaDB + embeddings
│   │   │   └── rag_pipeline.py        # LangChain RAG chain
│   │   └── routes/
│   │       ├── documents.py           # Document CRUD endpoints
│   │       └── chat.py                # Chat Q&A endpoints
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Main application
│   │   ├── index.css                  # Design system
│   │   ├── components/
│   │   │   ├── Sidebar.jsx            # Document & chat management
│   │   │   ├── ChatArea.jsx           # Chat interface
│   │   │   ├── MessageBubble.jsx      # Message display
│   │   │   ├── DocumentUpload.jsx     # Drag-and-drop upload
│   │   │   └── SourceCard.jsx         # Source citations
│   │   └── utils/
│   │       └── api.js                 # API client functions
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

## 🔬 How It Works

1. **Document Upload** — Files are parsed (PDF → text, DOCX → text) and split into overlapping chunks of ~1000 characters

2. **Embedding** — Each chunk is converted to a 384-dimensional vector using the `all-MiniLM-L6-v2` model (runs locally, no API needed)

3. **Storage** — Vectors are stored in ChromaDB with metadata (filename, page number, chunk position)

4. **Query** — When you ask a question, it's embedded and the top 5 most similar chunks are retrieved

5. **Generation** — The retrieved chunks are sent to Google Gemini along with your question. The AI generates an answer based *only* on the provided context

6. **Citations** — Each source chunk is returned with its filename, page number, and relevance score

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using RAG, LangChain, and Google Gemini**

*If you found this useful, give it a ⭐!*

</div>
