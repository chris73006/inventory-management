"""Track price column

Revision ID: d60090f3cc99
Revises: 3023f9865ef3
Create Date: 2025-05-10 22:22:56.588013

"""
from typing import Sequence, Union
from alembic import context
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = 'd60090f3cc99'
down_revision: Union[str, None] = '3023f9865ef3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    conn = context.get_bind()  # ✅ Get database connection
    inspector = inspect(conn)  # ✅ Use SQLAlchemy inspector
    existing_tables = [t.lower() for t in inspector.get_table_names()] 
    if "products" not in existing_tables: # ✅ Check if table exi
        op.create_table(
            "products",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(255), nullable=False),
            sa.Column("price", sa.Float(), nullable=False),
            sa.Column("stock",sa.Integer(),nullable=False,server_default=sa.text("0"))
        )
        op.alter_column("products", "stock", server_default=None)

    else:
       existing_columns = [col["name"].lower() for col in inspector.get_columns("products")]
       if "stock" not in existing_columns:
           op.add_column("products",
                sa.Column("stock", sa.Integer(), nullable=False, server_default="0")
            )
       op.alter_column("products","stock",server_default=None)

    # ### end Alembic commands ###


def downgrade() -> None:
   
    op.drop_column("products","stock")
    