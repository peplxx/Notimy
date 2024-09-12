__all__ = ['BaseRepository']

from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        # self._session_maker = SessionManager().session_maker
        self._session = session
