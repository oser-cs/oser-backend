"""Partner model tests."""

from django.utils.timezone import now

from showcase_site.factory import PartnerFactory
from showcase_site.models import Partner
from tests.utils import ModelTestCase


class PartnerTest(ModelTestCase):
    """Test the Partner model."""

    model = Partner
    field_tests = {
        'name': {
            'verbose_name': 'nom',
            'max_length': 200,
        },
        'logo': {
            'blank': False,
        },
        'website': {
            'verbose_name': 'site internet',
            'blank': False,
        },
        'premium': {
            'verbose_name': 'partenaire privilégié',
            'default': False,
        },
        'active': {
            'verbose_name': 'actif',
            'default': True,
        },
        'start_date': {
            'verbose_name': 'début du partenariat',
            'default': now,
        }
    }
    model_tests = {
        'verbose_name': 'partenaire',
        'ordering': ('-active', '-premium', '-start_date', 'name',),
    }

    def setUp(self):
        self.obj = PartnerFactory.create()

    def test_str_is_name(self):
        self.assertEqual(str(self.obj), self.obj.name)
