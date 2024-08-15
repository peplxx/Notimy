from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse

from app.config import get_settings
from app.config.constants import Roles
from app.data.db.connection import get_session
from app.data.db.models import User, Alias, Spot, Channel
from app.src.common import exceptions
from app.src.common.dtos import UserData
from app.src.middleware.login_manager import manager, current_user
from app.src.modules.users.exceptions import SpotDoestHaveChannels, NotSubscribedOrChannelDoesntExist, \
    SystemUsersJoinRestrict
from app.src.modules.users.service import find_service_user

router = APIRouter(prefix='', tags=['Users'])
settings = get_settings()


@router.get("/login")
@router.post("/login")
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
            user = await session.scalar(select(User).where(User.id == service_user_id))
            session_token = manager.create_access_token(
                data={"id": str(service_user_id)},
                expires=settings.SESSION_TOKEN_LIFETIME
            )
    if cookie_is_set and not session_token:
        user = await current_user(request, session)
        if user:
            response = JSONResponse(content={
                "type": "existing",
                "login_as": user.role,
                "session_token": request.cookies.get('session_token'),
                "token_type": "bearer"
            })
            return response
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

    if next:
        response = RedirectResponse(next)
    else:
        response = JSONResponse(content={
            "type": "new" if not is_service else "existing",
            "login_as": user.role,
            "session_token": session_token,
            "token_type": "bearer"
        })
    response.set_cookie(key="session_token", value=session_token)
    return response


@router.get(
    "/me",
    responses={}
)
async def get_self(
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
) -> UserData:
    response: UserData = await UserData.by_model(session, user)
    return response


@router.get("/logout")
async def logout(
        request: Request,
        response: Response,
):
    if request.cookies.get("session_token"):
        response = JSONResponse(content={"message": "Logged out!"})
        response.delete_cookie("session_token")
        return response
    return JSONResponse(content={"message": "You are not logged in!"})


@router.post(
    "/join/{alias}",
    responses={
        **exceptions.InvalidInvitationLink.responses,
        **SystemUsersJoinRestrict.responses,
        **SpotDoestHaveChannels.responses
    }
)
async def join_channel(
        alias: str,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
):
    if user.role != Roles.default.value:
        raise SystemUsersJoinRestrict
    alias_db: Alias = await session.scalar(
        select(Alias).where(Alias.name == alias)
    )
    if not alias_db:
        raise exceptions.InvalidInvitationLink()

    spot: Spot = await session.scalar(
        select(Spot).where(Spot.id == alias_db.base)
    )

    channel_id = spot.last_channel
    if not channel_id:
        raise SpotDoestHaveChannels
    channel: Channel = await session.scalar(select(Channel).where(Channel.id == channel_id))
    channel.add_listener(user.id)
    user.add_channel(channel_id)
    await session.commit()

    return await UserData.by_model(session, user)


@router.delete(
    "/forget/{channel_id}",
    responses={
        **NotSubscribedOrChannelDoesntExist.responses
    }
)
async def forget_channel(
        channel_id: UUID,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
):
    if channel_id not in user.channels:
        raise NotSubscribedOrChannelDoesntExist
    channel: Channel = await session.scalar(
        select(Channel).where(Channel.id == channel_id)
    )
    user.delete_channel(channel_id)
    channel.delete_listener(user.id)
    await session.commit()
    return await UserData.by_model(session, user)
