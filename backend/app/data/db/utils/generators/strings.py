__all__ = [
    "generate_spot_token",
    "generate_provider_token",
    "generate_alias_name",
    "generate_invitation_code"
]

import random
from string import ascii_letters, digits, ascii_lowercase, ascii_uppercase

from app.config import get_settings

settings = get_settings()

TOKEN_ALPHABET = ascii_letters + digits
ALIAS_ALPHABET = ascii_lowercase + digits
CODE_ALPHABET = ascii_uppercase + digits


def generate_string(alphabet: str, length: int) -> str:
    return ''.join([random.choice(alphabet) for i in range(length)])


def generate_spot_token() -> str:
    return generate_string(
        alphabet=TOKEN_ALPHABET,
        length=settings.SPOT_TOKEN_SIZE
    )


def generate_provider_token() -> str:
    return generate_string(
        alphabet=TOKEN_ALPHABET,
        length=settings.PROVIDER_TOKEN_SIZE
    )


def generate_alias_name() -> str:
    return generate_string(
        alphabet=ALIAS_ALPHABET,
        length=settings.ALIAS_NAME_SIZE
    )


def generate_invitation_code() -> str:
    return generate_string(
        alphabet=CODE_ALPHABET,
        length=settings.INVITATION_CODE_SIZE
    )
