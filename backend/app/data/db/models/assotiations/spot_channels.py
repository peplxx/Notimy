from sqlalchemy import Table
from app.data.db import DeclarativeBase as Base
import sqlalchemy as sa
__all__ = [
    "spot_channels_association"
]

spot_channels_association = Table(
    'spot_channels', Base.metadata,
    sa.Column('spot_id', sa.UUID, sa.ForeignKey('spots.id'), primary_key=True),
    sa.Column('channel_id', sa.UUID, sa.ForeignKey('channels.id'), primary_key=True)
)