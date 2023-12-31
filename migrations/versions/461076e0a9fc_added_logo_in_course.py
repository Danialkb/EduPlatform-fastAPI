"""added logo in course

Revision ID: 461076e0a9fc
Revises: b1ad06d0ae59
Create Date: 2023-08-02 18:17:04.408140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '461076e0a9fc'
down_revision = 'b1ad06d0ae59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('is_private', sa.Boolean(), nullable=True))
    op.add_column('course', sa.Column('logo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'logo')
    op.drop_column('course', 'is_private')
    # ### end Alembic commands ###
