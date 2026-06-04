from flask import Flask, request, jsonify
import anthropic
import os
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import PyPDF2
import io

load_dotenv()

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

vector_store = []
index = None


def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    return chunks


def build_index(embeddings):
    embeddings_array = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings_array)
    dimension = embeddings_array.shape[1]
    idx = faiss.IndexFlatIP(dimension)
    idx.add(embeddings_array)
    return idx


def retrieve_relevant_chunks(question, top_k=3):
    global index
    if index is None or len(vector_store) == 0:
        return []
    question_embedding = embedding_model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")
    faiss.normalize_L2(question_embedding)
    distances, indices = index.search(question_embedding, top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1 and distances[0][i] > 0.3:
            results.append(vector_store[idx]["text"])
    return results


def query_llm(messages):
    system_message = next(
        (m["content"] for m in messages if m["role"] == "system"),
        "You are a helpful assistant."
    )
    conversation = [m for m in messages if m["role"] != "system"]
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=system_message,
        messages=conversation
    )
    return response.content[0].text


@app.route("/ingest", methods=["POST"])
def ingest():
    global index, vector_store

    text = None

    if request.content_type and "multipart/form-data" in request.content_type:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        file = request.files["file"]
        if file.filename.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        else:
            text = file.read().decode("utf-8")
    else:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Please provide text or a file"}), 400
        text = data["text"]

    if not text or not text.strip():
        return jsonify({"error": "Document is empty"}), 400

    chunks = chunk_text(text, chunk_size=500, overlap=50)

    embeddings = embedding_model.encode(chunks)

    for i, chunk in enumerate(chunks):
        vector_store.append({
            "text": chunk,
            "embedding": embeddings[i]
        })

    index = build_index([item["embedding"] for item in vector_store])

    return jsonify({
        "message": f"Successfully ingested document",
        "chunks_created": len(chunks),
        "total_chunks_stored": len(vector_store)
    })


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Please provide a question"}), 400
    question = data["question"]
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Keep your answers clear and concise."},
        {"role": "user", "content": question}
    ]
    answer = query_llm(messages)
    return jsonify({"answer": answer})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"error": "Please provide a messages array"}), 400

    messages = data["messages"]
    user_question = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"),
        None
    )

    relevant_chunks = []
    if user_question:
        relevant_chunks = retrieve_relevant_chunks(user_question, top_k=3)

    if relevant_chunks:
        context = "\n\n".join(relevant_chunks)
        system_content = f"""You are a helpful assistant. Answer questions based on the provided context when available. If the context does not contain enough information to answer the question, say so clearly instead of making something up.

Context from documents:
{context}"""
    else:
        system_content = "You are a helpful assistant. Keep your answers clear and concise. If you are asked about specific documents or files and none have been provided, let the user know."

    MAX_MESSAGES = 10
    if len(messages) > MAX_MESSAGES:
        messages = messages[-MAX_MESSAGES:]

    full_messages = [{"role": "system", "content": system_content}] + messages

    answer = query_llm(full_messages)

    messages.append({"role": "assistant", "content": answer})

    return jsonify({
        "answer": answer,
        "messages": messages,
        "context_used": len(relevant_chunks) > 0,
        "chunks_retrieved": len(relevant_chunks)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)