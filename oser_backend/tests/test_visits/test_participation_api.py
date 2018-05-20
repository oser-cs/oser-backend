"""Participation API tests."""

from rest_framework import status

from tests.utils import HyperlinkedAPITestCase
from users.factory import UserFactory
from visits.factory import VisitFactory, ParticipationFactory
from visits.serializers import ParticipationSerializer


class ParticipationEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the Participations endpoints."""

    factory = ParticipationFactory
    serializer_class = ParticipationSerializer

    @classmethod
    def setUpTestData(cls):
        """Create a bunch of users and visits to choose from."""
        UserFactory.create_batch(10)
        VisitFactory.create_batch(10)
        cls.factory.create_batch(5)

    def perform_create(self):
        obj = self.factory.build()
        url = '/api/participations/'
        data = {
            'user': obj.user.id,
            'visit': obj.visit.id,
        }
        response = self.client.post(url, data, format='json')
        return response

    def test_create_authentication_required(self):
        self.assertRequiresAuth(self.perform_create,
                                expected_status_code=status.HTTP_201_CREATED)

    def perform_delete(self):
        obj = self.factory.create()
        url = '/api/participations/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url, format='json')
        return response

    def test_delete_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_delete,
            expected_status_code=status.HTTP_204_NO_CONTENT)
