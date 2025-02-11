from datetime import datetime, timezone
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.config import constants
from app.data.db import DeclarativeBase as Base
from app.data.db.models.assotiations.provider_spots import provider_spots_association
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.models.mixins.token import TokenizedObject
from app.data.db.utils import get_now as now


class Provider(Base, IndexedObject, TokenizedObject):
    __tablename__ = 'providers'

    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)

    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    spots = sa.Column(sa.Integer, nullable=False, default=0)
    max_spots = sa.Column(sa.Integer, nullable=False, default=1)
    account = sa.Column(sa.UUID)

    spots_relation = relationship(
        'Spot',
        secondary=provider_spots_association,
        back_populates='provider_relation',
        cascade="all, delete"
    )

    @property
    async def spots_list(self):
        return await self.awaitable_attrs.spots_relation

    def __init__(
            self,
            name: str,
            account: UUID,
            description: str = None,
    ):
        super().__init__()
        self.name = name
        self.description = description if description else constants.NO_DESCRIPTION
        self.account = account

    @property
    def service_user_data(self):
        return {
            "token": self.token,
            "entity": self.id
        }
