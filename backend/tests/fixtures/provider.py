__all__ = [

    "has_provider",
]


from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import Roles
from app.data.db.models import Provider, User


@pytest.fixture(scope="function")
async def has_provider(session: AsyncSession) -> Provider:
    print('fsdgdfg')
    connection = await session.connection()
    # Get the URL from the connection's engine
    db_url = str(connection.engine.url)
    print(db_url)
    service_account = User(
        role=Roles.providerUser.value,
    )
    session.add(service_account)
    await session.commit()
    provider = Provider(
        name=uuid4().hex,
        description=uuid4().hex,
        account=service_account.id
    )
    session.add(provider)
    await session.commit()
    return provider


