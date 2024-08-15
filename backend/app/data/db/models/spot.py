from datetime import datetime, timezone
from json import dumps, loads
from uuid import UUID

import sqlalchemy as sa

from app.config import constants
from app.data.db import DeclarativeBase as Base
from app.data.db.models import Channel
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.models.mixins.token import TokenizedObject
from app.data.db.utils.encoders import UUIDEncoder

now = datetime.now(tz=timezone.utc).replace(tzinfo=None)


class Spot(Base, IndexedObject, TokenizedObject):
    __tablename__ = 'spots'

    additional_info = sa.Column(sa.String, nullable=True, default=constants.NO_ADDITIONAL_INFO)
    provider = sa.Column(sa.UUID, nullable=False)
    channels_raw = sa.Column(sa.String, nullable=False, default='[]')
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    account = sa.Column(sa.UUID, nullable=False)

    @property
    def channels(self):
        return [UUID(channel_id) for channel_id in loads(self.channels_raw)]

    @channels.setter
    def channels(self, value):
        self.channels_raw = dumps(value, default=str, cls=UUIDEncoder)

    def add_channel(self, channel: Channel):
        channels = set(self.channels)
        channels.add(channel.id)
        self.channels = [e for e in channels]

    @property
    def last_channel(self):
        if not self.channels:
            return None
        return self.channels[-1]

    @property
    def service_user_data(self):
        return {
            "token": self.token,
            "entity": self.id
        }
