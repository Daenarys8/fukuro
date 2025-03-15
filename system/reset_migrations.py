"""Reset the database migration state completely and start fresh with base schema."""
from pathlib import Path
import sys
from alembic.config import Config
from alembic import command
import psycopg2
from sqlalchemy import create_engine, text
import os

def reset_migrations():
    """Reset database schema completely without using Alembic migrations."""
    try:
        # Get database connection details
        DB_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/securitydb')
        
        # Connect directly with psycopg2 first to handle low-level operations
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        try:
            # Drop everything from database
            cur.execute("""
                DO $$ DECLARE r RECORD;
                BEGIN
                    -- Drop all tables
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                    END LOOP;
                    
                    -- Drop all types
                    FOR r IN (SELECT typname FROM pg_type 
                             WHERE typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = current_schema())
                             AND typtype = 'e') LOOP
                        EXECUTE 'DROP TYPE IF EXISTS ' || quote_ident(r.typname) || ' CASCADE';
                    END LOOP;
                END $$;""")
            
            # Create fresh alembic_version table and set initial version
            cur.execute('CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL);')
            cur.execute("INSERT INTO alembic_version (version_num) VALUES ('1a2b3c4d5e6f');")
            
        finally:
            # Always close connections
            cur.close()
            conn.close()
        
        # Create tables and set version stamp in one transaction
        engine = create_engine(DB_URL)
        with engine.begin() as connection:
            # Create all tables from models
            from .models import Base
            Base.metadata.create_all(connection)
            
            # Set version stamp manually
            connection.execute(text('DROP TABLE IF EXISTS alembic_version'))
            connection.execute(text('CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)'))
            connection.execute(text("INSERT INTO alembic_version (version_num) VALUES ('1a2b3c4d5e6f')"))
        
        # Touch file to indicate clean migration state
        Path(__file__).parent / '.migration_reset_completed'.touch()
        print("Successfully reset database schema")
        return True
        
    except Exception as e:
        print(f"Error resetting migrations: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = reset_migrations()
    sys.exit(0 if success else 1)