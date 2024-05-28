"""changing in init method

Revision ID: 78f566440191
Revises: 4628170ae412
Create Date: 2024-04-06 01:22:31.380399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78f566440191'
down_revision = '4628170ae412'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dataformat_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fields_dataformats_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'dataformats', ['dataformat_id'], ['id'])
        batch_op.drop_column('dataformats')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dataformats', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fields_dataformats_fkey', 'dataformats', ['dataformats'], ['id'])
        batch_op.drop_column('dataformat_id')

    # ### end Alembic commands ###