#!/usr/bin/env python3
import asyncio
from chatbot import get_response, initialize_chat_session

async def example_usage():
    """Example of how to use the chatbot as an API."""
    print("Example 1: Single response mode")
    # Get a response for a single message
    response = await get_response("What can you help me with?")
    print(f"Response: {response}")
    
    print("\nExample 2: Conversation mode")
    # Initialize a chat session
    chat_session = await initialize_chat_session(use_tools=False)
    
    # Send multiple messages to the same session
    response1 = await chat_session.process_message("Hello, who are you?")
    print(f"Response 1: {response1}")
    
    response2 = await chat_session.process_message("What can you do for me?")
    print(f"Response 2: {response2}")
    
    response3 = await chat_session.process_message("Can you remember what I asked first?")
    print(f"Response 3: {response3}")

if __name__ == "__main__":
    asyncio.run(example_usage())
