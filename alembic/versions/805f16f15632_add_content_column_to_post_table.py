"""add content column to post table

Revision ID: 805f16f15632
Revises: ce3ab694ad32
Create Date: 2024-11-17 16:40:33.057992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '805f16f15632'
down_revision: Union[str, None] = 'ce3ab694ad32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
