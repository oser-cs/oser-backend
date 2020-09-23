"""Student model tests."""

from profiles.factory import StudentFactory
from profiles.models import Student
from tests.utils import ModelTestCase
from users.factory import UserFactory


class StudentTestCase(ModelTestCase):
    """Test case for Student model."""

    model = Student
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
        },
        'registration': {
            'verbose_name': "dossier d'inscription",
            'null': True,
            'blank': True,
        }
    }
    model_tests = {
        'verbose_name': 'lycéen',
    }

    @classmethod
    def setUpTestData(self):
        self.obj = StudentFactory.create()

    def test_user_relationship(self):
        self.assertEqual(self.obj, self.obj.user.student)

    def test_get_absolute_url(self):
        UserFactory.create(is_staff = True)
        self.client.force_login(staff_user)
        url = self.obj.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
