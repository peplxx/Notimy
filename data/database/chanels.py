from datetime import datetime, timedelta
import random
from hashlib import sha256

import sqlalchemy as sa
from .db_session import Base

from string import ascii_letters as CODE_ALPHABET
from fastapi.encoders import jsonable_encoder
from ..datatypes import Message


def generate_code() -> str:
    return ''.join([CODE_ALPHABET[random.randint(0, len(CODE_ALPHABET)) - 1] for i in range(6)])


class Channel(Base):
    __tablename__ = 'channels'

    id = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    provider = sa.Column(sa.Integer, nullable=False)
    listeners = sa.Column(sa.JSON, nullable=False, default=[])
    closed_by = sa.Column(sa.Integer, nullable=False, default=-1)
    code = sa.Column(sa.String, nullable=False, unique=True)
    messages = sa.Column(sa.JSON, nullable=False, default=[])
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.now())
    closed_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.now() + timedelta(1))

    @property
    def isClosed(self):
        return datetime.now() > self.closed_at

    def __init__(
            self,
            name: str,
            provider: int,
            messages: list[Message],
            code: str = None):
        self.name = name
        self.provider = provider
        self.messages = jsonable_encoder(messages)
        self.code = generate_code() if not code else code
        self.read_messages = 0

    @property
    def dict(self):
        items = self.__dict__
        items.pop("_sa_instance_state")
        return items

    def read_messages(self):
        self.read_messages = len(self.messages)

    @property
    def unread_messages(self):
        return len(self.messages) - self.read_messages
