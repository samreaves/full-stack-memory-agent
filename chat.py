from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

sessions = {}

@router.post("")
async def chat(request: ChatRequest):
    sessions[request.session_id] = sessions.get(request.session_id, []) + [{"role": "user", "content": request.message}]
    print(sessions)
    return { "session_id": request.session_id, "message": request.message}