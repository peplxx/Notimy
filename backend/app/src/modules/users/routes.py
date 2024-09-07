from typing import Optional
from uuid import UUID

from duplicity.config import hostname
from fastapi import APIRouter, Depends, Query, Response
from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse

from app.config import get_settings
from app.config.constants import Roles
from app.data.db.connection import get_session
from app.data.db.models import User, Alias, Spot, Channel
from app.limiter import limiter
from app.src.common import exceptions
from app.src.common.dtos import ChannelData
from app.src.middleware.login_manager import manager, current_user, user_from_cookie
from app.src.modules.users.exceptions import SpotDoestHaveChannels, NotSubscribedOrChannelDoesntExist, \
    SystemUsersJoinRestrict
from app.src.modules.users.schemas import UserResponse, UserChannel
from app.src.modules.users.service import find_service_user

router = APIRouter(prefix='', tags=['Users'])
settings = get_settings()


@router.get("/login")
@router.post("/login")
@limiter.limit("3/second")
async def login(
        request: Request,
        next: Optional[str] = Query(None),
        token: Optional[str] = Query(None),
        session: AsyncSession = Depends(get_session),
):
    cookie_is_set = request.cookies.get("session_token")
    is_service = False
    session_token = None
    if token:
        service_user_id = await find_service_user(
            session=session,
            token=token
        )
        if service_user_id:
            is_service = True
            user = await User.find_by_id(session, service_user_id)
            session_token = manager.create_access_token(
                data={"id": str(service_user_id)},
                expires=settings.SESSION_TOKEN_LIFETIME
            )
    if cookie_is_set and not session_token:
        user = await user_from_cookie(request, session)
        if user:
            session_token = manager.create_access_token(
                data={"id": str(user.id)},
                expires=settings.SESSION_TOKEN_LIFETIME
            )
        else:
            user = User()
            session.add(user)
            await session.commit()
            session_token = manager.create_access_token(
                data={"id": str(user.id)},
                expires=settings.SESSION_TOKEN_LIFETIME
            )
    if not session_token:  # If token is invalid and just login
        user = User()
        session.add(user)
        await session.commit()
        session_token = manager.create_access_token(
            data={"id": str(user.id)},
            expires=settings.SESSION_TOKEN_LIFETIME
        )

    login_path = '/api/login'
    if next and "login" not in next:
        response = RedirectResponse(next)
    else:
        response = JSONResponse(content={
            "type": "new" if not is_service else "existing",
            "login_as": user.role,
            "session_token": session_token,
            "token_type": "bearer"
        })
    response.set_cookie(key="session_token", value=session_token,
                        samesite="none", secure=True, hostname="notimy.ru")
    return response


@router.get(
    "/me",
    responses={}
)
@router.post('/me')
@limiter.limit("3/second")
async def get_self(
        request: Request,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
) -> UserResponse:
    return await UserResponse.by_model(session, user)


@router.get("/logout")
@limiter.limit("3/second")
async def logout(
        request: Request
):
    if request.cookies.get("session_token"):
        response = JSONResponse(content={"message": "Logged out!"})
        response.delete_cookie("session_token")
        return response
    return JSONResponse(content={"message": "You are not logged in!"})


@router.get(
    "/channel/{channel_id}",
    responses={
        **NotSubscribedOrChannelDoesntExist.responses
    }
)
@limiter.limit("5/second")
async def get_channel_info(
        request: Request,
        channel_id: UUID,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
) -> UserChannel:
    if channel_id not in user.channels:
        raise NotSubscribedOrChannelDoesntExist()
    channel_data: ChannelData = await ChannelData.by_id(session, channel_id)
    return await UserChannel.by_data(channel_data)


@router.post(
    "/join/{alias}",
    responses={
        **exceptions.InvalidInvitationLink.responses,
        **SystemUsersJoinRestrict.responses,
        **SpotDoestHaveChannels.responses
    }
)
@limiter.limit("10/second")
async def join_channel(
        request: Request,
        alias: str,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
) -> UserResponse:
    if user.role != Roles.default.value:
        raise SystemUsersJoinRestrict
    alias_db: Alias = await session.scalar(
        select(Alias).where(Alias.name == alias)
    )
    if not alias_db:
        raise exceptions.InvalidInvitationLink()

    spot: Spot = await Spot.find_by_id(session, alias_db.base)

    channel = await spot.last_channel
    if not channel:
        raise SpotDoestHaveChannels

    if user.id not in [_.id for _ in await channel.listeners_list]:
        (await channel.listeners_list).append(user)
    await session.commit()

    return await UserResponse.by_model(session, user)


@router.delete(
    "/forget/{channel_id}",
    responses={
        **NotSubscribedOrChannelDoesntExist.responses
    }
)
@limiter.limit("3/second")
async def forget_channel(
        request: Request,
        channel_id: UUID,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
) -> UserResponse:
    # TODO: refactor this stupid code
    user_channels = await user.channels_list
    channels_ids = [_.id for _ in user_channels]
    if channel_id not in channels_ids:
        raise NotSubscribedOrChannelDoesntExist
    channel: Channel = await Channel.find_by_id(session, channel_id)
    user.channels.remove(channel)
    await session.commit()
    return await UserResponse.by_model(session, user)
