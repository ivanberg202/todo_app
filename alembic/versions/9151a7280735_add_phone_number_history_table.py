"""Add phone_number_history table

Revision ID: 9151a7280735
Revises: defd401ba1f0
Create Date: 2024-11-11 09:34:22.662439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9151a7280735'
down_revision: Union[str, None] = 'defd401ba1f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Creating phone_number_history table
    op.create_table(
        'phone_number_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Dropping phone_number_history table
    op.drop_table('phone_number_history')
