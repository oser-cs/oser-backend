"""KeyFigure API tests."""

from showcase_site.factory import KeyFigureFactory
from showcase_site.serializers import KeyFigureSerializer
from tests.utils import SimpleAPITestCase
from tests.utils import SimpleReadOnlyResourceTestMixin


class KeyFigureEndpointsTest(
        SimpleReadOnlyResourceTestMixin, SimpleAPITestCase):
    """Test access to the key figures endpoints."""

    factory = KeyFigureFactory
    serializer_class = KeyFigureSerializer

    list_url = '/api/keyfigures/'
    retrieve_url_fmt = '/api/keyfigures/{obj.pk}/'
