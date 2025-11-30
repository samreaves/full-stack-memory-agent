# Learning AI Agents with Memory in Python | The Project

## Objective
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