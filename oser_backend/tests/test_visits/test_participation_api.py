"""Participation API tests."""

from django.test import TestCase
from rest_framework import status

from tests.utils import HyperlinkedAPITestCase
from users.factory import UserFactory
from visits.factory import VisitFactory, ParticipationFactory
from visits.models import Participation
from visits.serializers import (ParticipationIdentifySerializer,
                                ParticipationWriteSerializer)


class ParticipationEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the Participations endpoints."""

    factory = ParticipationFactory
    serializer_class = ParticipationWriteSerializer

    @classmethod
    def setUpTestData(cls):
        """Create a bunch of users and visits to choose from."""
        UserFactory.create_batch(10)
        VisitFactory.create_batch(10)
        cls.factory.create_batch(5)

    def perform_create(self):
        obj = self.factory.build()
        url = '/api/participants/'
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def test_create_authentication_required(self):
        self.assertRequiresAuth(self.perform_create,
                                expected_status_code=status.HTTP_201_CREATED)

    def perform_get_id(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/participants/get-id/'
        serializer = ParticipationIdentifySerializer(obj)
        data = serializer.data
        response = self.client.put(url, data, format='json')
        return response

    def test_get_id_authentication_required(self):
        self.assertRequiresAuth(self.perform_get_id,
                                expected_status_code=status.HTTP_200_OK)

    def perform_delete(self):
        obj = self.factory.create()
        url = '/api/participants/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url, format='json')
        return response

    def test_delete_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_delete,
            expected_status_code=status.HTTP_204_NO_CONTENT)


class ParticipationWriteSerializerTest(TestCase):
    """Test the write serializer for Participation."""

    def setUp(self):
        self.serializer = ParticipationWriteSerializer()

    # Following 2 tests = regression tests. The source needs to be defined
    # otherwise DRF will not convert them to User and Visit objects.
    # As a result, deserialization will fail.

    def test_user_id_source_is_defined(self):
        self.assertEqual(self.serializer.fields['user_id'].source,
                         'user')

    def test_visit_id_source_is_defined(self):
        self.assertEqual(self.serializer.fields['visit_id'].source,
                         'visit')
