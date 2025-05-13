# app/agents/rag_agent.py

from google.adk.agents import Agent

# Import the calendar tool functions
from .tools.rag_tools.google_calendar import (
    tool_get_next_10_calendar_events,
    tool_get_calendar_events_in_range
)

def getRagAgent() -> Agent:
    """Creates the RAG agent specialized in accessing Google Calendar."""

    calendar_tools = [
        tool_get_next_10_calendar_events,
        tool_get_calendar_events_in_range,
    ]

    rag_agent = Agent(
        name="google_calendar_rag_agent",
        # Use a model strong enough for function calling and understanding dates
        model="gemini-1.5-flash", # Or gemini-pro
        description=(
            "An agent that can access and retrieve information from the user's "
            "primary Google Calendar. It can fetch upcoming events or events "
            "within a specified date range."
        ),
        instruction=(
            "You are a helpful assistant with access to the user's Google Calendar. "
            "Use the provided tools to answer questions about calendar events. "
            "When retrieving events in a range, ensure you understand the start and end dates/times "
            "from the user's query and provide them to the tool in ISO 8601 format "
            "(e.g., 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SSZ'). "
            "Clearly present the event information (summary and start time) found. "
            "If no events are found, state that clearly. If an error occurs, report it."
            "You need valid, pre-existing authentication credentials (token.json) to function."
        ),
        tools=calendar_tools,
        # enable_feedback=False # Optional
    )
    return rag_agent

# Example of how you might use it elsewhere (similar to your WeatherTimeAgent setup)
# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService
# from app.config.env import get_settings # Assuming you need API key for ADK/GenAI
#
# async def initialize_rag_agent(user_id):
#     settings = get_settings()
#     # Ensure GenAI API key is set if needed by the underlying model
#     # os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
#
#     agent_instance = getRagAgent()
#     session_service = InMemorySessionService()
#     APP_NAME = "rag_calendar_app"
#     SESSION_ID = f"session_{user_id}_calendar" # Make session ID unique per user maybe
#
#     session = session_service.create_session(
#         app_name=APP_NAME, user_id=user_id, session_id=SESSION_ID
#     )
#     runner = Runner(
#         agent=agent_instance, app_name=APP_NAME, session_service=session_service
#     )
#     # You might create a wrapper class like WeatherTimeAgent or use the runner directly
#     print(f"RAG Agent Runner initialized for user {user_id}")
#     return runner, session # Return runner and session for interaction