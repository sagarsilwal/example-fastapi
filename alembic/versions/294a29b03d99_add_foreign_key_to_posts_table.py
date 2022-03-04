"""add foreign-key to posts table

Revision ID: 294a29b03d99
Revises: 39dfbee9c97b
Create Date: 2022-03-04 09:36:57.079127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '294a29b03d99'
down_revision = '39dfbee9c97b'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
                            local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass