from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.data.db.connection import get_session
from app.data.db.models import User, Provider, Spot
from app.src.common import exceptions
from app.src.middleware.login_manager import user_from_cookie

settings = get_settings()


async def get_token(
        request: Request,
        session: AsyncSession
) -> str:
    token = None
    if header := request.headers.get('Authorization'):
        token = header.split(" ")[1]
    else:
        user: User = await user_from_cookie(request, session)
        if user:
            token = user.get_data().get('token')
    if not token:
        raise exceptions.IncorrectCredentialsException(no_credentials=True)
    return token


async def root_auth(
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    token = await get_token(request, session)
    if token != settings.ROOT_TOKEN:
        raise exceptions.IncorrectCredentialsException()


async def provider_auth(
        request: Request,
        session: AsyncSession = Depends(get_session)
) -> Provider:
    token = await get_token(request, session)
    provider: Provider = await Provider.find_by_token(session, token)
    if not provider:
        raise exceptions.IncorrectCredentialsException()
    return provider


async def spot_auth(
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    token = await get_token(request, session)
    spot: Spot = await Spot.find_by_token(session, token)
    if not spot:
        raise exceptions.IncorrectCredentialsException()
    return spot
