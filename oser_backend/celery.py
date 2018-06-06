"""
Celery config for oser_backend project.

It exposes the Celery application that other apps can use to
schedule and execute tasks in the background.

See:
http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django
"""
import os
from celery import Celery

# set the default Django settings module for Celery
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'oser_backend.settings.production')

app = Celery('oser_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from 'tasks.py' modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Log Celery requests information."""
    print('Request: {0!r}'.format(self.request))
