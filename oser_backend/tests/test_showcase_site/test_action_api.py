"""Action API tests."""

from showcase_site.factory import ActionFactory
from showcase_site.serializers import ActionSerializer
from tests.utils import SimpleAPITestCase

from tests.utils import SimpleReadOnlyResourceTestMixin


class ActionEndpointsTest(SimpleReadOnlyResourceTestMixin,
                          SimpleAPITestCase):
    """Test access to the actions endpoints."""

    factory = ActionFactory
    serializer_class = ActionSerializer

    list_url = '/api/actions/'
    retrieve_url_fmt = '/api/actions/{obj.pk}/'
