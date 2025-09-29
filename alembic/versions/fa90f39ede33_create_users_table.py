"""create users table

Revision ID: fa90f39ede33
Revises: 
Create Date: 2025-09-29 14:31:15.566502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa90f39ede33'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cars",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model", sa.String(length=50), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("arrival_time", sa.String(length=50), nullable=False),
        sa.Column("departure_time", sa.String(length=50), nullable=False),
        sa.Column("price_range", sa.String(length=50), nullable=False),
        sa.Column("phone_number", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_cars_id"), "cars", ["id"], unique=False)

def downgrade() -> None:
    op.drop_index(op.f("ix_cars_id"), table_name="cars")
    op.drop_table("cars")
