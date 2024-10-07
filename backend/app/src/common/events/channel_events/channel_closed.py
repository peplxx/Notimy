__all__ = ["ChannelClosedEvent"]

from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.models import Channel, Message
from app.src.common.events.channel_events.base import ChannelEvent
from app.src.common.push_notifications import DefaultPushNotification
from app.src.common.push_notifications.dto import PushNotification
from app.src.modules.spots.logic import close_channel_by_id

event_type = "ChannelClosedEvent"


class ChannelClosedEvent(ChannelEvent):
    event_type: str = ChannelEvent._event_type(event_type)
    pushNotification: PushNotification = DefaultPushNotification(title="Изменился статус заказа!",
                                                                 body="Ваш заказ готов!\nПриятного аппетита!😋")

    def __init__(self, source: Channel, session: AsyncSession) -> None:
        super().__init__(source, session)

    async def invoke(self):
        await close_channel_by_id(self.session, (await self.source.spot), channel_id=self.source.id)
