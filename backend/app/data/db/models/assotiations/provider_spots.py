from sqlalchemy import Table
from app.data.db import DeclarativeBase as Base
import sqlalchemy as sa
__all__ = [
    "provider_spots_association"
]

provider_spots_association = Table(
    'provider_spots', Base.metadata,
    sa.Column('provider_id', sa.UUID, sa.ForeignKey('providers.id'), primary_key=True),
    sa.Column('spot_id', sa.UUID, sa.ForeignKey('spots.id'), primary_key=True)
)