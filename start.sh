#!/usr/bin/env bash

# Collect static files
exec python3 manage.py collectstatic

# Initialize database
exec python3 manage.py makemigrations
exec python3 manage.py migrate

# Initialize admin users
exec python3 manage.py initadmin

# Run server
exec gunicorn oser_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3
