"""adding a new column name issue_date

Revision ID: dc50e6c35949
Revises: daa4c0077180
Create Date: 2024-04-03 23:20:20.265641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc50e6c35949'
down_revision = 'daa4c0077180'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('issue_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.drop_column('issue_date')

    # ### end Alembic commands ###