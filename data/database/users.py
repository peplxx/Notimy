import datetime
import json

import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import Base


class User(Base, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    channels = sa.Column(sa.String, nullable=False, default='{"channels":[]}')
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.datetime.now())
    def __init__(self):
        pass

    @property
    def listen_to(self):
        return json.loads(self.channels)['channels']

    @listen_to.setter
    def listen_to(self, value):
        self.channels = '{' + f'"channels":{json.dumps(value)}' + '}'

    def add_channel(self, channel_id: int):
        channels = self.listen_to
        if channel_id not in channels:
            channels.append(channel_id)
        self.listen_to = channels
