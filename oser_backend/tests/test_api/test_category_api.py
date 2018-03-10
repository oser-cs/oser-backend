"""Category API tests."""

from rest_framework import status

from showcase_site.factory import CategoryFactory
from showcase_site.serializers import CategorySerializer
from tests.utils import HyperlinkedAPITestCase


class CategoryEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the categories endpoints."""

    factory = CategoryFactory
    serializer_class = CategorySerializer

    def perform_list(self):
        url = '/api/categories/'
        response = self.client.get(url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/categories/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)
