"""Student model tests."""

from django.contrib.auth import get_user_model
from users.models import Student

from tests.factory import StudentFactory
from tests.utils import ModelTestCase


User = get_user_model()


class StudentTestCase(ModelTestCase):
    """Test case for Student model."""

    model = Student
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
        },
        'address': {
            'verbose_name': 'adresse',
            'blank': False,
        }
    }
    model_tests = {
        'verbose_name': 'lycéen',
    }

    @classmethod
    def setUpTestData(self):
        self.obj = StudentFactory.create()

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/students/{self.obj.pk}/')
        self.assertEqual(200, response.status_code)
