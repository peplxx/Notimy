import ssl
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings
from threading import Lock

settings = get_settings()


class SessionManager:
    _instance = None

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        if not hasattr(self, 'session_maker'):
            self.session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        return self.session_maker

    def dev_engine(self):
        self.engine = create_async_engine(
            settings.database_uri,
            echo=settings.is_dev,  # Control echo with settings
            future=True
        )

    def prod_engine(self):
        my_ssl_ctx = ssl.create_default_context(cafile=settings.ssl_cert_path)
        my_ssl_ctx.verify_mode = ssl.CERT_REQUIRED
        self.engine = create_async_engine(
            settings.database_uri,
            echo=False,
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
