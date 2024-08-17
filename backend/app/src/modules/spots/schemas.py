from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.config import get_settings
from app.data.db.models import Message

settings = get_settings()


class SpotChangeAlias(BaseModel):
    name: str


class SpotCreateChannel(BaseModel):
    message: Optional[Message] = None


class SpotAddMessage(BaseModel):
    channel_id: UUID
    message: Message


class CloseChannel(BaseModel):
    channel_id: UUID
