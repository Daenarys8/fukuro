#!/bin/bash

# Exit on any error
set -e

echo "Starting server initialization..."

# Run init_server.sh first if needed
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found, running initialization..."
    chmod +x init_server.sh
    ./init_server.sh
fi

# Source virtual environment
source venv/bin/activate

# Cleanup and setup
echo "Preparing server start..."

# Clean up server processes
echo "Cleaning up server..."
python clean_server.py

# Double check no processes remain
echo "Verifying port is available..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "Error: Port 8000 is still in use"
    exit 1
fi

# Clean Python cache
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Ensure data directory exists with proper permissions
echo "Setting up data directory..."
mkdir -p data
chmod -R 777 data

# Export required environment variables
export PYTHONPATH=$(pwd)
export ENVIRONMENT=development
export HOST=0.0.0.0
export PORT=8000
export SQLALCHEMY_DATABASE_URL=sqlite:///./data/security.db
export FRONTEND_URL=http://localhost:5173
export PYTHONDONTWRITEBYTECODE=1

# Start the server
echo "Starting FastAPI server..."
python run.py

# Check if server started successfully
sleep 2
if curl -s http://localhost:8000/health > /dev/null; then
    echo "Server started successfully!"
else
    echo "Server failed to start. Check logs for details."
    exit 1
fi