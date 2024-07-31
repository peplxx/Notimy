from typing import Optional

from pydantic import BaseModel


class RegisterProvider(BaseModel):
    token: Optional[str] = None
    name: str
    description: str


class ProviderAuth(BaseModel):
    token: Optional[str] = None


class UpdateProviderData(BaseModel):
    token: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
