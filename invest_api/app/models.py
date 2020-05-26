from typing import Dict

import sqlalchemy as sa
from marshmallow import Schema, fields
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

DATE_FORMAT = "%Y-%m-%d"

__all__ = (
    "Base",
    "Company",
)

Base: DeclarativeMeta = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = sa.Column(sa.BIGINT, primary_key=True)

    # Общая информация
    name = sa.Column(sa.TEXT, nullable=False)
    size = sa.Column(sa.TEXT, nullable=False)
    registered_at = sa.Column(sa.DATE, nullable=False)
    itn = sa.Column(sa.TEXT, unique=True)
    psrn = sa.Column(sa.TEXT, unique=True)
    region_code = sa.Column(sa.TEXT, nullable=False)
    region_name = sa.Column(sa.TEXT, nullable=False)
    activity_code = sa.Column(sa.TEXT)
    activity_name = sa.Column(sa.TEXT)
    charter_capital = sa.Column(sa.BIGINT)
    is_acting = sa.Column(sa.BOOLEAN, nullable=False)

    # Риск факторы
    is_liquidating = sa.Column(sa.BOOLEAN)
    not_reported_last_year = sa.Column(sa.BOOLEAN)
    not_in_sme_registry = sa.Column(sa.BOOLEAN)
    ceo_has_other_companies = sa.Column(sa.BOOLEAN)
    negative_list_risk = sa.Column(sa.BOOLEAN)

    # Банкротство
    bankruptcy_probability = sa.Column(sa.INT)
    bankruptcy_vars = sa.Column(sa.JSON(none_as_null=True))

    # Финансы
    is_enough_finance_data = sa.Column(sa.BOOLEAN)
    relative_success = sa.Column(sa.SMALLINT)
    revenue_forecast = sa.Column(sa.BIGINT)
    assets_forecast = sa.Column(sa.BIGINT)
    dev_stage = sa.Column(sa.TEXT)
    dev_stage_coordinates = sa.Column(sa.JSON(none_as_null=True))

    def to_dict(self) -> Dict:
        return CompanySchema().dump(self)


class CompanySchema(Schema):
    id = fields.Int(required=True)

    # Общая информация
    name = fields.Str(required=True)
    size = fields.Str(required=True)
    registered_at = fields.Date(required=True, format=DATE_FORMAT)
    itn = fields.Str(required=True)
    psrn = fields.Str(required=True)
    region_code = fields.Str(required=True)
    region_name = fields.Str(required=True)
    activity_code = fields.Str(required=True, allow_none=True)
    activity_name = fields.Str(required=True, allow_none=True)
    charter_capital = fields.Int(required=True, allow_none=True)
    is_acting = fields.Bool(required=True)

    # Риск факторы
    is_liquidating = fields.Bool(required=True, allow_none=True)
    not_reported_last_year = fields.Bool(required=True, allow_none=True)
    not_in_sme_registry = fields.Bool(required=True, allow_none=True)
    ceo_has_other_companies = fields.Bool(required=True, allow_none=True)
    negative_list_risk = fields.Bool(required=True, allow_none=True)

    # Банкротство
    bankruptcy_probability = fields.Int(required=True, allow_none=True)
    bankruptcy_vars = fields.Raw(required=True, allow_none=True)

    # Финансы
    is_enough_finance_data = fields.Bool(required=True, allow_none=True)
    relative_success = fields.Int(required=True, allow_none=True)
    revenue_forecast = fields.Int(required=True, allow_none=True)
    assets_forecast = fields.Int(required=True, allow_none=True)
    dev_stage = fields.Str(required=True, allow_none=True)
    dev_stage_coordinates = fields.Raw(required=True, allow_none=True)
