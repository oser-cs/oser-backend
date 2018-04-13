"""EmergencyContact model tests."""

from register.models import EmergencyContact
from register.factory import EmergencyContactFactory
from tests.utils import ModelTestCase


class EmergencyContactTest(ModelTestCase):
    """Test the EmergencyContact model."""

    model = EmergencyContact
    field_tests = {
        'first_name': {
            'max_length': 50,
            'verbose_name': 'prénom',
            'blank': True,
        },
        'last_name': {
            'max_length': 50,
            'verbose_name': 'nom',
            'blank': True,
        },
        'contact': {
            'max_length': 100,
        },
    }
    model_tests = {
        'ordering': ('last_name', 'first_name',),
        'verbose_name': "contact d'urgence",
        'verbose_name_plural': "contacts d'urgence",
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = EmergencyContactFactory.create()

    def test_str(self):
        expected = '{o.first_name} {o.last_name}'.format(o=self.obj)
        self.assertEqual(expected, str(self.obj))
