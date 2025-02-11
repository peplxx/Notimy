from sqlalchemy import Table
from app.data.db import DeclarativeBase as Base
import sqlalchemy as sa
__all__ = [
    "users_channels_association"
]

users_channels_association = Table(
    'users_channels', Base.metadata,
    sa.Column('user_id', sa.UUID, sa.ForeignKey('users.id'), primary_key=True),
    sa.Column('channel_id', sa.UUID, sa.ForeignKey('channels.id'), primary_key=True)
)