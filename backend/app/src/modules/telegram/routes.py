from uuid import UUID

from fastapi import APIRouter, Query, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse, Response, JSONResponse

from app.data.db.connection import get_session
from app.data.db.models import User
from app.data.db.repositories import RepositoriesManager
from app.data.db.repositories.user import AuthModule, BadJwtException
from app.src.modules.telegram.exceptions import UserNotFound, JWTIsInvalid, TelegramUserAlreadyConnected
from app.src.modules.telegram.schemas import TelegramData
from app.src.modules.users.logic import get_session_token, set_session_token

router = APIRouter(
    prefix="/tg",
    tags=["Telegram Api"],
)

@router.post(
    "/auth",
    status_code=status.HTTP_200_OK,
    responses={
        **UserNotFound.responses,
        **JWTIsInvalid.responses,
        **TelegramUserAlreadyConnected.responses,
    }
)
async def auth_telegram_user(
        uuid: UUID = Query(..., description="UUID of existing user in system"),
        tg_data: str = Query(..., description="JWT token with telegram data for authentication"),
        session: AsyncSession = Depends(get_session)
):
    manager: RepositoriesManager = RepositoriesManager(session)
    user = await User.find_by_id(session, uuid)
    if not user:
        raise UserNotFound()
    try:
        payload: dict = await AuthModule.get_payload(tg_data)
        telegram_data = TelegramData(**payload)
    except BadJwtException:
        raise JWTIsInvalid()
    telegram_login = await session.scalar(select(User).where(User.telegram_id == telegram_data.telegram_id))
    if telegram_login:
        raise TelegramUserAlreadyConnected()
    await manager.U.set_telegram_data(user, telegram_data)
    return JSONResponse(
        {"details": "Telegram is connected to this user!"},
        status_code=status.HTTP_200_OK,
    )

@router.post(
    "/login",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
async def login_existing_user(
        request: Request,
        uuid: UUID = Query(..., description="UUID of existing user in system"),
        session: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    response = RedirectResponse('/api/me')
    user: User = await User.find_by_id(session, uuid)
    session_token = await get_session_token(session, user)
    await set_session_token(response, session_token)
    return response
