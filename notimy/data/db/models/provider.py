from datetime import timezone, datetime
from uuid import uuid4

import sqlalchemy as sa

from notimy.data.db import DeclarativeBase as Base
from notimy.utils import generate_provider_token

now = datetime.now(tz=timezone.utc)

class Provider(Base):
    __tablename__ = 'providers'
    id = sa.Column(sa.UUID, nullable=False, primary_key=True, default=uuid4)
    token = sa.Column(sa.String, index=True, nullable=False, default=generate_provider_token)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    registered_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    last_channel = sa.Column(sa.Integer, default=-1, nullable=False)
    spots = sa.Column(sa.Integer, nullable=False, default=0)
    max_spots = sa.Column(sa.Integer, nullable=False, default=1)

    def __init__(
            self,
            name: str,
            description: str = None):
        self.name = name
        self.description = description if description else "NO_DESCRIPTION"

    def dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
