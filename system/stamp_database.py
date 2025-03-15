"""Force a clean database state with latest schema."""
import os
import sys
from sqlalchemy import create_engine, text
from system.config import settings

def stamp_clean_state():
    """Force database into a clean state with latest revision."""
    engine = create_engine(settings.DATABASE_URL)
    
    # Drop everything and recreate schema
    with engine.connect() as conn:
        conn.execute(text('DROP SCHEMA IF EXISTS public CASCADE'))
        conn.execute(text('CREATE SCHEMA public'))
        conn.execute(text("""
            DROP TABLE IF EXISTS alembic_version CASCADE;
            CREATE TABLE alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            );
            INSERT INTO alembic_version (version_num) VALUES ('1a2b3c4d5e6f');
        """))
        conn.commit()

if __name__ == '__main__':
    stamp_clean_state()