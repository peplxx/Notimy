__all__ = ['RepositoriesManager']

from app.data.db.repositories.channel import ChannelRepository
from app.data.db.repositories.provider import ProviderRepository
from app.data.db.repositories.spot import SpotRepository
from app.data.db.repositories.user import UserRepository

from sqlalchemy.ext.asyncio import AsyncSession


class RepositoriesManager:
    U: UserRepository
    S: SpotRepository
    P: ProviderRepository
    C: ChannelRepository

    def __init__(self, session: AsyncSession):
        self._session = session
        self.U = UserRepository(session)
        self.P = ProviderRepository(session)
        self.C = ChannelRepository(session)
        self.S = SpotRepository(session)