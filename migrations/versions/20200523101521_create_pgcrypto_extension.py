"""Create pgcrypto extension.

Revision ID: 8029d353248e
Revises:
Create Date: 2020-05-23 10:15:21.412223

"""

from alembic import op

revision = "8029d353248e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
