"""create mytest table

Revision ID: 5c095bd30630
Revises: 67a056f586cb
Create Date: 2025-07-13 08:54:46.307153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c095bd30630'
down_revision: Union[str, None] = '67a056f586cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
