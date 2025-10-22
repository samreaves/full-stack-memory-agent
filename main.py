from fastapi import FastAPI
from chat import router as chat_router
from health import router as health_router
import uvicorn

app = FastAPI()

app.include_router(chat_router, prefix="/chat")
app.include_router(health_router, prefix="/health")

@app.get("/")
async def root():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)