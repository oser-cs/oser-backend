"""API tests."""

import random
from string import ascii_lowercase

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User

# Create your tests here.


def random_username():
    """Return a random username with 12 lowercase letters."""
    return random.choices(ascii_lowercase, k=12)


class UserAPITest(APITestCase):
    """Test the users API."""

    def test_list(self):
        for _ in range(5):
            User.objects.create(username=random_username())
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_retrieve(self):
        user = User.objects.create(username=random_username())
        response = self.client.get(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        user = User.objects.create(
            email='john.doe@example.net',
        )
        response = self.client.get(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO test the content of response.data
