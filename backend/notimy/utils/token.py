from random import randint
from string import ascii_letters, digits

from frontend.config import config

TOKEN_ALPHABET = ascii_letters + digits


def generate_token(length: int) -> str:
    return ''.join(
        [TOKEN_ALPHABET[randint(0, len(TOKEN_ALPHABET)) - 1] for _ in range(length)]
    )


def generate_spot_token(length: int = config.SPOT_TOKEN_SIZE) -> str:
    return ''.join(
        [TOKEN_ALPHABET[randint(0, len(TOKEN_ALPHABET)) - 1] for _ in range(length)]
    )


def generate_provider_token(length: int = config.PROVIDER_TOKEN_SIZE) -> str:
    return ''.join(
        [TOKEN_ALPHABET[randint(0, len(TOKEN_ALPHABET)) - 1] for _ in range(length)]
    )
