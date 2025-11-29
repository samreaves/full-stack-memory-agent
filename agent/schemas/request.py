from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class EmbeddingRequest(BaseModel):
    message: str