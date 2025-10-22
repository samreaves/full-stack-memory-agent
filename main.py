from fastapi import FastAPI
from chat import router
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/chat")

@app.get("/")
async def root():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)