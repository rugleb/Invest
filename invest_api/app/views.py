from aiohttp import hdrs, web

from .db import DB
from .responses import ok

__all__ = ("add_routes", )


def get_db(request: web.Request) -> DB:
    return request.app["db"]


async def ping_view(_) -> web.Response:
    return ok(message="pong")


async def health_view(request: web.Request) -> web.Response:
    await get_db(request).check_health()
    return ok()


def add_routes(app: web.Application) -> None:
    app.router.add_route(hdrs.METH_ANY, "/ping", ping_view, name="ping")
    app.router.add_route(hdrs.METH_ANY, "/health", health_view, name="health")
