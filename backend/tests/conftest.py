import asyncio
import random
from asyncio import get_event_loop_policy
from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.config.utils import get_settings
from app.data.db.connection import SessionManager
from app.src.app import app
from tests.utils import make_alembic_config

settings = get_settings()


@pytest.fixture(scope="function")
def postgres() -> str:
    # Create a temporary database name for testing
    tmp_name = uuid4().hex
    settings.POSTGRES_DB = tmp_name
    environ["POSTGRES_DB"] = tmp_name

    tmp_url = settings.database_uri_sync
    if not database_exists(tmp_url):
        create_database(tmp_url)
    try:
        yield settings.database_uri
    finally:
        drop_database(tmp_url)


def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    upgrade(cfg, "head")


async def run_async_upgrade(config: Config, engine_async):
    print("Starting upgrade")
    async with engine_async.begin() as conn:
        await conn.run_sync(run_upgrade, config)
    print("Upgrade completed")


@pytest.fixture
def alembic_config(postgres) -> Config:
    # Generate the Alembic config for the temporary database
    cmd_options = SimpleNamespace(config="", name="alembic", pg_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture(scope="function")
async def engine_async(postgres) -> AsyncEngine:
    # Create an async engine for database operations
    engine = create_async_engine(postgres, future=True)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function", autouse=True)
async def migrated_postgres(postgres, alembic_config: Config, engine_async):
    # Run migrations before the tests
    await run_async_upgrade(alembic_config, engine_async)
    yield


@pytest.fixture(scope="function")
async def client(manager: SessionManager = SessionManager()) -> AsyncClient:
    # Refresh the SessionManager to ensure the new database is used
    manager.refresh()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def session_factory_async(engine_async, ) -> sessionmaker:
    # Return a session factory using the async engine
    return sessionmaker(engine_async, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope='function')
async def session(session_factory_async) -> AsyncSession:
    # Provide a database session for tests
    async with session_factory_async() as session:
        yield session


@pytest.fixture
async def random_string() -> str:
    # Generate a random string using uuid4 for uniqueness
    return uuid4().hex


@pytest.fixture
async def root_header() -> dict:
    # Provide an authorization header for the root user
    return {"Authorization": f"Bearer {settings.ROOT_TOKEN}"}
