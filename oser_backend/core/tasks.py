"""Core Celery tasks."""

from oser_backend.celery import app
from django.core.management import call_command


@app.task
def clean_media():
    """Clean unused media files."""
    call_command('clean_media')
