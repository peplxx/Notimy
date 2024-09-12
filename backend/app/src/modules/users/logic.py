__all__ = ["forget_channel_by_id", 'login_user', "find_service_user", 'join_channel_by_alias']

from uuid import UUID

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.models import Provider
from app.data.db.models import User, Spot, Channel
from app.data.db.repositories import RepositoriesManager
from app.src.common.exceptions import InvalidInvitationLink
from app.src.modules.users.exceptions import SpotDoestHaveChannels, NotSubscribedOrChannelDoesntExist, \
    SystemUsersJoinRestrict


async def find_service_user(
        session: AsyncSession,
        token: str,
) -> User | None:
    if not token:
        return None
    tables = [Spot, Provider]
    for table in tables:
        result = await session.scalar(select(table).where(table.token == token))
        if result:
            return await User.find_by_id(session, table.account)
    return None


async def join_channel_by_alias(session: AsyncSession, user: User, alias_name: str):
    manager = RepositoriesManager(session)
    if not user.is_default:
        raise SystemUsersJoinRestrict
    alias_db = await manager.S.get_alias(alias_name)
    if not alias_db:
        raise InvalidInvitationLink

    spot: Spot = await Spot.find_by_id(session, alias_db.base)

    channel = await spot.last_channel
    if not channel:
        raise SpotDoestHaveChannels

    await manager.C.add_listener(channel, user)


async def forget_channel_by_id(session: AsyncSession, user: User, channel_id: UUID):
    manager = RepositoriesManager(session)
    channels_ids = await manager.U.channels_ids(user)
    if channel_id not in channels_ids:
        raise NotSubscribedOrChannelDoesntExist

    channel: Channel = await Channel.find_by_id(session, channel_id)
    await manager.U.forget_channel(user, channel)


async def login_user(session: AsyncSession, request: Request, token: str | None) -> tuple[str, str, User]:
    manager = RepositoriesManager(session)

    cookie_is_set = request.cookies.get("session_token")
    login_type = "new"
    user = None

    if token:  # Force load spot token if it presented
        user = await find_service_user(session=session, token=token)
        login_type = "existing" if user else "new"
    if cookie_is_set and not user:  # if We did not log in using token -> login using cookies
        user = await manager.U.user_from_cookie(request)
        login_type = "existing" if user else "new"

    if not user:  # If token is invalid and just create new user
        user = await manager.U.create()

    session_token = manager.U.create_access_token(
        data={"id": str(user.id)},
        expires=settings.SESSION_TOKEN_LIFETIME
    )
    return session_token, login_type, user
