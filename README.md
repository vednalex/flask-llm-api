# Flask LLM API

A simple Flask web API that lets you ask questions to an AI and have multi-turn conversations. Built using Python, Flask, and the Anthropic API (Claude).

---

## What This Project Does

This app has two endpoints:

- POST /ask — Send a single question, get a single AI-generated answer
- POST /chat — Send a full conversation history, get a response that remembers context

---

## Requirements

- Python 3.10 or higher
- An Anthropic API key (get one at https://console.anthropic.com)

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/vednalex/flask-llm-api.git
cd flask-llm-api

### 2. Create and activate a virtual environment
Mac:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set up your environment variables
cp .env.example .env
Then open .env and replace the placeholder with your real Anthropic API key.

### 5. Run the app
python app.py
The server will start at http://localhost:5001

---

## How to Use the Endpoints

### Endpoint 1: POST /ask
Send a single question and get an answer back.

curl -X POST http://localhost:5001/ask -H "Content-Type: application/json" -d '{"question": "What is the capital of France?"}'

Response:
{"answer": "The capital of France is Paris."}

### Endpoint 2: POST /chat
Send a conversation history and get a response with full context.

curl -X POST http://localhost:5001/chat -H "Content-Type: application/json" -d '{"messages": [{"role": "user", "content": "My name is Ved. What is your name?"}]}'

Response includes the answer plus the full updated conversation history.

---

## How Multi-Turn Conversation Works

LLM's dont have memory. Basically the way an LLM can remember is by passing the whole converstaion through again. So each time you ask a question the LLM parses through all the previous conversation then asnwers the latest one. But there is a limit to the memory. For example in the flask app we have set the limit to 10 lines. This means the LLM can only use the previous 10 lines of conversation to answer the response. This can be changed, but as you increase the memory limit other variables can change. For example cost.

---

## Project Structure

app.py — the main Flask application with both endpoints
requirements.txt — the list of Python packages needed
.env.example — a template showing what environment variables are needed
.gitignore — tells Git which files to never upload
README.md — this file

---

## Environment Variables

ANTHROPIC_API_KEY — your Anthropic API key from console.anthropic.com

---

## What I Learned

- Flask is a lightweight Python tool for building web APIs
- An API endpoint is a URL that accepts data and returns data
- Environment variables keep secrets out of your code
- Virtual environments keep each project's packages isolated
- LLMs have no memory — conversation history must be passed with every request
- Long conversations need to be trimmed to avoid hitting the model's context limit