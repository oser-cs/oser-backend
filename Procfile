web: gunicorn oser_backend.wsgi:application --bind 0.0.0.0:$PORT

# Toggle next line to start Celery in a worker process
# worker: celery -A oser_backend worker --beat -l info
