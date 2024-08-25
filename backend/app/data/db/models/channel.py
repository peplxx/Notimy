from json import dumps, loads
from uuid import UUID

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.orm import relationship

from app.config import get_settings
from app.data.db import DeclarativeBase as Base
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.utils import get_dispose_at as dispose_at
from app.data.db.utils import get_now as now
from app.data.db.utils.encoders import UUIDEncoder
from app.data.db.utils.generators import generate_invitation_code
from app.data.db.models.assotiations import user_channel_association
config = get_settings()


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

    listeners = relationship('User', secondary=user_channel_association, back_populates='channels', cascade="all, delete")

    messages_raw = sa.Column(sa.String, nullable=False, default='[]')

    open = sa.Column(sa.BOOLEAN, nullable=False, default=True)

    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    closed_at = sa.Column(sa.TIMESTAMP, nullable=True)
    dispose_at = sa.Column(sa.TIMESTAMP, nullable=False, default=dispose_at)

    @property
    async def listeners_list(self):
        return await self.awaitable_attrs.listeners


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
        return self.dispose_at < now()

    def close(self):
        self.open = False
        self.closed_at = now
