__all__ = ['BaseRepository']

from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.connection import SessionManager


class BaseRepository:
    def __init__(self, session: AsyncSession):
        # self._session_maker = SessionManager().session_maker
        self._session = session
