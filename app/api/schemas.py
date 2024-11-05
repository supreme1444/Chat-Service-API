from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str


class UserSch(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    recipient_username: str
    content: str

class MessageSch(BaseModel):
    sender_id: int
    recipient_id: int
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True
