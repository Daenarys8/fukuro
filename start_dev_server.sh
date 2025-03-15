#!/bin/bash

# Set working directory to script location
cd "$(dirname "$0")"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Kill any existing processes on port 8000
echo "Checking for existing processes on port 8000..."
if command_exists lsof; then
    lsof -ti:8000 | xargs -r kill -9
elif command_exists netstat; then
    pid=$(netstat -ano | grep ':8000' | awk '{print $5}')
    if [ ! -z "$pid" ]; then
        kill -9 $pid
    fi
fi

# Clean up any stale .pyc files
echo "Cleaning up Python cache files..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Ensure data directory exists with proper permissions
echo "Setting up data directory..."
mkdir -p data
chmod 777 data

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export PYTHONPATH=$(pwd)
export ENVIRONMENT=development
export HOST=0.0.0.0
export PORT=8000
export SQLALCHEMY_DATABASE_URL=sqlite:///./data/security.db
export FRONTEND_URL=http://localhost:5173

# Start the server
echo "Starting FastAPI server..."
python run.py