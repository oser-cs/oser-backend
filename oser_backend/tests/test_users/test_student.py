"""Student model tests."""

from tests.factory import StudentFactory
from tests.test_users.mixins import ProfileTestMixin
from tests.utils import ModelTestCase

from tutoring.models import School, TutoringGroup
from users.models import Student


class StudentTestCase(ProfileTestMixin, ModelTestCase):
    """Test case for Student model."""

    model = Student
    field_tests = {
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

    def test_school_relationship(self):
        self.assertEqual(School.objects.get(), self.obj.school)
        self.assertIn(self.obj, School.objects.get().students.all())

    def test_tutoring_group_relationship(self):
        self.assertEqual(TutoringGroup.objects.get(), self.obj.tutoring_group)
        self.assertIn(self.obj, TutoringGroup.objects.get().students.all())

    def test_visits_relationship(self):
        self.assertEqual(self.obj.visit_set.all().count(), 0)

    # TODO test 1-n relationship with tutoring group
