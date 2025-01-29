"""Add new column to users

Revision ID: 71726c62413d
Revises: a5b94caf64b7
Create Date: 2025-01-28 16:18:16.602648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71726c62413d'
down_revision: Union[str, None] = 'a5b94caf64b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('number', sa.Integer(), nullable=True))
    pass


