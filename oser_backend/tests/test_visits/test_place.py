"""Place model tests."""

from visits.models import Place
from tests.factory import PlaceFactory
from tests.utils import ModelTestCase


class PlaceTest(ModelTestCase):
    """Test the Place model."""

    model = Place
    field_tests = {
        'name': {
            'verbose_name': 'nom',
            'max_length': 200,
        },
        'address': {
            'verbose_name': 'adresse',
            'max_length': 200,
        },
    }
    model_tests = {
        'verbose_name': 'lieu',
        'verbose_name_plural': 'lieux',
        'ordering': ('name',),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = PlaceFactory.create()

    def test_get_absolute_url(self):
        url = self.obj.get_absolute_url()
        expected = '/api/places/{}/'.format(self.obj.pk)
        self.assertEqual(url, expected)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_str_is_name(self):
        self.assertEqual(str(self.obj), str(self.obj.name))
