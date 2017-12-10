"""Student API tests."""

from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from tests.utils import random_email
from persons.models import Student
from tutoring.models import School, TutoringGroup


User = get_user_model()


class StudentAPITest(APITestCase):
    """Test the student API."""

    def _create_student(self, **kwargs):
        user = User.objects.create(email=random_email())
        kwargs.setdefault('user', user)
        return Student.objects.create(**kwargs)

    def test_list(self):
        for _ in range(5):
            self._create_student()
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_retrieve(self):
        student = self._create_student()
        response = self.client.get(f'/api/students/{student.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        student = self._create_student()
        response = self.client.get(f'/api/students/{student.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('address', response.data)
        self.assertIn('tutoring_group', response.data)
        self.assertIn('school', response.data)

    def test_create(self):
        """Ensure we can create a new student object through the API."""
        user = User.objects.create(email=random_email())
        school = School.objects.create(uai_code='1234567A')
        tutoring_group = TutoringGroup.objects.create()

        url = reverse('api:student-list')
        data = {
            'user': user.get_absolute_url(),
            'address': '3 rue des Acacias, 75000 PARIS',
            'school': school.get_absolute_url(),
            'tutoring_group': tutoring_group.get_absolute_url(),
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().user, user)
        self.assertEqual(Student.objects.get().school, school)
