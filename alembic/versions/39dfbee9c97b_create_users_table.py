"""create users table

Revision ID: 39dfbee9c97b
Revises: 3ceb058e18f1
Create Date: 2022-03-04 09:35:30.976469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39dfbee9c97b'
down_revision = '3ceb058e18f1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
