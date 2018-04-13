"""Category API tests."""

from showcase_site.factory import CategoryFactory
from showcase_site.serializers import CategorySerializer
from tests.utils import SimpleAPITestCase

from tests.utils import SimpleReadOnlyResourceTestMixin


class CategoryEndpointsTest(
        SimpleReadOnlyResourceTestMixin, SimpleAPITestCase):
    """Test access to the categories endpoints."""

    factory = CategoryFactory
    serializer_class = CategorySerializer

    list_url = '/api/categories/'
    retrieve_url_fmt = '/api/categories/{obj.pk}/'
