"""Student API tests."""
from rest_framework import status
from users.factory import StudentInTutoringGroupFactory
from tests.utils.api import HyperlinkedAPITestCase

from users.serializers import StudentSerializer


class StudentEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the students endpoints."""

    factory = StudentInTutoringGroupFactory
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

    def test_retrieve_tutoring_group(self):
        def perform_retrieve_tutoring_group():
            obj = self.factory.create()
            response = self.client.get(
                '/api/students/{}/tutoringgroup/'.format(obj.pk))
            return response

        self.assertRequiresAuth(
            perform_retrieve_tutoring_group,
            expected_status_code=status.HTTP_200_OK)
