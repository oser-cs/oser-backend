#!/usr/bin/env bash

# Run server
exec gunicorn oser_backend.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 3 \
  --access-logfile=- \
  --reload \
