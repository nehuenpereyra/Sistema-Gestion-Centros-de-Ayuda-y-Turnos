"""Se agregaron los siguientes atributos al modelo de un centro de ayuda: protocolo de vista, latitud y longitud.

Revision ID: c1bda1433a5c
Revises: dd1986470026
Create Date: 2020-10-30 20:49:28.693010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1bda1433a5c'
down_revision = 'dd1986470026'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('help_center', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('help_center', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('help_center', sa.Column('view_protocol', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('help_center', 'view_protocol')
    op.drop_column('help_center', 'longitude')
    op.drop_column('help_center', 'latitude')
    # ### end Alembic commands ###
