"""Tutor API tests."""
from rest_framework import status

from profiles.factory import TutorFactory
from profiles.serializers import TutorSerializer
from tests.utils.api import HyperlinkedAPITestCase


class TutorEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the tutors endpoints."""

    factory = TutorFactory
    serializer_class = TutorSerializer

    def perform_list(self):
        response = self.client.get('/api/tutors/')
        return response

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.get('/api/tutors/{obj.pk}/'.format(obj=obj))
        return response

    def test_list(self):
        self.assertRequiresAuth(
            self.perform_list,
            expected_status_code=status.HTTP_200_OK)

    def test_retrieve(self):
        self.assertRequiresAuth(
            self.perform_retrieve,
            expected_status_code=status.HTTP_200_OK)
