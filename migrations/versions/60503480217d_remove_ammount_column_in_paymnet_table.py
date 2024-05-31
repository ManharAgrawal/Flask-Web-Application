"""remove ammount column in paymnet table

Revision ID: 60503480217d
Revises: 461b31efa9c7
Create Date: 2024-06-01 01:32:49.310581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60503480217d'
down_revision = '461b31efa9c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments', 'amount')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
