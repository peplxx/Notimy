from json import dumps, loads
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.config import constants
from app.data.db import DeclarativeBase as Base
from app.data.db.models import Channel
from app.data.db.models import Subscription
from app.data.db.models.assotiations.provider_spots import provider_spots_association
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.models.mixins.token import TokenizedObject
from app.data.db.utils import get_now as now
from app.data.db.utils.encoders import UUIDEncoder
from app.data.db.models.assotiations import spot_channels_association


class Spot(Base, IndexedObject, TokenizedObject):
    __tablename__ = 'spots'

    additional_info = sa.Column(sa.String, nullable=True, default=constants.NO_ADDITIONAL_INFO)
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    account = sa.Column(sa.UUID, sa.ForeignKey("users.id"), index=True)

    channels_relation = relationship(
        'Channel',
        secondary=spot_channels_association,
        back_populates='spot_relation',
        cascade="all, delete"
    )

    provider_relation = relationship(
        'Provider',
        secondary=provider_spots_association,
        back_populates='spots_relation',
        cascade="all, delete"
    )

    @property
    async def provider(self):
        return (await self.awaitable_attrs.provider_relation)[0]

    @property
    async def channels_list(self):
        return await self.awaitable_attrs.channels_relation



    @property
    async def last_channel(self):
        channels_list = await self.channels_list
        if not channels_list or len(channels_list) == 0:
            return None
        return channels_list[-1]

    @property
    def service_user_data(self):
        return {
            "token": self.token,
            "entity": self.id
        }

    async def is_subscribed(self, session: AsyncSession) -> bool:
        subscription = await self.get_subscription(session)
        return subscription.is_active if subscription else False

    async def get_subscription(self, session: AsyncSession) -> Subscription | None:
        subscription = await session.scalar(select(Subscription).where(
            Subscription.spot_id == self.id and Subscription.provider_id == self.provider
        ))
        return subscription
