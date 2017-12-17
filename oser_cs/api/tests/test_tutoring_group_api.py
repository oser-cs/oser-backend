"""School API tests."""

from django.contrib.auth import get_user_model
from rest_framework import status

from users.models import Student, Tutor
from tutoring.models import TutoringGroup, School

from tests.utils import random_email, random_uai_code, ModelAPITestCase


User = get_user_model()


class TutoringGroupAPITest(ModelAPITestCase):
    """Test the tutoring group API."""

    model = TutoringGroup

    def create_data(self):
        school = School.objects.create(uai_code=random_uai_code(),
                                       name='Lycée Matisse')
        for _ in range(3):
            user = User.objects.create(email=random_email())
            Student.objects.create(user=user)
        for _ in range(3):
            user = User.objects.create(email=random_email())
            Tutor.objects.create(user=user)
        data = {
            'name': 'Matisse Secondes',
            'school': school,
        }
        return data

    def create_obj(self, **kwargs):
        obj = super().create_obj(**kwargs)
        for student in Student.objects.all():
            obj.students.add(student)
        for tutor in Tutor.objects.all():
            obj.tutors.add(tutor)
        return obj

    def test_list(self):
        n_items = 5
        for _ in range(n_items):
            self.create_obj()
        url = '/api/tutoring/groups/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_retrieve(self):
        obj = self.create_obj()
        url = f'/api/tutoring/groups/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        obj = self.create_obj()
        url = f'/api/tutoring/groups/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        keys = (
            'id', 'url', 'name', 'tutors', 'students',
            'tutors_count', 'students_count',
            'school',
        )
        for key in keys:
            self.assertIn(key, response.data)

    def test_create(self):
        """Ensure we can create a new object through the API."""
        data = self.create_data()
        data['tutors'] = Tutor.objects.all()
        data['students'] = Student.objects.all()

        students_serialized = [student.get_absolute_url()
                               for student in data['students']]
        tutors_serialized = [tutor.get_absolute_url()
                             for tutor in data['tutors']]
        data_serialized = {
            **data,
            'students': students_serialized,
            'tutors': tutors_serialized,
            'school': data['school'].get_absolute_url()
        }

        url = '/api/tutoring/groups/'
        response = self.client.post(url, data_serialized, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(TutoringGroup.objects.count(), 1)
        group = TutoringGroup.objects.get()
        students = group.students.all()
        tutors = group.tutors.all()
        self.assertQuerysetEqual(students, map(repr, data['students']),
                                 ordered=False)
        self.assertQuerysetEqual(tutors, map(repr, data['tutors']),
                                 ordered=False)
        self.assertEqual(group.school, data['school'])
        self.assertEqual(group.name, 'Matisse Secondes')
