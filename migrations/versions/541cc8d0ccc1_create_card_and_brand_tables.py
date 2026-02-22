"""create card and brand tables

Revision ID: 541cc8d0ccc1
Revises: 096e8a994744
Create Date: 2026-02-06 06:23:39.099158
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "541cc8d0ccc1"
down_revision: Union[str, Sequence[str], None] = "096e8a994744"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "brands",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),

        sa.Column(
            "update_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "cars",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("factory_year", sa.Integer(), nullable=False),
        sa.Column("model_year", sa.Integer(), nullable=False),
        sa.Column("color", sa.String(), nullable=False),
        sa.Column("plate", sa.String(), nullable=False),
        sa.Column("fuel_type", sa.String(), nullable=False),
        sa.Column("transmission", sa.String(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("brand_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),

        sa.Column(
            "update_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(["brand_id"], ["brands.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(op.f("ix_cars_plate"), "cars", ["plate"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f("ix_cars_plate"), table_name="cars")
    op.drop_table("cars")
    op.drop_table("brands")