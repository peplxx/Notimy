import json
from datetime import datetime, timezone
from json import dumps, loads
from uuid import UUID, uuid4

import sqlalchemy as sa
from flask_login import UserMixin

from notimy.config.roles import Roles
from notimy.data.db import DeclarativeBase as Base
from notimy.utils.json_encoder import UUIDEncoder

now = datetime.now(tz=timezone.utc)


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.UUID, primary_key=True, default=uuid4)
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
        channels = set(self.channels)
        channels.add(channel_id)
        self.channels = [e for e in channels]

    def delete_channel(self, channel_id: UUID):
        channels = set(self.channels)
        self.channels = [e for e in channels if e != channel_id]

    def get_data(self):
        return json.loads(self.data)

    def dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
