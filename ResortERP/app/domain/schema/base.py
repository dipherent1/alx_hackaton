from pydantic import BaseModel

class RoomSchema(BaseModel):
    number: str
    is_booked: bool = False # Add default if applicable

    class Config:
        from_attributes = True # Use this instead of orm_mode in Pydantic v2
        arbitrary_types_allowed = True
        # json_encoders removed as UUID is handled better by default in Pydantic v2
        schema_extra = {
            "example": {
                "number": "101",
                "is_booked": False
            }
        }

class UserSchema(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True # Use this instead of orm_mode in Pydantic v2
        arbitrary_types_allowed = True
        # json_encoders removed
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }

# Optional: Define a specific response model if you want the "message" field
class MessageResponse(BaseModel):
    message: str

class RoomResponse(MessageResponse):
     room: RoomSchema

class UserResponse(MessageResponse):
     user: UserSchema
