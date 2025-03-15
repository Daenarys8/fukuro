#!/bin/bash

# Exit on any error
set -e

echo "Initializing server..."

# Kill any existing processes
echo "Cleaning up existing processes..."
pkill -f "uvicorn system.main:app" || true
pkill -f "python run.py" || true
lsof -ti:8000 | xargs -r kill -9 || true

# Clean up Python cache
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Set up virtual environment
echo "Setting up Python environment..."
python3 -m venv venv || python -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Ensure data directory exists with proper permissions
echo "Setting up data directory..."
mkdir -p data
chmod -R 777 data

# Make scripts executable
chmod +x run.sh start.sh start_dev_server.sh start-server.sh

echo "Server initialization complete!"
echo "Run './start-server.sh' to start the server"