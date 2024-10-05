from uuid import UUID

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from app.data.db.connection import get_session
from app.data.db.models import User
from app.src.modules.telegram.exceptions import UserNotFound
from app.src.modules.users.logic import get_session_token, set_session_token

router = APIRouter(
    prefix="/tg",
    tags=["Telegram Api"],
)


@router.post(
    "/auth",
    responses={
        **UserNotFound.responses,

    }
)
async def auth_telegram_user(
        uuid: UUID = Query(..., description="UUID of existing user in system"),
        tg_data: str = Query(..., description="JWT token with telegram data for authentication"),
        session: AsyncSession = Depends(get_session)
):
    user_exist = await User.find_by_id(session, uuid)
    if not user_exist:
        raise UserNotFound()

    # check if user with uuid is existed
    # check if telegram user is already link an account
    pass


@router.post(
    "/login",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
async def login_existing_user(
        uuid: UUID = Query(..., description="UUID of existing user in system"),
        session: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    response = RedirectResponse('/api/me')
    user: User = await User.find_by_id(session, uuid)
    session_token = await get_session_token(session, user)
    await set_session_token(response, session_token)
    return response
