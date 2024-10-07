from typing import Optional

from pydantic import BaseModel


class TelegramData(BaseModel):
    telegram_id: int
    telegram_username: Optional[str]
    telegram_firstname: Optional[str]
    telegram_lastname: Optional[str]