import datetime
import random

import sqlalchemy as sa

from . import Channel
from .db_session import Base
from string import ascii_letters as TOKEN_ALPHABET


def generate_token() -> str:
    return ''.join([TOKEN_ALPHABET[random.randint(0, len(TOKEN_ALPHABET)) - 1] for i in range(50)])


class Provider(Base):
    __tablename__ = 'providers'

    id = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    token = sa.Column(sa.String, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    registered_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.datetime.now())
    channels = sa.Column(sa.JSON, default=[], nullable=False)
    last_channel = sa.Column(sa.Integer, default=-1, nullable=False)

    def __init__(
            self,
            name: str,
            description: str):
        self.name = name
        self.description = description
        self.token = generate_token()

    def add_channel(self, channel: Channel):
        self.channels.append(channel)
        self.last_channel = channel.id