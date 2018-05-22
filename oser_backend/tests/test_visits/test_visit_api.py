"""Visit API tests."""

from django.test import TestCase
from rest_framework import status
from tests.utils import SerializerTestCaseMixin, SimpleAPITestCase

from users.factory import UserFactory
from visits.factory import VisitFactory
from visits.models import Participation
from visits.serializers import VisitSerializer


class VisitEndpointsTest(SimpleAPITestCase):
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

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/visits/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_retrieve, expected_status_code=status.HTTP_200_OK)

    def perform_retrieve_with_participant(self):
        obj = self.factory.create()
        user = UserFactory.create()
        Participation.objects.create(visit=obj, user=user)
        self.client.force_login(user=user)
        response = self.perform_retrieve(obj=obj)
        return response

    def test_retrieve_with_participant(self):
        response = self.perform_retrieve_with_participant()
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         response.data)


class VisitSerializerTestCase(SerializerTestCaseMixin, TestCase):
    """Test the VisitSerializer."""

    serializer_class = VisitSerializer
    factory_class = VisitFactory
    request_url = '/api/visits/'

    expected_fields = (
        'id', 'url',
        'title', 'summary', 'description',
        'place', 'date', 'start_time', 'end_time', 'meeting',
        'passed', 'deadline', 'registrations_open',
        'participants', 'organizers',
        'image', 'fact_sheet', 'permission',
    )
