# pylint: disable=W0621

from typing import Callable

import pytest
from aiohttp.abc import Application
from aiohttp.test_utils import TestClient

import invest_api

pytest_plugins = [
    "invest_api.pytest_plugin",
]


@pytest.fixture
async def app() -> Application:
    return await invest_api.create_app()


@pytest.fixture
async def client(aiohttp_client: Callable, app: Application) -> TestClient:
    return await aiohttp_client(app)
