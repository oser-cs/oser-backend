"""School API tests."""

from django.contrib.auth import get_user_model
from rest_framework import status

from persons.models import Student
from tutoring.models import School

from tests.utils import random_email, random_uai_code, ModelAPITestCase


User = get_user_model()


class SchoolAPITest(ModelAPITestCase):
    """Test the school API."""

    model = School

    def create_data(self):
        data = {
            'uai_code': random_uai_code(),
            'name': 'Lycée Michelin',
        }
        return data

    def test_list(self):
        n_items = 5
        for _ in range(n_items):
            self.create_obj()
        url = '/api/schools/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_retrieve(self):
        obj = self.create_obj()
        url = f'/api/schools/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        obj = self.create_obj()
        url = f'/api/schools/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('uai_code', response.data)
        self.assertIn('students', response.data)
        self.assertIn('name', response.data)
        self.assertIn('url', response.data)

    def test_create(self):
        """Ensure we can create a new tutor object through the API."""
        data = self.create_data()
        names = (('John', 'Doe'), ('Alice', 'Smith'), ('Adam', 'Adam'))
        for first_name, last_name in names:
            user = User.objects.create(email=random_email(),
                                       first_name=first_name,
                                       last_name=last_name)
            Student.objects.create(user=user)
        data['students'] = Student.objects.all()
        students_serialized = [student.get_absolute_url()
                               for student in data['students']]
        data_serialized = {**data, 'students': students_serialized}

        url = '/api/schools/'
        response = self.client.post(url, data_serialized, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(School.objects.count(), 1)
        school_students = School.objects.get().students.all()
        # print(school_students)
        # print(data['students'])
        self.assertQuerysetEqual(school_students, map(repr, data['students']),
                                 ordered=False)
        self.assertEqual(School.objects.get().name, 'Lycée Michelin')
