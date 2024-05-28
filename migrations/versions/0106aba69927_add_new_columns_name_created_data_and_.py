"""Add new columns name created data and updated data in status table

Revision ID: 0106aba69927
Revises: 2b89069e0bc5
Create Date: 2024-05-01 23:30:58.978950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0106aba69927'
down_revision = '2b89069e0bc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('status', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('updated_date', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('status', schema=None) as batch_op:
        batch_op.drop_column('updated_date')
        batch_op.drop_column('created_date')

    # ### end Alembic commands ###