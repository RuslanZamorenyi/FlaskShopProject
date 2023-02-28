"""Initial migration.

Revision ID: 2c58a6c989c5
Revises: 188a029f75d9
Create Date: 2023-02-28 13:48:53.591695

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2c58a6c989c5'
down_revision = '188a029f75d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('choose_shoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('colours_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('choose_shoes_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'colours', ['colours_id'], ['id'])
        batch_op.drop_column('names_id')

    with op.batch_alter_table('sizes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('names_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'names', ['names_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sizes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('names_id')

    with op.batch_alter_table('choose_shoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('names_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('choose_shoes_ibfk_1', 'names', ['names_id'], ['id'])
        batch_op.drop_column('colours_id')

    # ### end Alembic commands ###
