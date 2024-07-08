from datetime import timezone, datetime
from json import loads, dumps
from uuid import uuid4, UUID

from flask_login import UserMixin

from notimy.data.db import DeclarativeBase as Base
import sqlalchemy as sa

from notimy.utils.json_encoder import UUIDEncoder

now = datetime.now(tz=timezone.utc)


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.UUID, primary_key=True, default=uuid4)
    channels_raw = sa.Column(sa.String, nullable=False, default='[]')
    registered_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)

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

    def dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
