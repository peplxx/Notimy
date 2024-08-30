import sqlalchemy as sa

from app.data.db import DeclarativeBase as Base
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.utils import get_now as now


class Subscription(Base, IndexedObject):
    __tablename__ = 'subscriptions'

    spot_id = sa.Column(sa.UUID, sa.ForeignKey('spots.id'), index=True)
    provider_id = sa.Column(sa.UUID, sa.ForeignKey('providers.id'), index=True)
    created_at = sa.Column(sa.TIMESTAMP, index=True, nullable=False, default=now)
    expires_at = sa.Column(sa.TIMESTAMP, index=True, nullable=True)

    @property
    def is_active(self):
        """Проверяет, активна ли подписка."""
        return self.expires_at is None or self.expires_at > now()
