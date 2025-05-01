# app/repo/base.py (Add getResortManager here)

import uuid
from sqlalchemy.orm import Session
from datetime import datetime, timezone
# Assuming models are defined in app.domain.model.base
from app.domain.model.base import User, Room, Booking
# Assuming schemas are defined in app.domain.schema.base
from app.domain.schema.base import UserSchema, RoomSchema
from fastapi import HTTPException, Depends # <--- Add Depends
from typing import List
# Assuming get_db is in app.config.db
from app.config.db import get_db

class ResortManager:
    def __init__(self, db: Session):
        # The manager now holds the session for its lifetime (per request)
        self.db = db

    # ... (keep all your methods as they are in your last snippet) ...
    # (Methods like create_user, create_room now use self.db directly)
    # Create a user
    def create_user(self, user_data: UserSchema) -> User:
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=409, detail=f"User with email '{user_data.email}' already exists.")

        user = User(name=user_data.name, email=user_data.email)
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            print(f"Database error creating user: {e}")
            raise RuntimeError(f"Failed to save user to database") from e

    # Create a room
    def create_room(self, room_data: RoomSchema) -> Room:
        existing_room = self.db.query(Room).filter(Room.number == room_data.number).first()
        if existing_room:
            raise HTTPException(status_code=409, detail=f"Room with number '{room_data.number}' already exists.")

        room = Room(number=room_data.number, is_booked=room_data.is_booked)
        try:
            self.db.add(room)
            self.db.commit()
            self.db.refresh(room)
            return room
        except Exception as e:
            self.db.rollback()
            print(f"Database error creating room: {e}")
            raise RuntimeError(f"Failed to save room to database") from e

    # --- Rest of your manager methods using self.db ---
    # Book a room
    def book_room(self, user_id: uuid.UUID, room_id: uuid.UUID) -> Booking | None:
        # ... uses self.db ...
        room = self.db.query(Room).filter(Room.id == room_id).first()
        # ... rest of the logic ...
        if room and not room.is_booked:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                 raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found.")
            room.is_booked = True
            booking = Booking(user_id=user_id, room_id=room_id)
            # ... try/except block using self.db ...
            try:
                self.db.add(booking)
                # self.db.add(room) # Add room too if its state needs explicit add
                self.db.commit()
                self.db.refresh(booking)
                self.db.refresh(room) # Refresh room too
                return booking
            except Exception as e:
                self.db.rollback()
                print(f"Database error booking room: {e}")
                raise RuntimeError(f"Failed to book room") from e
        # ... other conditions ...
        elif room and room.is_booked:
            raise HTTPException(status_code=409, detail=f"Room '{room.number}' (ID: {room_id}) is already booked.")
        else:
            raise HTTPException(status_code=404, detail=f"Room with id '{room_id}' not found.")

    # Unbook a room
    def unbook_room(self, room_id: uuid.UUID) -> Room | None:
        # ... uses self.db ...
        room = self.db.query(Room).filter(Room.id == room_id).first()
        # ... rest of the logic using self.db ...
        if room and room.is_booked:
            try:
                booking = self.db.query(Booking).filter(Booking.room_id == room_id).first()
                if booking:
                    self.db.delete(booking)
                else:
                    print(f"Warning: Room {room_id} is booked but no corresponding booking found.")
                room.is_booked = False
                # self.db.add(room) # Add room if state needs explicit add
                self.db.commit()
                self.db.refresh(room)
                return room
            except Exception as e:
                 self.db.rollback()
                 print(f"Database error unbooking room: {e}")
                 raise RuntimeError(f"Failed to unbook room") from e
        # ... other conditions ...
        elif room and not room.is_booked:
             print(f"Room {room_id} was not booked.")
             return room
        else:
             raise HTTPException(status_code=404, detail=f"Room with id '{room_id}' not found.")


    # Get all bookings from user
    def get_user_bookings(self, user_id: uuid.UUID) -> List[Booking]:
        # ... uses self.db ...
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found.")
        return self.db.query(Booking).filter(Booking.user_id == user_id).all()


    # Get all available rooms
    def get_available_rooms(self) -> List[Room]:
        # ... uses self.db ...
        return self.db.query(Room).filter(Room.is_booked == False).all()


    # Is room booked
    def is_room_booked(self, room_id: uuid.UUID) -> bool | None:
        # ... uses self.db ...
        room = self.db.query(Room).filter(Room.id == room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail=f"Room with id '{room_id}' not found.")
        return room.is_booked


# --- Dependency function ---
def getResortManager(db: Session = Depends(get_db)) -> ResortManager:
    """
    Dependency function that provides a ResortManager instance
    initialized with a database session obtained from Depends(get_db).
    """
    return ResortManager(db) # Create instance with the injected session