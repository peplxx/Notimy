import json

import pytest
from frontend.__main__ import app  # Adjust the import to match your application entry point
from asyncio import get_event_loop_policy
from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from backend.tests import make_alembic_config

from frontend.__main__ import get_app
from frontend.config.default import DefaultSettings
from frontend.data.db.connection import SessionManager
from sqlalchemy import create_engine

# Define fixtures
@pytest.fixture
async def client(migrated_postgres, manager: SessionManager = SessionManager()) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    yield AsyncClient(app=app, base_url="http://test" + DefaultSettings().PATH_PREFIX)


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def postgres() -> str:
    """
    Создает временную БД для запуска теста.
    """
    settings = DefaultSettings()

    tmp_name = ".".join([uuid4().hex, "pytest"])
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


async def run_upgrade(config: Config, database_uri: str):
    async_engine = create_engine(database_uri, echo=True)
    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, config)


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(config="/", name="alembic", pg_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
def alembic_engine():
    """
    Override this fixture to provide pytest-alembic powered tests with a database handle.
    """
    settings = DefaultSettings()
    return create_async_engine(settings.database_uri_sync, echo=True)


@pytest.fixture
async def migrated_postgres(postgres, alembic_config: Config):
    """
    Проводит миграции.
    """
    await run_upgrade(alembic_config, postgres)


@pytest.fixture
def engine_async(postgres):
    engine = create_async_engine(postgres, future=True)
    return engine


@pytest.fixture
def session_factory_async(engine) -> sessionmaker:
    return sessionmaker(engine, class_=Session, expire_on_commit=False)


@pytest.fixture
async def session(session_factory_async) -> Session:
    return session_factory_async()

