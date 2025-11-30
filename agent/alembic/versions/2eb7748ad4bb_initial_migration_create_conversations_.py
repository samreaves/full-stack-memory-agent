"""Initial migration: create conversations and messages tables with pgvector

Revision ID: 2eb7748ad4bb
Revises:
Create Date: 2025-11-29 18:21:46.701480

"""
from typing import Sequence, Union
import os
import dotenv

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# Load environment variables
dotenv.load_dotenv()

# Get embedding dimensions from environment (default to 768 if not set)
EMBEDDING_MODEL_DIMENSIONS = int(os.getenv("EMBEDDING_MODEL_DIMENSIONS", "768"))

# revision identifiers, used by Alembic.
revision: str = '2eb7748ad4bb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding', Vector(EMBEDDING_MODEL_DIMENSIONS), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )

    # Create index on messages for conversation_id and created_at
    op.create_index(
        'idx_messages_conversation',
        'messages',
        ['conversation_id', 'created_at'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop index
    op.drop_index('idx_messages_conversation', table_name='messages')

    # Drop tables (messages first due to foreign key)
    op.drop_table('messages')
    op.drop_table('conversations')

    # Note: We don't drop the vector extension as it might be used by other databases
