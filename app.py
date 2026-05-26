from flask import Flask, request, jsonify
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def query_llm(messages):
    system_message = next((m["content"] for m in messages if m["role"] == "system"), "You are a helpful assistant.")
    conversation = [m for m in messages if m["role"] != "system"]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=system_message,
        messages=conversation
    )
    return response.content[0].text


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

    MAX_MESSAGES = 10
    system_message = {"role": "system", "content": "You are a helpful assistant. Keep your answers clear and concise."}

    if len(messages) > MAX_MESSAGES:
        messages = messages[-MAX_MESSAGES:]

    full_messages = [system_message] + messages

    answer = query_llm(full_messages)

    messages.append({"role": "assistant", "content": answer})

    return jsonify({
        "answer": answer,
        "messages": messages
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)