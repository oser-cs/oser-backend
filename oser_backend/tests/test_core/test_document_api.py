"""Document API tests."""

from core.factory import DocumentFactory
from core.serializers import DocumentSerializer
from tests.utils import SimpleAPITestCase
from tests.utils import SimpleReadOnlyResourceTestMixin


class DocumentEndpointsTest(
        SimpleReadOnlyResourceTestMixin, SimpleAPITestCase):
    """Test access to the documents endpoints."""

    factory = DocumentFactory
    serializer_class = DocumentSerializer

    list_url = '/api/documents/'
    retrieve_url_fmt = '/api/documents/{obj.slug}/'
