__all__ = ["generate_vapid_keys", "SubscriptionKeys", "PushSubscription", "send_notification"]

import base64
from json import dumps
from typing import Optional

import ecdsa
from fastapi import HTTPException
from pydantic import BaseModel
from pywebpush import webpush, WebPushException

from app.config import get_settings
from app.data.db.models import User
from app.src.common.push_notifications.dto import PushNotification

settings = get_settings()


class SubscriptionKeys(BaseModel):
    p256dh: str
    auth: str


class PushSubscription(BaseModel):
    endpoint: str
    expirationTime: Optional[int] = None
    keys: SubscriptionKeys



def generate_vapid_keypair():
    """
  Generate a new set of encoded key-pair for VAPID
  """
    pk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
    vk = pk.get_verifying_key()

    return {
        'private_key': base64.urlsafe_b64encode(pk.to_string()).strip(b"="),
        'public_key': base64.urlsafe_b64encode(b"\x04" + vk.to_string()).strip(b"=")
    }


def generate_vapid_keys():
    settings = get_settings()

    if settings.VAPID_PUBLIC_KEY and settings.VAPID_PRIVATE_KEY:
        return

    vapid_keys = generate_vapid_keypair()

    public_key = vapid_keys["public_key"]
    private_key = vapid_keys["private_key"]

    settings.VAPID_PUBLIC_KEY = public_key
    settings.VAPID_PRIVATE_KEY = private_key

    print(f"VAPID_PUBLIC_KEY={str(public_key)}\nVAPID_PRIVATE_KEY={str(private_key)}\n")


async def send_notification(user: User, push_data: PushNotification):
    if not user.can_get_push:
        return
    try:

        webpush(
            subscription_info=user.push_data,
            data=dumps(push_data.dict()),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:notimy_oficial@gmail.com", "aud": user.push_data['endpoint']},
            # vapid_claims=settings.vapid_claims(firefox="mozilla" in user.push_data['endpoint'],
            #                                    apple='apple' in user.push_data['endpoint']),
        )
    except WebPushException as ex:
        print("Error while send push notification: ", repr(ex))
        raise HTTPException(status_code=500, detail=str(ex))
