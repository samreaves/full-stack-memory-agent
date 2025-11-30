import requests
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

FRONTIER_MODEL_URL = os.getenv("FRONTIER_MODEL_URL")
FRONTIER_MODEL_NAME = os.getenv("FRONTIER_MODEL_NAME")
FRONTIER_MODEL_PROVIDER_API_KEY = os.getenv("FRONTIER_MODEL_PROVIDER_API_KEY")
EMBEDDING_MODEL_URL = os.getenv("EMBEDDING_MODEL_URL")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
EMBEDDING_MODEL_DIMENSIONS = os.getenv("EMBEDDING_MODEL_DIMENSIONS")
EMBEDDING_MODEL_PROVIDER_API_KEY = os.getenv("EMBEDDING_MODEL_PROVIDER_API_KEY")

if not FRONTIER_MODEL_URL:
    raise ValueError("FRONTIER_MODEL_URL is not set")
if not FRONTIER_MODEL_NAME:
    raise ValueError("FRONTIER_MODEL_NAME is not set")
if not EMBEDDING_MODEL_NAME:
    raise ValueError("EMBEDDING_MODEL_NAME is not set")
if not EMBEDDING_MODEL_URL:
    raise ValueError("EMBEDDING_MODEL_URL is not set")
if not FRONTIER_MODEL_PROVIDER_API_KEY:
    logger.warning("FRONTIER_MODEL_PROVIDER_API_KEY is not set")
if not EMBEDDING_MODEL_PROVIDER_API_KEY:
    logger.warning("EMBEDDING_MODEL_PROVIDER_API_KEY is not set")
if not EMBEDDING_MODEL_DIMENSIONS:
    raise ValueError("EMBEDDING_MODEL_DIMENSIONS is not set")


async def generate_chat_stream(messages: list):
    """
    Generate a chat stream from a list of messages.
    """

    response = requests.post(
        FRONTIER_MODEL_URL + "/v1/chat/completions",
        json={
            "model": FRONTIER_MODEL_NAME,
            "messages": messages,
            "stream": True
        },
        headers={
            "Authorization": f"Bearer {FRONTIER_MODEL_PROVIDER_API_KEY}"
        },
        stream=True,
        timeout=60
    )
    return response

async def generate_chat(messages: list):
    """
    Generate a chat from a list of messages.
    """
    response = requests.post(
        FRONTIER_MODEL_URL + "/v1/chat/completions",
        json={
            "model": FRONTIER_MODEL_NAME,
            "messages": messages,
        },
        headers={
            "Authorization": f"Bearer {FRONTIER_MODEL_PROVIDER_API_KEY}"
        },
        timeout=30
    )
    return response


async def get_embedding(message: str):
    """
    Get embedding for a given message.
    """
    embedding_response = requests.post(
        EMBEDDING_MODEL_URL + "/v1/embeddings",
        json={
            "model": EMBEDDING_MODEL_NAME,
            "dimensions": int(EMBEDDING_MODEL_DIMENSIONS),
            "input": message,
        },
        headers={
            "Authorization": f"Bearer {EMBEDDING_MODEL_PROVIDER_API_KEY}"
        },
        timeout=30
    )
    return embedding_response