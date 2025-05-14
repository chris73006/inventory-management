"""Updated models.py to include new columns

Revision ID: a990caeabea2
Revises: 14b7648fc304
Create Date: 2025-05-11 20:30:08.291707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a990caeabea2'
down_revision: Union[str, None] = '14b7648fc304'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Add new columns without dropping the table."""
    op.add_column('products', sa.Column('category', sa.String(255), nullable=False))
    op.add_column('products', sa.Column('discount_percentage', sa.Float, default=0.0))
    op.add_column('products', sa.Column('seller_name', sa.String(255), nullable=True))
    op.add_column('products', sa.Column('seller_contact', sa.String(255), nullable=True))
def downgrade() -> None:
    """Downgrade schema: Remove newly added columns."""
    op.drop_column('products', 'category')
    op.drop_column('products', 'discount_percentage')
    op.drop_column('products', 'seller_name')
    op.drop_column('products', 'seller_contact')