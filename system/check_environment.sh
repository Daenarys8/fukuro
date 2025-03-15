#!/bin/bash

# Check if running in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Not running in a virtual environment"
    
    # Try to activate virtual environment
    if [ -f "../venv/bin/activate" ]; then
        source ../venv/bin/activate
    elif [ -f "./venv/bin/activate" ]; then
        source ./venv/bin/activate
    else
        echo "Error: Virtual environment not found"
        exit 1
    fi
fi

# Verify Python environment
which python
python -c "import sys; print(sys.prefix)"

# Verify critical packages
python -c "import fastapi" || echo "FastAPI not installed"
python -c "import sqlalchemy" || echo "SQLAlchemy not installed"
python -c "import uvicorn" || echo "Uvicorn not installed"

# Check database connectivity
python -c "
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://fukuro:fukuro@localhost/fukurodb')
try:
    with engine.connect() as conn:
        conn.execution_options(timeout=10)
        conn.execute(text('SELECT 1'))
        print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
"