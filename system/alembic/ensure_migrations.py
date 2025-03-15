"""Ensure clean migration state."""
import os
import shutil
from pathlib import Path
from sqlalchemy import create_engine, text, inspect
from system.config import settings

def ensure_clean_migrations():
    """Force clean migration state."""
    base_dir = Path(__file__).parent
    engine = create_engine(settings.DATABASE_URL)
    
    # Clean database state
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        
        # Force single version table
        conn.execute(text("""
            DROP TABLE IF EXISTS alembic_version CASCADE;
            CREATE TABLE alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            );
            INSERT INTO alembic_version (version_num) VALUES ('1a2b3c4d5e6f');
        """))
    
    # Clean versions directory
    versions_dir = base_dir / "versions"
    if versions_dir.exists():
        shutil.rmtree(versions_dir)
    versions_dir.mkdir(exist_ok=True)
    
    # Copy base schema
    base_schema = base_dir / "1a2b3c4d5e6f_base_schema.py"
    if base_schema.exists():
        shutil.copy2(base_schema, versions_dir / "1a2b3c4d5e6f_base_schema.py")
    
    # Remove legacy files
    legacy_patterns = ["*security_log.py", "*threat_model.py", "*initial_db_setup.py"]
    for pattern in legacy_patterns:
        for f in base_dir.rglob(pattern):
            if f.exists():
                f.unlink()

if __name__ == "__main__":
    ensure_clean_migrations()