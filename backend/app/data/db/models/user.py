import json
from json import dumps, loads
from uuid import UUID

import sqlalchemy as sa

from app.config.constants import Roles
from app.data.db import DeclarativeBase as Base
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.utils import get_now as now
from app.data.db.utils.encoders import UUIDEncoder


class User(Base, IndexedObject):
    __tablename__ = 'users'

    channels_raw = sa.Column(sa.String, nullable=False, default='[]')
    registered_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    role = sa.Column(sa.String, nullable=False, default=Roles.default.value)
    data = sa.Column(sa.String, nullable=False, default='{}')

    @property
    def channels(self):
        return [UUID(channel_id) for channel_id in loads(self.channels_raw)]

    @channels.setter
    def channels(self, new_value):
        self.channels_raw = dumps(new_value, default=str, cls=UUIDEncoder)

    def add_channel(self, channel_id: UUID):
        channels = self.channels
        if channel_id not in channels:
            channels += [channel_id]
        self.channels = channels

    def delete_channel(self, channel_id: UUID):
        channels = self.channels
        self.channels = [e for e in channels if e != channel_id]

    def get_data(self):
        return json.loads(self.data)

    def set_data(self, data):
        self.data = dumps(data, default=str, cls=UUIDEncoder)