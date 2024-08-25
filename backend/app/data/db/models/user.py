import json
from json import dumps, loads
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.config.constants import Roles
from app.data.db import DeclarativeBase as Base
from app.data.db.models.assotiations import user_channel_association
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.utils import get_now as now
from app.data.db.utils.encoders import UUIDEncoder


class User(Base, IndexedObject):
    __tablename__ = 'users'

    registered_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    role = sa.Column(sa.String, nullable=False, default=Roles.default.value)
    data = sa.Column(sa.String, nullable=False, default='{}')

    channels = relationship('Channel', secondary=user_channel_association, back_populates='listeners',
                            cascade="all, delete")

    @property
    async def channel_list(self):
        return await self.awaitable_attrs.channels

    def get_data(self):
        return json.loads(self.data)

    def set_data(self, data):
        self.data = dumps(data, default=str, cls=UUIDEncoder)
