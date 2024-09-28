__all__ = ["generate_vapid_keys", "SubscriptionKeys", "PushSubscription"]

import base64
from json import dumps
from typing import List, Optional

import ecdsa
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field
from pywebpush import webpush, WebPushException

from app.config import get_settings
from app.data.db.models import User

settings = get_settings()


class SubscriptionKeys(BaseModel):
    p256dh: str
    auth: str


class PushSubscription(BaseModel):
    endpoint: str
    expirationTime: Optional[int] = None
    keys: SubscriptionKeys


class Action(BaseModel):
    action: str = Field(..., description="The action identifier for the notification")
    title: str = Field(..., description="The title of the action button")


class NotificationData(BaseModel):
    offerId: str = Field(..., description="The ID of the offer")
    userId: str = Field(..., description="The ID of the user")


class PushNotification(BaseModel):
    title: str = Field(..., description="Title of the notification")
    body: str = Field(..., description="Body text of the notification")
    icon: Optional[str] = Field(None, description="URL of the icon for the notification")
    image: Optional[str] = Field(None, description="URL of the image for the notification")
    badge: Optional[str] = Field(None, description="URL of the badge for the notification")
    vibrate: Optional[List[int]] = Field(None, description="Vibration pattern for the notification")
    tag: Optional[str] = Field(None, description="Tag for the notification")
    actions: Optional[List[Action]] = Field(..., description="List of actions associated with the notification")
    data: Optional[NotificationData] = Field(..., description="Additional data related to the notification")
    url: Optional[str] = Field(None, description="URL associated with the notification")


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
    try:
        webpush(
            subscription_info=user.push_data,
            data=dumps(push_data.dict()),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims=settings.VAPID_CLAIMS
        )
    except WebPushException as ex:
        print("Error while send push notification: ", repr(ex))
        raise HTTPException(status_code=500, detail=str(ex))
