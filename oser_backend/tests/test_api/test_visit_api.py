"""Visit API tests."""

from rest_framework import status
from tests.factory import VisitFactory, UserFactory
from tests.utils import HyperlinkedAPITestCase
from visits.serializers import VisitSerializer


class VisitEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the visits endpoints."""

    factory = VisitFactory
    serializer_class = VisitSerializer

    def perform_list(self):
        url = '/api/visits/'
        response = self.client.get(url)
        return response

    def test_list_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_list, expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/visits/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_retrieve, expected_status_code=status.HTTP_200_OK)

    def perform_list_participants(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/visits/{obj.pk}/participants/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_participants_contains_participants_of_visit(self):
        self.client.force_login(UserFactory.create())
        obj = self.factory.create()
        response = self.perform_list_participants(obj=obj)
        num_participants = obj.participants.all().count()
        self.assertEqual(len(response.data), num_participants)

    def test_participants_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_list_participants,
            expected_status_code=status.HTTP_200_OK)
