import datetime
from datetime import timezone
from json import dumps, loads
from uuid import UUID, uuid4

import pytz
import sqlalchemy as sa
from pydantic import BaseModel

from app.config import get_settings
from app.data.db import DeclarativeBase as Base
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.utils.encoders import UUIDEncoder
from app.data.db.utils.generators import generate_invitation_code

config = get_settings()
now = datetime.datetime.now(tz=timezone.utc).replace(tzinfo=None)


class Message(BaseModel):
    text: str

    def __dict__(self):
        return {
            "text": self.text
        }


class Channel(Base, IndexedObject):
    __tablename__ = 'channels'

    provider = sa.Column(sa.UUID, index=True, nullable=False)
    spot = sa.Column(sa.UUID, index=True, nullable=False)

    code = sa.Column(sa.String, index=True, nullable=False, unique=True, default=generate_invitation_code)
    users_raw = sa.Column(sa.String, nullable=False, default='[]')
    messages_raw = sa.Column(sa.String, nullable=False, default='[]')

    open = sa.Column(sa.BOOLEAN, nullable=False, default=True)

    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    closed_at = sa.Column(sa.TIMESTAMP, nullable=True)
    dispose_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now + config.CHANNEL_LIFETIME)

    @property
    def listeners(self):
        return [UUID(user_id) for user_id in loads(self.users_raw)]

    @listeners.setter
    def listeners(self, new_value):
        self.users_raw = dumps(new_value, default=str, cls=UUIDEncoder)

    def add_listener(self, listener_id: UUID):
        users = set(self.listeners)
        users.add(listener_id)
        self.listeners = [e for e in users]

    def delete_listener(self, listener_id: UUID):
        users = set(self.listeners)
        self.listeners = [e for e in users if e != listener_id]

    @property
    def messages(self):
        return [Message(**_) for _ in loads(self.messages_raw)]

    @messages.setter
    def messages(self, new_value: list):
        self.messages_raw = dumps([_.__dict__ for _ in new_value], default=str)

    def add_message(self, message):
        messages = self.messages
        messages.append(message)
        self.messages = messages

    @property
    def disposed(self):
        dt_now = datetime.datetime.now(datetime.UTC).astimezone(timezone.utc)
        return self.dispose_at.replace(tzinfo=pytz.utc) < dt_now

    @property
    def closed(self):
        dt_now = datetime.datetime.now(datetime.UTC).astimezone(timezone.utc)
        return self.closed_at.replace(tzinfo=pytz.utc) < dt_now or not self.open
