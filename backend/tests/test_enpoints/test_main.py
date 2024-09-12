from logging import getLogger, Logger
from uuid import uuid4

import pytest
from httpx import AsyncClient
from starlette import status

from app.config import get_settings
from app.data.db.models import Provider
from app.src.common.dtos import SpotData, ChannelData, ProviderData
from app.src.modules.users.schemas import UserResponse
from tests.conftest import url, auth, clients_params

get_settings().TESTING = True
settings = get_settings()
logger: Logger = getLogger(f"[pytest] {__name__}")

root: str = '/root'


class TestRootModule:
    class TestChangeMaxSpotLimit:
        url: str = url(root + "/change_max_spots")

        @pytest.mark.asyncio
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
        url: str = url(root + "/new_provider")

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
        url: str = url(root + "/subscription/upsert")

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


providers = '/providers'


class TestProviderModule:
    class TestNewSpot:
        url: str = url(providers + "/new_spot")

        async def test_spot_creation(self, has_spot: SpotData):
            assert has_spot.id

    class TestProviderMe:
        url: str = url(providers + '/me')

        async def test_provider_me(self, provider_client: AsyncClient):
            response = await provider_client.get(
                self.url
            )
            assert response.status_code == status.HTTP_200_OK

    class TestUpdateData:
        url: str = url(providers + '/update')

        async def test_update_provider_name(self, provider_client: AsyncClient):
            response = await provider_client.put(
                self.url,
                json={
                    "name": "UPD"
                }
            )
            assert response.status_code == status.HTTP_200_OK
            response_data = response.json()

            assert response_data['name'] == 'UPD'

        async def test_update_provider_description(self, provider_client: AsyncClient):
            response = await provider_client.put(
                self.url,
                json={
                    "description": "UPD"
                }
            )
            assert response.status_code == status.HTTP_200_OK
            response_data = response.json()

            assert response_data['description'] == 'UPD'


spots = "/spots"


