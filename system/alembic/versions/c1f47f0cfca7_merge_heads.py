"""Merge heads

Revision ID: c1f47f0cfca7
Revises: 1a2b3c4d5e6f, 2024_01_threat_schema_update
Create Date: 2025-03-15 11:48:43.875535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1f47f0cfca7'
down_revision: Union[str, None] = ('1a2b3c4d5e6f', '2024_01_threat_schema_update')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
