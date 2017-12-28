"""Tutor model tests."""

from django.contrib.auth import get_user_model
from users.models import Tutor

from tests.factory import TutorFactory
from tests.utils import ModelTestCase


User = get_user_model()


class TutorTestCase(ModelTestCase):
    """Test case for Tutor model."""

    model = Tutor
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
        },
        'promotion': {
            'blank': False,
        }
    }
    model_tests = {
        'verbose_name': 'tuteur',
    }

    @classmethod
    def setUpTestData(self):
        self.obj = TutorFactory.create()

    def test_get_absolute_url(self):
        url = self.obj.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
