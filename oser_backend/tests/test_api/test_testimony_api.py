"""Testimony API tests."""

from rest_framework import status

from showcase_site.factory import TestimonyFactory
from showcase_site.serializers import TestimonySerializer
from tests.utils import HyperlinkedAPITestCase


class TestimonyEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the testimonies endpoints."""

    factory = TestimonyFactory
    serializer_class = TestimonySerializer

    def perform_list(self):
        url = '/api/testimonies/'
        response = self.client.get(url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/testimonies/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)
