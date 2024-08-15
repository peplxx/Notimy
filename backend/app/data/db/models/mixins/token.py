import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.utils.generators import generate_provider_token


class TokenizedObject:
    __abstract__ = True
    token = sa.Column(sa.String, index=True, nullable=False, default=generate_provider_token)

    @classmethod
    async def find_by_token(cls, session: AsyncSession, entity_token: str):
        return await session.scalar(select(cls).where(cls.token == entity_token))
