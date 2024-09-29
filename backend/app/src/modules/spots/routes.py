from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.data.db.connection import get_session
from app.data.db.models import Spot, Channel
from app.src.common.dtos import SpotData, ChannelData
from app.src.common.events import NewMessageEvent
from app.src.limiter import limiter
from app.src.middleware.push_notifications import PushNotification, send_notification
from app.src.middleware.token_auth import spot_auth, subscribed_spot
from app.src.modules.spots.exceptions import WrongAliasName, AliasAlreadyExist, InvalidChannelLink, ChannelIsNotFound
from app.src.modules.spots.logic import create_channel, change_alias, add_message, close_channel_by_id
from app.src.modules.spots.schemas import SpotChangeAlias, SpotAddMessage, CloseChannel

router = APIRouter(prefix="/spots", tags=["Spots"])
settings = get_settings()


@router.post("/new_channel")
@limiter.limit("2/second")
async def create_new_channel(
        request: Request,
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(subscribed_spot)
) -> ChannelData:
    channel = await create_channel(session, spot)
    return await ChannelData.by_model(session, channel)


@router.get("/me")
@limiter.limit("3/second")
async def get_self(
        request: Request,
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(spot_auth)
) -> SpotData:
    return await SpotData.by_model(session, spot)


@router.post(
    "/change_alias",
    responses={
        **WrongAliasName.responses,
        **AliasAlreadyExist.responses
    }
)
@limiter.limit("3/second")
async def change_alias_name(
        request: Request,
        alias_data: SpotChangeAlias = Body(...),
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(subscribed_spot)
) -> SpotData:
    await change_alias(session, spot, alias_data.name)
    return await SpotData.by_model(session, spot)


@router.post(
    "/add_message",
    responses={
        **InvalidChannelLink.responses
    }
)
@limiter.limit("3/second")
async def add_message_to_channel(
        request: Request,
        data: SpotAddMessage = Body(...),
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(subscribed_spot)
) -> ChannelData:
    channel = await Channel.find_by_id(session, data.channel_id)
    await NewMessageEvent(message=data.message, source=channel, session=session).process()
    return await ChannelData.by_model(session, channel)


@router.post(
    "/close_channel",
    responses={
        **ChannelIsNotFound.responses
    }
)
@limiter.limit("3/second")
async def close_channel(
        request: Request,
        data: CloseChannel = Body(...),
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(spot_auth)
) -> ChannelData:
    channel = await close_channel_by_id(session, spot, channel_id=data.channel_id)
    users = await channel.awaitable_attrs.listeners
    test_msg = PushNotification(title=f"Заказ готов!", body="Ваш заказ готов!\nПриятного аппетита!😋")
    for user in users:
        await send_notification(user, test_msg)

    return await ChannelData.by_model(session, channel)
