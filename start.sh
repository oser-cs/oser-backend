#!/usr/bin/env bash

# Run server
exec gunicorn oser_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3
