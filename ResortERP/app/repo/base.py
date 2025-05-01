import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from datetime import datetime

Base = declarative_base()

# Define the User table
class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Define the Room table
class Room(Base):
    __tablename__ = 'rooms'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    number = Column(String, unique=True, nullable=False)
    is_booked = Column(Boolean, default=False)

# Define the Booking table
class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey('rooms.id'), nullable=False)
    booking_date = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))

    user = relationship("User")
    room = relationship("Room")

class ResortManager:
    def __init__(self, db: Session):
        self.db = db

    # Create a user
    def create_user(self, name: str, email: str):
        user = User(name=name, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Create a room
    def create_room(self, number: str):
        room = Room(number=number)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    # Book a room
    def book_room(self, user_id: uuid.UUID, room_id: uuid.UUID):
        room = self.db.query(Room).filter(Room.id == room_id).first()
        if room and not room.is_booked:
            room.is_booked = True
            booking = Booking(user_id=user_id, room_id=room_id)
            self.db.add(booking)
            self.db.commit()
            self.db.refresh(booking)
            return booking
        return None

    # Unbook a room
    def unbook_room(self, room_id: uuid.UUID):
        room = self.db.query(Room).filter(Room.id == room_id).first()
        if room and room.is_booked:
            room.is_booked = False
            self.db.query(Booking).filter(Booking.room_id == room_id).delete()
            self.db.commit()
            return room
        return None
    
    # Get all bookings from user
    def get_user_bookings(self, user_id: uuid.UUID):
        bookings = self.db.query(Booking).filter(Booking.user_id == user_id).all()
        return bookings