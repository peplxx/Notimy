from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.config import get_settings
from pywebpush import webpush, WebPushException

from app.data.db.connection import get_session
from app.data.db.models import User, subscription
from app.src.middleware.login_manager import current_user
from app.src.middleware.push_notifications import PushSubscription, PushNotification, send_notification

router = APIRouter(prefix='', tags=['WebPush'])
settings = get_settings()


@router.post("/webpush/subscribe")
async def webpush_subscribe(
        subscription: PushSubscription,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_session)
):
    if user.is_default:
        user.push_data = subscription.dict()
        await session.commit()
        return JSONResponse({'message': 'Subscribed successfully!'})
    return JSONResponse({'message': 'No pushes for service users!'})


@router.post("/webpush/unsubscribe")
async def webpush_unsubscribe(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_session)
):
    user.push_data = {}
    await session.commit()
    return JSONResponse({'message': 'Cleared push data!'})


@router.post("/webpush/test")
async def webpush_unsubscribe(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_session)
):
    test_msg = PushNotification(title="Test notification", body="Test notification")
    if user.can_get_push:
        await send_notification(user, test_msg)
        return JSONResponse({'message': 'Message was sent!'})
    else:
        return JSONResponse({'message': 'Use subscribe endpoint first!'})
