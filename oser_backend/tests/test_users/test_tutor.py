"""Tutor model tests."""

from tests.test_users.mixins import ProfileTestMixin
from tests.utils import ModelTestCase
from users.factory import TutorFactory
from users.models import Tutor


class TutorTestCase(ProfileTestMixin, ModelTestCase):
    """Test case for Tutor model."""

    model = Tutor
    field_tests = {
        'promotion': {
            'blank': False,
        }
    }
    model_tests = {
        'verbose_name': 'tuteur',
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = TutorFactory.create()

    def test_make_staff_signal(self):
        self.assertTrue(self.obj.user.is_staff)
