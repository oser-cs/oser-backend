"""SchoolStaffMember model tests."""

from tests.test_users.mixins import ProfileTestMixin
from tests.utils import ModelTestCase
from tutoring.models import School
from users.factory import SchoolStaffMemberFactory
from users.models import SchoolStaffMember


class SchoolStaffMemberTestCase(ProfileTestMixin, ModelTestCase):
    """Test case for SchoolStaffMember model."""

    model = SchoolStaffMember
    field_tests = {
        'role': {
            'verbose_name': 'rôle',
            'max_length': 100,
        },
    }
    model_tests = {
        'verbose_name': 'membre du personnel de lycée',
        'verbose_name_plural': 'membres du personnel de lycée',
    }

    @classmethod
    def setUpTestData(self):
        self.obj = SchoolStaffMemberFactory.create()

    def test_school_one_to_many_relationship(self):
        self.assertEqual(School.objects.get(), self.obj.school)
        self.assertIn(self.obj, School.objects.get().staffmembers.all())
