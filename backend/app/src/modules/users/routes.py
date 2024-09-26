import hashlib
import hmac
import time
from typing import Optional
from urllib.parse import parse_qs
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi import Request
from jose import jwt, JWTError
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
    get_session_token
from app.src.modules.users.schemas import UserResponse, UserChannel

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


def check_telegram_data(data):
    try:
        # Decode the JWT token
        payload = jwt.decode(data, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        tg_data = {key: value[0] for key, value in payload.items()}
        return tg_data
    except JWTError:
        return False


@router.post("/telegram/auth")
async def register_user_using_telegram(
        request: Request,
        init_data: str,
        user: Optional[User] = Depends(current_user),  # User must already exist in system
        session: AsyncSession = Depends(get_session),
):
    telegram_data = check_telegram_data(init_data)
    if not telegram_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid telegram auth data")

    telegram_id = telegram_data["id"]
    exist = await session.scalar(select(User).where(User.telegram_id == telegram_id))
    response = RedirectResponse('/me')
    if exist:  # If user is existed so login it and redirect to me
        await logout(request)
        session_token = await get_session_token(session, exist)
        await set_session_token(response, session_token)
        return response
    if not user.is_default:  # Ensure that user to register is default
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't associate telegram with system user!")
    user.telegram_username = telegram_data["username"]
    user.telegram_id = telegram_data["id"]
    user.telegram_firstname = telegram_data["first_name"]
    user.telegram_lastname = telegram_data["last_name"]
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
):
    if user.is_default:
        return await UserResponse.by_model(session, user)
    return await UserData.by_model(session, user)


@router.get("/logout")
@limiter.limit("3/second")
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
@limiter.limit("5/second")
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
