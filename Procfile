release: python manage.py migrate --noinput
web: gunicorn oser_backend.wsgi:application --bind 0.0.0.0:$PORT
