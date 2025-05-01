from . import Agent
from app.repo.base import ResortManager
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class RoomSchema(BaseModel):
    id: UUID
    number: str
    is_booked: bool

    model_config = ConfigDict(from_attributes=True)

resortManager = ResortManager()

def getAvailableRooms():
    """
    Function to get available rooms from the database and return them 
    as a JSON serializable list using a Pydantic model.

    Args:
        None
    Returns:
        list: A list of available rooms, each represented as a dictionary.
    """
    rooms = resortManager.get_available_rooms()
    return [RoomSchema.model_validate(room).model_dump() for room in rooms]

def getUserBookings(user_id: UUID):
    """
    Function to get user bookings from the database and return them 
    as a JSON serializable list using a Pydantic model.

    Args:
        user_id (UUID): The ID of the user whose bookings are to be retrieved.
    
    Returns:
        list: A list of user bookings, each represented as a dictionary.
    """
    bookings = resortManager.get_user_bookings(user_id)
    return [RoomSchema.model_validate(booking).model_dump() for booking in bookings]

def bookRoom(user_id: UUID, room_id: UUID):
    """
    Function to book a room for a user. It checks if the room is available
    If the room is available, it return a booking uri so user can click it to book the room.

    Args:
        user_id (UUID): The ID of the user booking the room.
        room_id (UUID): The ID of the room to be booked.
    
    Returns:
        dict: A dictionary containing either an error message or a booking URI.
    """
    if resortManager.is_room_booked(room_id):
        return {"error": "Room is already booked."}
    
    # return uri for booking
    return {"booking_uri": f"http://localhost:8000/booking?user_id={user_id}&room_id={room_id}"}

def getRepoAgent():
    try:
        RepoAgent = Agent(
            name="RepoAgent",
            description="A repo agent that can manage resort bookings, including checking available rooms, booking rooms, and retrieving user bookings.",
            instruction=(
            "You are a repo agent responsible for managing resort bookings. "
            "Your tasks include checking the availability of rooms, booking rooms for users, "
            "and retrieving bookings made by specific users. When checking available rooms, "
            "ensure you provide accurate and up-to-date information about room availability. "
            "When booking a room, verify that the room is not already booked before proceeding, "
            "and provide a booking URI for the user to complete the booking process. "
            "When retrieving user bookings, ensure you return all relevant details about the bookings "
            "in a structured and JSON-serializable format."
            ),
            tools=[bookRoom, getAvailableRooms, getUserBookings],
        )
    except Exception as e:
        print(f"Error creating RepoAgent: {e}")
        return None
    
    return RepoAgent