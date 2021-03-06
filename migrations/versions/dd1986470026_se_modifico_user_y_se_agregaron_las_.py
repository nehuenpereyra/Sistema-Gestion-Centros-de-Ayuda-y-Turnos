"""Se modifico User y se agregaron las clases UserRole y UserPermission

Revision ID: dd1986470026
Revises: d24ba8629500
Create Date: 2020-10-15 20:43:38.807485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd1986470026'
down_revision = 'd24ba8629500'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###
