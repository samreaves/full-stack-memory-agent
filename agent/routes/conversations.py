from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from libs.llm_service import generate_chat
from libs.database import get_db
from sqlalchemy.orm import Session
from repositories.conversation import create_conversation, get_all_conversations, get_conversation_by_id
from repositories.message import get_messages
from schemas.conversation import Conversation, ChatConversation
from schemas.message import ChatMessage, Message
from schemas.request import ChatRequest

router = APIRouter()

@router.post("")
async def create_conversation_endpoint(chat_request: ChatRequest, db: Session = Depends(get_db)) -> Conversation:
    """
    Create a new conversation with title based on the first message
    """
    response = await generate_chat([{
        "role": "user",
        "content": f"Generate a title for a new conversation between a user and an assistant based on the following message: {chat_request.message}"
    }])

    title = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    conversation = create_conversation(db, title)
    db.commit()
    db.refresh(conversation)
    messages = get_messages(db, conversation.id)
    return Conversation(id=str(conversation.id), title=conversation.title, messages=[Message(role=message.role, content=message.content, embedding=message.embedding) for message in messages])


@router.get("")
async def get_conversations(db: Session = Depends(get_db)) -> list[Conversation]:
    """
    Get all conversations
    """
    try:
        conversations = get_all_conversations(db)
        return [Conversation(id=str(conversation.id), title=conversation.title) for conversation in conversations]
    except Exception as e:
        return JSONResponse(status_code=500, content=str("Internal server error"))


@router.get("/{conversation_id}")
async def get_conversations_by_id(conversation_id: str, db: Session = Depends(get_db)) -> ChatConversation:
    """
    Get conversation by id
    """
    try:
        conversation = get_conversation_by_id(db, conversation_id)
        if conversation is None:
            return JSONResponse(status_code=404, content=str("Conversation not found"))

        db_messages = get_messages(db, str(conversation.id))  # Convert UUID to string

        conversation_messages = [ChatMessage(role=message.role, content=message.content) for message in db_messages]

        conversation = ChatConversation(id=str(conversation.id), title=conversation.title, messages=conversation_messages)
        return conversation
    except Exception as e:
        print(f"DEBUG: Exception occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content=str("Internal server error"))
