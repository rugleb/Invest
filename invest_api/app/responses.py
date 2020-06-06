from http import HTTPStatus
from typing import Any, Dict

import orjson
from aiohttp import hdrs, web

from invest_api.types import Headers

__all__ = (
    "create_response",
    "error_response",
    "ok",
    "validation_error",
    "server_error",
)

HEADERS: Headers = {
    hdrs.SERVER: "Invest API v0.0.1",
    hdrs.CACHE_CONTROL: "no-cache, no-store",
    hdrs.EXPIRES: "0",
    hdrs.PRAGMA: "no-cache",
    hdrs.ACCESS_CONTROL_ALLOW_ORIGIN: "*",
}


def create_response(content: Dict, status: int) -> web.Response:
    body = orjson.dumps(content)

    return web.json_response(
        body=body,
        status=status,
        headers=HEADERS,
    )


def error_response(status: int, message: str = None) -> web.Response:
    http_status = HTTPStatus(status)

    if not message:
        message = http_status.phrase

    content = {
        "message": message.capitalize(),
    }
    return create_response(content, status)


def ok(data: Any = None, message: str = None) -> web.Response:  # 200
    content = {
        "data": data,
        "message": message or "OK",
    }
    return create_response(content, HTTPStatus.OK)


def validation_error(errors: Any) -> web.Response:  # 422
    message = "Input payload validation failed"

    content = {
        "errors": errors,
        "message": message,
    }

    return create_response(content, HTTPStatus.UNPROCESSABLE_ENTITY)


def server_error() -> web.Response:  # 500
    return error_response(HTTPStatus.INTERNAL_SERVER_ERROR)
