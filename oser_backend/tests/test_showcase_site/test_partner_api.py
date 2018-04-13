"""Partner API tests."""

from showcase_site.models import Partner
from showcase_site.factory import PartnerFactory
from showcase_site.serializers import PartnerSerializer
from tests.utils import SimpleAPITestCase
from tests.utils import SimpleReadOnlyResourceTestMixin


class PartnerEndpointsTest(
        SimpleReadOnlyResourceTestMixin, SimpleAPITestCase):
    """Test access to the partners endpoints."""

    factory = PartnerFactory
    serializer_class = PartnerSerializer

    list_url = '/api/partners/'
    retrieve_url_fmt = '/api/partners/{obj.pk}/'
    # only active partners are exposed by API => ensure object
    # created in perform_retrieve() is an active partner.
    retrieve_kwargs = {'active': True}

    @classmethod
    def setUpTestData(cls):
        cls.factory.create_batch(5)

    def test_only_active_partners_listed(self):
        response = self.perform_list()
        self.assertEqual(response.status_code, 200)
        for partner_data in response.data:
            partner = Partner.objects.get(pk=partner_data['id'])
            self.assertTrue(partner.active)
