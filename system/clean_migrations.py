"""Clean up stale Alembic migration state."""
import os
import shutil
from sqlalchemy import create_engine, text
from system.config import settings

def check_python_cache():
    """Clean all Python cache files."""
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
        for f in files:
            if f.endswith(('.pyc', '.pyo', '.pyd')):
                os.remove(os.path.join(root, f))

def verify_clean_state():
    """Verify no stale migrations exist."""
    check_python_cache()
    versions_dir = os.path.join(os.path.dirname(__file__), 'alembic', 'versions')
    if os.path.exists(versions_dir):
        files = [f for f in os.listdir(versions_dir) 
                if f != '1a2b3c4d5e6f_base_schema.py' and not f.startswith('__')]
        if files:
            raise RuntimeError(f"Found stale migration files: {files}")

def clean_migrations():
    """Clean up all migration state and cached files."""
    verify_clean_state()
    # First clean up filesystem
    versions_dir = os.path.join(os.path.dirname(__file__), 'alembic', 'versions')
    if os.path.exists(versions_dir):
        # Only remove files other than base schema
        # Skip any backup process since we're preserving the file directly
        for file in os.listdir(versions_dir):
            file_path = os.path.join(versions_dir, file)
            if file != '1a2b3c4d5e6f_base_schema.py':
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        # Clean up any orphaned migration references
        # Drop all migration tables and version tracking
        conn.execute(text("""
            DO $$
            BEGIN
                -- Keep base schema version but remove other versions
                IF EXISTS (SELECT 1 FROM alembic_version) THEN
                    DELETE FROM alembic_version 
                    WHERE version_num != '1a2b3c4d5e6f';
                END IF;
                
                -- Remove config table if it exists
                DROP TABLE IF EXISTS alembic_version_config CASCADE;
                
                -- Clean up sequences while preserving base schema
                IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'alembic_version_id_seq') THEN
                    ALTER SEQUENCE alembic_version_id_seq RESTART WITH 1;
                END IF;
            END $$;
        """))
        conn.commit()

        # Drop all application tables to start fresh
        conn.execute(text("""
            -- Only drop non-essential tables
            DROP TABLE IF EXISTS security_logs CASCADE;
            DROP TABLE IF EXISTS threat_models CASCADE;
            DROP TABLE IF EXISTS anomaly_detections CASCADE;
            DROP TABLE IF EXISTS response_actions CASCADE;
        """))
        conn.commit()
        
        # Reset sequence if it exists
        conn.execute(text("""
            DO $$ 
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'alembic_version_id_seq') THEN
                    ALTER SEQUENCE alembic_version_id_seq RESTART WITH 1;
                END IF;
            END $$;
        """))
        conn.commit()

if __name__ == "__main__":
    clean_migrations()