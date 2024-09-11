from uuid import UUID

from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.data.db.connection import get_session
from app.data.db.models import Spot, Channel, User, Alias, Message
from app.data.db.repositories import ChannelRepository, UserRepository, SpotRepository
from app.src.limiter import limiter
from app.src.common.dtos import SpotData, ChannelData
from app.src.middleware.token_auth import spot_auth, subscribed_spot
from app.src.modules.spots.exceptions import WrongAliasName, AliasAlreadyExist, InvalidChannelLink, ChannelIsNotFound
from app.src.modules.spots.schemas import SpotChangeAlias, SpotAddMessage, CloseChannel

router = APIRouter(prefix="/spots", tags=["Spots"])
settings = get_settings()


async def create_channel(session: AsyncSession, spot: Spot) -> Channel:
    provider_id = (await spot.provider).id
    channel_repo = ChannelRepository(session)
    user_repo = UserRepository(session)
    channel = await channel_repo.create(spot=spot, provider_id=provider_id)
    service_user = await User.find_by_id(session, spot.account)
    await user_repo.add_channel(service_user, channel)
    return channel


async def change_alias(session: AsyncSession, spot: Spot, alias_name) -> None:
    spot_repo = SpotRepository(session)
    if len(alias_name) != settings.ALIAS_NAME_SIZE:
        raise WrongAliasName
    exist: Alias = await session.scalar(select(Alias).where(Alias.name.is_(alias_name)))
    if exist:
        raise AliasAlreadyExist
    await spot_repo.change_alias(spot, alias_name)


async def add_message(session: AsyncSession, spot: Spot, message: Message, channel_id: UUID) -> Channel:
    # TODO: It is better to check a relation not an array
    channels_repo = ChannelRepository(session)
    channels_ids = channels_repo.get_channel_ids(spot)
    if channel_id not in channels_ids:
        raise InvalidChannelLink
    channel: Channel = await Channel.find_by_id(session, channel_id)
    await channels_repo.add_message(channel, message.message)
    return channel


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
    channel = await add_message(session, spot, message=data.message, channel_id=data.channel_id)
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
