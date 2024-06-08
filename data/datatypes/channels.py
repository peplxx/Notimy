from pydantic import BaseModel


class Message(BaseModel):
    message: str



# Spot-token is used for channel creation
class ChanelCreation(BaseModel):
    token: str
    start_message: Message
    name: str

class AddMessage(BaseModel):
    token: str
    message: Message
    channel: int