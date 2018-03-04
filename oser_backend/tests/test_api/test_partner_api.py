"""Partner API tests."""

from django.test import TestCase
from rest_framework import status
from tests.factory import PartnerFactory
from tests.utils import HyperlinkedAPITestCase
from showcase_site.serializers import PartnerSerializer
from showcase_site.views import PartnerViewSet
from showcase_site.models import Partner


class PartnerEndpointsTest(HyperlinkedAPITestCase):
    """Test access to the key figures endpoints."""

    factory = PartnerFactory
    serializer_class = PartnerSerializer

    def perform_list(self):
        url = '/api/partners/'
        response = self.client.get(url)
        return response

    def test_list_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_list,
            user=None,
            expected_status_code=status.HTTP_200_OK)

    def perform_retrieve(self):
        obj = self.factory.create()
        url = '/api/partners/{obj.pk}/'.format(obj=obj)
        response = self.client.get(url)
        return response

    def test_retrieve_no_authentication_required(self):
        self.assertRequestResponse(
            self.perform_retrieve,
            user=None,
            expected_status_code=status.HTTP_200_OK)


class PartnerViewSetTest(TestCase):
    """Test partners viewset."""

    def test_queryset_is_active_partners_only(self):
        self.assertQuerysetEqual(
            PartnerViewSet().get_queryset(),
            Partner.objects.filter(active=True))
