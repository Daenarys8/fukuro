#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root or with sudo"
  exit
fi

# Stop any existing FastAPI processes
echo "Stopping any existing FastAPI processes..."
pkill -f "uvicorn system.main:app"

# Kill any process using port 8000
echo "Freeing port 8000..."
fuser -k 8000/tcp 2>/dev/null

# Create and set permissions for data directory
echo "Setting up data directory..."
mkdir -p data
chmod -R 777 data
chown -R $SUDO_USER:$SUDO_USER data

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make start script executable
chmod +x start.sh

# Export environment variables
export ENVIRONMENT=development
export HOST=0.0.0.0
export PORT=8000
export SQLALCHEMY_DATABASE_URL=sqlite:///./data/security.db
export FRONTEND_URL=http://localhost:5173

echo "Server setup complete. Run './start.sh' to start the server."