"""School API tests."""

from rest_framework import status
from tutoring.factory import SchoolFactory
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
        self.assertRequestResponse(
            self.perform_list,
            user=None,
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

    def test_choices_returns_list_of_uai_codes_and_names(self):
        self.factory.create_batch(5)
        url = '/api/schools/choices/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertSetEqual(set(item), {'uai_code', 'name'})