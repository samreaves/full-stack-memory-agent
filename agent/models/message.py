from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid
import os
import dotenv
dotenv.load_dotenv()

from libs.database import Base

EMBEDDING_MODEL_DIMENSIONS = os.getenv("EMBEDDING_MODEL_DIMENSIONS")

if EMBEDDING_MODEL_DIMENSIONS:
    EMBEDDING_MODEL_DIMENSIONS = int(EMBEDDING_MODEL_DIMENSIONS)
else:
    raise ValueError("EMBEDDING_MODEL_DIMENSIONS is not set")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"))
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(EMBEDDING_MODEL_DIMENSIONS))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    conversation = relationship("Conversation", back_populates="messages")
