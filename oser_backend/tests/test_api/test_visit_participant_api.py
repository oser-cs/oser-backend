"""VisitParticipant API tests."""

from rest_framework import status
from tests.factory import VisitParticipantFactory
from tests.factory import VisitFactory, StudentFactory
from tests.utils import HyperlinkedAPITestCase


class VisitParticipantEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the VisitParticipants endpoints."""

    factory = VisitParticipantFactory

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create a bunch of students and visits to choose from
        StudentFactory.create_batch(10)
        VisitFactory.create_batch(10)
        cls.factory.create_batch(5)

    def perform_list(self):
        url = '/api/visit-participants/'
        response = self.client.get(url)
        return response

    def test_list_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_list, expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/visit-participants/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_retrieve, expected_status_code=status.HTTP_200_OK)
