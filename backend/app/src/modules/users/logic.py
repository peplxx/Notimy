from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.models import Spot, Provider


async def find_service_user(
        session: AsyncSession,
        token: str,
) -> UUID | None:
    if not token:
        return None
    tables = [Spot, Provider]
    for table in tables:
        result = await session.scalar(select(table).where(table.token == token))
        if result:
            return result.account
    return None
