from sqlalchemy.orm import Session
from models.conversation import Conversation
import uuid

def create_conversation(
    db: Session,
    title: str
) -> Conversation:
    if not title:
        raise ValueError("title cannot be None or empty")
    try:
        title = title.strip()
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid title format: {title}") from e
    conversation = Conversation(title=title)
    db.add(conversation)

    return conversation

def get_conversation_by_id(db: Session, conversation_id: str) -> Conversation:
    return db.query(Conversation).filter(Conversation.id == uuid.UUID(conversation_id)).first()

def get_all_conversations(db: Session) -> list[Conversation]:
    return db.query(Conversation).all()