# Learning Outcomes — Task 1

## What I Built
A Flask web API with two endpoints that accepts questions and returns AI-generated responses using the Anthropic API. One endpoint handles single questions, the other handles multi-turn conversations with full history.

## What I Learned

### Python and Flask
I learned that Flask is a lightweight Python framework that lets you create web endpoints with just a few lines of code. A decorator like @app.route tells Flask which URL to listen on and which function to run when a request comes in. I learned the difference between GET and POST requests and why POST is used when sending data to a server.

### APIs and HTTP
I learned that an API is a door that companies open so developers can use their product inside their own apps. Instead of using claude.ai in a browser, my code talks directly to Anthropic's servers by sending HTTP requests. Every request includes headers that give the server context, a body that contains the data, and gets back a response with the answer.

### Prompt Structure
I learned that LLM prompts have two types of messages. A system message gives the AI its instructions and personality before the conversation starts. A user message is the actual question being asked. Parameters like temperature control how creative the response is, and max_tokens limits how long the response can be.

### Why LLMs Have No Memory
This was the most important thing I learned. Every time you call an LLM API, it starts completely fresh with no knowledge of previous requests. To simulate memory, you have to pass the entire conversation history with every single request. The AI reads the full transcript each time and uses it as context. It is not actually remembering — it is re-reading.

### Handling Long Conversations
When a conversation gets too long it can exceed the model's context limit. I handled this by keeping only the most recent 10 messages. If the history is longer than that, the app trims it automatically using Python slice notation.

### Virtual Environments
I learned that a virtual environment is an isolated bubble for a project's Python packages. Installing packages inside a venv means they only exist for that project and don't conflict with other projects on the same computer. You have to activate it every time you open a new terminal session.

### Environment Variables and Secrets
I learned never to hardcode API keys or passwords directly in code. Instead they go in a .env file which is loaded at runtime by python-dotenv. The .env file is listed in .gitignore so it never gets uploaded to GitHub. A .env.example file is uploaded instead as a safe template showing what variables are needed.

### Git and GitHub
I learned the core Git workflow — git add stages files, git commit takes a snapshot with a message, and git push uploads it to GitHub. I also learned what a .gitignore file does and why every project needs one.

## Challenges I Faced
The Hugging Face API was blocked on my network so I switched to the Anthropic API instead. I learned how to debug connection errors by reading error messages in the terminal and isolating which part of the system was failing. I also ran into issues with port 5000 being taken by AirPlay on my Mac and learned to run Flask on a different port.

## What I Would Do Differently
I would set up the virtual environment and test the API connection before writing any application code, so I catch network or environment issues early rather than debugging them mid-build.