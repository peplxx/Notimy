from datetime import timezone
import datetime
from json import loads, dumps
import pytz
from notimy.config import config
from uuid import uuid4, UUID
from notimy.data.db import DeclarativeBase as Base
import sqlalchemy as sa

from sqlalchemy import func
from notimy.utils import generate_code
from notimy.utils.json_encoder import UUIDEncoder

now = datetime.datetime.now(tz=timezone.utc)




class Channel(Base):
    __tablename__ = 'channels'
    id = sa.Column(sa.UUID, nullable=False, primary_key=True, default=uuid4)
    name = sa.Column(sa.String, nullable=False)
    provider = sa.Column(sa.UUID, index=True, nullable=False)
    spot = sa.Column(sa.UUID, index=True, nullable=False)

    closed_by = sa.Column(sa.Integer, nullable=False, default=-1)
    code = sa.Column(sa.String, index=True, nullable=False, unique=True, default=generate_code)
    users_raw = sa.Column(sa.String, nullable=False, default='[]')
    messages_raw = sa.Column(sa.String, nullable=False, default='[]')
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    closed_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now+config.CHANNEL_LIFETIME)

    @property
    def listeners(self):
        return [UUID(user_id) for user_id in loads(self.users_raw)]

    @listeners.setter
    def listeners(self, new_value):
        self.users_raw = dumps(new_value, default=str, cls=UUIDEncoder)

    def add_listener(self, listener_id: uuid4):
        users = set(self.listeners)
        users.add(listener_id)
        self.listeners = [e for e in users]

    @property
    def messages(self):
        return loads(self.messages_raw)

    @messages.setter
    def messages(self, new_value):
        self.messages_raw = dumps(new_value, default=str)

    def add_message(self, message):
        messages = self.messages
        messages.append(message)
        self.messages = messages

    @property
    def expired(self):
        dt_now = datetime.datetime.now(datetime.UTC).astimezone(timezone.utc)
        return self.closed_at.replace(tzinfo=pytz.utc) < dt_now

    def dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}