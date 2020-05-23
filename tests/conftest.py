# pylint: disable=W0621

from typing import Callable

import pytest
from aiohttp.abc import Application
from aiohttp.test_utils import TestClient
from sqlalchemy import orm

import invest_api

pytest_plugins = [
    "invest_api.pytest_plugin",
]


@pytest.fixture
async def app(invest_api_session: orm.Session) -> Application:
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

    return await invest_api.create_app(config)


@pytest.fixture
async def client(aiohttp_client: Callable, app: Application) -> TestClient:
    return await aiohttp_client(app)
