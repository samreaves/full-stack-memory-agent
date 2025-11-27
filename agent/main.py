from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from routes.chat import router as chat_router
from routes.health import router as health_router
from routes.conversations import router as conversations_router
import uvicorn
from libs.database import engine, wait_for_db
from models.conversation import Base
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        # Wait for database to be ready
        wait_for_db()

        # Create tables (in production, use Alembic migrations instead)
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise  # Fail fast if database setup fails

app.include_router(chat_router, prefix="/chat")
app.include_router(conversations_router, prefix="/conversations")
app.include_router(health_router, prefix="/health")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your client origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
        Serve static HTML file for the chat interface.
    """
    with open("statics/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)