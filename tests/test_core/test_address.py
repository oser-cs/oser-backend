"""Address model tests."""

from core.models import Address
from core.factory import AddressFactory
from tests.utils import ModelTestCase


class AddressTest(ModelTestCase):
    """Test the Address model."""

    model = Address
    field_tests = {
        'line1': {
            'verbose_name': 'ligne 1',
            'blank': False,
            'max_length': 300,
        },
        'line2': {
            'verbose_name': 'ligne 2',
            'max_length': 300,
            'blank': True,
            'default': '',
        },
        'post_code': {
            'verbose_name': 'code postal',
            'blank': False,
            'max_length': 20,
        },
        'city': {
            'verbose_name': 'ville',
            'blank': False,
            'max_length': 100,
        },
        'country': {
            'verbose_name': 'pays',
            'blank': False,
            'default': 'FR',
        },
    }
    model_tests = {
        'verbose_name': 'adresse',
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = AddressFactory.create(
            line1='3 Rue Joliot Curie',
            post_code='91190',
            city='Gif-sur-Yvette',
        )

    def test_str(self):
        expected = '3 Rue Joliot Curie, 91190 Gif-sur-Yvette, France'
        self.assertEqual(expected, str(self.obj))
