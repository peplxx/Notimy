__all__ = ['UserRepository', "BadJwtException"]

from abc import ABC
from uuid import UUID

from jose import JWTError, jwt

from app.config import get_settings
from app.config.constants import Roles
from app.data.db.models import User, Channel
from app.data.db.repositories.base import BaseRepository
from fastapi import Request

from app.src.middleware.login_manager import manager
from app.src.modules.telegram.schemas import TelegramData

settings = get_settings()


class NotAuthenticatedException(Exception):
    pass


class BadJwtException(Exception):
    pass


class AuthModule(BaseRepository, ABC):
    @staticmethod
    async def get_payload(token: str) -> dict:
        try:
            payload: dict = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            raise BadJwtException

    @staticmethod
    async def uuid_from_jwt(token: str) -> UUID | None:
        try:
            payload = await AuthModule.get_payload(token)
            user_id: str = payload.get("id")
            if user_id is None:
                return None
            return UUID(user_id)
        except BadJwtException:
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
        return await self.load_user_from_jwt(session_token=request.cookies.get("session_token"), )

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

    async def set_telegram_data(self, user: User, tg_data: TelegramData):
        user.telegram_id = tg_data.telegram_id
        user.telegram_username = tg_data.telegram_username
        user.telegram_firstname = tg_data.telegram_firstname
        user.telegram_lastname = tg_data.telegram_lastname
        await self._session.commit()