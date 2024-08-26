import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import sqlalchemy as sa
from app.config import get_settings
from logging import getLogger, Logger

settings = get_settings()
def url(url):
    return settings.PATH_PREFIX + url

class TestRootModule:
    async def test_ping_module(self):
        assert True

    class TestProviderCreation:
        logger: Logger = getLogger("[pytest] /root/new_provider")


        async def test_create_provider(self, root_header: dict, client: AsyncClient, random_string: str):
            response = await client.post(
                url("/root/new_provider"),
                json={
                    "name": random_string,
                    "description": random_string
                },
                headers=root_header
            )
            assert response.status_code == status.HTTP_200_OK
            response_data = response.json()
            self.logger.debug("Data recieve: %s", response_data)
            assert False

