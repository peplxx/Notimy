__all__ = ['UserRepository']

from app.config.constants import Roles
from app.data.db.models import User


class UserRepository:

    def __init__(self, session):
        self._session = session

    async def create(self, role: Roles = Roles.default) -> User:
        user = User(role=role.value)
        self._session.add(user)
        await self._session.commit()
        return user

    async def set_data(self, user: User, data: dict) -> None:
        user.set_data(data)
        await self._session.commit()
