"""Base schema migration for the security system.

This migration creates the initial database schema including tables for security logs,
threats, anomaly detections, and response action logs.

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Optional
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision: str = '1a2b3c4d5e6f'
down_revision: Optional[str] = None
branch_labels: Optional[str] = None
depends_on: Optional[str] = None


def upgrade() -> None:
    """Create base schema with standard SQL types."""
    # Skip dropping any types since we only use standard SQL types
    # Create threats table
    op.create_table(
        'threats',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('threat_type', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('source_ip', sa.String(), nullable=True),
        sa.Column('target_system', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'security_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('log_type', sa.String(), nullable=False),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('additional_info', sa.JSON(), nullable=True),  # Renamed 'metadata' to 'additional_info'
        sa.Column('threat_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['threat_id'], ['threats.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'anomaly_detections',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('detection_type', sa.String(), nullable=False),
        sa.Column('confidence_score', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source_data', sa.JSON(), nullable=True),
        sa.Column('impact_severity', sa.String(), nullable=True),
        sa.Column('affected_systems', sa.JSON(), nullable=True),
        sa.Column('false_positive', sa.Integer(), nullable=True),
        sa.Column('additional_info', sa.JSON(), nullable=True),  # Renamed 'metadata' to 'additional_info'
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'response_action_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('action_type', sa.String(), nullable=False),
        sa.Column('target_system', sa.String(), nullable=True),
        sa.Column('action_details', sa.JSON(), nullable=True),
        sa.Column('success', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('additional_info', sa.JSON(), nullable=True),  # Renamed 'metadata' to 'additional_info'
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """No downgrade supported for base schema."""
    pass
