#!/usr/bin/env bash

# Collect static files
python3 manage.py collectstatic

# Initialize database
python3 manage.py makemigrations
python3 manage.py migrate

# Initialize admin users
python3 manage.py initadmin

# Run server
exec gunicorn oser_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3
