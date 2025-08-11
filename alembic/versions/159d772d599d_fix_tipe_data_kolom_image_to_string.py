"""Fix: Tipe data kolom Image to String

Revision ID: 159d772d599d
Revises: 0910dbfa6d5b
Create Date: 2025-08-11 11:48:26.276925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '159d772d599d'
down_revision: Union[str, Sequence[str], None] = '0910dbfa6d5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "products",
        "image",
        existing_type=sa.INT,
        type_=sa.String,
        existing_nullable=True,
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "products",
        "image",
        existing_type=sa.String,
        type_=sa.INT,
        existing_nullable=True,
    )
