import ssl

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

settings = get_settings()


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
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def dev_engine(self):
        self.engine = create_async_engine(get_settings().database_uri, echo=True, future=True)

    def prod_engine(self):
        my_ssl_ctx = ssl.create_default_context(cafile="PATH_TO_CRT")
        my_ssl_ctx.verify_mode = ssl.CERT_REQUIRED
        self.engine = create_async_engine(get_settings().database_uri,
                                          echo=True,
                                          future=True,
                                          connect_args={"ssl": my_ssl_ctx}
                                          )

    def refresh(self) -> None:
        if settings.is_dev:
            self.dev_engine()
        else:
            self.prod_engine()



async def get_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


__all__ = ["get_session", "SessionManager"]
