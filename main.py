from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes.chat import router as chat_router
from routes.health import router as health_router
import uvicorn

app = FastAPI()

app.include_router(chat_router, prefix="/chat")
app.include_router(health_router, prefix="/health")

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