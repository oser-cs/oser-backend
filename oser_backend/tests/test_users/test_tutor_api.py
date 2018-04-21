"""Tutor API tests."""
from rest_framework import status

from tests.utils.api import HyperlinkedAPITestCase
from tutoring.factory import TutorTutoringGroupFactory
from users.factory import TutorFactory
from users.serializers import TutorSerializer


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

    def test_list_tutoring_groups(self):
        def perform_list_tutoring_groups():
            obj = self.factory.create()
            # add tutor to several tutoring groups
            TutorTutoringGroupFactory.create_batch(3, tutor=obj)
            url = '/api/tutors/{}/tutoringgroups/'.format(obj.pk)
            response = self.client.get(url)
            return response

        self.assertRequiresAuth(
            perform_list_tutoring_groups,
            expected_status_code=status.HTTP_200_OK)
