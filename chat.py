from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import requests
import dotenv
import os

dotenv.load_dotenv()

router = APIRouter()

MODEL_NAME = os.getenv("FRONTIER_MODEL")
MODEL_URL = os.getenv("FRONTIER_MODEL_URL")

class ChatRequest(BaseModel):
    session_id: str
    message: str

class llmRequest(BaseModel):
    session_id: str
    messages: list[dict[str, str]]

sessions = {}

async def generate_stream(session_id: str, messages: list):
    """
    Generator function that streams tokens from LLM source and accumulates the complete response.
    """
    complete_response = ""
    
    # Make streaming request to LMStudio
    try:
        response = requests.post(
            MODEL_URL + "/v1/chat/completions",
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": True
            },
            stream=True,
            timeout=60
        )
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
            sessions[session_id].append({
                "role": "assistant",
                "content": complete_response
            })
        
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
    
    # Append user message to session
    sessions[session_id].append({
        "role": "user",
        "content": request.message
    })
    
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