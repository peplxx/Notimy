__all__ = ['ChannelRepository']

from uuid import UUID

from app.data.db.models import Spot, Channel, Message
from app.data.db.repositories.base import BaseRepository


class ChannelRepository(BaseRepository):

    async def create(self, spot: Spot, provider_id: UUID) -> Channel:
        channel = Channel(
            provider=provider_id,
            local_number=await Channel.get_next_local_number(self._session, spot.id)
        )
        self._session.add(channel)
        (await spot.channels_list).append(channel)
        await self._session.commit()

    async def get_channel_ids(self, spot: Spot) -> list[UUID]:
        return [_.id for _ in await spot.channels_list]

    async def add_message(self, channel: Channel, message: Message):
        channel.add_message(message)
        await self._session.commit()
