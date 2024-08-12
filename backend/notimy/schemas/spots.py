from pydantic import BaseModel


class ChangeAlias(BaseModel):
    name: str
