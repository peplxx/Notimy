__all__ = [
    "has_spot",
    "spot_header"
]

import pytest
from httpx import AsyncClient
from starlette import status

from app.config import get_settings
from app.src.common.dtos import SpotData


@pytest.fixture(scope="function")
async def has_spot(provider_client: AsyncClient) -> SpotData:
    url = get_settings().PATH_PREFIX+"/providers/new_spot"
    response = await provider_client.post(
        url,
        json={}
    )
    assert response.status_code == status.HTTP_200_OK
    return SpotData(**response.json())


@pytest.fixture(scope="function")
async def spot_header(has_spot: SpotData) -> dict:
    return {"Authorization": f"Bearer {has_spot.token}"}
