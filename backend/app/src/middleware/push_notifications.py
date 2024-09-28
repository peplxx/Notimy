__all__ = ["generate_vapid_keys", ]

import base64

import ecdsa

from app.config import get_settings
from logging import getLogger
logger = getLogger(__name__)

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
