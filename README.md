# Learning AI Agents with Memory in Python

## Objective
1. Set up a basic server using Python, uv, and FastAPI
2. Store sessions in memory first
3. Create an endpoint that receives chat messages, communicates to a model, saves the response, and streams the response back to the client

## Later goals
1. Add Svelte UI for lightweight chat client
2. Embed meanings and store them in vector db. Adjust model prompts with additional context from this db

## How to run this project
1. Install uv ```brew install uv```
2. Install dependencies ```uv sync```
3. Add an .env file with the following environment variables:
- FRONTIER_MODEL_URL={your-model-provider-domain-name} (https://api.openai.com)
- FRONTIER_MODEL={your-selected-model} (gpt-4o-mini)
4. Run the app ```uv run main.py```