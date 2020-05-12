from http import HTTPStatus

import aiohttp
from yarl import URL

from invest_api.utils import is_valid_uuid


async def test_invest_api_server_fixture(invest_api_server: URL) -> None:
    url = invest_api_server.with_path("health")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == HTTPStatus.OK

            assert await response.json() == {
                "data": {},
                "message": "OK",
            }

            request_id = response.headers.get("X-Request-ID")
            assert is_valid_uuid(request_id)
