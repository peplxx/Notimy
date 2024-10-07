from abc import ABC

from app.data.db.models import Channel
from app.src.common.events.base import Event
from app.src.middleware.push_notifications import send_notification


class ChannelEvent(Event, ABC):
    source: Channel

    @classmethod
    def _event_type(cls, postfix: str = None) -> str:
        return f"{cls.__class__.__name__}.{postfix}" if postfix else cls.__class__.__name__

    async def after_invoke(self):
        # Send notifications after success invoke
        for user in (await self.source.listeners_list):
            await user.notify(self.pushNotification)

    async def before_invoke(self):
        pass
