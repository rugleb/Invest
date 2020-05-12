from aiohttp import hdrs, web

from .responses import ok

__all__ = ("add_routes", )


async def ping_view(_: web.Request) -> web.Response:
    return ok(message="pong")


def add_routes(app: web.Application) -> None:
    app.router.add_route(hdrs.METH_ANY, "/ping", ping_view, name="ping")
