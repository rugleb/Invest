from http import HTTPStatus
from typing import Callable

import aiohttp

from invest_api.utils import is_valid_uuid


async def test_invest_api_server_factory_fixture(
        invest_api_server_factory: Callable,
) -> None:
    async with invest_api_server_factory() as base_url:
        url = base_url.with_path("ping")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == HTTPStatus.OK

                assert await response.json() == {
                    "data": {},
                    "message": "pong",
                }

                request_id = response.headers.get("X-Request-ID")
                assert is_valid_uuid(request_id)
