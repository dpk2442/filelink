#!/bin/bash
# Script that gets executed in Docker containers

# Activate virtual environment
source .venv/bin/activate

# Create data folder
mkdir -p data

# Run database migrations
python manage.py migrate

# Generate secret key file if needed
python manage.py generate_secret_key

# Collect static files
python manage.py collectstatic

# Start uwsgi server
exec uwsgi uwsgi.ini
