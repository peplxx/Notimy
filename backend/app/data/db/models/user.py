import json
from json import dumps

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.config.constants import Roles
from app.data.db import DeclarativeBase as Base
from app.data.db.models.assotiations import users_channels_association
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.utils import get_now as now
from app.data.db.utils.encoders import UUIDEncoder
from app.src.common.push_notifications.dto import PushNotification
from app.src.common.telegram_api.send_message import send_telegram_message
from app.src.middleware.push_notifications import send_notification


class User(Base, IndexedObject):
    __tablename__ = 'users'

    # Telegram data
    telegram_id = sa.Column(sa.INTEGER, nullable=True, index=True)
    telegram_username = sa.Column(sa.String(255), nullable=True, index=True)
    telegram_firstname = sa.Column(sa.String(255), nullable=True)
    telegram_lastname = sa.Column(sa.String(255), nullable=True)

    registered_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    role = sa.Column(sa.String(255), nullable=False, default=Roles.default.value)
    data = sa.Column(sa.String, nullable=False, default='{}')

    channels = relationship('Channel', secondary=users_channels_association, back_populates='listeners',
                            cascade="all, delete")
    push_data = sa.Column(sa.JSON, nullable=True)

    @property
    async def channels_list(self):
        return await self.awaitable_attrs.channels

    @property
    def is_default(self):
        return self.role == Roles.default.value

    def get_data(self):
        return json.loads(self.data)

    def set_data(self, data):
        self.data = dumps(data, default=str, cls=UUIDEncoder)

    @property
    def can_get_push(self):
        return self.push_data and self.is_default

    async def notify(self, push_data: PushNotification):
        if self.telegram_id:
            await send_telegram_message(chat_id=self.telegram_id, push_data=push_data)
            # do telegram push
            pass
        elif self.can_get_push:
            await send_notification(self, push_data)
