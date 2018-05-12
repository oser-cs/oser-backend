"""Student model tests."""

from profiles.factory import StudentInTutoringGroupFactory
from profiles.models import Student
from tests.utils import ModelTestCase
from tutoring.models import School, TutoringGroup
from users.factory import UserFactory


class StudentTestCase(ModelTestCase):
    """Test case for Student model."""

    model = Student
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
        },
        'tutoring_group': {
            'verbose_name': 'groupe de tutorat',
            'null': True,
            'blank': True,
        },
        'school': {
            'verbose_name': 'lycée',
            'null': True,
            'blank': True,
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
        self.obj = StudentInTutoringGroupFactory.create()

    def test_user_relationship(self):
        self.assertEqual(self.obj, self.obj.user.student)

    def test_school_relationship(self):
        self.assertEqual(School.objects.get(), self.obj.school)
        self.assertIn(self.obj, School.objects.get().students.all())

    def test_tutoring_group_relationship(self):
        self.assertEqual(TutoringGroup.objects.get(), self.obj.tutoring_group)
        self.assertIn(self.obj, TutoringGroup.objects.get().students.all())

    def test_get_absolute_url(self):
        self.client.force_login(UserFactory.create())
        url = self.obj.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
