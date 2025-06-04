from pydantic import BaseModel

class Message(BaseModel):
    """Message model for chat requests"""
    message: str
    context: str = ""  # Learning context/history 