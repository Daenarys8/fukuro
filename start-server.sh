#!/bin/bash

# Exit on any error
set -e

# Set working directory to script location
cd "$(dirname "$0")"

# Kill any existing processes on port 8000
echo "Checking for existing processes on port 8000..."
pkill -f "uvicorn system.main:app" || true
lsof -ti:8000 | xargs -r kill -9 || true

# Clean up Python cache files
echo "Cleaning up Python cache..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Ensure data directory exists with proper permissions
echo "Setting up data directory..."
mkdir -p data
chmod -R 777 data

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set environment variables
export PYTHONPATH=$(pwd)
export ENVIRONMENT=development
export HOST=0.0.0.0
export PORT=8000
export SQLALCHEMY_DATABASE_URL=sqlite:///./data/security.db
export FRONTEND_URL=http://localhost:5173
export PYTHONDONTWRITEBYTECODE=1  # Prevent .pyc files

# Start the server with proper error handling
echo "Starting FastAPI server..."
python run.py