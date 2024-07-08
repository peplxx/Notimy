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


def create_spot(provider_token):
    result = requests.post(
        url=f"{APP_HOST}:{APP_PORT}" + f"/providers/new_spot",
        json={
            "token": provider_token,
        }
    )
    return json.loads(result.text)


def get_spot(token):
    result = requests.get(
        url=f"{APP_HOST}:{APP_PORT}/spots/me",
        headers={"Authorization": f"Bearer {token}"})
    return json.loads(result.text)


class TestAddMessage:
    @staticmethod
    def get_url():
        return f"{APP_HOST}:{APP_PORT}" + f"/channels/add_message"

    def test_add_message_to_channel(self):
        provider = create_provider()
        provider_token = provider["token"]
        spot = create_spot(provider_token)
        spot_token = spot['token']
        request = requests.post(
            url=f"{APP_HOST}:{APP_PORT}" + f"/channels/new",
            json={"name": "Заказ кабачков"},
            headers={"Authorization": f"Bearer {spot_token}"}
        )
        assert request.status_code == 200
        channel = json.loads(request.text)
        spot = get_spot(spot_token)
        assert spot["channels"][0]['id'] == channel['id']
        request = requests.post(
            url=self.get_url(),
            json={"channel_id": channel['id'],
                  "message":{'text':"some text message"}
                  },
            headers={"Authorization": f"Bearer {spot_token}"}
        )
        assert request.status_code == 200


