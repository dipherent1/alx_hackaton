# from . import Agent
# from app.repo.base import ResortManager
# from pydantic import BaseModel, ConfigDict
# from uuid import UUID
# from app.repo.base import getResortManager
# from fastapi import Depends

# class RoomSchema(BaseModel):
#     id: UUID
#     number: str
#     is_booked: bool

#     model_config = ConfigDict(from_attributes=True)

# def getResortManager(resortManager: ResortManager = Depends(ResortManager)):
#     """
#     Function to get the ResortManager instance. If not provided, it creates a new one.

#     Args:
#         resortManager (ResortManager, optional): An existing ResortManager instance. Defaults to None.

#     Returns:
#         ResortManager: The ResortManager instance.
#     """
#     if resortManager is None:
#         resortManager = ResortManager()
#     return resortManager

# def getAvailableRooms():
#     """
#     Function to get available rooms from the database and return them 
#     as a JSON serializable list using a Pydantic model.

#     Returns:
#         list: A list of available rooms, each represented as a dictionary.
#     """
#     print("Available Rooms:")
#     resortManager = getResortManager()
#     rooms = resortManager.get_available_rooms()
#     rooms = [RoomSchema.model_validate(room).model_dump() for room in rooms]
#     print(rooms)
#     return rooms

# def getUserBookings(user_id: str):
#     """
#     Function to get user bookings from the database and return them 
#     as a JSON serializable list using a Pydantic model.

#     Args:
#         user_id (str): The ID of the user whose bookings are to be retrieved.
    
#     Returns:
#         list: A list of user bookings, each represented as a dictionary.
#     """
#     print("User Bookings:")
#     resortManager = getResortManager()
#     bookings = resortManager.get_user_bookings(user_id)
#     bookings = [RoomSchema.model_validate(booking).model_dump() for booking in bookings]
#     print(bookings)
#     return bookings

# def bookRoom(user_id: str, room_id: str):
#     """
#     Function to book a room for a user. It checks if the room is available
#     If the room is available, it return a booking uri so user can click it to book the room.

#     Args:
#         user_id (str): The ID of the user booking the room.
#         room_id (str): The ID of the room to be booked.
    
#     Returns:
#         dict: A dictionary containing either an error message or a booking URI.
#     """
#     print("Booking Room:")
#     resortManager = getResortManager()
#     if resortManager.is_room_booked(room_id):
#         return {"error": "Room is already booked."}
    
#     # return uri for booking
#     return {"booking_uri": f"http://localhost:8000/booking?user_id={user_id}&room_id={room_id}"}

from google.adk.agents import Agent
# Import the NEW tool functions
from .tools.repo_tools.repo_tools import (
    tool_get_available_rooms,
    tool_get_user_bookings,
    tool_book_room,
    tool_unbook_room
    # Add any other tools you create
)

def getRepoAgent() -> Agent:
    """Creates the sub-agent responsible for resort repository interactions."""

    # List the agent-specific tool functions
    repo_tools = [
        tool_get_available_rooms,
        tool_get_user_bookings,
        tool_book_room,
        tool_unbook_room,
    ]

    repo_agent = Agent(
        name="resort_database_manager",
        # Use a model capable of function calling
        model="gemini-1.5-flash", # Or gemini-pro, etc.
        description=(
            "Manages interactions with the resort's database. "
            "Can find available rooms, list user bookings, book rooms, and unbook rooms."
        ),
        instruction=(
            "You are a database interaction agent for a resort. "
            "Use the provided tools accurately based on the user's request. "
            "You can query room availability, user bookings, book a room, or unbook a room. "
            "Provide results clearly. Ask for user ID or room ID if needed and not provided."
            "For room booking, check if the room is available before booking, and you don't need user ID to book a room."
            "When booking or unbooking, confirm the action and provide relevant details like booking ID or room number."
        ),
        tools=repo_tools, # Use the wrapper tools
        # enable_feedback=False # Optional: disable if not needed
    )
    return repo_agent