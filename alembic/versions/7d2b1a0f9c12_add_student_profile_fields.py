"""add student profile fields

Revision ID: 7d2b1a0f9c12
Revises: 48c1c110a756
Create Date: 2026-03-27 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d2b1a0f9c12'
down_revision: Union[str, None] = '48c1c110a756'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('students', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('students', sa.Column('experience', sa.Text(), nullable=True))
    op.add_column('students', sa.Column('research_interests', sa.Text(), nullable=True))
    op.add_column('students', sa.Column('skills', sa.Text(), nullable=True))
    op.add_column('students', sa.Column('cv_url', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('students', 'cv_url')
    op.drop_column('students', 'skills')
    op.drop_column('students', 'research_interests')
    op.drop_column('students', 'experience')
    op.drop_column('students', 'bio')
