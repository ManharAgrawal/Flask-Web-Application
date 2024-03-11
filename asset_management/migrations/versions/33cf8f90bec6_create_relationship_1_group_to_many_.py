"""Create relationship 1 group to many group

Revision ID: 33cf8f90bec6
Revises: 8073df749b1d
Create Date: 2024-03-12 01:54:10.814937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33cf8f90bec6'
down_revision = '8073df749b1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datatype', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'groups', ['group_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('datatype', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('group_id')

    # ### end Alembic commands ###
