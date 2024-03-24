from pydantic import BaseModel

class RegisterUser(BaseModel):
    id: str
    listen_to: list[str]

class UserListen(BaseModel):
    channel: int
