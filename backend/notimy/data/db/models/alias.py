import random
from datetime import datetime, timezone
from uuid import uuid4, UUID

import sqlalchemy as sa

from notimy.data.db import DeclarativeBase as Base
from notimy.utils import generate_provider_token

now = datetime.now(tz=timezone.utc)

from string import ascii_lowercase, digits

ALIAS_ALPHABET = ascii_lowercase + digits
ALIAS_NAME_LENGTH = 10


def generate_name() -> str:
    return ''.join([random.choice(ALIAS_ALPHABET) for _ in range(ALIAS_NAME_LENGTH)])


class Alias(Base):
    __tablename__ = 'aliases'
    id = sa.Column(sa.UUID, nullable=False, primary_key=True, default=uuid4)
    base = sa.Column(sa.UUID, nullable=False, index=True)
    name = sa.Column(sa.Text, nullable=False, index=True)

    def __init__(self, base: UUID):
        super().__init__()
        self.base = base
        self.name = generate_name()

    def dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
