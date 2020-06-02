"""Create extensions.

Revision ID: d6bc2eff5e21
Revises: None
Create Date: 2020-06-02 11:09:54.449859

"""

from alembic import op

revision = "d6bc2eff5e21"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION pg_trgm")
    op.execute("CREATE EXTENSION pgcrypto")


def downgrade() -> None:
    op.execute("DROP EXTENSION pgcrypto")
    op.execute("DROP EXTENSION pg_trgm")
