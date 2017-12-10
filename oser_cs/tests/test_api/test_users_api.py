"""Users API tests."""

from datetime import date

from django.utils.formats import date_format
from django.shortcuts import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

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
        }
        return data

    def test_data_has_expected_values(self):
        obj = self.create_obj()
        url = reverse('api:user-detail', args=[str(obj.pk)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(obj.email, data['email'])
        self.assertEqual(obj.first_name, data['first_name'])
        self.assertEqual(obj.last_name, data['last_name'])
        self.assertEqual(obj.phone_number, data['phone_number'])
        date_of_birth = date_format(obj.date_of_birth, 'd/m/Y')
        self.assertEqual(date_of_birth, data['date_of_birth'])

    def test_create(self):
        # data = self.create_data()
        # data['password'] = 'hello25'
        url = reverse('api:user-list')
        data = {
            'email': 'john.doe@example.net',
            'password': 'hello25',
            'first_name': 'john',
            'last_name': 'doe',
            'phone_number': '0601020304',
            'date_of_birth': '01/01/2000',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        special_fields = ('password', 'date_of_birth')
        for field in filter(lambda f: f not in special_fields, data):
            self.assertEqual(getattr(user, field), data[field])
        date_of_birth = date_format(user.date_of_birth, 'd/m/Y')
        self.assertEqual(date_of_birth, data['date_of_birth'])
