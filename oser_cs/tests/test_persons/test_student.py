"""Persons utilities tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from persons.models import Student

from tests.utils import random_email, FieldTestCase


User = get_user_model()


class StudentTestCase(TestCase):
    """Test case for Student model."""

    @classmethod
    def setUpTestData(self):
        user = User.objects.create(email=random_email())
        self.obj = Student.objects.create(
            user=user,
            address='3 Rue Pierre Martin, 75000 PARIS',
            tutoring_group=None,
        )


class StudentURLTest(StudentTestCase):
    """Test the Student absolute URL."""

    def test_get_absolute_url(self):
        response = self.client.get(f'/api/students/{self.obj.id}', follow=True)
        self.assertEqual(200, response.status_code)


class UserFieldTest(StudentTestCase, FieldTestCase):
    """Test the Student.user field."""

    model = Student
    field_name = 'user'
    tests = {
        'verbose_name': 'utilisateur',
    }

    def test_user_one_to_one_relationship(self):
        self.assertEqual(User.objects.get(), self.obj.user)


class AddressFieldTest(FieldTestCase):
    """Test the Student.address field."""

    model = Student
    field_name = 'address'
    tests = {
        'verbose_name': 'adresse',
    }
