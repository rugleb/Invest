# pylint: disable=W0621

import asyncio
import time
from contextlib import contextmanager
from os import path
from typing import AsyncIterator, Iterator

import attr
import docker
import pytest
import sqlalchemy as sa
from aiohttp.test_utils import unused_port
from alembic import command as alembic_command
from alembic import config as alembic_config
from sqlalchemy import engine, exc, orm

from invest_api import create_tcp_server

pytest_plugins = [
    "aiohttp.pytest_plugin",
]

LOCALHOST = "127.0.0.1"

HERE = path.dirname(__file__)
ROOT = path.dirname(HERE)

ALEMBIC_INI = path.join(ROOT, "alembic.ini")


@attr.s(slots=True, frozen=True)
class PostgresConfig:
    host: str = attr.ib(default=LOCALHOST)
    port: int = attr.ib(factory=unused_port)
    username: str = attr.ib(default="postgres")
    password: str = attr.ib(default="postgres")
    database: str = attr.ib(default="postgres")

    def url(self) -> str:
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.username,
            self.password,
            self.host,
            self.port,
            self.database,
        )


@contextmanager
def postgres_server_context(config: PostgresConfig) -> Iterator:
    client = docker.from_env()

    container = client.containers.run(
        image="postgres:11-alpine",
        detach=True,
        environment={
            "POSTGRES_PASSWORD": config.password,
            "POSTGRES_USER": config.username,
            "POSTGRES_DB": config.database,
        },
        ports={
            "5432/tcp": (config.host, config.port),
        },
    )

    try:
        yield config.url()
    finally:
        container.remove(force=True)
        client.close()


def establish_connection(bind: engine.Engine) -> engine.Engine:
    for _ in range(100):
        try:
            bind.connect()
            break
        except exc.OperationalError:
            time.sleep(0.05)
    return bind


@contextmanager
def sqlalchemy_bind_context(url: str) -> Iterator:
    bind = sa.engine.create_engine(url)
    try:
        yield establish_connection(bind)
    finally:
        bind.dispose()


@contextmanager
def sqlalchemy_session_context(bind: sa.engine.Engine) -> Iterator:
    session_factory = orm.sessionmaker(bind)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session")
def postgres_server() -> Iterator:
    config = PostgresConfig()
    with postgres_server_context(config) as url:
        yield url


@contextmanager
def migrations_context(alembic_ini_path: str, db_url: str) -> Iterator:
    cfg = alembic_config.Config(alembic_ini_path)
    cfg.set_main_option("url", db_url)

    alembic_command.upgrade(cfg, "head")
    try:
        yield
    finally:
        alembic_command.downgrade(cfg, "base")


@pytest.fixture
def invest_api_bind(postgres_server: str) -> Iterator:
    with sqlalchemy_bind_context(postgres_server) as bind:
        yield bind


@pytest.fixture
def invest_api_session(invest_api_bind: sa.engine.Engine) -> Iterator:
    db_url = str(invest_api_bind.url)
    with migrations_context(ALEMBIC_INI, db_url):
        with sqlalchemy_session_context(invest_api_bind) as session:
            yield session


@pytest.fixture
async def invest_api_server(
        loop: asyncio.AbstractEventLoop,
        invest_api_session: orm.Session,
) -> AsyncIterator:
    assert loop.is_running()

    db_url = str(invest_api_session.bind.url)

    config = {
        "db": {
            "pool": {
                "dsn": db_url,
                "min_size": 1,
                "max_size": 5,
            },
            "logger": {
                "name": "db",
            },
        },
    }

    host = LOCALHOST
    port = unused_port()

    async with create_tcp_server(host, port, config) as url:
        yield url
