from datetime import datetime
from json import dumps, loads
from uuid import UUID

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.config import get_settings
from app.data.db import DeclarativeBase as Base
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.utils import get_dispose_at as dispose_at
from app.data.db.utils import get_now as now
from app.data.db.utils.encoders import UUIDEncoder
from app.data.db.utils.generators import generate_invitation_code
from app.data.db.models.assotiations import users_channels_association, spot_channels_association

config = get_settings()


class Message(BaseModel):
    text: str


class Channel(Base, IndexedObject):
    __tablename__ = 'channels'

    provider = sa.Column(sa.UUID, sa.ForeignKey("providers.id"), index=True)

    code = sa.Column(sa.String, index=True, nullable=False, unique=False, default=generate_invitation_code)

    listeners = relationship('User', secondary=users_channels_association, back_populates='channels',
                             cascade="all, delete")

    messages_raw = sa.Column(sa.String, nullable=False, default='[]')

    open = sa.Column(sa.BOOLEAN, nullable=False, default=True)

    local_number = sa.Column(sa.INTEGER, nullable=True)

    spot_relation = relationship(
        'Spot',
        secondary=spot_channels_association,
        back_populates='channels_relation',
        cascade="all, delete"
    )

    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    closed_at = sa.Column(sa.TIMESTAMP, nullable=True)
    dispose_at = sa.Column(sa.TIMESTAMP, nullable=False, default=dispose_at)

    @property
    async def spot(self):
        return (await self.awaitable_attrs.spot_relation)[0]

    @property
    async def listeners_list(self):
        return await self.awaitable_attrs.listeners

    @property
    def messages(self):
        return [Message(**_) for _ in loads(self.messages_raw)]

    @messages.setter
    def messages(self, new_value: list):
        self.messages_raw = dumps([_.dict() for _ in new_value], default=str)

    def add_message(self, message):
        messages = self.messages
        messages.append(message)
        self.messages = messages

    @property
    def disposed(self):
        return self.dispose_at < now()

    def close(self):
        self.open = False
        self.closed_at = now()

    @staticmethod
    async def get_next_local_number(session: AsyncSession, spot_id: UUID):
        today = datetime.now().date()
        result = await session.scalar(
            select(func.count(Channel.id))
            .where(
                and_(
                    Channel.spot_relation.any(id=spot_id),
                    func.date(Channel.created_at) == today
                )
            )
        )
        return (result or 0) + 1