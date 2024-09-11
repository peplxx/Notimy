__all__ = ['BaseRepository']

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
