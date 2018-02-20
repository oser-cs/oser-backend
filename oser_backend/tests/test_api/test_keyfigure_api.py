"""KeyFigure API tests."""

from rest_framework import status
from tests.factory import KeyFigureFactory
from tests.utils import HyperlinkedAPITestCase
from showcase_site.serializers import KeyFigureSerializer


class KeyFigureEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the key figures endpoints."""

    factory = KeyFigureFactory
    serializer_class = KeyFigureSerializer

    def perform_list(self):
        url = '/api/keyfigures/'
        response = self.client.get(url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/keyfigures/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)
