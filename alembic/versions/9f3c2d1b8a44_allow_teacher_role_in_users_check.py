"""allow teacher role in users check

Revision ID: 9f3c2d1b8a44
Revises: 0e61a3c2a7f1
Create Date: 2026-03-27 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '9f3c2d1b8a44'
down_revision: Union[str, None] = '0e61a3c2a7f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('users_role_check', 'users', type_='check')
    op.create_check_constraint(
        'users_role_check',
        'users',
        "role IN ('STUDENT','TEACHER','ADMIN','PARTNER','MCA','PROFESSOR','DOCTOR','RESEARCHER')",
    )


def downgrade() -> None:
    op.drop_constraint('users_role_check', 'users', type_='check')
    op.create_check_constraint(
        'users_role_check',
        'users',
        "role IN ('STUDENT','MCA','PROFESSOR','DOCTOR','ADMIN','RESEARCHER')",
    )
