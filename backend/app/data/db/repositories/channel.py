__all__ = ['ChannelRepository']

from uuid import UUID

from app.data.db.models import Spot, Channel, Message, User
from app.data.db.repositories.base import BaseRepository


class ChannelRepository(BaseRepository):

    async def create(self, spot: Spot, provider_id: UUID) -> Channel:
        created = False
        max_tries = 5
        while not created:
            try:
                channel = Channel(
                    provider=provider_id,
                    local_number=await Channel.get_next_local_number(self._session, spot.id)
                )
                created = True
            except Exception as e:
                max_tries -= 1
                if max_tries == 0:
                    raise e

        self._session.add(channel)
        await self._session.commit()
        (await spot.channels_list).append(channel)
        await self._session.commit()
        return channel

    async def add_message(self, channel: Channel, message: Message):
        channel.add_message(message)
        await self._session.commit()

    async def close(self, channel: Channel):
        if channel.open:
            channel.close()
            await self._session.commit()

    async def listeners_ids(self, channel: Channel):
        return [_.id for _ in await channel.listeners_list]

    async def add_listener(self, channel: Channel, user: User):
        if user.id not in await self.listeners_ids(channel):
            (await channel.listeners_list).append(user)
        await self._session.commit()
