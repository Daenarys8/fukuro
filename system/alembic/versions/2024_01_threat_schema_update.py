from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2024_01_threat_schema_update'
down_revision = '1a2b3c4d5e6f'  # Ensure this is the correct previous revision
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Apply schema changes with conditional checks."""
    # Check if the 'threats' table exists before attempting to create it
    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'threats') THEN
            CREATE TABLE threats (
                id VARCHAR NOT NULL, 
                threat_type VARCHAR NOT NULL, 
                title VARCHAR NOT NULL, 
                description TEXT, 
                severity VARCHAR NOT NULL, 
                status VARCHAR NOT NULL, 
                timestamp TIMESTAMP WITHOUT TIME ZONE, 
                source_ip VARCHAR, 
                target_system VARCHAR, 
                PRIMARY KEY (id)
            );
        END IF;
    END $$;
    """)

    # Alter SecurityLog id column from Integer to String (if needed)
    op.alter_column('security_logs', 'id',
        type_=sa.String(),
        existing_type=sa.Integer(),
        postgresql_using="id::text"
    )
    
    # Update Threat table columns from enum to string if the columns exist
    op.alter_column('threats', 'severity',
        type_=sa.String(),
        existing_type=sa.Enum('low', 'medium', 'high', name='threatseverity'),
        postgresql_using="severity::text"
    )
    
    op.alter_column('threats', 'status',
        type_=sa.String(),
        existing_type=sa.Enum('active', 'resolved', 'false_positive', name='threatstatus'),
        postgresql_using="status::text"
    )


def downgrade() -> None:
    """Downgrade logic with conditional checks to handle schema changes gracefully."""
    op.execute("""
    DO $$ BEGIN
        IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'threats') THEN
            ALTER TABLE threats ALTER COLUMN status TYPE threatstatus
            USING status::threatstatus;
            ALTER TABLE threats ALTER COLUMN severity TYPE threatseverity
            USING severity::threatseverity;
        END IF;
    END $$;
    """)

    # Revert SecurityLog id back to integer if needed
    op.alter_column('security_logs', 'id',
        type_=sa.Integer(),
        existing_type=sa.String(),
        postgresql_using="id::integer"
    )
