"""adding a column name plan_id

Revision ID: 71e80f28b96a
Revises: 60503480217d
Create Date: 2024-06-01 02:48:38.049777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71e80f28b96a'
down_revision = '60503480217d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('groups', 'payment_link_url')
    op.drop_column('groups', 'payment_status')
    op.drop_column('groups', 'price')
    op.add_column('payments', sa.Column('payment_status', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('payment_link_url', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('plain_id', sa.String(length=100), nullable=True))
    op.add_column('payments', sa.Column('price', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments', 'price')
    op.drop_column('payments', 'plain_id')
    op.drop_column('payments', 'payment_link_url')
    op.drop_column('payments', 'payment_status')
    op.add_column('groups', sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('payment_status', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('payment_link_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###