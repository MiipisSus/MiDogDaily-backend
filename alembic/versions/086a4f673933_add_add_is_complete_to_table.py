"""[Add] Add is_complete to  table

Revision ID: 086a4f673933
Revises: 6d71992d0740
Create Date: 2025-05-20 05:59:34.283229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '086a4f673933'
down_revision: Union[str, None] = '6d71992d0740'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
