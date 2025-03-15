#!/bin/bash

# Source virtual environment if available
if [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
elif [ -f "./venv/bin/activate" ]; then
    source ./venv/bin/activate
fi

# Make migration script executable
chmod +x run_migrations.sh

# Run database migrations with proper Python environment
./run_migrations.sh

# Check migration result
if [ $? -ne 0 ]; then
    echo "Error: Database migrations failed"
    exit 1
fi

# Start the application
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload