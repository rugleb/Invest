"""Create companies table.

Revision ID: 96ad09283de8
Revises: d6bc2eff5e21
Create Date: 2020-05-23 10:16:55.630632

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as pg

revision = "96ad09283de8"
down_revision = "d6bc2eff5e21"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        # Название таблицы
        "companies",

        # Уникальный идентификатор компании
        sa.Column("id", pg.BIGINT, primary_key=True),

        # ИНН компании, 10 цифр, уникальный по всей таблице
        sa.Column("itn", pg.TEXT, unique=True),
        sa.CheckConstraint(r"itn ~ '^[0-9]{10}$'"),

        # ОГРН компании, 13 цифр, уникальный по всей таблице
        sa.Column("psrn", pg.TEXT, unique=True),
        sa.CheckConstraint(r"psrn ~ '^[0-9]{13}$'"),

        # Название компании на русском языке
        sa.Column("name", pg.TEXT, nullable=False),

        # Размер компании, если неизвестно, то NULL
        sa.Column("size", pg.TEXT, nullable=False),
        sa.CheckConstraint("length(size) > 4"),

        # Номер региона страны предприятия, например: 05, 77 (2 цифры)
        sa.Column("region_code", pg.TEXT, nullable=False),
        sa.CheckConstraint(r"region_code ~ '^[0-9]{2}$'"),

        # Название региона страны предприятия
        sa.Column("region_name", pg.TEXT, nullable=False),
        sa.CheckConstraint("length(region_name) > 4"),

        # Код основного вида деятельности, если неизвестно, то NULL
        sa.Column("activity_code", pg.TEXT),
        sa.CheckConstraint(r"activity_code ~ '\d{1,2}(\.\d{1,2}){0,2}'"),

        # Название основного вида деятельности, если неизвестно, то NULL
        sa.Column("activity_name", pg.TEXT),
        sa.CheckConstraint("length(activity_name) > 4"),

        # Дата регистрации компании
        sa.Column("registered_at", pg.DATE, nullable=False),

        # Уставной капитал компании, больше 0
        sa.Column("charter_capital", pg.BIGINT, nullable=False),
        sa.CheckConstraint(sa.column("charter_capital") > 0),

        # Является ли действующей
        sa.Column("is_acting", pg.BOOLEAN, nullable=False),

        # Находится ли в стадии ликвидации
        sa.Column("is_liquidating", pg.BOOLEAN),

        # Не было финансового отчета за прошлый год
        sa.Column("not_reported_last_year", pg.BOOLEAN),

        # Отсутствует в реестре МСП
        sa.Column("not_in_sme_registry", pg.BOOLEAN),

        # Существует более 5 компаний с тем же управляющим
        sa.Column("ceo_has_other_companies", pg.BOOLEAN),

        # Риск быть в негативном списке
        sa.Column("negative_list_risk", pg.BOOLEAN),

        # вероятность банкротства
        sa.Column("bankruptcy_probability", pg.SMALLINT),
        sa.CheckConstraint(sa.column("bankruptcy_probability") >= 0),
        sa.CheckConstraint(sa.column("bankruptcy_probability") <= 100),

        # Значимость переменных для оценки вероятности
        sa.Column("bankruptcy_vars", pg.JSONB),

        # Достаточно ли данных для оценки
        sa.Column("is_enough_finance_data", pg.BOOLEAN),

        # Успешность относительно похожих компаний (целое от -9 до +9)
        sa.Column("relative_success", pg.SMALLINT),
        sa.CheckConstraint(sa.column("relative_success") >= -9),
        sa.CheckConstraint(sa.column("relative_success") <= +9),

        # Прогноз выручки за текущий год в тысячах рублей
        sa.Column("revenue_forecast", pg.BIGINT),
        sa.CheckConstraint(sa.column("revenue_forecast") > 0),

        # Оценка текущих активов в тысячах рублей
        sa.Column("assets_forecast", pg.BIGINT),
        sa.CheckConstraint(sa.column("assets_forecast") > 0),

        # Стадия развития компании
        sa.Column("dev_stage", pg.TEXT),

        # Значения для отрисовки графика с отображением линии тренда
        sa.Column("dev_stage_coordinates", pg.JSONB),

        sa.Index(
            "companies_itn_idx",
            "itn",
            postgresql_using="btree",
            postgresql_with={
                "fillfactor": 97,
            },
        ),

        sa.Index(
            "companies_psrn_idx",
            "psrn",
            postgresql_using="btree",
            postgresql_with={
                "fillfactor": 97,
            },
        ),

        sa.Index(
            "companies_name_idx",
            "name",
            postgresql_using="gist",
            postgresql_ops={
                "name": "gist_trgm_ops",
            },
            postgresql_with={
                "fillfactor": 97,
            },
        )
    )


def downgrade() -> None:
    op.drop_table("companies")
