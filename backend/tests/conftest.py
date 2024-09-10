from asyncio import get_event_loop_policy
from logging import getLogger
from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient, Cookies
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.config.utils import get_settings
from app.data.db.connection import SessionManager
from app.src.limiter import NoOpLimiter
from app.src.app import app
from tests.fixtures import *
from tests.utils import make_alembic_config

logger = getLogger('[pytest] conftest')
settings = get_settings()
get_settings().TESTING = True
limiter = NoOpLimiter()


def url(url):
    return settings.PATH_PREFIX + url

def auth(client: AsyncClient, entity):
    client.headers.update({"Authorization": f"Bearer {entity.token}"})
    return client


@pytest.fixture(scope="module")
def event_loop():
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres() -> str:
    tmp_name = uuid4().hex
    settings.POSTGRES_DB = tmp_name
    environ["POSTGRES_DB"] = tmp_name
    tmp_url = get_settings().database_uri_sync
    if not database_exists(tmp_url):
        create_database(tmp_url)
    try:
        yield get_settings().database_uri
    finally:
        drop_database(tmp_url)


def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    upgrade(cfg, "head")


async def run_async_upgrade(config: Config, engine_async):
    logger.debug("Starting upgrade")
    async with engine_async.begin() as conn:
        await conn.run_sync(run_upgrade, config)
    logger.debug("Upgrade completed")


@pytest.fixture(scope="session")
async def async_engine(postgres):
    cmd_options = SimpleNamespace(config="", name="alembic", pg_url=postgres, raiseerr=False, x=None)
    alembic_config = make_alembic_config(cmd_options)

    engine = create_async_engine(postgres, future=True, echo=True)
    await run_async_upgrade(alembic_config, engine)
    yield engine
    await engine.dispose()


@pytest.fixture(scope='session')
async def session(async_engine) -> AsyncSession:
    # Create a new session for each test function
    Session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
    session = Session()
    try:
        yield session
    finally:
        await session.close()


clients_params = {
    "app": app,
    "base_url": "http://test",
    "follow_redirects": True,
    "max_redirects": 3,
    "cookies": Cookies()
}

@pytest.fixture(scope="function")
async def client(async_engine, manager: SessionManager = SessionManager()) -> AsyncClient:
    manager.refresh()
    async with AsyncClient(**clients_params) as client:
        yield client



@pytest.fixture(scope="function")
async def root_client(async_engine, manager: SessionManager = SessionManager()) -> AsyncClient:
    manager.refresh()
    async with AsyncClient(**clients_params) as client:
        client.headers.update({'Authorization': f"Bearer {get_settings().ROOT_TOKEN}"})
        yield client

@pytest.fixture(scope="function")
async def provider_client(async_engine, provider_header: dict,
                          manager: SessionManager = SessionManager()) -> AsyncClient:
    manager.refresh()
    async with AsyncClient(**clients_params) as client:
        client.headers.update(provider_header)
        yield client

@pytest.fixture(scope="function")
async def spot_client(async_engine, spot_header: dict,
                      manager: SessionManager = SessionManager()) -> AsyncClient:
    manager.refresh()
    async with AsyncClient(**clients_params) as client:
        client.headers.update(spot_header)
        yield client
