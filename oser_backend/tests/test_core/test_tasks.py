"""Test Celery tasks."""

from django.test import TestCase
from celery.exceptions import TimeoutError

from core.tasks import clean_media


class CleanMediaTaskTest(TestCase):
    """Test the clean_media Celery task."""

    def test_run_task(self):
        try:
            clean_media.delay().get(timeout=2)
        except TimeoutError as e:
            message = str(e) + ' Is the Celery worker running?'
            raise TimeoutError(message)
