from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.data.db.connection import get_session
from app.data.db.models import Spot, Channel, User, Alias
from app.limiter import limiter
from app.src.common.dtos import SpotData, ChannelData
from app.src.middleware.token_auth import spot_auth, subscribed_spot
from app.src.modules.spots.exceptions import WrongAliasName, AliasAlreadyExist, InvalidChannelLink, ChannelIsNotFound
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
    provider_id = (await spot.provider).id

    channel = Channel(
        provider=provider_id,
        local_number=await Channel.get_next_local_number(session, spot.id)
    )
    session.add(channel)
    await session.commit()
    (await spot.channels_list).append(channel)
    await session.commit()

    service_account = await session.scalar(
        select(User).where(User.id == spot.account)
    )

    (await service_account.channels_list).append(channel)
    await session.commit()
    return await ChannelData.by_model(session, channel)


@router.get("/me")
@limiter.limit("3/second")
async def get_self(
        request: Request,
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(spot_auth)
) -> SpotData:
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
@limiter.limit("3/second")
async def change_alias_name(
        request: Request,
        alias_data: SpotChangeAlias = Body(...),
        session: AsyncSession = Depends(get_session),
        spot: Spot = Depends(subscribed_spot)
) -> SpotData:
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
    # TODO: It is better to check a relation not an array
    channels_ids = [_.id for _ in await spot.channels_list]
    if data.channel_id not in channels_ids:
        raise InvalidChannelLink
    channel: Channel = await Channel.find_by_id(session, data.channel_id)
    channel.add_message(data.message)
    await session.commit()
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
    clist = [_.id for _ in await spot.channels_list]
    if data.channel_id not in clist:
        raise ChannelIsNotFound
    channel: Channel = await Channel.find_by_id(session, data.channel_id)
    if channel.open:
        channel.close()
        await session.commit()
    return await ChannelData.by_model(session, channel)
