from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json
from models.requests import ChatRequest, EmbeddingRequest
from libs.llm_service import get_embedding, generate_chat_stream


router = APIRouter()


sessions = {}

async def generate_stream(session_id: str, messages: list):
    """
    Generator function that streams tokens from LLM source and accumulates the complete response.
    """
    complete_response = ""
    
    # Make streaming request to LMStudio
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
        if session_id in sessions:
            agent_response = {
                "role": "assistant",
                "content": complete_response
            }

            # Find embedding of the agent response and save it
            embedding_response = await get_embedding(agent_response["content"])
            agent_response_embedding = embedding_response.json().get("data", [{}])[0].get("embedding", [])
            agent_response["embedding"] = agent_response_embedding

            sessions[session_id].append(agent_response)
        
        # Signal completion to client
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    except Exception as e:
        error_msg = f"Error streaming from LMStudio: {str(e)}"
        yield f"data: {json.dumps({'error': error_msg})}\n\n"


@router.post("")
async def chat(request: ChatRequest):
    """
    Handle incoming chat messages and stream responses from LLM source.
    """
    session_id = request.session_id
    
    # Initialize session if it doesn't exist
    if session_id not in sessions:
        sessions[session_id] = []

    current_message = {
        "role": "user",
        "content": request.message
    }

    # Find embedding of the message and save it
    embedding_response = await get_embedding(request.message)
    message_embedding = embedding_response.json().get("data", [{}])[0].get("embedding", [])
    current_message["embedding"] = message_embedding
    
    # Append user message to session
    sessions[session_id].append(current_message)
    
    # Stream the response
    return StreamingResponse(
        generate_stream(session_id, sessions[session_id]),
        media_type="text/event-stream"
    )

@router.get("/history")
async def get_history(session_id: str):
    """
    Retrieve chat history for a given session.
    """
    return {
        "messages": sessions.get(session_id, [])
    }
