#!/usr/bin/env bash

exec gunicorn oser_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3
