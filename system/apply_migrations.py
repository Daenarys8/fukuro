import os
import shutil
from alembic import command
from alembic.config import Config
from pathlib import Path
from sqlalchemy import create_engine, text
from .database import SQLALCHEMY_DATABASE_URL

MIGRATION_RESET_MARKER = Path(__file__).parent / ".migration_reset_completed"

def reset_migration_state():
    """Reset database schema properly before applying migrations."""
    print("Starting reset_migration_state...")
    
    # Create engine with AUTOCOMMIT
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        isolation_level="AUTOCOMMIT",
        future=True
    )
    
    try:
        with engine.connect() as connection:
            # Force close other connections
            connection.execute(text("""
                SELECT pg_terminate_backend(pid) 
                FROM pg_stat_activity 
                WHERE datname = current_database() 
                AND pid <> pg_backend_pid()
            """))
            
            # Drop and recreate schema directly with SQL
            connection.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
            connection.execute(text("CREATE SCHEMA public"))
            connection.execute(text("GRANT ALL ON SCHEMA public TO public"))
    finally:
        engine.dispose()

    print("Schema reset complete")

def apply_migrations():
    """Apply all migrations after reset."""
    print("Starting migrations...")
    
    # First reset the state
    reset_migration_state()
    
    config_dir = Path(__file__).parent.resolve()
    alembic_cfg = Config(str(config_dir / "alembic.ini"))
    
    # Create engine for migrations
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        future=True,
        poolclass=None  # Disable connection pooling during migrations
    )
    
    try:
        with engine.begin() as connection:
            alembic_cfg.attributes["connection"] = connection
            # Stamp first, then upgrade
            command.stamp(alembic_cfg, "base")
            command.upgrade(alembic_cfg, "head")
    finally:
        engine.dispose()

    MIGRATION_RESET_MARKER.touch()
    print("Migrations complete")
