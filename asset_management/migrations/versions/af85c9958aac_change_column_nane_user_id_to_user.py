"""change column nane user_id to user

Revision ID: af85c9958aac
Revises: b9e3dacc5e2d
Create Date: 2024-02-21 20:07:45.490970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af85c9958aac'
down_revision = 'b9e3dacc5e2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user', sa.Integer(), nullable=True))
        batch_op.drop_constraint('groups_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('groups_user_id_fkey', 'users', ['user_id'], ['id'])
        batch_op.drop_column('user')

    # ### end Alembic commands ###
