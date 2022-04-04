 """Added Users table

Revision ID: 5ff696e8d2c3
Revises: 19383b6b20a9
Create Date: 2022-03-29 20:01:03.693390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ff696e8d2c3'
down_revision = '19383b6b20a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('password_sha256', sa.String(length=100), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
