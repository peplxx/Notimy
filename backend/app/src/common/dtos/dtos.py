__all__ = [
    "ChannelData",
    "UserData",
    "ProviderData",
    "SpotData"
]

import asyncio
import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.models import Provider, Spot, Channel, User, Alias


class ChannelData(BaseModel):
    id: UUID
    provider: UUID
    open: bool
    code: str
    created_at: datetime.datetime
    dispose_at: datetime.datetime
    closed_at: datetime.datetime | None
    local_number: int | None

    spot_id: Optional[UUID] = None
    provider_name: Optional[str] = ""
    users_ids: Optional[list[UUID]] = []
    messages_data: Optional[list[dict]] = []

    @staticmethod
    async def by_model(
            session: AsyncSession,
            channel: Channel
    ):
        result = ChannelData.model_validate(
            channel,
            from_attributes=True
        )
        provider: Provider = await session.scalar(
            select(Provider).where(Provider.id == channel.provider)
        )
        result.provider_name = provider.name
        result.users_ids = [_.id for _ in await channel.listeners_list]
        result.messages_data = channel.messages
        result.spot_id = (await channel.spot).id
        return result

    @staticmethod
    async def by_id(
            session: AsyncSession,
            channel_id: UUID
    ):
        channel: Channel = await Channel.find_by_id(session, channel_id)
        return await ChannelData.by_model(session, channel)


class UserData(BaseModel):
    id: UUID
    registered_at: datetime.datetime
    role: str

    tg: Optional[bool] = False
    provider_name: Optional[str] = ''
    channels_ids: Optional[list[UUID]] = []
    channels_data: Optional[list[ChannelData]] = []
    data_json: Optional[dict] = {}

    @staticmethod
    async def by_model(
            session: AsyncSession,
            user: User
    ):
        result = UserData.model_validate(
            user,
            from_attributes=True
        )
        user_channels = await user.channels_list
        ids = [_.id for _ in user_channels]
        ids, data = await actual_channels(
            session=session,
            channels_ids=ids
        )
        result.data_json = user.get_data()
        if user.role == Roles.spotUser.value:
            spot: Spot = await session.scalar(select(Spot).where(Spot.token == user.get_data()['token']))
            provider: Provider = (await spot.provider)
            result.provider_name = provider.name
        result.channels_ids = ids
        result.channels_data = data
        result.tg = bool(user.telegram_id is not None)
        return result


class SpotData(BaseModel):
    id: UUID
    token: str
    additional_info: str
    created_at: datetime.datetime
    account: UUID

    subscription: Optional[dict] = {}
    provider_id: Optional[UUID] = None
    alias: Optional[dict] = {}
    channels_ids: Optional[list[UUID]] = []
    channels_data: Optional[list[ChannelData]] = []

    @staticmethod
    async def by_model(
            session: AsyncSession,
            spot: Spot
    ):
        # Validate and prepare the result model
        result = SpotData.model_validate(
            spot,
            from_attributes=True
        )

        # Use asyncio.gather to batch asynchronous operations
        channels_list, alias, subscription, provider = await asyncio.gather(
            spot.channels_list,
            session.scalar(select(Alias).where(Alias.base == spot.id)),
            spot.get_subscription(session),
            spot.provider
        )

        # Set values
        result.channels_ids = [_.id for _ in channels_list]
        result.alias = alias.dict() if alias else {}
        subscribe_existence = {"exist": subscription is not None}
        subscription_dict: dict = subscription.dict() if subscription else {}
        subscription_dict.update(subscribe_existence)
        result.subscription = subscription_dict
        result.provider_id = provider.id
        return result


class ProviderData(BaseModel):
    id: UUID
    token: str
    name: str
    description: str
    created_at: datetime.datetime
    spots: int
    max_spots: int
    account: UUID

    spots_ids: Optional[list] = []

    @staticmethod
    async def by_model(
            session: AsyncSession,
            provider: Provider
    ):
        result = ProviderData.model_validate(
            provider,
            from_attributes=True
        )
        if provider.spots:
            result.spots_ids = [_.id for _ in await provider.spots_list]
        return result

async def actual_channels(
        session: AsyncSession,
        channels_ids: list[UUID]
) -> tuple[list[UUID], list[ChannelData]]:
    actual_ids, data = [], []
    for channel_id in channels_ids:
        entity: Channel = await session.scalar(
            select(Channel).where(Channel.id == channel_id)
        )
        if not entity or entity.disposed:
            if not entity:
                pass  # UNPREDICTABLE BEHAVIOR

            users_to_unsubscribe = await entity.listeners_list
            for user in users_to_unsubscribe:
                (await user.channels_list).remove(entity)
                await session.commit()
            continue
        actual_ids += [channel_id]
        data += [await ChannelData.by_model(session, entity)]
    return actual_ids, data
