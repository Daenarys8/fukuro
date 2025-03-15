#!/bin/bash

# Kill any existing processes on port 8000
echo "Checking for existing processes on port 8000..."
lsof -ti:8000 | xargs -r kill -9

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Ensure data directory exists with proper permissions
echo "Setting up data directory..."
mkdir -p data
chmod 777 data

# Export environment variables
export ENVIRONMENT=development
export HOST=0.0.0.0
export PORT=8000
export SQLALCHEMY_DATABASE_URL=sqlite:///./data/security.db
export FRONTEND_URL=http://localhost:5173

# Start the FastAPI server
echo "Starting FastAPI server..."
python run.py