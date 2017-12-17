"""Student model tests."""

from django.contrib.auth import get_user_model
from users.models import Student

from tests.utils import random_email, ModelTestCase


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

    @classmethod
    def setUpTestData(self):
        user = User.objects.create(email=random_email())
        self.obj = Student.objects.create(
            user=user,
            address='3 Rue Pierre Martin, 75000 PARIS',
            tutoring_group=None,
        )

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/students/{self.obj.pk}', follow=True)
        self.assertEqual(200, response.status_code)

    def test_user_one_to_one_relationship(self):
        self.assertEqual(User.objects.get(), self.obj.user)
