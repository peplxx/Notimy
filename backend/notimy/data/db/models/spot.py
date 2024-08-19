from datetime import datetime, timezone
from json import dumps, loads
from uuid import UUID, uuid4

import sqlalchemy as sa

from frontend.data.db import DeclarativeBase as Base
from frontend.data.db.models import Channel
from frontend.utils import generate_spot_token
from frontend.utils.json_encoder import UUIDEncoder

now = datetime.now(tz=timezone.utc)


class Spot(Base):
    __tablename__ = 'spots'

    id = sa.Column(sa.UUID, nullable=False, primary_key=True, default=uuid4)
    token = sa.Column(sa.String, index=True, nullable=False, default=generate_spot_token)
    additional_info = sa.Column(sa.String, nullable=True, default="NO_INFO")
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

    def dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
