"""Student API tests."""

from django.contrib.auth import get_user_model
from rest_framework import status

from users.models import Student
from tutoring.models import School, TutoringGroup

from tests.utils import random_email, random_uai_code, ModelAPITestCase


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
        url = '/api/students/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_retrieve(self):
        student = self.create_obj()
        url = f'/api/students/{student.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        student = self.create_obj()
        url = f'/api/students/{student.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        keys = (
            'user', 'address', 'tutoring_group', 'school', 'url',
        )
        for key in keys:
            self.assertIn(key, response.data)

    def test_create(self):
        """Ensure we can create a new student object through the API."""
        data = self.create_data()
        hyperlinked = 'user school tutoring_group'.split()
        data_serialized = {
            key: key in hyperlinked and value.get_absolute_url() or value
            for key, value in data.items()
        }
        url = '/api/students/'

        response = self.client.post(url, data_serialized, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().user, data.get('user'))
        self.assertEqual(Student.objects.get().school, data.get('school'))
        self.assertEqual(Student.objects.get().tutoring_group,
                         data.get('tutoring_group'))
