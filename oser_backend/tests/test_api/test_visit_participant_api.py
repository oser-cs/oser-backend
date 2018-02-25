"""VisitParticipant API tests."""

from django.test import TestCase
from rest_framework import status
from tests.factory import VisitParticipantFactory
from tests.factory import VisitFactory, StudentFactory, UserFactory
from tests.utils import HyperlinkedAPITestCase
from visits.serializers import VisitParticipantWriteSerializer
from visits.models import VisitParticipant


class VisitParticipantEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the VisitParticipants endpoints."""

    factory = VisitParticipantFactory
    serializer_class = VisitParticipantWriteSerializer

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create a bunch of students and visits to choose from
        StudentFactory.create_batch(10)
        VisitFactory.create_batch(10)
        cls.factory.create_batch(5)

    # def perform_list(self):
    #     url = '/api/visit-participants/'
    #     response = self.client.get(url)
    #     return response
    #
    # def test_list_authentication_required(self):
    #     self.assertRequiresAuth(
    #         self.perform_list, expected_status_code=status.HTTP_200_OK)

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
        self.assertRequiresAuth(
            self.perform_create, expected_status_code=status.HTTP_201_CREATED)


class WriteSerializerTest(TestCase):
    """Test the write serializer for VisitParticipant."""

    def test_id_fields_sources_are_defined(self):
        """Test that student and visit fields define a source parameter.

        This is mostly a regression test. Without it, serialization will
        fail.
        """
        serializer = VisitParticipantWriteSerializer()
        self.assertEqual(serializer.fields['student_id'].source, 'student')
        self.assertEqual(serializer.fields['visit_id'].source, 'visit')
