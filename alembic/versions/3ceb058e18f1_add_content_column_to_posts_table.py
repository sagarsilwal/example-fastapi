"""add content column to posts table

Revision ID: 3ceb058e18f1
Revises: cffc3bffa343
Create Date: 2022-03-04 09:33:19.085290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ceb058e18f1'
down_revision = 'cffc3bffa343'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
