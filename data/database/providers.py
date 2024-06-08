import datetime
import random

import sqlalchemy as sa

from .db_session import Base
from string import ascii_letters as TOKEN_ALPHABET


from ..config import PROVIDER_TOKEN_SIZE


def generate_token() -> str:
    return ''.join(
        [TOKEN_ALPHABET[random.randint(0, len(TOKEN_ALPHABET)) - 1] for _ in range(PROVIDER_TOKEN_SIZE)]
    )

class Provider(Base):
    __tablename__ = 'providers'

    id = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    token = sa.Column(sa.String, nullable=False, default=generate_token())
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    registered_at = sa.Column(sa.TIMESTAMP, nullable=False, default=datetime.datetime.now())
    last_channel = sa.Column(sa.Integer, default=-1, nullable=False)

    def __init__(
            self,
            name: str,
            description: str):
        self.name = name
        self.description = description