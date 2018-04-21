"""School API tests."""

from rest_framework import status
from tutoring.factory import SchoolFactory
from users.factory import UserFactory
from tests.utils.api import HyperlinkedAPITestCase

from tutoring.serializers import SchoolSerializer


class SchoolEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the school endpoints."""

    factory = SchoolFactory
    serializer_class = SchoolSerializer

    def perform_list(self):
        url = '/api/schools/'
        response = self.client.get(url)
        return response

    def test_list(self):
        self.assertRequiresAuth(
            self.perform_list,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/schools/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve(self):
        self.assertRequiresAuth(
            self.perform_retrieve,
            expected_status_code=status.HTTP_200_OK)

    def test_list_students(self):
        pass  # TODO

    def test_list_tutors(self):
        pass  # TODO

    def test_list_staff(self):
        pass  # TODO

    def test_list_tutoring_groups(self):
        pass  # TODO

    def test_list_meetings(self):
        pass  # TODO

    def test_list_past_meetings(self):
        pass  # TODO

    def test_list_next_meetings(self):
        pass  # TODO
