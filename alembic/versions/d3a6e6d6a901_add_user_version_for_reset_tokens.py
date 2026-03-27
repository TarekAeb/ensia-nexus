"""add user version for reset tokens

Revision ID: d3a6e6d6a901
Revises: 48c1c110a756
Create Date: 2026-03-27 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d3a6e6d6a901"
down_revision = "48c1c110a756"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password_version", sa.Integer(), nullable=False, server_default="0"))


def downgrade() -> None:
    op.drop_column("users", "password_version")

