# Flask LLM API

A Flask web API that supports single-turn Q&A, multi-turn conversation, and document-grounded answers using Retrieval-Augmented Generation (RAG). Built with Python, Flask, and the Anthropic API (Claude).

---

## What This Project Does

This app has three endpoints:

- POST /ask — Send a single question, get a single AI-generated answer
- POST /ingest — Upload a document (text or PDF), chunk it, embed it, and store it in a vector store
- POST /chat — Send a conversation history and get a response grounded in your uploaded documents

---

## Requirements

- Python 3.10 or higher
- An Anthropic API key (get one at https://console.anthropic.com)

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/vednalex/flask-llm-api.git
cd flask-llm-api

### 2. Switch to the task-2 branch
git checkout task-2

### 3. Create and activate a virtual environment
Mac:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate

### 4. Install dependencies
pip install -r requirements.txt

### 5. Set up your environment variables
cp .env.example .env
Then open .env and replace the placeholder with your real Anthropic API key.

### 6. Run the app
python app.py
The server will start at http://localhost:5001

---

## How to Use the Endpoints

### Endpoint 1: POST /ask
Send a single question and get an answer back.

curl -X POST http://localhost:5001/ask -H "Content-Type: application/json" -d '{"question": "What is the capital of France?"}'

Response:
{"answer": "The capital of France is Paris."}

### Endpoint 2: POST /ingest
Upload a plain text document to be chunked, embedded, and stored.

curl -X POST http://localhost:5001/ingest -H "Content-Type: application/json" -d '{"text": "Your document text goes here..."}'

Response:
{"message": "Successfully ingested document", "chunks_created": 3, "total_chunks_stored": 3}

To upload a PDF file:
curl -X POST http://localhost:5001/ingest -F "file=@your_document.pdf"

### Endpoint 3: POST /chat
Send a conversation history and get a response grounded in your uploaded documents.

curl -X POST http://localhost:5001/chat -H "Content-Type: application/json" -d '{"messages": [{"role": "user", "content": "Who founded Anthropic?"}]}'

Response includes the answer, the updated conversation history, whether context was used, and how many chunks were retrieved.

---

## How RAG Works in This App

RAG stands for Retrieval-Augmented Generation. The idea is simple: instead of relying on Claude's general training knowledge, the app retrieves specific pieces of your own documents and injects them into the prompt as context. Claude then answers based on your documents rather than guessing.

Here is the full flow:

1. You upload a document to /ingest
2. The app splits it into chunks of 500 words with 50 word overlap between chunks
3. Each chunk is converted into an embedding using a local model called all-MiniLM-L6-v2
4. The embeddings are stored in a FAISS vector store in memory
5. When you ask a question via /chat, your question is also converted into an embedding
6. The app compares your question embedding against all stored chunk embeddings using cosine similarity
7. The most relevant chunks are retrieved and injected into Claude's prompt as context
8. Claude answers based on that context and says clearly when the documents don't contain the answer

---

## How Multi-Turn Conversation Works

The /chat endpoint keeps full conversation history working alongside RAG. Every request includes all previous messages so Claude has context of what was said before. If the conversation gets longer than 10 messages, the oldest ones are trimmed automatically to stay within the model's limits.

---

## Key Concepts

Embeddings — a way of converting text into a list of numbers that captures its meaning. Similar text produces similar numbers, which lets the app find relevant chunks mathematically.

Cosine similarity — the method used to measure how similar two embeddings are. It measures the angle between two lists of numbers. A small angle means they are similar. This is how the app decides which chunks are most relevant to a question.

Chunking — splitting a long document into smaller pieces so each piece can be embedded and retrieved individually. Chunks are 500 words with 50 word overlap to avoid cutting meaning at boundaries.

Vector store — a database designed to store and search through embeddings quickly. This app uses FAISS which is an in-memory vector store. It resets every time the app restarts.

top_k retrieval — the number of chunks retrieved for each question. This app retrieves the top 3 most relevant chunks. Retrieving more gives more context but uses more of the prompt space.

Grounding vs hallucination — when Claude answers from your documents it is grounded. When it makes something up it is hallucinating. This app instructs Claude to say clearly when the documents do not contain enough information instead of guessing.

---

## Project Structure

app.py — the main Flask application with all three endpoints
requirements.txt — the list of Python packages needed
.env.example — a template showing what environment variables are needed
.gitignore — tells Git which files to never upload
README.md — this file
LEARNING.md — learning outcomes from both tasks

---

## Environment Variables

ANTHROPIC_API_KEY — your Anthropic API key from console.anthropic.com