print("Hello, World!")
import asyncio
from app.AI.chatbot import get_response, main, initialize_chat_session

async def demo():
    print("Starting the chatbot...")
    print("This may take a moment to initialize the servers...")

    # Option 1: Get a single response
    # response = await get_response("Hello, how can you help me?")
    # print(f"\nChatbot response: {response}")

    # Option 2: Start an interactive session with tools if available
    try:
        # First try with tools
        await main()
    except Exception as e:
        print(f"Error starting chatbot with tools: {e}")
        print("Falling back to basic chat without tools...")

        # Initialize without tools
        chat_session = await initialize_chat_session(use_tools=False)
        await chat_session.start()

if __name__ == "__main__":
    asyncio.run(demo())