from pydantic import BaseModel


class Message(BaseModel):
    message: str


class ChanelCreation(BaseModel):
    token: str
    start_message: Message
    name: str
