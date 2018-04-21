"""Tutor model tests."""

from tests.utils import ModelTestCase
from users.factory import TutorFactory, UserFactory
from users.models import Tutor


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
    def setUpTestData(cls):
        cls.obj = TutorFactory.create()

    def test_user_relationship(self):
        self.assertEqual(self.obj, self.obj.user.tutor)

    def test_make_staff_signal(self):
        self.assertTrue(self.obj.user.is_staff)

    def test_get_absolute_url(self):
        self.client.force_login(UserFactory.create())
        url = self.obj.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
