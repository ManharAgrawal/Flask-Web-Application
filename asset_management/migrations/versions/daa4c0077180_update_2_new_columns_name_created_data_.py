"""update 2 new columns name created_data and updated_data to created_date and update_date

Revision ID: daa4c0077180
Revises: daff9ccfe664
Create Date: 2024-04-03 20:25:50.742937

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'daa4c0077180'
down_revision = 'daff9ccfe664'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('updated_date', sa.DateTime(), nullable=False))
        batch_op.drop_column('updated_data')
        batch_op.drop_column('created_data')

    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('updated_date', sa.DateTime(), nullable=False))
        batch_op.drop_column('updated_data')
        batch_op.drop_column('created_data')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_data', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('updated_data', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('updated_date')
        batch_op.drop_column('created_date')

    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_data', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('updated_data', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('updated_date')
        batch_op.drop_column('created_date')

    # ### end Alembic commands ###
