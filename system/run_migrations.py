"""Run migrations safely by ensuring reset state first."""
from pathlib import Path
import os
import shutil
from system.apply_migrations import apply_migrations
from pathlib import Path

# Ensure base schema exists
base_dir = Path(__file__).parent
versions_dir = base_dir / "alembic" / "versions"
base_schema = base_dir / "alembic" / "1a2b3c4d5e6f_base_schema.py"

if base_schema.exists():
    versions_dir.mkdir(exist_ok=True)
    if not (versions_dir / "1a2b3c4d5e6f_base_schema.py").exists():
        shutil.copy2(base_schema, versions_dir / "1a2b3c4d5e6f_base_schema.py")

if __name__ == "__main__":
    apply_migrations()