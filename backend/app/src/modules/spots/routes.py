from fastapi import APIRouter, Depends, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.data.db.connection import get_session
from app.data.db.models import Spot, Channel, User, Alias
from app.src.common.dtos import SpotData, ChannelData
from app.src.middleware.token_auth import spot_auth
from app.src.modules.spots.exceptions import WrongAliasName, AliasAlreadyExist, InvalidChannelLink
from app.src.modules.spots.schemas import SpotChangeAlias, SpotAddMessage

router = APIRouter(prefix="/spots", tags=["Spots"])
settings = get_settings()


@router.post("/new_channel")
async def create_new_channel(
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(spot_auth)
):
    channel = Channel(
        provider=spot.provider,
        spot=spot.id
    )
    session.add(channel)
    await session.commit()
    channel.add_listener(spot.account)
    spot.add_channel(channel)
    await session.commit()

    service_account = await session.scalar(
        select(User).where(User.id == spot.account)
    )

    service_account.add_channel(channel.id)
    await session.commit()
    return await ChannelData.by_model(session, channel)


@router.get("/me")
async def get_self(
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(spot_auth)
):
    response: SpotData = await SpotData.by_model(
        session,
        spot
    )
    return response


@router.post(
    "/change_alias",
    responses={
        **WrongAliasName.responses,
        **AliasAlreadyExist.responses
    }
)
async def change_alias_name(
        alias_data: SpotChangeAlias = Body(...),
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(spot_auth)
):
    if len(alias_data.name) != settings.ALIAS_NAME_SIZE:
        raise WrongAliasName
    exist: Alias = await session.scalar(select(Alias).where(Alias.name == alias_data.name))
    if exist:
        raise AliasAlreadyExist
    exist_alais: Alias = await session.scalar(select(Alias).where(Alias.base == spot.id))
    exist_alais.name = alias_data.name
    await session.commit()
    return await SpotData.by_model(session, spot)


@router.post(
    "/add_message",
    responses={
        **InvalidChannelLink,
    }
)
async def add_message_to_channel(
        data: SpotAddMessage = Body(...),
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(spot_auth)
):
    if data.channel_id not in spot.channels:
        raise InvalidChannelLink
    channel: Channel = await session.scalar(
        select(Channel).where(Channel.id == data.channel_id)
    )
    channel.add_message(data.message)
    await session.commit()
    return await ChannelData.by_model(session, channel)
