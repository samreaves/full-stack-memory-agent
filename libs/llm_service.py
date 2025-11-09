import requests
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_URL = os.getenv("FRONTIER_MODEL_URL")
MODEL_NAME = os.getenv("FRONTIER_MODEL")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")

async def generate_chat_stream(messages: list):
    """
    Generate a chat stream from a list of messages.
    """
    response = requests.post(
        MODEL_URL + "/v1/chat/completions",
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": True
        },
        stream=True,
        timeout=60
    )
    return response

async def get_embedding(message: str):
    """
    Get embedding for a given message.
    """
    embedding_response = requests.post(
        MODEL_URL + "/v1/embeddings",
        json={
            "model": EMBEDDING_MODEL_NAME,
            "input": message,
        },
        timeout=60
    )
    return embedding_response