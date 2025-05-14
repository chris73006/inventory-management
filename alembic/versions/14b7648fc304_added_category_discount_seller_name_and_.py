"""Added category, discount, seller name, and contact to products

Revision ID: 14b7648fc304
Revises: d60090f3cc99
Create Date: 2025-05-11 20:22:23.350942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '14b7648fc304'
down_revision: Union[str, None] = 'd60090f3cc99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Add category, discount_percentage, seller_name, seller_contact."""
    # ✅ Add new columns instead of dropping the table!
    op.add_column('products', sa.Column('category', sa.String(255), nullable=False))
    op.add_column('products', sa.Column('discount_percentage', sa.Float, default=0.0))
    op.add_column('products', sa.Column('seller_name', sa.String(255), nullable=True))
    op.add_column('products', sa.Column('seller_contact', sa.String(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema: Remove newly added columns."""
    # ✅ Remove only the new columns instead of recreating the table!
    op.drop_column('products', 'category')
    op.drop_column('products', 'discount_percentage')
    op.drop_column('products', 'seller_name')
    op.drop_column('products', 'seller_contact')