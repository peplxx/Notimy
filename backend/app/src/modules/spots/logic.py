__all__ = ["create_channel", "change_alias", "close_channel_by_id", "add_message"]
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.data.db.models import Spot, Channel, User, Alias, Message
from app.data.db.repositories import ChannelRepository, UserRepository, SpotRepository
from app.src.modules.spots.exceptions import WrongAliasName, AliasAlreadyExist, InvalidChannelLink, ChannelIsNotFound

settings = get_settings()


async def create_channel(session: AsyncSession, spot: Spot) -> Channel:
    provider_id = (await spot.provider).id
    channel_repo = ChannelRepository(session)
    user_repo = UserRepository(session)
    channel = await channel_repo.create(spot=spot, provider_id=provider_id)
    service_user = await User.find_by_id(session, spot.account)
    channel = await user_repo.add_channel(service_user, channel)
    return channel


async def change_alias(session: AsyncSession, spot: Spot, alias_name) -> None:
    spot_repo = SpotRepository(session)
    if len(alias_name) != settings.ALIAS_NAME_SIZE:
        raise WrongAliasName
    exist: Alias = await session.scalar(select(Alias).where(Alias.name == alias_name))
    if exist:
        raise AliasAlreadyExist
    await spot_repo.change_alias(spot, alias_name)


async def add_message(session: AsyncSession, spot: Spot, message: Message, channel_id: UUID) -> Channel:
    # TODO: It is better to check a relation not an array
    channels_repo = ChannelRepository(session)
    spot_repo = SpotRepository(session)
    channels_ids = await spot_repo.get_channel_ids(spot)
    if channel_id not in channels_ids:
        raise InvalidChannelLink
    channel: Channel = await Channel.find_by_id(session, channel_id)
    await channels_repo.add_message(channel, message)
    return channel


async def close_channel_by_id(session: AsyncSession, spot: Spot, channel_id: UUID) -> Channel:
    spot_repo = SpotRepository(session)
    channel_repo = ChannelRepository(session)

    channels_ids = await spot_repo.get_channel_ids(spot)
    if channel_id not in channels_ids:
        raise ChannelIsNotFound
    channel: Channel = await Channel.find_by_id(session, channel_id)
    await channel_repo.close(channel)
    return channel
