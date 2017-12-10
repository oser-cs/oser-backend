"""Student API tests."""

from django.shortcuts import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from tests.utils import random_email, random_uai_code, ModelAPITestCase
from persons.models import Student
from tutoring.models import School, TutoringGroup


User = get_user_model()


class StudentAPITest(ModelAPITestCase):
    """Test the student API."""

    model = Student

    def create_data(self):
        user = User.objects.create(email=random_email())
        school = School.objects.create(uai_code=random_uai_code())
        tutoring_group = TutoringGroup.objects.create()
        data = {
            'user': user,
            'address': '3 Place de la Barre, 59000 LILLE',
            'school': school,
            'tutoring_group': tutoring_group,
        }
        return data

    def test_list(self):
        n_items = 5
        for _ in range(n_items):
            self.create_obj()
        url = reverse('api:student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_retrieve(self):
        student = self.create_obj()
        url = reverse('api:student-detail', args=[str(student.pk)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        student = self.create_obj()
        url = reverse('api:student-detail', args=[str(student.pk)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('address', response.data)
        self.assertIn('tutoring_group', response.data)
        self.assertIn('school', response.data)

    def test_create(self):
        """Ensure we can create a new student object through the API."""
        data = self.create_data()
        hyperlinked = 'user school tutoring_group'.split()
        data_serialized = {
            key: key in hyperlinked and value.get_absolute_url() or value
            for key, value in data.items()
        }
        url = reverse('api:student-list')

        response = self.client.post(url, data_serialized, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().user, data.get('user'))
        self.assertEqual(Student.objects.get().school, data.get('school'))
        self.assertEqual(Student.objects.get().tutoring_group,
                         data.get('tutoring_group'))
