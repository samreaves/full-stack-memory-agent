from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import logging

from libs.llm_service import get_embedding, generate_chat_stream
from libs.vector_service import find_relevant_context_from_db
from libs.database import get_db
from repositories.message import create_message, get_messages
from schemas.request import ChatRequest
import json

logger = logging.getLogger(__name__)


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
            try:
                embedding_response = await get_embedding(agent_response["content"])
                embedding_response.raise_for_status()  # Raise an exception for bad status codes
                embedding_data = embedding_response.json()
                
                # Extract embedding with proper validation
                data_list = embedding_data.get("data", [])
                if not data_list:
                    raise ValueError("No embedding data in response")
                
                agent_response_embedding = data_list[0].get("embedding", [])
                if not agent_response_embedding:
                    raise ValueError("Embedding is empty in response")
                
                agent_response["embedding"] = agent_response_embedding
            except Exception as e:
                logger.error(f"Error getting embedding: {str(e)}")
                # Yield error and skip saving message
                yield f"data: {json.dumps({'error': f'Error getting embedding: {str(e)}'})}\n\n"
                return

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
        try:
            embedding_response = await get_embedding(request.message)
            embedding_response.raise_for_status()  # Raise an exception for bad status codes
            embedding_data = embedding_response.json()

            # Extract embedding with proper validation
            data_list = embedding_data.get("data", [])
            if not data_list:
                raise ValueError("No embedding data in response")

            message_embedding = data_list[0].get("embedding", [])
            if not message_embedding:
                raise ValueError("Embedding is empty in response")

            current_message["embedding"] = message_embedding
        except Exception as e:
            logger.error(f"Error getting embedding for user message: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting embedding: {str(e)}")

        message = create_message(db, request.conversation_id, current_message["role"], current_message["content"], current_message["embedding"])
        db.commit()
        db.refresh(message)
        messages = get_messages(db, request.conversation_id)

        relevant_context = await find_relevant_context_from_db(
            db=db,
            query_embedding=message_embedding,
            top_n=5
        )

        # Filter to only cross-conversation context as messages from current conversation already included
        cross_conversation_context = [
            llm_message for llm_message in relevant_context
            if str(llm_message.conversation_id) != str(request.conversation_id)
        ]

        if len(messages) > 6 and cross_conversation_context:
            older_messages = messages[:-6]
            recent_messages = messages[-6:]

            # Flatten into a single list of {role, content} dicts in the order:
            # older conversation messages -> cross‑conversation context -> recent messages
            messages_for_stream = [
                *[{"role": llm_message.role, "content": llm_message.content} for llm_message in older_messages],
                *[{"role": llm_message.role, "content": llm_message.content} for llm_message in cross_conversation_context],
                *[{"role": llm_message.role, "content": llm_message.content} for llm_message in recent_messages],
            ]
        elif len(messages) <= 5 and cross_conversation_context:
            # Cross‑conversation context first, then current conversation messages
            messages_for_stream = [
                *[{"role": llm_message.role, "content": llm_message.content} for llm_message in cross_conversation_context],
                *[{"role": llm_message.role, "content": llm_message.content} for llm_message in messages],]
        else:
            # Only current conversation messages
            messages_for_stream = [
                {"role": llm_message.role, "content": llm_message.content} for llm_message in messages
            ]

        # Stream the response
        return StreamingResponse(
            generate_stream(request.conversation_id, messages_for_stream, db),
            media_type="text/event-stream"
        )
