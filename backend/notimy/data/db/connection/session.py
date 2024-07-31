from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from notimy.config import config


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=Session, expire_on_commit=False)

    def refresh(self) -> None:
        # self.engine = create_async_engine(config.database_uri_sync, echo=True, future=True)
        self.engine = create_engine(config.database_uri_sync, echo=True)


def get_session() -> Session:
    session_maker = SessionManager().get_session_maker()
    with session_maker() as session:
        return session


__all__ = [
    "get_session",
]
