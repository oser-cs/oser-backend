"""Registration model tests."""

from register.models import Registration
from register.factory import RegistrationFactory
from tests.utils import ModelTestCase


class RegistrationTest(ModelTestCase):
    """Test the Registration model."""

    model = Registration
    field_tests = {
        'first_name': {
            'max_length': 50,
            'verbose_name': 'prénom',
        },
        'last_name': {
            'max_length': 50,
            'verbose_name': 'nom',
        },
        'date_of_birth': {
            'blank': True,
            'null': True,
            'verbose_name': 'date de naissance',
        },
        'phone': {
            'max_length': 30,
            'blank': True,
            'null': True,
            'verbose_name': 'téléphone',
        },
        'email': {
            'verbose_name': 'adresse email',
        },
        'submitted': {
            'verbose_name': 'envoyé le',
            'auto_now_add': True,
        },
        'validated': {
            'verbose_name': 'validé',
            'default': False,
        },
        'address': {
            'blank': True,
            'null': True,
            'verbose_name': 'adresse',
        },
        'emergency_contact': {
            'blank': True,
            'null': True,
            'verbose_name': "contact d'urgence",
        },
    }
    model_tests = {
        'ordering': ('-submitted',),
        'verbose_name': "dossier d'inscription",
        'verbose_name_plural': "dossiers d'inscription",
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = RegistrationFactory.create()
