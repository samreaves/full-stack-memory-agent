from pydantic import BaseModel
from uuid import UUID

class Message(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    embedding: list[float]

class ChatMessage(BaseModel):
    role: str
    content: str