__all__ = ["NewMessageEvent"]
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.models import Channel, Message, Provider
from app.src.common.events.channel_events.base import ChannelEvent
from app.src.common.push_notifications import DefaultPushNotification
from app.src.common.push_notifications.dto import PushNotification
from app.src.modules.spots.logic import add_message

event_type = "NewMessageEvent"


class NewMessageEvent(ChannelEvent):
    event_type: str = ChannelEvent._event_type(event_type)

    def __init__(self, message: Message, source: Channel, session: AsyncSession) -> None:
        self.message = message
        self.pushNotification = DefaultPushNotification(title=f"У вас новое сообщение!", body=f"{self.message.text}")
        super().__init__(source, session)

    async def invoke(self):
        await add_message(self.session, (await self.source.spot), message=self.message, channel_id=self.source.id)
