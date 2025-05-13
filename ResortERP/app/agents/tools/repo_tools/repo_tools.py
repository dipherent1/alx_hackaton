# app/agents/repo_tools.py (New File)

import uuid
from typing import List, Dict, Any  # Use Dict/Any for JSON-serializable returns
from app.config.db import SessionLocal  # Import the session factory directly
from app.repo.base import ResortManager
from fastapi import HTTPException  # Keep for status codes if needed

# --- Helper to create manager within a context ---
# Optional, but helps reduce repetition
def _get_manager_with_session():
    """
    Helper function to create a ResortManager instance with a database session.
    
    Returns:
        Tuple[ResortManager, SessionLocal]: A tuple containing the ResortManager instance and the database session.
    """
    db = SessionLocal()
    manager = ResortManager(db)
    return manager, db

# --- Wrapper Tools for the Agent ---

def tool_get_available_rooms() -> List[Dict[str, Any]]:
    """
    Retrieves a list of available rooms for the agent.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a room with the following keys:
            - "id" (str): The unique identifier of the room.
            - "number" (str): The room number.
            - "is_booked" (bool): Indicates whether the room is booked.
            - "error" (str, optional): An error message if the operation fails.
    """
    manager, db = _get_manager_with_session()
    try:
        rooms = manager.get_available_rooms()
        return [
            {"id": str(room.id), "number": room.number, "is_booked": room.is_booked}
            for room in rooms
        ]
    except Exception as e:
        print(f"Error in tool_get_available_rooms: {e}")
        return [{"error": f"Failed to retrieve available rooms: {str(e)}"}]
    finally:
        db.close()

def tool_get_user_bookings(user_id_str: str) -> List[Dict[str, Any]]:
    """
    Retrieves a list of bookings for a specific user.

    Args:
        user_id_str (str): The user ID as a string (UUID format).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a booking with the following keys:
            - "id" (str): The unique identifier of the booking.
            - "user_id" (str): The user ID associated with the booking.
            - "room_id" (str): The room ID associated with the booking.
            - "booking_date" (str): The booking date in ISO 8601 format.
            - "room_number" (str): The room number, or "N/A" if unavailable.
            - "error" (str, optional): An error message if the operation fails.
    """
    manager, db = _get_manager_with_session()
    try:
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            return [{"error": f"Invalid user ID format: '{user_id_str}'"}]

        bookings = manager.get_user_bookings(user_id=user_id)
        return [
            {
                "id": str(booking.id),
                "user_id": str(booking.user_id),
                "room_id": str(booking.room_id),
                "booking_date": booking.booking_date.isoformat(),
                "room_number": booking.room.number if booking.room else "N/A"
            }
            for booking in bookings
        ]
    except HTTPException as http_exc:
        print(f"Error in tool_get_user_bookings: {http_exc.detail}")
        return [{"error": http_exc.detail}]
    except Exception as e:
        print(f"Error in tool_get_user_bookings: {e}")
        return [{"error": f"Failed to retrieve user bookings: {str(e)}"}]
    finally:
        db.close()

def tool_book_room(room_number: str) -> Dict[str, Any]:
    """
    Generates a booking URL for a specific room based on its room number.

    Args:
        room_number (str): The room number as a string. Must be a valid numeric string.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "status" (str): "success" if the URL was generated successfully.
            - "booking_url" (str): The generated booking URL.
            - "error" (str, optional): An error message if the operation fails.
    
    Example:
        Input: "101"
        Output: {"status": "success", "booking_url": "https://example.com/book?room_number=101"}
    """
    try:
        if not room_number.isdigit():
            return {"error": "Invalid room number format."}

        booking_url = f"https://example.com/book?room_number={room_number}"
        return {"status": "success", "booking_url": booking_url}
    except Exception as e:
        print(f"Error in tool_book_room: {e}")
        return {"error": f"Failed to generate booking URL: {str(e)}"}

def tool_unbook_room(room_number: str) -> Dict[str, Any]:
    """
    Generates an unbooking URL for a specific room based on its room number.

    Args:
        room_number (str): The room number as a string. Must be a valid numeric string.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "status" (str): "success" if the URL was generated successfully.
            - "unbooking_url" (str): The generated unbooking URL.
            - "error" (str, optional): An error message if the operation fails.
    
    Example:
        Input: "101"
        Output: {"status": "success", "unbooking_url": "https://example.com/unbook?room_number=101"}
    """
    try:
        if not room_number.isdigit():
            return {"error": f"Invalid room number format: '{room_number}'"}

        unbooking_url = f"https://example.com/unbook?room_number={room_number}"
        return {"status": "success", "unbooking_url": unbooking_url}
    except Exception as e:
        print(f"Error in tool_unbook_room: {e}")
        return {"error": f"Failed to generate unbooking URL: {str(e)}"}
