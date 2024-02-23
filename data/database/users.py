import datetime
import sqlalchemy as sa
from .db_session import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    listen_to = sa.Column(sa.JSON, nullable=False, default='[]')
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.datetime.now())
