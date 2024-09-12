__all__ = ["create_channel", "change_alias", "close_channel_by_id", "add_message"]
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.data.db.models import Spot, Channel, User, Alias, Message
from app.data.db.repositories import RepositoriesManager
from app.src.modules.spots.exceptions import WrongAliasName, AliasAlreadyExist, InvalidChannelLink, ChannelIsNotFound

settings = get_settings()


async def create_channel(session: AsyncSession, spot: Spot) -> Channel:
    manager = RepositoriesManager(session)
    provider_id = (await spot.provider).id

    channel = await manager.C.create(spot=spot, provider_id=provider_id)
    service_user = await User.find_by_id(session, spot.account)
    channel = await manager.U.add_channel(service_user, channel)
    return channel


async def change_alias(session: AsyncSession, spot: Spot, alias_name) -> None:
    manager = RepositoriesManager(session)

    if len(alias_name) != settings.ALIAS_NAME_SIZE:
        raise WrongAliasName
    exist: Alias = await session.scalar(select(Alias).where(Alias.name == alias_name))
    if exist:
        raise AliasAlreadyExist
    await manager.S.change_alias(spot, alias_name)


async def add_message(session: AsyncSession, spot: Spot, message: Message, channel_id: UUID) -> Channel:
    # TODO: It is better to check a relation not an array
    manager = RepositoriesManager(session)

    channels_ids = await manager.S.get_channel_ids(spot)
    if channel_id not in channels_ids:
        raise InvalidChannelLink
    channel: Channel = await Channel.find_by_id(session, channel_id)
    await manager.C.add_message(channel, message)
    return channel


async def close_channel_by_id(session: AsyncSession, spot: Spot, channel_id: UUID) -> Channel:
    manager = RepositoriesManager(session)

    channels_ids = await manager.S.get_channel_ids(spot)
    if channel_id not in channels_ids:
        raise ChannelIsNotFound
    channel: Channel = await Channel.find_by_id(session, channel_id)
    await manager.C.close(channel)
    return channel
