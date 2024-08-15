from uuid import uuid4, UUID

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class IndexedObject:
    __abstract__ = True
    id = sa.Column(sa.UUID, nullable=False, primary_key=True, default=uuid4)

    @classmethod
    async def find_by_id(cls, session: AsyncSession, entity_id: UUID):
        return await session.scalar(select(cls).where(cls.id == entity_id))
