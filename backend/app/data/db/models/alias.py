from uuid import uuid4, UUID

import sqlalchemy as sa

from app.data.db import DeclarativeBase as Base
from app.data.db.models.mixins.index import IndexedObject
from app.data.db.utils.generators import generate_alias_name


class Alias(Base, IndexedObject):
    __tablename__ = 'aliases'
    base = sa.Column(sa.UUID, nullable=False, index=True)
    name = sa.Column(sa.Text, nullable=False, index=True)

    def __init__(self, base: UUID):
        super().__init__()
        self.base = base
        self.name = generate_alias_name()