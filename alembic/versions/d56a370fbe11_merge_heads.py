"""merge heads

Revision ID: d56a370fbe11
Revises: bca3306ae21d, d3a6e6d6a901
Create Date: 2026-03-27 22:25:48.184852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd56a370fbe11'
down_revision: Union[str, None] = ('bca3306ae21d', 'd3a6e6d6a901')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
