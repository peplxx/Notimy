import json
from datetime import datetime, timedelta
import random
from json import JSONEncoder

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
    spot = sa.Column(sa.Integer, nullable=False)
    users = sa.Column(sa.String, nullable=False, default='{"listeners":[]}')
    closed_by = sa.Column(sa.Integer, nullable=False, default=-1)
    code = sa.Column(sa.String, nullable=False, unique=True)
    messages_raw = sa.Column(sa.String, nullable=False, default='{"messages":[]}')
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.now())
    closed_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.now() + timedelta(1))

    @property
    def listeners(self):
        return json.loads(self.users)['listeners']

    @listeners.setter
    def listeners(self, value):
        self.users = '{'+f'"listeners":{json.dumps(value)}'+'}'

    def add_listener(self, listener: int):
        usr = self.listeners
        if listener not in usr:
            usr.append(listener)
        self.listeners = usr

    @property
    def messages(self):
        return json.loads(self.messages_raw)['messages']

    @messages.setter
    def messages(self, value: dict):
        self.messages_raw = '{'+f'"messages":{json.dumps(value)}'+'}'

    def add_message(self, message: Message):
        msg = self.messages
        if message not in msg:
            msg.append(message.__dict__)
        print(msg)
        self.messages = msg

    @property
    def isClosed(self):
        return datetime.now() > self.closed_at

    def __init__(
            self,
            name: str,
            provider: int,
            messages: list[Message],
            spot: int,
            code: str = None):
        self.name = name
        self.provider = provider
        self.messages = jsonable_encoder(messages)
        self.code = generate_code() if not code else code
        self.read_messages = 0
        self.spot = spot

    @property
    def dict(self):
        return {
            "name": self.name,
            'code': self.code,
            'provider': self.provider,
            "spot": self.spot,
            "listeners": self.listeners,
            "closed_by": self.closed_by,
            "created_at": self.created_at,
            "messages": self.messages,
            "closed_at": self.closed_at
        }

    def read_messages(self):
        self.read_messages = len(self.messages)

    @property
    def unread_messages(self):
        return len(self.messages) - self.read_messages
