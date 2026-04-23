# DocuMind AI: Project Overview & Interview Guide

This guide is designed to help you simply explain your project, its technologies, and its core concepts to interviewers or peers.

---

## 1. The Elevator Pitch (What is this project?)
**DocuMind AI** is a full-stack **Document Intelligence App**. It allows users to upload their own documents (PDFs, Word files, Text) and ask questions about them in plain English. Instead of reading through hundreds of pages, the AI reads it for you and instantly provides an accurate answer, complete with exact source citations showing where it found the information.

## 2. The Core Concept: "RAG" Simply Explained
The entire project is built on a modern AI architecture called **RAG (Retrieval-Augmented Generation)**. 

If you ask an AI model like ChatGPT a specific question about your private company document, it won't know the answer because it was never trained on your document. 
RAG solves this. Here's how DocuMind AI does RAG in 3 simple steps:
1. **Upload**: You upload a document. The system chops the document into hundreds of small text chunks.
2. **Retrieval**: When you ask a question (e.g., "What is the company policy?"), the system searches the chopped-up chunks and **Retrieves** only the 3 or 4 chunks that are highly relevant to your question.
3. **Generation**: It sends your question PLUS those highly relevant chunks to the AI model. The AI then **Generates** an answer using *only* information from those chunks. 

## 3. Tech Stack Breakdown
You built this using modern, industry-standard tools:

*   **Frontend (User Interface):** Built with **React** and **Vite**. Features a modern, responsive Glassmorphism design. Hosted securely on **Vercel**.
*   **Backend (The Brains):** Built with **FastAPI** (Python). It handles file uploads, memory, and routing. Hosted in a Docker container on **Hugging Face Spaces**.
*   **Vector Database:** **ChromaDB**. This is a specialized database that stores the "chopped-up chunks" of text as math coordinates (vectors) so the system can search them lightning-fast.
*   **The AI Model:** **Groq Llama 3** (Meta's open-source model). Chosen because it is currently the fastest AI inference model in the world.

## 4. Key Technical Terms (Simplified)
*   **Embeddings:** Think of embeddings as translating english text into math. When you upload a document, text is converted into long arrays of numbers (vectors). This allows the computer to find text that has similar *meaning*, not just exact keyword matches.
*   **Sentence-Transformers / ONNX:** The local, free technology running in your backend that creates the "Embeddings" without needing to pay for an external API.
*   **Docker:** A technology that packages the entire backend into a standardized "container" so it runs perfectly on any server (like Hugging Face) without crashing.

## 5. Typical Interview Questions & Your Answers

**Q: Why did you use FastAPI over Django or Flask?**
> *"I chose FastAPI because it is extremely modern, fast, and handles asynchronous (async/await) requests perfectly. Since AI generation and file processing take time, an asynchronous framework prevents the server from freezing while the AI thinks."*

**Q: How do you prevent the AI from "hallucinating" (making things up)?**
> *"That's the main benefit of the RAG architecture! In my backend "System Prompt", I gave the AI a strict instruction: 'Answer ONLY based on the provided context. Do not make up information.' I also implemented source citations so users can verify exactly which page the AI got its facts from."*

**Q: How does the document search actually work? Is it just searching for matching words?**
> *"No, it uses 'Semantic Search'. When text is uploaded, it's converted into mathematical vectors using an embedding model. When a user asks a question, the question is also converted into a vector. ChromaDB calculates the 'Cosine Distance' between the vectors. This means it finds answers that mean the same thing conceptually, even if the user used slightly different vocabulary!"*

**Q: How did you handle large PDFs without breaking the AI's token limit?**
> *"I used LangChain's 'RecursiveCharacterTextSplitter'. When a PDF is uploaded, it smartly breaks it down into overlapping chunks of about 1000 characters. Instead of sending the entire 50-page PDF to the AI, I only send the top 4 most relevant chunks, which keeps the system incredibly fast and cheap."*
