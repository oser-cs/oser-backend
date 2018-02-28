"""VisitParticipant API tests."""

from django.test import TestCase
from rest_framework import status
from tests.factory import VisitParticipantFactory
from tests.factory import VisitFactory, UserFactory
from tests.utils import HyperlinkedAPITestCase
from visits.serializers import (
    VisitParticipantWriteSerializer, VisitParticipantIdentifySerializer)
from visits.models import VisitParticipant


class VisitParticipantEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the VisitParticipants endpoints."""

    factory = VisitParticipantFactory
    serializer_class = VisitParticipantWriteSerializer

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create a bunch of users and visits to choose from
        UserFactory.create_batch(10)
        VisitFactory.create_batch(10)
        cls.factory.create_batch(5)

    def perform_list(self):
        url = '/api/visit-participants/'
        response = self.client.get(url)
        return response

    def test_list_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_list, expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/visit-participants/{obj.visit.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_retrieve, expected_status_code=status.HTTP_200_OK)

    def test_retrieve_returns_participants_of_visit(self):
        obj = self.factory.create()
        response = self.perform_retrieve(obj=obj)
        self.assertEqual(
            len(response.json()),
            VisitParticipant.objects.filter(visit=obj.visit).count())

    def perform_create(self):
        obj = self.factory.build()
        url = '/api/visit-participants/'
        data = self.serialize(obj, 'post', url)
        response = self.client.post(url, data, format='json')
        return response

    def test_create_authentication_required(self):
        self.assertRequiresAuth(self.perform_create,
                                expected_status_code=status.HTTP_201_CREATED)

    def perform_get_id(self, obj=None):
        if obj is None:
            obj = self.factory.create()
        url = '/api/visit-participants/get-id/'
        serializer = VisitParticipantIdentifySerializer(obj)
        data = serializer.data
        response = self.client.put(url, data, format='json')
        return response

    def test_get_id_authentication_required(self):
        self.assertRequiresAuth(self.perform_get_id,
                                expected_status_code=status.HTTP_200_OK)

    def perform_delete(self):
        obj = self.factory.create()
        url = '/api/visit-participants/{obj.pk}/'.format(obj=obj)
        response = self.client.delete(url, format='json')
        return response

    def test_delete_authentication_required(self):
        self.assertRequiresAuth(
            self.perform_delete,
            expected_status_code=status.HTTP_204_NO_CONTENT)


class VisitParticipantWriteSerializerTest(TestCase):
    """Test the write serializer for VisitParticipant."""

    def setUp(self):
        self.serializer = VisitParticipantWriteSerializer()

    # Following 2 tests = regression tests. The source needs to be defined
    # otherwise DRF will not convert them to User and Visit objects.
    # As a result, deserialization will fail.

    def test_user_id_source_is_defined(self):
        self.assertEqual(self.serializer.fields['user_id'].source,
                         'user')

    def test_visit_id_source_is_defined(self):
        self.assertEqual(self.serializer.fields['visit_id'].source,
                         'visit')
