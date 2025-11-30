from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from routes.chat import router as chat_router
from routes.health import router as health_router
from routes.conversations import router as conversations_router
import uvicorn
from libs.database import engine, wait_for_db
import logging
import os
import dotenv
from alembic import command
from alembic.config import Config
dotenv.load_dotenv()

AGENT_PORT = os.getenv("AGENT_PORT") or 8000
AGENT_HOST = os.getenv("AGENT_HOST") or "0.0.0.0"
CLIENT_PORT = os.getenv("CLIENT_PORT") or 5173
CLIENT_HOST = os.getenv("CLIENT_HOST") or "localhost"

logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS before adding routers
client_origins = [
    f"http://{CLIENT_HOST}:{CLIENT_PORT}",
    f"https://{CLIENT_HOST}:{CLIENT_PORT}"
]

# Add CORS middleware (must be added before routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=client_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        # Wait for database to be ready
        wait_for_db()

        # Run Alembic migrations
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations applied successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise  # Fail fast if database setup fails

app.include_router(chat_router, prefix="/chat")
app.include_router(conversations_router, prefix="/conversations")
app.include_router(health_router, prefix="/health")

if __name__ == "__main__":
    uvicorn.run(app, host=AGENT_HOST, port=AGENT_PORT)