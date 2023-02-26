"""Initial migration.

Revision ID: c1eaf12d7bb2
Revises: 
Create Date: 2023-02-25 14:07:59.238024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1eaf12d7bb2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('names',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('prise', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('colours',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('colour', sa.String(length=80), nullable=False),
    sa.Column('nam_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['nam_id'], ['names.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sizes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('size', sa.String(length=80), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['names.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sizes')
    op.drop_table('colours')
    op.drop_table('names')
    # ### end Alembic commands ###
