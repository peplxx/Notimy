from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    text: str


class CreateChannel(BaseModel):
    token: Optional[str] = None
    message: Optional[Message] = None
    name: str


