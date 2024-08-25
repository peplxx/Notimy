from sqlalchemy import Table
from app.data.db import DeclarativeBase as Base
import sqlalchemy as sa
__all__ = [
    "spot_channel_association"
]

spot_channel_association = Table(
    'spot_channel', Base.metadata,
    sa.Column('spot_id', sa.UUID, sa.ForeignKey('spot.id'), primary_key=True),
    sa.Column('channel_id', sa.UUID, sa.ForeignKey('channels.id'), primary_key=True)
)