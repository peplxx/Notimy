from datetime import datetime, timezone

import sqlalchemy as sa

from app.data.db import DeclarativeBase as Base
from app.data.db.models.mixins.index import IndexedObject

now = datetime.now(tz=timezone.utc).replace(tzinfo=None)


class Subscription(Base, IndexedObject):
    __tablename__ = 'subscriptions'

    spot_id = sa.Column(sa.UUID, sa.ForeignKey('spots.id'), nullable=False, unique=True)
    provider_id = sa.Column(sa.UUID, sa.ForeignKey('providers.id'), nullable=False, unique=True)
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    expires_at = sa.Column(sa.TIMESTAMP, nullable=True)

    @property
    def is_active(self):
        """Проверяет, активна ли подписка."""
        return self.expires_at is None or self.expires_at > now
