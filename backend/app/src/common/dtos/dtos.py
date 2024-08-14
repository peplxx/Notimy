__all__ = [
    "ChannelData",
    "UserData",
    "ProviderData",
    "SpotData"
]

import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.models import Provider, Spot, Channel, User, Alias


class ChannelData(BaseModel):
    id: UUID
    name: str
    provider: UUID
    spot: UUID
    closed_by: int
    code: str
    created_at: datetime.datetime
    closed_at: datetime.datetime

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
        result.users_ids = channel.listeners
        result.messages_data = channel.messages
        return result

    @staticmethod
    async def by_id(
            session: AsyncSession,
            channel_id: UUID
    ):
        channel: Channel = await session.scalar(
            select(Channel).where(Channel.id == channel_id)
        )
        return await ChannelData.by_model(session, channel)


class UserData(BaseModel):
    id: UUID
    registered_at: datetime.datetime
    role: str

    channels_ids: Optional[list[UUID]] = []
    data_json: Optional[dict] = {}
    channels_data: Optional[list[ChannelData]] = []

    @staticmethod
    async def by_model(
            session: AsyncSession,
            user: User
    ):
        result = UserData.model_validate(
            user,
            from_attributes=True
        )

        ids, data = await actual_channels(
            session=session,
            channels_ids=user.channels
        )
        result.data_json = user.get_data()
        result.channels_ids = ids
        result.channels_data = data
        return result

    @staticmethod
    async def by_id(
            session: AsyncSession,
            user_id: UUID
    ):
        user = await session.scalar(
            select(User).where(User.id == user_id)
        )
        return await UserData.by_model(session, user)


class SpotData(BaseModel):
    id: UUID
    token: str
    additional_info: str
    provider: UUID
    created_at: datetime.datetime
    account: UUID

    alias: Optional[dict] = {}
    channels_ids: Optional[list[UUID]] = []
    channels_data: Optional[list[ChannelData]] = []

    @staticmethod
    async def by_model(
            session: AsyncSession,
            spot: Spot
    ):
        result = SpotData.model_validate(
            spot,
            from_attributes=True
        )

        ids, data = await actual_channels(
            session=session,
            channels_ids=spot.channels
        )

        result.channels_ids = ids
        result.channels_data = data

        alias = await session.scalar(
            select(Alias).where(Alias.base == spot.id)
        )
        result.alias = alias.dict()
        return result

    @staticmethod
    async def by_id(
            session: AsyncSession,
            spot_id: UUID
    ):
        spot: Spot = await session.scalar(
            select(Spot).where(Spot.id == spot_id)
        )
        return await SpotData.by_model(session, spot)


class ProviderData(BaseModel):
    id: UUID
    token: str
    name: str
    description: str
    registered_at: datetime.datetime
    spots: int
    max_spots: int
    account: UUID

    spots_ids: Optional[list[UUID]] = []
    spots_data: Optional[list[SpotData]] = []

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
            spots: list[Spot] = list(await session.scalars(
                select(Spot).where(Spot.provider == provider.id)
            ))

            spots_ids = [spot.id for spot in spots]
            spots_data = [await SpotData.by_model(session, spot) for spot in spots]

            result.spots_ids = spots_ids
            result.spots_data = spots_data
        return result

    @staticmethod
    async def by_id(
            session: AsyncSession,
            provider_id: UUID
    ):
        provider: Provider = await session.scalar(
            select(Provider).where(Provider.id == provider_id)
        )
        return await ProviderData.by_model(session, provider)


async def actual_channels(
        session: AsyncSession,
        channels_ids: list[UUID]
) -> tuple[list[UUID], list[ChannelData]]:
    actual_ids, data = [], []
    for channel_id in channels_ids:
        entity: Channel = await session.scalar(
            select(Channel).where(Channel.id == channel_id)
        )
        if not entity or entity.expired:
            # TODO: MAKE CHANNELS DISPOSE
            continue
        actual_ids += [channel_id]
        data += [await ChannelData.by_model(session, entity)]
    return actual_ids, data
