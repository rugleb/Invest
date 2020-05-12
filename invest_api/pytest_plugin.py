# pylint: disable=W0621

import asyncio
import time
from contextlib import contextmanager
from typing import AsyncIterator, Dict, Iterator

import docker
import pytest
from aiohttp.test_utils import unused_port
from sqlalchemy import engine, exc, orm

from invest_api import create_tcp_server

pytest_plugins = [
    "aiohttp.pytest_plugin",
]

LOCALHOST = "127.0.0.1"

POSTGRES = "postgres"


@contextmanager
def postgres_server(config: Dict) -> Iterator:
    client = docker.from_env()

    container = client.containers.run(
        image="postgres:11-alpine",
        detach=True,
        environment={
            "POSTGRES_PASSWORD": config["password"],
            "POSTGRES_USER": config["user"],
            "POSTGRES_DB": config["database"],
        },
        ports={
            "5432/tcp": (config["host"], config["port"]),
        },
    )

    try:
        yield config
    finally:
        container.remove(force=True)
        client.close()


@contextmanager
def sqlalchemy_engine(config: Dict) -> Iterator:
    url_template = "postgresql://{user}:{password}@{host}:{port}/{database}"
    url = url_template.format_map(config)
    bind = engine.create_engine(url)
    try:
        yield bind
    finally:
        bind.dispose()


def establish_connection(bind: engine.Engine) -> engine.Engine:
    for _ in range(100):
        try:
            bind.connect()
            break
        except exc.OperationalError:
            time.sleep(0.05)
    return bind


@pytest.fixture(scope="session")
def db_engine() -> Iterator:
    port = unused_port()

    postgres_config = {
        "host": LOCALHOST,
        "port": port,
        "user": "postgres",
        "password": "postgres",
        "database": "postgres",
    }

    with postgres_server(postgres_config):
        with sqlalchemy_engine(postgres_config) as bind:
            yield establish_connection(bind)


@pytest.fixture
def db_session(db_engine: engine.Engine) -> Iterator:
    session_factory = orm.sessionmaker(db_engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
async def invest_api_server(
        loop: asyncio.AbstractEventLoop,
        db_session: orm.Session,
) -> AsyncIterator:
    assert loop.is_running()

    db_url = str(db_session.bind.url)

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
