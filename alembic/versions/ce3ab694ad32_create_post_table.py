"""create post table

Revision ID: ce3ab694ad32
Revises: 
Create Date: 2024-11-17 16:34:42.601109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce3ab694ad32'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#handle updating of table
def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    pass

#handle rollback
def downgrade():
    op.drop_table('posts')
    pass
