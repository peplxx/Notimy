__all__ = ['UserRepository']

from app.config.constants import Roles
from app.data.db.models import User, Channel
from app.data.db.repositories.base import BaseRepository


class UserRepository(BaseRepository):

    async def create(self, role: Roles = Roles.default) -> User:
        user = User(role=role.value)
        self._session.add(user)
        await self._session.commit()
        return user

    async def set_data(self, user: User, data: dict) -> None:
        user.set_data(data)
        await self._session.commit()

    async def add_channel(self, user: User, channel: Channel) -> Channel:
        (await user.channels_list).append(channel)
        await self._session.commit()
        return channel
