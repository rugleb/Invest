import logging
from typing import Dict

from async_lru import alru_cache
from asyncpg.pool import Pool, create_pool
from marshmallow import Schema, fields, post_load

from .exceptions import CompanyNotFound
from .models import Company, CompanySelection

__all__ = (
    "DB",
    "DBSchema",
)

CACHED = alru_cache(maxsize=512, cache_exceptions=False)


class DB:
    __slots__ = ("_pool", "_logger")

    def __init__(self, pool: Pool, logger: logging.Logger):
        self._pool = pool
        self._logger = logger

    async def setup(self) -> None:
        await self._pool

    async def cleanup(self) -> None:
        await self._pool.close()

    async def check_health(self) -> bool:
        return await self._pool.fetchval("select $1::bool", True)

    @CACHED
    async def get_company_by_itn(self, itn: str) -> Company:
        query = "SELECT * FROM companies WHERE itn = $1::TEXT LIMIT 1;"
        record = await self._pool.fetchrow(query, itn)
        if record is None:
            raise CompanyNotFound()
        return Company(**record)

    @CACHED
    async def get_company_by_psrn(self, psrn: str) -> Company:
        query = "SELECT * FROM companies WHERE psrn = $1::TEXT LIMIT 1;"
        record = await self._pool.fetchrow(query, psrn)
        if record is None:
            raise CompanyNotFound()
        return Company(**record)

    @CACHED
    async def get_companies_by_name(
            self,
            name: str,
            limit: int = 5,
    ) -> list:
        query = """
            SELECT
                *
                , companies.name <-> $1::TEXT AS distance
            FROM companies
            ORDER BY distance
            LIMIT $2::SMALLINT
            ;
        """

        return await self._pool.fetch(query, name, limit)

    @CACHED
    async def select_company(self, params: CompanySelection) -> list:
        query = """
            SELECT * FROM companies WHERE
                size = $1::TEXT
                AND region_code = any($2::TEXT[])
                AND is_acting = $3::BOOL
                AND bankruptcy_probability <= $4::SMALLINT
                AND is_liquidating = $5::BOOL
                AND not_reported_last_year = $6::BOOL
                AND not_in_same_registry = $7::BOOL
                AND ceo_has_other_companies = $8::BOOL
                AND negative_list_risk = $9::BOOL
            ORDER BY
                bankruptcy_probability
            LIMIT $10::SMALLINT
            OFFSET $11::SMALLINT
            ;
        """

        return await self._pool.fetch(
            query,
            params.size,
            params.region_codes.split(","),
            params.is_acting,
            params.bankruptcy_probability,
            params.is_liquidating,
            params.not_reported_last_year,
            params.not_in_same_registry,
            params.ceo_has_other_companies,
            params.negative_list_risk,
            params.limit,
            params.offset
        )

    async def get_regions(self) -> list:
        query = """
            SELECT
                DISTINCT region_code, region_name
            FROM
                companies
            ORDER BY
                region_code
            ;
        """

        return await self._pool.fetch(query)

    @classmethod
    def from_dict(cls, data: Dict) -> "DB":
        return DBSchema().load(data)


class AsyncPGPoolSchema(Schema):
    dsn = fields.Str(required=True)
    min_size = fields.Int(missing=0)
    max_size = fields.Int(missing=10)
    max_queries = fields.Int(missing=1000)
    max_inactive_connection_lifetime = fields.Float(missing=3600)
    timeout = fields.Float(missing=10)
    command_timeout = fields.Float(missing=10)
    statement_cache_size = fields.Int(missing=1024)
    max_cached_statement_lifetime = fields.Int(missing=3600)

    @post_load
    def make_pool(self, data: Dict, **kwargs) -> Pool:
        return create_pool(**data)


class LoggerSchema(Schema):
    name = fields.Str(required=True)

    @post_load
    def make_logger(self, data: Dict, **kwargs) -> logging.Logger:
        return logging.getLogger(**data)


class DBSchema(Schema):
    pool = fields.Nested(AsyncPGPoolSchema, required=True)
    logger = fields.Nested(LoggerSchema, required=True)

    @post_load
    def make_db(self, data: Dict, **kwargs) -> DB:
        return DB(**data)
