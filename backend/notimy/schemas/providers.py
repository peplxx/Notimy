from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator


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


class MaxSpotLimit(BaseModel):
    id: UUID
    value: int