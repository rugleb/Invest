from http import HTTPStatus
from typing import Callable, NoReturn

from aiohttp.test_utils import TestClient
from aiohttp.web import Application, Request


async def test_default_error_handler_middleware(
        aiohttp_client: Callable,
        app: Application,
) -> None:
    url = "/error"

    async def handler(_: Request) -> NoReturn:
        raise RuntimeError("Something goes wrong")

    app.router.add_get(url, handler)

    client = await aiohttp_client(app)
    assert app.frozen

    response = await client.get(url)
    assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR

    assert await response.json() == {
        "message": "Internal server error",
    }


async def test_client_error_handler_middleware(
        client: TestClient,
) -> None:
    url = "/undefined"

    response = await client.get(url)
    assert response.status == HTTPStatus.NOT_FOUND

    assert await response.json() == {
        "message": "Not found",
    }
