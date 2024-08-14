from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RootProviderCreate(BaseModel):
    token: Optional[str] = None
    name: str
    description: str


class RootChangeMaxSpotLimit(BaseModel):
    id: UUID
    value: int
