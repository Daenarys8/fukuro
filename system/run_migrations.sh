#!/bin/bash
# Run database migrations
echo "Running database migrations..."
python3 -m alembic upgrade head

# Check if migrations were successful
if [ $? -eq 0 ]; then
    echo "Database migrations completed successfully"
    exit 0
else
    echo "Error running database migrations"
    exit 1
fi