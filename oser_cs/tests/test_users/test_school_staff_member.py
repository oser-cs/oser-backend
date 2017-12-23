"""SchoolStaffMember model tests."""

from django.contrib.auth import get_user_model
from users.models import SchoolStaffMember
from tutoring.models import School
from tests.factory import SchoolStaffMemberFactory
from tests.utils import ModelTestCase


User = get_user_model()


class SchoolStaffMemberTestCase(ModelTestCase):
    """Test case for SchoolStaffMember model."""

    model = SchoolStaffMember
    field_tests = {
        'user': {
            'verbose_name': 'utilisateur',
        },
        'role': {
            'verbose_name': 'rôle',
            'max_length': 100,
        },
    }

    @classmethod
    def setUpTestData(self):
        self.obj = SchoolStaffMemberFactory.create()

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/schoolstaffmembers/{self.obj.pk}/')
        self.assertEqual(200, response.status_code)

    def test_school_one_to_many_relationship(self):
        self.assertEqual(School.objects.get(), self.obj.school)
        self.assertIn(self.obj, School.objects.get().staffmembers.all())
