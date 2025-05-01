# app/routers/your_router_file.py

from fastapi import APIRouter, HTTPException, Depends
# Removed Session import as it's no longer directly injected here
from uuid import UUID
from typing import List

# Import the manager and the dependency function
from app.repo.base import ResortManager, getResortManager # <--- Import dependency
# Import your schemas
from app.domain.schema.base import UserSchema, RoomSchema # Adjust import path

base_router = APIRouter()

# Endpoint to create a room
@base_router.post("/room", response_model=RoomSchema)
async def create_room_endpoint(
    room_data: RoomSchema,
    # Only depend on getResortManager
    resort_manager: ResortManager = Depends(getResortManager) # <--- Correct dependency
):
    """
    Endpoint to create a room in the database using injected ResortManager.
    """
    try:
        # Call manager method directly (it uses its own self.db)
        created_room_model = resort_manager.create_room(room_data=room_data) # <--- No db passed
        return created_room_model

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating room: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while creating room.")


# Endpoint to create a user
@base_router.post("/user", response_model=UserSchema)
async def create_user_endpoint(
    user_data: UserSchema,
    # Only depend on getResortManager
    resort_manager: ResortManager = Depends(getResortManager) # <--- Correct dependency
):
    """
    Endpoint to create a user in the database using injected ResortManager.
    """
    try:
        # Call manager method directly
        created_user_model = resort_manager.create_user(user_data=user_data) # <--- No db passed
        return created_user_model

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while creating user.")


# Example: Get available rooms
@base_router.get("/rooms/available", response_model=List[RoomSchema])
async def get_available_rooms_endpoint(
    # Only depend on getResortManager
    resort_manager: ResortManager = Depends(getResortManager) # <--- Correct dependency
):
    """
    Endpoint to get available rooms using injected ResortManager.
    """
    try:
        # Call manager method directly
        available_rooms = resort_manager.get_available_rooms() # <--- No db passed
        return available_rooms
    except Exception as e:
        print(f"Error getting available rooms: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# --- Update ALL other endpoints similarly ---
# Example: Book a room (assuming you have endpoint parameters for user_id, room_id)
@base_router.post("/booking/user/{user_id}/room/{room_id}") # Assuming BookingSchema exists
async def book_room_endpoint(
    user_id: UUID,
    room_id: UUID,
    resort_manager: ResortManager = Depends(getResortManager)
):
     try:
         booking = resort_manager.book_room(user_id=user_id, room_id=room_id)
         # Need BookingSchema for response_model
         return booking # FastAPI converts if BookingSchema.Config.from_attributes=True
     except HTTPException as http_exc:
        raise http_exc
     except Exception as e:
        print(f"Error booking room: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while booking room.")