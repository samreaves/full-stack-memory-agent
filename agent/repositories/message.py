from sqlalchemy.orm import Session
from models.message import Message
import uuid

def create_message(
    db: Session,
    conversation_id: str,
    role: str,
    content: str,
    embedding: list[float]
) -> Message:
    if not conversation_id:
        raise ValueError("conversation_id cannot be None or empty")

    if not role:
        raise ValueError("role cannot be None or empty")

    if not content:
        raise ValueError("content cannot be None or empty")

    if not embedding:
        raise ValueError("embedding cannot be None or empty")

    try:
        uuid_obj = uuid.UUID(str(conversation_id).strip())
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid conversation_id format: {conversation_id}") from e

    message = Message(
        conversation_id=uuid_obj,
        role=role,
        content=content,
        embedding=embedding
    )
    db.add(message)
    return message

def get_messages(db: Session, conversation_id: str) -> list[Message]:
    if not conversation_id:
        raise ValueError("conversation_id cannot be None or empty")

    try:
        uuid_obj = uuid.UUID(str(conversation_id).strip())
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid conversation_id format: {conversation_id}") from e

    return db.query(Message).filter(Message.conversation_id == uuid_obj).all()