class TestSpotModule:

    @staticmethod
    async def create_channel(spot_data: SpotData):
        async with AsyncClient(**clients_params) as client:
            client.headers.update({"Authorization": f"Bearer {spot_data.token}"})
            response = await client.post(get_settings().PATH_PREFIX + "/spots/new_channel")
            assert response.status_code == status.HTTP_200_OK
            return spot_data.alias['name'], ChannelData(**response.json())

    class TestNewChannel:
        url: str = url(spots + "/new_channel")

        async def test_channel_creation_wo_subscription(self, has_spot: SpotData, client: AsyncClient):
            spot = has_spot
            auth(client, spot)
            response = await client.post(
                self.url,
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

        async def test_channel_creation(self, has_spot_sub: SpotData, client: AsyncClient):
            spot = has_spot_sub
            auth(client, spot)
            response = await client.post(
                self.url,
            )
            assert response.status_code == status.HTTP_200_OK

        async def test_multiple_channel_creation(self, has_spot_sub: SpotData, client: AsyncClient):
            spot = has_spot_sub
            auth(client, spot)
            for i in range(3):
                response = await client.post(
                    self.url,
                )
                assert response.status_code == status.HTTP_200_OK

    class TestSpotMe:
        url: str = url(spots + "/me")

        async def test_spotme_without_channels(self, client: AsyncClient, has_spot: SpotData):
            auth(client, has_spot)
            response = await client.get(
                self.url
            )
            assert response.status_code == status.HTTP_200_OK

        async def test_spot_me_with_channel(self, client: AsyncClient, has_spot_sub: SpotData):
            auth(client, has_spot_sub)
            await client.post(TestSpotModule.TestNewChannel.url)
            response = await client.get(
                self.url
            )
            assert response.status_code == status.HTTP_200_OK
            response_data = response.json()
            assert len(response_data['channels_ids']) == 1

        async def test_subscribed_spot(self, client: AsyncClient, has_spot_sub: SpotData):
            auth(client, has_spot_sub)
            response = await client.get(self.url)
            assert response.status_code == status.HTTP_200_OK
            data = SpotData(**response.json())
            assert data.subscription['exist']

        async def test_unsubscribed_spot(self, client: AsyncClient, has_spot: SpotData):
            auth(client, has_spot)
            response = await client.get(self.url)
            assert response.status_code == status.HTTP_200_OK
            data = SpotData(**response.json())
            assert not data.subscription['exist']

        async def test_spot_alias(self, client: AsyncClient, has_spot: SpotData):
            auth(client, has_spot)
            response = await client.get(self.url)
            assert response.status_code == status.HTTP_200_OK
            data = SpotData(**response.json())
            assert data.alias["name"]
            assert data.alias["base"] == str(has_spot.id)

    class TestChangeAlias:
        url: str = url(spots + "/change_alias")

        async def test_change_alais(self, client: AsyncClient, has_spot_sub: SpotData):
            auth(client, has_spot_sub)
            response = await client.post(
                self.url,
                json={
                    "name": str(uuid4())[:get_settings().ALIAS_NAME_SIZE]
                }
            )
            assert response.status_code == status.HTTP_200_OK

        async def test_change_alais_wrong_length(self, client: AsyncClient, has_spot_sub: SpotData):
            auth(client, has_spot_sub)
            response = await client.post(
                self.url,
                json={
                    "name": str(uuid4())
                }
            )
            assert response.status_code == status.HTTP_400_BAD_REQUEST

        async def test_change_alais_existing(self, client: AsyncClient, has_spot_sub: SpotData):
            auth(client, has_spot_sub)
            response = await client.post(
                self.url,
                json={
                    "name": (used := str(uuid4())[:get_settings().ALIAS_NAME_SIZE])
                }
            )
            assert response.status_code == status.HTTP_200_OK

            response = await client.post(
                self.url,
                json={
                    "name": used
                }
            )
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    class TestAddMessage:
        url: str = url(spots + "/add_message")

        async def test_add_message(self, client: AsyncClient, has_spot_sub: SpotData):
            auth(client, has_spot_sub)
            response = await client.post(url(spots + "/new_channel"))
            assert response.status_code == status.HTTP_200_OK
            channel_data = ChannelData(**response.json())
            response = await client.post(
                self.url,
                json={
                    "channel_id": str(channel_data.id),
                    "message": {
                        "text": uuid4().hex,
                    }
                }
            )
            assert response.status_code == status.HTTP_200_OK
            channel_data = ChannelData(**response.json())
            assert len(channel_data.messages_data) == 1

        async def test_add_several_messages(self, client: AsyncClient, has_spot_sub: SpotData):
            auth(client, has_spot_sub)
            response = await client.post(url(spots + "/new_channel"))
            assert response.status_code == status.HTTP_200_OK
            channel_data = ChannelData(**response.json())
            n = 4
            for _ in range(n):
                response = await client.post(
                    self.url,
                    json={
                        "channel_id": str(channel_data.id),
                        "message": {
                            "text": uuid4().hex,
                        }
                    }
                )
                assert response.status_code == status.HTTP_200_OK
            channel_data = ChannelData(**response.json())
            assert len(channel_data.messages_data) == n

    class TestCloseChannel:
        url: str = url(spots + "/close_channel")

        async def test_close_channel(self, client: AsyncClient, has_spot_sub: SpotData):
            auth(client, has_spot_sub)
            response = await client.post(url(spots + "/new_channel"))
            assert response.status_code == status.HTTP_200_OK
            channel_data = ChannelData(**response.json())
            response = await client.post(
                self.url,
                json={
                    "channel_id": str(channel_data.id)
                }
            )
            assert response.status_code == status.HTTP_200_OK
            channel_data = ChannelData(**response.json())
            assert not channel_data.open


class TestUserModule:
    @staticmethod
    async def login_client(client: AsyncClient, token=None):
        response = await client.get(TestUserModule.TestUserMe.login + (f'?token={token}' if token else ""))
        assert response.status_code == status.HTTP_200_OK
        client.cookies.set("session_token", client.cookies['session_token'])

    class TestUserMe:
        login: str = url("/login")
        me: str = url("/me")

        async def test_regular_user(self, client: AsyncClient):
            await TestUserModule.login_client(client)
            response = await client.get(self.me)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['role'] == "user"

        async def test_spot_user(self, client: AsyncClient, has_spot: SpotData):
            await TestUserModule.login_client(client, has_spot.token)
            response = await client.get(self.me)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['role'] == "spot_user"

        async def test_provider_user(self, client: AsyncClient, has_provider: ProviderData):
            await TestUserModule.login_client(client, has_provider.token)
            response = await client.get(self.me)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()['role'] == "provider_user"

    class TestJoinChannel:
        join_url = lambda _, alias: url("/join/" + alias)

        async def test_join_channel(self, client: AsyncClient, has_spot_sub: SpotData):
            await TestUserModule.login_client(client)
            alias, channel_data = await TestSpotModule.create_channel(has_spot_sub)
            response = await client.post(
                self.join_url(alias)
            )
            assert response.status_code == status.HTTP_200_OK
            user_data = UserResponse(**response.json())
            assert channel_data.id in user_data.channels_ids

        async def test_join_channel_to_spot_with_2_channels(self, client: AsyncClient, has_spot_sub: SpotData):
            await TestUserModule.login_client(client)
            alias, channel_data = await TestSpotModule.create_channel(has_spot_sub)
            alias, channel_data = await TestSpotModule.create_channel(has_spot_sub)
            response = await client.post(
                self.join_url(alias)
            )
            assert response.status_code == status.HTTP_200_OK
            user_data = UserResponse(**response.json())
            assert channel_data.id in user_data.channels_ids

    class TestForgetChannel:
        forget_url = lambda _, channel_id: url("/forget/" + str(channel_id))

        async def test_forget_channel(self, client: AsyncClient, has_spot_sub: SpotData):
            await TestUserModule.login_client(client)
            alias, channel_data = await TestSpotModule.create_channel(has_spot_sub)
            response = await client.post(
                TestUserModule.TestJoinChannel().join_url(alias)
            )
            assert response.status_code == status.HTTP_200_OK
            user_data = UserResponse(**response.json())
            assert channel_data.id in user_data.channels_ids
            response = await client.delete(
                self.forget_url(channel_data.id)
            )
            assert response.status_code == status.HTTP_200_OK
            user_data = UserResponse(**response.json())
            assert channel_data.id not in user_data.channels_ids

