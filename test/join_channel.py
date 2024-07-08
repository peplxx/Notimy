import requests
from notimy.config import config
from json import loads


def get_spot(token):
    return requests.get(
        url=f"{host}/spots/me",
        headers={"Authorization": f"Bearer {token}"}).text


host = "http://127.0.0.1:5000"
root_token = config.ROOT_TOKEN

provider_data = loads(requests.post(
    url=f"{host}/providers/new",
    headers={"Authorization": f"Bearer {root_token}"},
    json={
        "name": "test-1",
        "description": "test-purpose provider"
    }
).text)

provider_token = provider_data['token']
print("Create new provider:", provider_token)

spot_data = loads(requests.post(
    url=host+"/providers/new_spot",
    headers={"Authorization": f"Bearer {provider_token}"},
    json={

    }
).text)
spot_token = spot_data['token']

print("Create new spot:", spot_token)


channel_data = requests.post(
    url=host+"/channels/new",
    headers={"Authorization": f"Bearer {spot_token}"},
    json={
        "name": "Заказ сандалей"
    }
)

print(channel_data.text)

print(get_spot(spot_token))

print(spot_data['id'])

join_channel = requests.post(
    url=host+f"/spot/{spot_data["id"]}"
)

print(join_channel.text)


result = requests.get(
    cookies=join_channel.cookies,
    url=f"{host}/me",
).text

print("/me\t\t", result)

