"""Student API tests."""
from rest_framework import status

from profiles.factory import StudentFactory
from profiles.serializers import StudentSerializer
from tests.utils.api import HyperlinkedAPITestCase


class StudentEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the students endpoints."""

    factory = StudentFactory
    serializer_class = StudentSerializer

    def perform_list(self):
        response = self.client.get('/api/students/')
        return response

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        response = self.client.get('/api/students/{obj.pk}/'.format(obj=obj))
        return response

    def test_list(self):
        self.assertRequiresAuth(
            self.perform_list,
            expected_status_code=status.HTTP_200_OK)

    def test_retrieve(self):
        self.assertRequiresAuth(
            self.perform_retrieve,
            expected_status_code=status.HTTP_200_OK)
