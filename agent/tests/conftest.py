import os

# Set minimal env vars
os.environ.setdefault("FRONTIER_MODEL_NAME", "somemodel")
os.environ.setdefault("FRONTIER_MODEL_URL", "https://api.openai.com")
os.environ.setdefault("EMBEDDING_MODEL_NAME", "somemodel")
os.environ.setdefault("EMBEDDING_MODEL_URL", "https://api.openai.com")
os.environ.setdefault("EMBEDDING_MODEL_DIMENSIONS", "1024")
os.environ.setdefault("EMBEDDING_MODEL_PROVIDER_API_KEY", "somemodel")
os.environ.setdefault("FRONTIER_MODEL_PROVIDER_API_KEY", "somemodel")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "testdb")
os.environ.setdefault("POSTGRES_USER", "testuser")
os.environ.setdefault("POSTGRES_PASSWORD", "testpassword")

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)