from aiohttp import web

__all__ = ("CompanyNotFound", )


class CompanyNotFound(web.HTTPNotFound):
    pass
