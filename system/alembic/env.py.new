"""Alembic environment configuration."""
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

# Import the SQLAlchemy declarative Base from the models
from system.models import Base

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add model's MetaData object for autogenerate support
target_metadata = Base.metadata

def get_url():
    """Get database URL from environment variable."""
    return os.getenv("DATABASE_URL", "postgresql://localhost/securitydb")

def process_revision_directives(context, revision, directives):
    """Prevent multiple heads and enforce single migration path."""
    if not directives:
        return
        
    # Only allow running our base migration
    if hasattr(directives[0], 'head_revision') and directives[0].head_revision != '1a2b3c4d5e6f':
        directives[:] = []
    return directives

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        process_revision_directives=process_revision_directives,
        # Prevent downgrades
        downgrade_token=None
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            compare_type=True,
            compare_server_default=True,
            # Prevent downgrades
            downgrade_token=None
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()