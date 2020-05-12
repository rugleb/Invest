from contextlib import asynccontextmanager
from typing import AsyncIterator, Callable

import pytest
from aiohttp.test_utils import unused_port

from invest_api import create_tcp_server

pytest_plugins = [
    "aiohttp.pytest_plugin",
]

LOCALHOST = "127.0.0.1"


@pytest.fixture
def invest_api_server_factory() -> Callable:
    host = LOCALHOST
    port = unused_port()

    @asynccontextmanager
    async def server_factory() -> AsyncIterator:
        async with create_tcp_server(host, port) as url:
            yield url

    return server_factory
