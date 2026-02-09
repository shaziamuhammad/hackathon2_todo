"""Add advanced task fields and conversation model

Revision ID: phase3_ai_chatbot
Revises:
Create Date: 2026-02-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = 'phase3_ai_chatbot'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new fields to task table
    op.add_column('task', sa.Column('priority', sa.String(), nullable=True, server_default='medium'))
    op.add_column('task', sa.Column('status', sa.String(), nullable=True, server_default='pending'))
    op.add_column('task', sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('task', sa.Column('recurrence_pattern', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('task', sa.Column('completed_at', sa.DateTime(), nullable=True))

    # Add new fields to user table
    op.add_column('user', sa.Column('name', sa.String(), nullable=True))
    op.add_column('user', sa.Column('theme_preference', sa.String(), nullable=True, server_default='light'))
    op.add_column('user', sa.Column('provider', sa.String(), nullable=True, server_default='email'))
    op.add_column('user', sa.Column('provider_id', sa.String(), nullable=True))

    # Make hashed_password nullable for OAuth users
    op.alter_column('user', 'hashed_password', nullable=True)

    # Create conversation table
    op.create_table(
        'conversation',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('messages', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    # Drop conversation table
    op.drop_table('conversation')

    # Remove user table columns
    op.drop_column('user', 'provider_id')
    op.drop_column('user', 'provider')
    op.drop_column('user', 'theme_preference')
    op.drop_column('user', 'name')
    op.alter_column('user', 'hashed_password', nullable=False)

    # Remove task table columns
    op.drop_column('task', 'completed_at')
    op.drop_column('task', 'recurrence_pattern')
    op.drop_column('task', 'due_date')
    op.drop_column('task', 'tags')
    op.drop_column('task', 'status')
    op.drop_column('task', 'priority')
