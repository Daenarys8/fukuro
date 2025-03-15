"""Pre-initialization cleanup utilities."""
import os
import shutil
from pathlib import Path
from sqlalchemy import create_engine, text
from system.config import settings

def clean_legacy_files():
    """Remove any stale migration files."""
    system_dir = Path(__file__).parent
    
    # Remove known problematic files
    legacy_patterns = [
        "*_security_log.py",
        "*_update_security_log.py",
        "*_initial_db_setup.py",
        "*_create_threat_model.py"
    ]
    
    for pattern in legacy_patterns:
        for f in system_dir.rglob(pattern):
            try:
                f.unlink()
            except Exception:
                pass

    # Clean Python cache
    for cache_dir in system_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(cache_dir)
        except Exception:
            pass

def clean_database_state():
    """Reset database to clean state."""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.begin() as conn:
        # Drop and recreate schema
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        
        # Remove version tables
        conn.execute(text("""
            DROP TABLE IF EXISTS alembic_version CASCADE;
            CREATE TABLE alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            )
        """))
        conn.execute(text("INSERT INTO alembic_version (version_num) VALUES ('1a2b3c4d5e6f')"))