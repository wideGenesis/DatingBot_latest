"""models fixed

Revision ID: d8930d50fe36
Revises: f18b6348a73c
Create Date: 2022-07-14 19:50:04.210880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8930d50fe36'
down_revision = 'f18b6348a73c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('advertisements', 'email_is_hidden',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_constraint('areas_area_en_key', 'areas', type_='unique')
    op.drop_constraint('areas_area_key', 'areas', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('areas_area_key', 'areas', ['area'])
    op.create_unique_constraint('areas_area_en_key', 'areas', ['area_en'])
    op.alter_column('advertisements', 'email_is_hidden',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###