"""Tutoring group API tests."""

from rest_framework import status
from tutoring.factory import TutoringGroupFactory
from tests.utils.api import HyperlinkedAPITestCase

from tutoring.serializers import TutoringGroupSerializer


class TutoringGroupEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the tutoring group endpoints."""

    factory = TutoringGroupFactory
    serializer_class = TutoringGroupSerializer

    def perform_list(self):
        url = '/api/groups/'
        response = self.client.get(url)
        return response

    def test_list_requires_authentication(self):
        self.assertRequiresAuth(self.perform_list,
                                expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/groups/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_requires_authentication(self):
        self.assertRequiresAuth(self.perform_retrieve,
                                expected_status_code=status.HTTP_200_OK)

    def test_list_students(self):
        pass  # TODO

    def test_add_student(self):
        pass  # TODO

    def test_remove_student(self):
        pass  # TODO

    def test_list_tutors(self):
        pass  # TODO

    def test_add_tutor(self):
        pass  # TODO

    def test_remove_tutor(self):
        pass  # TODO

    def test_list_meetings(self):
        pass  # TODO

    def test_list_past_meetings(self):
        pass  # TODO

    def test_list_next_meetings(self):
        pass  # TODO

    def test_add_meeting(self):
        pass  # TODO

    def test_remove_meeting(self):
        pass  # TODO
