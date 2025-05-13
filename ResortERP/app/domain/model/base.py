import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.config.db import Base


# Define the User table
class User(Base):
    __tablename__ = 'users'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)

# Define the Room table
class Room(Base):
    __tablename__ = 'rooms'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    number = Column(String, unique=True, nullable=False, index=True)
    is_booked = Column(Boolean, default=False, nullable=False)

# Define the Booking table
class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    room_id = Column(PG_UUID(as_uuid=True), ForeignKey('rooms.id'), nullable=False)
    booking_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")
    room = relationship("Room")
