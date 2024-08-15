from datetime import datetime, timezone
from uuid import uuid4, UUID

import sqlalchemy as sa

from app.config import constants
from app.data.db import DeclarativeBase as Base

from app.data.db.utils.generators import generate_provider_token

now = datetime.now(tz=timezone.utc).replace(tzinfo=None)


class Provider(Base):
    __tablename__ = 'providers'

    id = sa.Column(sa.UUID, nullable=False, primary_key=True, default=uuid4)
    token = sa.Column(sa.String, index=True, nullable=False, default=generate_provider_token)

    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)

    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=now)
    spots = sa.Column(sa.Integer, nullable=False, default=0)
    max_spots = sa.Column(sa.Integer, nullable=False, default=1)
    account = sa.Column(sa.UUID)

    def __init__(
            self,
            name: str,
            account: UUID,
            description: str = None,
    ):
        super().__init__()
        self.name = name
        self.description = description if description else constants.NO_DESCRIPTION
        self.account = account

    @property
    def service_user_data(self):
        return {
            "token": self.token,
            "entity": self.id
        }