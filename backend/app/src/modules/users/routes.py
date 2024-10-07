from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse

from app.config import get_settings
from app.data.db.connection import get_session
from app.data.db.models import User
from app.src.common import exceptions
from app.src.common.dtos import ChannelData, UserData
from app.src.limiter import limiter
from app.src.middleware.login_manager import current_user
from app.src.modules.users.exceptions import SpotDoestHaveChannels, NotSubscribedOrChannelDoesntExist, \
    SystemUsersJoinRestrict
from app.src.modules.users.logic import join_channel_by_alias, forget_channel_by_id, login_user, set_session_token, \
    get_session_token, check_telegram_data, join_channel_by_channel_id
from app.src.modules.users.schemas import UserResponse, UserChannel

router = APIRouter(prefix='', tags=['Users'])
settings = get_settings()


@router.get("/login")
@router.post("/login")
@limiter.limit("10/second")
async def login(
        request: Request,
        next: Optional[str] = Query(None),
        token: Optional[str] = Query(None),
        session: AsyncSession = Depends(get_session),
):
    session_token, login_type, user = await login_user(session, request, token)
    if next and "login" not in next:
        response = RedirectResponse(next)
    else:
        response = JSONResponse(content={
            "type": login_type,
            "login_as": user.role,
            "user_id": str(user.id),
            "session_token": session_token,
            "token_type": "bearer"
        })
    await set_session_token(response, session_token)
    return response


@router.get(
    "/me",
    responses={}
)
@router.post('/me')
@limiter.limit("10/second")
async def get_self(
        request: Request,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
):
    if user.is_default:
        return await UserResponse.by_model(session, user)
    return await UserData.by_model(session, user)


@router.get("/logout")
@limiter.limit("10/second")
async def logout(
        request: Request
):
    if request.cookies.get("session_token"):
        response = JSONResponse(content={"message": "Session is cleared!"})
        response.delete_cookie("session_token")
        return response
    return JSONResponse(content={"message": "You do not have session!"})


@router.get(
    "/channel/{channel_id}",
    responses={
        **NotSubscribedOrChannelDoesntExist.responses
    }
)
@limiter.limit("10/second")
async def get_channel_info(
        request: Request,
        channel_id: UUID,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
) -> UserChannel:
    user_channels = await user.channels_list
    if channel_id not in user_channels:
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
    await join_channel_by_alias(session, user, alias)
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
    await forget_channel_by_id(session, user, channel_id)
    return await UserResponse.by_model(session, user)


@router.post(
    "/join/channel/{channel_id}",
    responses={
        **exceptions.InvalidInvitationLink.responses,
        **SystemUsersJoinRestrict.responses,
    }
)
@limiter.limit("10/second")
async def join_channel_by_id(
        request: Request,
        channel_id: UUID,
        session: AsyncSession = Depends(get_session),
        user: Optional[User] = Depends(current_user)
) -> UserResponse:
    await join_channel_by_channel_id(session, user, channel_id)
    return await UserResponse.by_model(session, user)
