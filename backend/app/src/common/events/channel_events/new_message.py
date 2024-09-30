__all__ = ["NewMessageEvent"]
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.models import Channel, Message
from app.src.common.events.channel_events.base import ChannelEvent
from app.src.common.push_notifications import DefaultPushNotification
from app.src.modules.spots.logic import add_message

event_type = "NewMessageEvent"


class NewMessageEvent(ChannelEvent):
    event_type: str = ChannelEvent._event_type(event_type)
    message: Message

    def __init__(self, message: Message, source: Channel, session: AsyncSession) -> None:
        super().__init__(source, session)
        self.message = message
        push_message = f"{message.text}"
        self.pushNotification = DefaultPushNotification(title=f"Новое сообщение!", body=push_message)

    async def invoke(self):
        await add_message(self.session, (await self.source.spot), message=self.message, channel_id=self.source.id)
