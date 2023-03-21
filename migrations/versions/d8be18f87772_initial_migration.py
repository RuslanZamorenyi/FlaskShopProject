"""Initial migration.

Revision ID: d8be18f87772
Revises: cef33ce88ef9
Create Date: 2023-03-10 16:58:19.564702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8be18f87772'
down_revision = 'cef33ce88ef9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('black_jwt_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('black_jwt_list')
    # ### end Alembic commands ###