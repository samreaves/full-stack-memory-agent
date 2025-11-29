# Learning AI Agents with Memory in Python | The Agent

## How to run this app
1. Install uv ```brew install uv```
2. Install dependencies ```uv sync```
3. Copy the root .env.example file to an .env file with your own environment variables:
- FRONTIER_MODEL_URL={your-model-provider-domain-name} (https://api.openai.com)
- FRONTIER_MODEL={your-selected-model} (gpt-4o-mini)
- EMBEDDING_MODEL={your-embedding-model} (text-embedding-nomic-embed-text-v1.5)
4. Run the app ```uv run main.py```