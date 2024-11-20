"""Add phone_number_last_changed column to Users

Revision ID: defd401ba1f0
Revises: e156fb76756e
Create Date: 2024-11-11 08:52:56.261341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'defd401ba1f0'
down_revision: Union[str, None] = 'e156fb76756e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('phone_number_last_changed', sa.DateTime(timezone=True), nullable=True))

def downgrade():
    op.drop_column('users', 'phone_number_last_changed')

