"""Add field_key column to fields table

Revision ID: 8d7fd6140245
Revises: f2701733768d
Create Date: 2024-04-02 22:59:19.348380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d7fd6140245'
down_revision = 'f2701733768d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('field_key', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.drop_column('field_key')

    # ### end Alembic commands ###
