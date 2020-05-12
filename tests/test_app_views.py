from http import HTTPStatus

from aiohttp.test_utils import TestClient

from invest_api.utils import is_valid_uuid


class TestPingView:
    url = "/ping"

    async def test_that_route_is_named(self, client: TestClient) -> None:
        url = client.app.router["ping"].url_for()

        assert self.url == str(url)

    async def test_that_service_is_alive(self, client: TestClient) -> None:
        response = await client.get(self.url)
        assert response.status == HTTPStatus.OK

        assert await response.json() == {
            "data": {},
            "message": "pong",
        }

        request_id = response.headers.get("X-Request-ID")
        assert is_valid_uuid(request_id)
