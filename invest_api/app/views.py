import re

from aiohttp import hdrs, web

from .db import DB
from .models import CompanyQuerySchema, CompanySchema
from .responses import ok

__all__ = ("add_routes", )

ITN_FORMAT = re.compile(r"[0-9]{10}")

COMPANY_SCHEMA = CompanySchema()
COMPANY_QUERY_SCHEMA = CompanyQuerySchema()


def get_db(request: web.Request) -> DB:
    return request.app["db"]


async def ping_view(_) -> web.Response:
    return ok(message="pong")


async def health_view(request: web.Request) -> web.Response:
    await get_db(request).check_health()
    return ok()


async def companies_view(request: web.Request) -> web.Response:
    query = COMPANY_QUERY_SCHEMA.load(request.query)
    db = get_db(request)
    records = await db.get_companies_by_name(**query)
    companies = map(dict, records)
    data = COMPANY_SCHEMA.dump(companies, many=True)
    return ok(data)


async def company_view(request: web.Request) -> web.Response:
    identifier = request.match_info["id"]
    db = get_db(request)

    if ITN_FORMAT.fullmatch(identifier):
        company = await db.get_company_by_itn(identifier)
    else:
        company = await db.get_company_by_psrn(identifier)

    data = company.to_dict()
    return ok(data)


def add_routes(app: web.Application) -> None:
    app.router.add_route(hdrs.METH_ANY, "/ping", ping_view, name="ping")
    app.router.add_route(hdrs.METH_ANY, "/health", health_view, name="health")

    app.router.add_get("/companies", companies_view, name="companies")
    app.router.add_get("/companies/{id}", company_view, name="company")
