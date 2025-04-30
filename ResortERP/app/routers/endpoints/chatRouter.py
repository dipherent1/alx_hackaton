from fastapi import APIRouter, HTTPException
from app.agents.agent import initialize_agent
chat_router = APIRouter()

@chat_router.post("/initialize-chat")
async def initialize_chat(user_id: int):
    """
    Endpoint to initialize a chat session for a user.
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # Logic to initialize the chat session
    chat_session = {
        "user_id": user_id,
        "session_id": "unique_session_id",  # Replace with actual session ID generation logic
        "status": "initialized"
    }
    
    return {"message": "Chat session initialized successfully", "data": chat_session}