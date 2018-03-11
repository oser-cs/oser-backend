#!/usr/bin/env bash

echo "Migrating database"
python manage.py makemigrations
python manage.py migrate

echo "Initializing admin"
python manage.py initadmin

echo "Collecting static files"
python manage.py collectstatic --noinput

# Run server
exec gunicorn oser_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --access-logfile=- \
  --reload
