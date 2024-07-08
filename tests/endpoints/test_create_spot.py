import json
from uuid import uuid4

import pytest
from sqlalchemy import select
from starlette import status
import requests


APP_HOST = "http://127.0.0.1"

APP_PORT = 5000
ROOT_TOKEN = "gUg8iTYWxbGQPFZJc0c7CS5RZQ9MVXawYHJ9WESUMeERNW2YmX"
def create_provider():
    result = requests.post(
        url=f"{APP_HOST}:{APP_PORT}" + f"/providers/new",
        json={
            "token": ROOT_TOKEN,
            "name": "some name",
            "description": "description"
        }
    )
    return json.loads(result.text)


class TestCreateSpot:
    @staticmethod
    def get_url():
        return f"{APP_HOST}:{APP_PORT}" + f"/providers/new_spot"

    @pytest.mark.parametrize(
        "provider_token",
        (
                (create_provider()['token']),
        ),
    )
    def test_success_spot_creation_header(self, provider_token):
        result = requests.post(
            url=self.get_url(),
            json={},
            headers={'Authorization': f"Bearer {provider_token}"}
        )
        assert result.status_code == 200

    @pytest.mark.parametrize(
        "provider_token",
        (
                (create_provider()['token']),
        ),
    )
    def test_success_spot_creation_body(self, provider_token):
        result = requests.post(
            url=self.get_url(),
            json={"token": f"{provider_token}"}
        )
        assert result.status_code == 200

    @pytest.mark.parametrize(
        "provider_token",
        (
            ("dfhgdgfhfdhgkjdfngkjdf"),
        ),
    )
    def test_bad_token(self, provider_token):
        result = requests.post(
            url=self.get_url(),
            json={"token": f"{provider_token}"}
        )
        assert result.status_code == 403

    def test_max_spots_reached(self):
        provider = create_provider()
        token = provider["token"]
        for i in range(provider['max_spots']):
            requests.post(
                url=self.get_url(),
                json={"token": f"{token}"}
            )
        result = requests.post(
            url=self.get_url(),
            json={"token": f"{token}"}
        )
        assert result.status_code == 403
