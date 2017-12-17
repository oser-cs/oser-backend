"""Users API tests."""

from datetime import date

from django.utils.formats import date_format
from django.contrib.auth import get_user_model
from rest_framework import status

from users.models import Student

from tests.utils import random_email
from tests.utils import ModelAPITestCase


User = get_user_model()


class UserAPITest(ModelAPITestCase):
    """Test the users API."""

    model = User

    def create_data(self):
        data = {
            'email': random_email(),
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '0601020304',
            'date_of_birth': date(2000, 1, 1),
            'profile_type': 'student',
        }
        return data

    def test_list(self):
        n_items = 5
        for _ in range(n_items):
            self.create_obj()
        url = '/api/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_retrieve(self):
        obj = self.create_obj()
        url = f'/api/users/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        obj = self.create_obj()
        url = f'/api/users/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        keys = (
            'id',
            'url',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'date_of_birth',
            'gender',
            'profile',
        )
        for key in keys:
            self.assertIn(key, response.data)

    def test_create(self):
        url = '/api/users/'
        data = {
            'email': 'john.doe@example.net',
            'password': 'hello25',
            'first_name': 'john',
            'last_name': 'doe',
            'gender': User.MALE,
            'phone_number': '0601020304',
            'date_of_birth': '01/01/2000',
            'profile_type': 'student',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertIsInstance(user.profile, Student)
        for key in data:
            if key == 'password':
                continue
            elif key == 'date_of_birth':
                date_of_birth = date_format(user.date_of_birth, 'd/m/Y')
                self.assertEqual(date_of_birth, data['date_of_birth'])
                continue
            if key == 'profile_type':
                continue
            self.assertEqual(getattr(user, key), data[key])
