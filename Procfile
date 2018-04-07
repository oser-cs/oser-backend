web: sh -c 'cd oser_backend && exec gunicorn oser_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 1'

worker: sh -c 'cd oser_backend && exec celery -A oser_backend worker --beat -l info'
