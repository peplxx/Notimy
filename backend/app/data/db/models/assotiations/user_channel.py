from sqlalchemy import Table
from app.data.db import DeclarativeBase as Base
import sqlalchemy as sa
__all__ = [
    "user_channel_association"
]

user_channel_association = Table(
    'user_channel', Base.metadata,
    sa.Column('user_id', sa.UUID, sa.ForeignKey('users.id'), primary_key=True),
    sa.Column('channel_id', sa.UUID, sa.ForeignKey('channels.id'), primary_key=True)
)