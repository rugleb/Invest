from aiohttp import web
from marshmallow import ValidationError

from invest_api.types import Handler
from invest_api.utils import generate_request_id

from .context import REQUEST_ID
from .responses import error_response, server_error, validation_error

__all__ = ("add_middlewares", )


@web.middleware
async def request_id_handler(request: web.Request, handler: Handler):
    request_id = generate_request_id()
    token = REQUEST_ID.set(request_id)
    response = await handler(request)
    REQUEST_ID.reset(token)
    response.headers["X-Request-ID"] = request_id
    return response


@web.middleware
async def default_error_handler(request: web.Request, handler: Handler):
    try:
        return await handler(request)
    except Exception as e:  # pylint: disable=W0703
        name = e.__class__.__name__
        request.app.logger.error(f"Caught unhandled {name} exception: {e}")
        return server_error()


@web.middleware
async def client_error_handler(request: web.Request, handler: Handler):
    try:
        return await handler(request)
    except web.HTTPClientError as e:
        return error_response(e.status)


@web.middleware
async def validation_error_handler(request: web.Request, handler: Handler):
    try:
        return await handler(request)
    except ValidationError as e:
        errors = e.normalized_messages()
        return validation_error(errors)


def add_middlewares(app: web.Application) -> None:
    app.middlewares.append(request_id_handler)
    app.middlewares.append(default_error_handler)
    app.middlewares.append(client_error_handler)
    app.middlewares.append(validation_error_handler)
