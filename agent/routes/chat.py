from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from libs.llm_service import get_embedding, generate_chat_stream
from libs.database import get_db
from repositories.message import create_message, get_messages
from schemas.request import ChatRequest
import json


router = APIRouter()

sessions = {}

async def generate_stream(conversation_id: str, messages: list, db: Session = Depends(get_db)):
    """
    Generator function that streams tokens from LLM source and accumulates the complete response.
    """
    complete_response = ""
    
    # Make streaming request to model provider
    try:
        response = await generate_chat_stream(messages)
        response.raise_for_status()
        
        # Process the streaming response
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                
                # SSE format: lines start with "data: "
                if line.startswith('data: '):
                    content = line[6:]  # Remove 'data: ' prefix
                    
                    # Check for stream end
                    if content.strip() == '[DONE]':
                        break
                    
                    try:
                        data = json.loads(content)
                        # Extract the token from the response
                        token = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                        
                        if token:
                            complete_response += token
                            # Yield in SSE format for the client
                            yield f"data: {json.dumps({'token': token})}\n\n"
                    
                    except json.JSONDecodeError:
                        continue
        
        # After streaming completes, save the full assistant response
        try:
            agent_response = {
                "role": "assistant",
                "content": complete_response
            }

            # Find embedding of the agent response and save it
            embedding_response = await get_embedding(agent_response["content"])
            agent_response_embedding = embedding_response.json().get("data", [{}])[0].get("embedding", [])
            agent_response["embedding"] = agent_response_embedding

            latest_message = create_message(db, conversation_id, agent_response["role"], agent_response["content"], agent_response_embedding)
            db.commit()
            db.refresh(latest_message)
        except Exception as e:
            error_msg = f"Error saving message: {str(e)}"
            yield f"data: {json.dumps({'error': error_msg})}\n\n"

        # Signal completion to client
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    except Exception as e:
        error_msg = f"Error streaming from LMStudio: {str(e)}"
        yield f"data: {json.dumps({'error': error_msg})}\n\n"


@router.post("")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Handle incoming chat messages and stream responses from LLM source.
    """

    if not request.conversation_id:
        raise HTTPException(status_code=400, detail="Conversation ID is required")

    else:

        current_message = {
            "role": "user",
            "content": request.message
        }

        # Find embedding of the message and save it
        embedding_response = await get_embedding(request.message)
        message_embedding = embedding_response.json().get("data", [{}])[0].get("embedding", [])
        current_message["embedding"] = message_embedding

        message = create_message(db, request.conversation_id, current_message["role"], current_message["content"], current_message["embedding"])
        db.commit()
        db.refresh(message)
        messages = get_messages(db, request.conversation_id)

        messages_for_stream = [{"role": llm_message.role, "content": llm_message.content} for llm_message in messages]

        # Stream the response
        return StreamingResponse(
            generate_stream(request.conversation_id, messages_for_stream, db),
            media_type="text/event-stream"
        )
