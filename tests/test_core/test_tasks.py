"""Test Celery tasks."""

from django.test import TestCase
from celery.exceptions import TimeoutError

from core.tasks import cleanmedia


class CleanMediaTaskTest(TestCase):
    """Test the cleanmedia Celery task."""

    def test_run_task(self):
        try:
            cleanmedia.delay().get(timeout=2)
        except TimeoutError as e:
            message = str(e) + ' Is the Celery worker running?'
            raise TimeoutError(message)
