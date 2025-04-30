from fastapi import APIRouter, HTTPException
from app.agents.agent import initialize_agent
from pydantic import BaseModel
chat_router = APIRouter()
CHATSESSION = None

@chat_router.post("/initialize-chat")
async def initialize_chat(user_id: str):
    global CHATSESSION
    """
    Endpoint to initialize a chat session for a user.
    """
    try:
        # Initialize the chat session
        CHATSESSION = await initialize_agent(user_id=user_id)
        if CHATSESSION is None:
            raise HTTPException(status_code=500, detail="Failed to initialize chat session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing chat session: {str(e)}")

    
    
    return {"message": "Chat session initialized successfully"}


class MessageRequest(BaseModel):
    message: str

@chat_router.post("/send_message")
async def chat(request: MessageRequest):
    """
    Endpoint to send a message to the chat session and receive a response.
    """
    global CHATSESSION
    if CHATSESSION is None:
        raise HTTPException(status_code=400, detail="Chat session not initialized")
    
    try:
        # Send the message to the chat session
        response = await CHATSESSION.call_agent_async(request.message)
        if response is None:
            raise HTTPException(status_code=500, detail="Failed to get response from chat session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat session: {str(e)}")

    return {"response": response}