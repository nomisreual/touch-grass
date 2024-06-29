#!/usr/bin/env bash
# Exit on error
set -o errexit

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Run the server:
python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
