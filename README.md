# Learning AI Agents with Memory in Python | The Project

## Purpose of this project
### Learn
1. Learn FastAPI, uv, and modern Python conventions
2. Learn LLM API endpoints and how they work (/chat/completions and /embeddings)
3. Learn how to find relevant data to user message, and inject context before agent response
4. Learn Svelte

### Demonstrate
While this is not the cleanest code or perfect example by any means, this is a demonstration of a working ChatGPT clone that can be run locally for free. There are no LLM frameworks such as Langchain or Agent SDK used, so anyone browsing can understand how agentic apps actually work under the hood. An example is included in .env.example that shows which models to run using Ollama or LMStudio to run this without any cost whatsoever (if your hardware can handle it).


## Objective (now complete)
1. Set up a basic server using Python, uv, and FastAPI
2. Store sessions in memory first
3. Create an endpoint that receives chat messages, communicates to a model, saves the response, and streams the response back to the client
4. Add Svelte UI for lightweight chat client
5. Embed meanings and store them in vector db. Adjust model prompts with additional context from this db

## How to run this project
1. Copy the .env.example file to an .env file with your own environment variables:
- FRONTIER_MODEL_URL=https://api.openai.com
- FRONTIER_MODEL_NAME=gpt-5-nano
- FRONTIER_MODEL_PROVIDER_API_KEY=your-openai-api-key
- EMBEDDING_MODEL_URL==https://api.openai.com
- EMBEDDING_MODEL_NAME=text-embedding-3-small
- EMBEDDING_MODEL_DIMENSIONS=1024
- EMBEDDING_MODEL_PROVIDER_API_KEY=your-openai-api-key
2. Run the agent, client & Postgres DB ```docker compose up --build -d```
3. Visit http://${CLIENT_HOST}:${CLIENT_PORT} to speak with your agent.