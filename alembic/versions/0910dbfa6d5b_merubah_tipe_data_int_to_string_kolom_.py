"""Merubah tipe data Int to String kolom image

Revision ID: 0910dbfa6d5b
Revises: 
Create Date: 2025-08-11 10:00:11.948401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0910dbfa6d5b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "products",
        "image",
        existing_type=sa.Integer(),
        type_=sa.String(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "products",
        "image",
        existing_type=sa.String(),
        type_=sa.Integer(),
        existing_nullable=False,
    )
