# Learning AI Agents with Memory in Python | The Project

## Objective
1. Set up a basic server using Python, uv, and FastAPI
2. Store sessions in memory first
3. Create an endpoint that receives chat messages, communicates to a model, saves the response, and streams the response back to the client
4. Add Svelte UI for lightweight chat client
5. Embed meanings and store them in vector db. Adjust model prompts with additional context from this db

## How to run this project
1. Copy the .env.example file to an .env file with your own environment variables:
- FRONTIER_MODEL_URL={your-model-provider-domain-name} (https://api.openai.com)
- FRONTIER_MODEL={your-selected-model} (gpt-4o-mini)
- EMBEDDING_MODEL={your-embedding-model} (text-embedding-nomic-embed-text-v1.5)
2. docker compose up -d