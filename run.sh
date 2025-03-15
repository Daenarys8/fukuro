#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Export environment variables
export ENVIRONMENT=development
export HOST=0.0.0.0
export PORT=8000
export SQLALCHEMY_DATABASE_URL=sqlite:///./data/security.db
export FRONTEND_URL=http://localhost:5173

# Run the FastAPI server
echo "Starting FastAPI server..."
python run.py