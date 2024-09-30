from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db import DeclarativeBase as Base
from app.data.db.utils import get_now
from app.src.common.push_notifications.dto import PushNotification


class Event(ABC):
    event_type: str
    source: Base
    session: AsyncSession
    pushNotification: Optional[PushNotification] = None
    registered_at: datetime = get_now()

    @abstractmethod
    def __init__(self, source: Base, session: AsyncSession):
        # Use init super().__init__ for subclasses after initializing all support properties
        self.source = source
        self.session = session

    async def process(self):
        await self.before_invoke()
        try:
            await self.invoke()
            await self.after_invoke()
        except Exception as e:
            raise e

    @abstractmethod
    async def invoke(self, *args, **kwargs) -> None:
        """Business logic implementation - must be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    async def after_invoke(self, *args, **kwargs) -> None:
        """Actions after successful result of invoke - must be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    async def before_invoke(self, *args, **kwargs) -> None:
        """Actions to perform before invoke - must be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement this method.")
