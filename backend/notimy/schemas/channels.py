from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    text: str


class CreateChannel(BaseModel):
    token: Optional[str] = None
    message: Optional[Message] = None
    name: str


class AddMessage(BaseModel):
    token: Optional[str] = None
    channel_id: UUID
    message: Message
