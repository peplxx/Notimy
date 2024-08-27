__all__ = [
    "has_provider",
    "provider_header",
]

from uuid import uuid4

import pytest
from httpx import AsyncClient
from starlette import status

from app.src.common.dtos import ProviderData


@pytest.fixture(scope="function")
async def has_provider(root_client: AsyncClient) -> ProviderData:
    response = await root_client.post(
        "/api/root/new_provider",
        json={
            "name": uuid4().hex,
            "description": uuid4().hex,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data: dict = response.json()
    return ProviderData(**data)


@pytest.fixture(scope="function")
async def provider_header(has_provider: ProviderData) -> dict:
    return {"Authorization": f"Bearer {has_provider.token}"}
