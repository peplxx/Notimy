import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import Base


class User(Base, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    listen_to = sa.Column(sa.JSON, nullable=False, default='[]')
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.datetime.now())
    def __init__(self,
                 listen_to: list):
        self.listen_to = listen_to

    def add_chanel(self,channel_id: int):
        self.listen_to.append(channel_id)
