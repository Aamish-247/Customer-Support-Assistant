from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_response
import uvicorn
import uuid
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name = "static")

# CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class chat_request(BaseModel):
    user_input: str
    user_id: str = None

@app.get("/")
async def root():
    """Root for Home page"""

    return FileResponse("static/home.html")

@app.get("/chat_interface")
async def chat_interface():
    """root for chat interface"""

    return FileResponse("static/index.html")

@app.post("/chat")
async def chat_bot(chat: chat_request):
    try:
        if not chat.user_id or chat.user_id == "" or chat.user_id == "string":
            chat_id = str(uuid.uuid4())
            current_user_id = chat_id
        else:
            current_user_id = chat.user_id
        response = get_response(chat.user_input, current_user_id)
        return {"response": response, "user_id": current_user_id}
    except Exception as e:
        error_user_id = current_user_id if current_user_id is not None else "unknown"
        raise HTTPException(status_code=500, detail={"message":f"internal server error: {str(e)}" , "user_id": error_user_id})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)