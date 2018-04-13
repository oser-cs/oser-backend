"""Testimony API tests."""

from showcase_site.factory import TestimonyFactory
from showcase_site.serializers import TestimonySerializer
from tests.utils import SimpleAPITestCase
from tests.utils import SimpleReadOnlyResourceTestMixin


class TestimonyEndpointsTest(
        SimpleReadOnlyResourceTestMixin, SimpleAPITestCase):
    """Test access to the testimonies endpoints."""

    factory = TestimonyFactory
    serializer_class = TestimonySerializer

    list_url = '/api/testimonies/'
    retrieve_url_fmt = '/api/testimonies/{obj.pk}/'
