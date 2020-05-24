"""Create companies table.

Revision ID: 96ad09283de8
Revises: 8029d353248e
Create Date: 2020-05-23 10:16:55.630632

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as pg

revision = "96ad09283de8"
down_revision = "8029d353248e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        # Название таблицы
        "companies",

        # Уникальный идентификатор компании
        sa.Column("id", pg.BIGINT, primary_key=True),

        # ИНН компании, 10-12 цифр, уникальный по всей таблице
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
        sa.Column("activity_code", pg.TEXT, nullable=True),
        sa.CheckConstraint(r"activity_code ~ '\d{1,2}(\.\d{1,2}){0,2}'"),

        # Название основного вида деятельности, если неизвестно, то NULL
        sa.Column("activity_name", pg.TEXT, nullable=True),
        sa.CheckConstraint("length(activity_name) > 4"),

        # Дата регистрации компании
        sa.Column("registered_at", pg.DATE, nullable=False),

        # Уставной капитал компании, 0 и более
        sa.Column("charter_capital", pg.BIGINT, nullable=False),
        sa.CheckConstraint(sa.column("charter_capital") > 0),

        # Является ли действующей
        sa.Column("is_acting", pg.BOOLEAN, nullable=False),

        # Находится ли в стадии ликвидации
        sa.Column("is_liquidating", pg.BOOLEAN, nullable=False),

        # Не было финансового отчета за прошлый год
        sa.Column("no_finance_report_last_year", pg.BOOLEAN, nullable=False),

        # Отсутствует в реестре МСП
        sa.Column("not_in_sme_registry", pg.BOOLEAN, nullable=False),

        # Существует более 5 компаний с тем же управляющим
        sa.Column("more_than_5_companies_with_same_manager", pg.BOOLEAN),

        # Риск быть в негативном списке
        sa.Column("negative_list_risk", pg.BOOLEAN, nullable=False),

        # вероятность банкротства
        sa.Column("bankruptcy_probability", pg.SMALLINT, nullable=False),
        sa.CheckConstraint(sa.column("bankruptcy_probability") >= 0),
        sa.CheckConstraint(sa.column("bankruptcy_probability") <= 100),

        # Значимость переменных для оценки вероятности
        sa.Column("bankruptcy_vars", pg.JSONB, nullable=False),

        # Достаточно ли данных для оценки
        sa.Column("is_enough_finance_data", pg.BOOLEAN, nullable=False),

        # Успешность относительно похожих компаний (целое от -9 до +9)
        sa.Column("relative_success", pg.SMALLINT, nullable=True),
        sa.CheckConstraint(sa.column("relative_success") >= -9),
        sa.CheckConstraint(sa.column("relative_success") <= +9),

        # Прогноз выручки за текущий год в тысячах рублей
        sa.Column("revenue_forecast", pg.BIGINT, nullable=True),
        sa.CheckConstraint(sa.column("revenue_forecast") > 0),

        # Оценка текущих активов в тысячах рублей
        sa.Column("assets_forecast", pg.BIGINT, nullable=True),
        sa.CheckConstraint(sa.column("assets_forecast") > 0),

        # Стадия развития компании
        sa.Column("development_stage", pg.TEXT, nullable=True),

        # Значения для отрисовки графика с отображением линии тренда
        sa.Column("development_stage_coordinates", pg.JSONB, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("companies")
