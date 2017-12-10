"""SchoolStaffMember model tests."""

from django.contrib.auth import get_user_model
from persons.models import SchoolStaffMember
from tutoring.models import School

from tests.utils import random_email, ModelTestCase


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
        user = User.objects.create(email=random_email())
        school = School.objects.create()
        self.obj = SchoolStaffMember.objects.create(
            user=user,
            school=school,
            role='directeur',
        )

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/schoolstaffmembers/{self.obj.pk}',
                                   follow=True)
        self.assertEqual(200, response.status_code)

    def test_user_one_to_one_relationship(self):
        self.assertEqual(User.objects.get(), self.obj.user)

    def test_school_one_to_many_relationship(self):
        self.assertEqual(School.objects.get(), self.obj.school)
        self.assertIn(self.obj, School.objects.get().staffmembers.all())
