#!/bin/bash

# Wait for the database to be ready (optional, if needed)
# Uncomment if your DB needs some time to be ready before migrations
# echo "Waiting for database to be ready..."
# sleep 10

# Run migrations
echo "Applying migrations..."
python manage.py migrate

# # Collect static files
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start the Django application
echo "Starting Django application..."
exec "$@"
