from pydantic import BaseModel

class RegisterUser(BaseModel):
    id: str
    listen_to: list[str]
