from uuid import UUID

from fastapi import Depends
from fastapi import Request
from fastapi_login import LoginManager
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.data.db.connection import get_session
from app.data.db.models import User

settings = get_settings()


class NotAuthenticatedException(Exception):
    pass


# these two argument are mandatory

manager = LoginManager(
    settings.SECRET_KEY,
    token_url=settings.PATH_PREFIX + '/login',
    cookie_name="session_token",
    use_cookie=True,
    not_authenticated_exception=NotAuthenticatedException
)


async def get_current_user_id(token: str) -> UUID | None:
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            return None
        return UUID(user_id)
    except JWTError:
        raise NotAuthenticatedException()


async def load_user(
        session_token: str | None,
        session: AsyncSession) -> User | None:
    if not session_token:
        return None

    user_id = await get_current_user_id(session_token)
    if not user_id:
        return None
    result = await session.scalar(select(User).where(User.id == user_id))
    return result


async def current_user(
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    current_user = await load_user(
        session_token=request.cookies.get("session_token"),
        session=session
    )
    if not current_user:
        raise NotAuthenticatedException("You must be logged in to access this")

    return current_user


async def user_from_cookie(
        request: Request,
        session: AsyncSession
):
    current_user = await load_user(
        session_token=request.cookies.get("session_token"),
        session=session
    )
    return current_user
