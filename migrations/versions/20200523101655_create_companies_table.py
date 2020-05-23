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
    server_uuid = sa.text("gen_random_uuid()")

    op.create_table(
        # Название таблицы
        "companies",

        # Уникальный идентификатор компании
        sa.Column("id", pg.UUID, server_default=server_uuid),

        # Название компании на русском языке
        sa.Column("name", pg.TEXT, unique=True),

        # Номер региона страны, например: 05, 77 (2 цифры)
        sa.Column("region", pg.TEXT),

        # Дата регистрации компании
        sa.Column("registered_at", pg.DATE),

        # Уставной капитал компании
        sa.Column("authorized_capital", pg.SMALLINT),

        # ИНН компании, 10-12 цифр, уникальный по всей таблице
        sa.Column("ITN", pg.TEXT, unique=True),

        # ОГРН компании, 13 цифр, уникальный по всей таблице
        sa.Column("PSRN", pg.TEXT, unique=True),

        # Категория предприятия, например: микропредприятие
        sa.Column("category", pg.TEXT),

        # Вероятность банкротства компаннии, диапазон: [0, 100]
        sa.Column("bankruptcy_probability", pg.SMALLINT),

        # Вероятность попадания в негативный лист, диапазон: [0, 100]
        sa.Column("negative_list_probability", pg.SMALLINT),

        # Количество замороженных счетов: 0 и боллее
        sa.Column("frozen_accounts_number", pg.SMALLINT),

        # Находится ли компания в процессе ликвидации
        sa.Column("in_liquidation_process", pg.BOOLEAN),

        # Количество открытых исполнительных производств компании: 0 и более
        sa.Column("open_enforcement_proceedings_number", pg.SMALLINT),

        # Число компаний с тем же управляющим, 0 и более
        sa.Column("same_manager_companies_number", pg.SMALLINT),

        # Отношение долга к выручке: например: 3,6
        sa.Column("debt_revenue_ratio", pg.FLOAT),

        # Успешность относительно похожих компаний, диапазон: [0, 5]
        sa.Column("relative_success", pg.SMALLINT),

        # Прогноз выручки компании в тысячах рублей
        sa.Column("revenue_forecast", pg.SMALLINT),

        # Оценка текущих активов в тысячах рублей
        sa.Column("asset_valuation", pg.SMALLINT),

        # Стадия развития компании, диапазон: [0, 5]
        sa.Column("development_stage", pg.SMALLINT),

        # Уникальный идентификатор таблицы, ПК
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("companies")
