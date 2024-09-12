from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse

from app.config import get_settings
from app.data.db.connection import get_session
from app.data.db.models import User
from app.src.common import exceptions
from app.src.common.dtos import ChannelData
from app.src.limiter import limiter
from app.src.middleware.login_manager import current_user
from app.src.modules.users.exceptions import SpotDoestHaveChannels, NotSubscribedOrChannelDoesntExist, \
    SystemUsersJoinRestrict
from app.src.modules.users.logic import join_channel_by_alias, forget_channel_by_id, login_user
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
<<<<<<< HEAD
    cookie_is_set = request.cookies.get("session_token")
    login_type = "new"
    session_token = None
    if token:
        service_user_id = await find_service_user(
            session=session,
            token=token
        )
        if service_user_id:
            is_service = True
            user = await User.find_by_id(session, service_user_id)
            login_type = "existing"
            session_token = manager.create_access_token(
                data={"id": str(service_user_id)},
                expires=settings.SESSION_TOKEN_LIFETIME
            )
    if cookie_is_set and not session_token:
        user = await user_from_cookie(request, session)
        if user:
            login_type = "existing"
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
=======
    session_token, login_type, user = await login_user(session, request, token)
>>>>>>> origin/backend
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
    response.set_cookie(key="session_token", value=session_token,
<<<<<<< HEAD
                        samesite="none", secure=True, domain="notimy.ru", max_age=int(settings.SESSION_TOKEN_LIFETIME.total_seconds()))
=======
                        samesite="none", secure=True,
                        domain=settings.cookie_domain, max_age=int(settings.SESSION_TOKEN_LIFETIME.total_seconds()))
>>>>>>> origin/backend
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
