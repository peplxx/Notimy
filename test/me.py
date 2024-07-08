import requests
from notimy.config import config
from json import loads


def get_spot(token):
    return requests.get(
        url=f"{host}/spots/me",
        headers={"Authorization": f"Bearer {token}"}).text


host = "http://127.0.0.1:5000"
root_token = config.ROOT_TOKEN

result = loads(requests.get(
    url=f"{host}/me",
).text)

print("/me\t\t", result)


