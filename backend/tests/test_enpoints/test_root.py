from logging import getLogger, Logger
from uuid import uuid4

import pytest
from httpx import AsyncClient
from starlette import status

from app.config import get_settings
from app.data.db.models import Provider
from app.src.common.dtos import SpotData
from conftest import url
from tests.fixtures import has_provider, has_spot

settings = get_settings()
logger: Logger = getLogger(f"[pytest] {__name__}")

prefix: str = '/root'


class TestRootModule:
    class TestChangeMaxSpotLimit:
        url: str = url(prefix + "/change_max_spots")

        async def test_change_max_spot_invalid_provider_id(
                self,
                root_client: AsyncClient
        ):
            response = await root_client.post(
                self.url,
                json={
                    "id": str(uuid4()),
                    "value": 1
                },
            )
            assert response.status_code == status.HTTP_400_BAD_REQUEST

        @pytest.mark.parametrize(
            "value, response_code", [
                (1, 200),
                (2, 200),
                (-1, 200),
                (-2, 403),
            ])
        async def test_change_max_spot(
                self,
                root_client: AsyncClient,
                has_provider: Provider,
                value: int,
                response_code: int
        ):
            provider = has_provider
            response = await root_client.post(
                self.url,
                json={
                    "id": str(provider.id),
                    "value": value
                }
            )
            assert response.status_code == response_code
            if response_code != 200:
                return
            response_data = response.json()
            changed_value = response_data['max_spots']
            assert provider.max_spots + value == changed_value


    class TestProviderCreation:
        url: str = url(prefix + "/new_provider")

        async def test_create_provider(self, root_client: AsyncClient, has_provider: Provider):

            logger.debug("Data recieve: %s", has_provider)
            assert Provider.token

        async def test_create_existing_provider(self, root_client: AsyncClient):
            response = await root_client.post(
                self.url,
                json={
                    "name": uuid4().hex,
                    "description": uuid4().hex
                }
            )
            assert response.status_code == status.HTTP_200_OK
            response_data = response.json()
            assert response_data['token']
            response = await root_client.post(
                self.url,
                json={
                    "name": response_data['name'],
                    "description": response_data['description']
                }
            )
            assert response.status_code == status.HTTP_200_OK
            new_provider_data = response.json()
            assert new_provider_data['id'] == str(response_data["id"])

        @pytest.mark.parametrize(
            "input_dict",
            [
                pytest.param(
                    {"description": uuid4().hex},
                    id='no-name-provided'
                ),
                pytest.param(
                    {"description": uuid4().hex},
                    id="no-description-provided"
                )
            ]
        )
        async def test_create_provider_wrong_input(self, root_client: AsyncClient, input_dict):
            response = await root_client.post(
                url("/root/new_provider"),
                json=input_dict,
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


    class TestUpsertSubscription:
        url: str = url(prefix + "/subscription/upsert")

        async def test_subscription(self, root_client: AsyncClient, has_spot: SpotData):
            spot = has_spot
            response = await root_client.post(
                self.url,
                json={
                    "spot_id": str(spot.id),
                    "days": 5
                }
            )
            assert response.status_code == status.HTTP_200_OK
