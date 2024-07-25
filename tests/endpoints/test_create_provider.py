from uuid import uuid4

import pytest
from sqlalchemy import select
from starlette import status
import requests

APP_HOST = "http://127.0.0.1"
APP_PORT = 5000
ROOT_TOKEN = "gUg8iTYWxbGQPFZJc0c7CS5RZQ9MVXawYHJ9WESUMeERNW2YmX"
class TestCreateProvider:
    @staticmethod
    def get_url():
        return f"{APP_HOST}:{APP_PORT}" + f"/providers/new"

    @staticmethod
    def auth_header(token):
        return {"Authorization": f"Bearer {token}"}

    @pytest.mark.parametrize(
        "headers, body, parameters",
        (
                (auth_header(ROOT_TOKEN), {}, {
                    "name": "Provider_1",
                    "description": "provider_1_description"
                }),
                ({}, {"token": ROOT_TOKEN}, {
                    "name": "Provider_2",
                    "description": "provider_2_description"
                }),
        ),
    )
    def test_success_provider_creation(self, headers, body, parameters):
        for key, value in parameters.items():
            body[key] = value
        result = requests.post(
            url=self.get_url(),
            json=body,
            headers=headers
        )
        assert result.status_code == 200

    @pytest.mark.parametrize(
        "headers, body, parameters",
        (
                (auth_header(ROOT_TOKEN), {}, {
                    "name": "Provider_1",
                }),
                ({}, {"token": ROOT_TOKEN}, {
                    "description": "provider_2_description"
                }),
                ({}, {"token": ROOT_TOKEN}, {
                    "description": "provider_2_description",
                    "some_extra_arg": "some_extra_arg",
                }),
        ),
    )
    def test_bad_args(self, headers, body, parameters):
        for key, value in parameters.items():
            body[key] = value
        result = requests.post(
            url=self.get_url(),
            json=body,
            headers=headers
        )
        assert result.status_code == 400

    @pytest.mark.parametrize(
        "headers, body, parameters",
        (
                (auth_header("BAadDD-TOKEN"), {}, {
                    "name": "Provider_1",
                    "description": "provider_2_description"
                }),
                ({}, {"token": "BAadDD-TOKEN"}, {
                    "name": "Provider_1",
                    "description": "provider_2_description"
                }),
                ({}, {}, {
                    "name": "Provider_1",
                    "description": "provider_2_description"
                }),
        ),
    )
    def test_bad_token(self, headers, body, parameters):
        for key, value in parameters.items():
            body[key] = value
        result = requests.post(
            url=self.get_url(),
            json=body,
            headers=headers
        )
        assert result.status_code == 403
