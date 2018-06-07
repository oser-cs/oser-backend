"""Participation API tests."""

from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase
from tests.utils import HyperlinkedAPITestCase

from users.factory import UserFactory
from visits.factory import ParticipationFactory, VisitFactory
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


class ParticipationCancelledTest(APITestCase):
    """Test endpoint to notify a user does not participate to visit anymore."""

    def setUp(self):
        self.user = UserFactory.create()
        VisitFactory.create()
        self.obj = ParticipationFactory.create()

    def perform(self):
        data = {'reason': 'Désolé, je ne peux plus venir.'}
        url = f'/api/participations/{self.obj.pk}/notify_cancelled/'
        response = self.client.post(url, data=data, format='json')
        return response

    def test(self):
        self.client.force_login(self.user)
        response = self.perform()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)
        self.assertSetEqual(set(response.data), {'sent', 'timestamp'})
        self.assertTrue(response.data['sent'])
