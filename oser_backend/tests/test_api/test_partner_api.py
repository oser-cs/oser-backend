"""Partner API tests."""

from showcase_site.factory import PartnerFactory
from showcase_site.serializers import PartnerSerializer
from tests.utils import SimpleAPITestCase
from .mixins import SimpleReadOnlyResourceTestMixin


class PartnerEndpointsTest(
        SimpleReadOnlyResourceTestMixin, SimpleAPITestCase):
    """Test access to the partners endpoints."""

    factory = PartnerFactory
    serializer_class = PartnerSerializer

    list_url = '/api/partners/'
    retrieve_url_fmt = '/api/partners/{obj.pk}/'
