from typing import Optional

from pydantic import BaseModel


class ProviderUpdateData(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


