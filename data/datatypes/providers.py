from pydantic import BaseModel


class RegisterProvider(BaseModel):
    token: str
    name: str
    description: str


class UpdateProviderData(BaseModel):
    token: str
    name: str
    description: str
