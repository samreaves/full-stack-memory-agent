from pydantic import BaseModel
from schemas.message import Message, ChatMessage
from typing import Optional

class Conversation(BaseModel):
    id: str
    title: str
    messages: Optional[list[Message]] = None

class ChatConversation(BaseModel):
    id: str
    title: str
    messages: Optional[list[ChatMessage]] = []