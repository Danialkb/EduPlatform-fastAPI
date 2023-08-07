"""added course student assosiation

Revision ID: 7d701d86bac7
Revises: 461076e0a9fc
Create Date: 2023-08-03 12:01:59.282120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d701d86bac7'
down_revision = '461076e0a9fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course_student_association',
    sa.Column('course_id', sa.UUID(), nullable=True),
    sa.Column('student_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('course_student_association')
    # ### end Alembic commands ###
