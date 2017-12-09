"""API docs tests."""
from django.test import TestCase
from rest_framework import status


class APIDocsTest(TestCase):
    """Test the access to the API docs."""

    def test_docs_url(self):
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
