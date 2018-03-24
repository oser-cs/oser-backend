"""Document API tests."""

from rest_framework import status

from core.factory import DocumentFactory
from core.serializers import DocumentSerializer
from tests.utils import HyperlinkedAPITestCase


class ArticleEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the articles endpoints."""

    factory = DocumentFactory
    serializer_class = DocumentSerializer

    def perform_list(self):
        url = '/api/documents/'
        response = self.client.get(url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/documents/{obj.slug}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)
