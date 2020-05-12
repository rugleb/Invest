from typing import Awaitable, Callable

from aiohttp import typedefs, web

__all__ = (
    "Handler",
    "Headers",
)

Handler = Callable[[web.Request], Awaitable[web.StreamResponse]]
Headers = typedefs.LooseHeaders
