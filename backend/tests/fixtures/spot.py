__all__ = [
    "has_spot",
    "spot_header",
    "has_spot_sub"
]

import pytest
from httpx import AsyncClient
from starlette import status

from app.config import get_settings
from app.src.common.dtos import SpotData


@pytest.fixture(scope="function")
async def has_spot(provider_client: AsyncClient) -> SpotData:
    url = get_settings().PATH_PREFIX + "/providers/new_spot"
    response = await provider_client.post(
        url,
        json={}
    )
    assert response.status_code == status.HTTP_200_OK
    return SpotData(**response.json())


@pytest.fixture(scope="function")
async def has_spot_sub(root_client, has_spot: SpotData) -> SpotData:
    url = get_settings().PATH_PREFIX + "/root/subscription/upsert"
    response = await root_client.post(
        url,
        json={
            "spot_id": str(has_spot.id),
            "days": 10,
        }
    )
    return SpotData(**response.json())


@pytest.fixture(scope="function")
async def spot_header(has_spot: SpotData) -> dict:
    return {"Authorization": f"Bearer {has_spot.token}"}
