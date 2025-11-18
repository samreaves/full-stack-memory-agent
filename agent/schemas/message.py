from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str
    embedding: list[float]

class ChatMessage(BaseModel):
    role: str
    content: str