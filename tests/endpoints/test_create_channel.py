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


class TestCreateChannel:
    @staticmethod
    def get_url():
        return f"{APP_HOST}:{APP_PORT}" + f"/channels/new"

    def test_success_channel_creation(self):
        provider = create_provider()
        provider_token = provider["token"]
        spot = create_spot(provider_token)
        spot_token = spot['token']
        request = requests.post(
            url=self.get_url(),
            json={"name": "Заказ кабачков"},
            headers={"Authorization": f"Bearer {spot_token}"}
        )
        assert request.status_code == 200
        channel = json.loads(request.text)
        spot = get_spot(spot_token)
        assert spot["channels"][0]['id'] == channel['id']

    def test_double_success_channel_creation(self):
        provider = create_provider()
        provider_token = provider["token"]
        spot = create_spot(provider_token)
        spot_token = spot['token']
        request = requests.post(
            url=self.get_url(),
            json={"name": "Заказ кабачков"},
            headers={"Authorization": f"Bearer {spot_token}"}
        )
        assert request.status_code == 200
        channel1 = json.loads(request.text)
        request = requests.post(
            url=self.get_url(),
            json={"name": "Заказ сандалей"},
            headers={"Authorization": f"Bearer {spot_token}"}
        )
        assert request.status_code == 200
        channel2 = json.loads(request.text)
        spot = get_spot(spot_token)
        assert channel1['id'] in [s["id"] for s in spot['channels']]
        assert channel2['id'] in [s["id"] for s in spot['channels']]

