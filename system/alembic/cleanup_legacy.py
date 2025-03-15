"""Remove legacy migration files and references."""
import os
import shutil
from pathlib import Path
from sqlalchemy import create_engine, text
from system.config import settings

def clean_legacy_migrations():
    """Remove all legacy migration files and references."""
    base_dir = Path(__file__).parent
    
    # Remove specific problematic files
    legacy_files = [
        "2023_security_log.py",
        "2023_update_security_log.py",
        "8ea1f525a755_initial_db_setup.py",
        "b4a1c3d2e5f7.py"
    ]
    
    for pattern in legacy_files:
        for f in base_dir.rglob(pattern):
            if f.exists():
                f.unlink()
                print(f"Removed legacy file: {f}")
    
    # Clean database references
    engine = create_engine(settings.DATABASE_URL)
    with engine.begin() as conn:
        conn.execute(text("""
            DELETE FROM alembic_version 
            WHERE version_num IN (
                '2023_security_log',
                '2023_update_security_log',
                '8ea1f525a755',
                'b4a1c3d2e5f7'
            );
        """))

if __name__ == "__main__":
    clean_legacy_migrations()