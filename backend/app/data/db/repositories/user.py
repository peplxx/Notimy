__all__ = ['UserRepository']

from abc import ABC
from uuid import UUID

from jose import JWTError, jwt

from app.config import get_settings
from app.config.constants import Roles
from app.data.db.models import User, Channel
from app.data.db.repositories.base import BaseRepository
from fastapi import Request

from app.src.middleware.login_manager import manager

settings = get_settings()


class NotAuthenticatedException(Exception):
    pass


class AuthModule(BaseRepository, ABC):
    @staticmethod
    async def uuid_from_jwt(token: str) -> UUID | None:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("id")
            if user_id is None:
                return None
            return UUID(user_id)
        except JWTError:
            raise NotAuthenticatedException()

    async def load_user_from_jwt(self, session_token: str | None) -> User | None:
        if not session_token:
            return None

        user_id = await AuthModule.uuid_from_jwt(session_token)
        if not user_id:
            return None
        result = await User.find_by_id(self._session, user_id)
        return result

    async def user_from_cookie(self, request) -> User | None:
        return await self.load_user_from_jwt(session_token=request.cookies.get("session_token"),)

    def create_access_token(self, **kwargs) -> str:
        return manager.create_access_token(**kwargs)

class UserRepository(AuthModule):

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

    async def channels_ids(self, user: User) -> list[UUID]:
        return [_.id for _ in await user.channels_list]

    async def forget_channel(self, user: User, channel: Channel):
        user.channels.remove(channel)
        await self._session.commit()