"""empty message

Revision ID: 2f55c7be7da9
Revises: 
Create Date: 2019-08-29 01:45:21.123691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f55c7be7da9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reports_to_export',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=True),
    sa.Column('column_number', sa.Integer(), nullable=True),
    sa.Column('export_to', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('file', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reports_to_export')
    # ### end Alembic commands ###
