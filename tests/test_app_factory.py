import asyncio
from http import HTTPStatus
from unittest.mock import patch

import aiohttp
from aiohttp.test_utils import TestClient
from yarl import URL

from invest_api.log import app_logger
from invest_api.utils import is_valid_uuid


async def test_invest_api_server_fixture(invest_api_server: URL) -> None:
    url = invest_api_server.with_path("health")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == HTTPStatus.OK

            assert await response.json() == {
                "data": None,
                "message": "OK",
            }

            request_id = response.headers.get("X-Request-ID")
            assert is_valid_uuid(request_id)


async def test_asyncio_error_handler(
        client: TestClient,
        loop: asyncio.AbstractEventLoop,
) -> None:
    assert client.app.frozen

    context = {
        "message": "Error message",
    }

    with patch.object(app_logger, "warning") as warning:
        loop.call_exception_handler(context)

    message = "Caught asyncio exception: {message}".format_map(context)
    warning.assert_called_with(message)
