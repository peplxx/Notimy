import json
from datetime import datetime
import random
import datetime
import sqlalchemy as sa

from . import Channel
from .db_session import Base

from string import ascii_letters as TOKEN_ALPHABET


def generate_token() -> str:
    return ''.join([TOKEN_ALPHABET[random.randint(0, len(TOKEN_ALPHABET)) - 1] for i in range(50)])


class Spot(Base):
    __tablename__ = 'spots'

    id = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    token = sa.Column(sa.String, nullable=False, default=generate_token())
    additional_info = sa.Column(sa.String, nullable=True)
    provider = sa.Column(sa.Integer, nullable=False)
    channels_raw = sa.Column(sa.String, nullable=False, default='{"channels":[]}')
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.datetime.now())

    def __init__(self,
                 info: str | None,
                 provider: int):
        self.additional_info = info if info is not None else 'No additional info'
        self.provider = provider

    @property
    def lastChannel(self):
        if len(self.channels) == 0:
            return None
        return self.channels[-1]

    @property
    def channels(self):
        return json.loads(self.channels_raw)['channels']

    def add_channel(self, channel: Channel) -> None:
        lst = self.channels
        if channel.id not in lst:
            lst.append(channel.id)
        self.channels_raw = '{'+f'"channels":{json.dumps(lst)}'+'}'

    @property
    def dict(self):
        return {
            'id': self.id,
            "token": self.token,
            "additional_info": self.additional_info,
            "provider": self.provider,
            "channels": self.channels,
            "created_at": self.created_at
        }
