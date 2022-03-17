"""Added required tables

Revision ID: 6cbf6e5a052e
Revises: 971573247181
Create Date: 2022-03-14 22:58:31.550384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cbf6e5a052e'
down_revision = '971573247181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('barriers', sa.Column('number', sa.Integer(), nullable=True))
    op.add_column('barriers', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('barriers', 'description')
    op.drop_column('barriers', 'number')
    # ### end Alembic commands ###