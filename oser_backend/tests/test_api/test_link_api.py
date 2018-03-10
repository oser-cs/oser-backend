"""Link API tests."""

from rest_framework import status

from core.factory import LinkFactory
from core.serializers import LinkSerializer
from tests.utils import HyperlinkedAPITestCase


class LinkEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the links endpoints."""

    factory = LinkFactory
    serializer_class = LinkSerializer

    def perform_list(self):
        url = '/api/links/'
        response = self.client.get(url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/links/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)
