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


async def company_view(request: web.Request) -> web.Response:
    itn = request.match_info["itn"]
    db = get_db(request)

    company = await db.get_company_by_itn(itn)
    data = company.to_dict()

    return ok(data)


def add_routes(app: web.Application) -> None:
    app.router.add_route(hdrs.METH_ANY, "/ping", ping_view, name="ping")
    app.router.add_route(hdrs.METH_ANY, "/health", health_view, name="health")

    app.router.add_get("/companies/{itn}", company_view, name="company")
