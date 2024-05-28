"""adding 2 columns name price and payment_status in groups

Revision ID: fba1c2cd0dbd
Revises: 25da3041f607
Create Date: 2024-05-29 00:51:13.540089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba1c2cd0dbd'
down_revision = '25da3041f607'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('paymenet_status', sa.String(), nullable=True, paymenet_status='pending'))
        batch_op.add_column(sa.Column('price', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.drop_column('price')
        batch_op.drop_column('paymenet_status')

    # ### end Alembic commands ###
