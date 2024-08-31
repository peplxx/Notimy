import pytest
from httpx import AsyncClient
from starlette import status

from app.config import get_settings
from tests.conftest import auth
from app.src.common.dtos import SpotData, ChannelData


@pytest.fixture(scope="function")
async def has_channel(client: AsyncClient, has_spot_sub: SpotData) -> ChannelData:
    auth(client, has_spot_sub)
    response = await client.post(
        get_settings().PATH_PREFIX+"/spots/new_channel"
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    return ChannelData(**response_data)

