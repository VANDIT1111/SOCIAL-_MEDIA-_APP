"""Description of the revision

Revision ID: e6e1dca39b3a
Revises: 
Create Date: 2025-01-28 16:03:24.477379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6e1dca39b3a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('phonenumber', sa.Integer))
    pass


def downgrade() -> None:
    pass
