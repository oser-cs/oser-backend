"""API tests."""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from tests.utils import random_email


User = get_user_model()


class UserAPITest(APITestCase):
    """Test the users API."""

    def test_list(self):
        for _ in range(5):
            User.objects.create(email=random_email())
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_retrieve(self):
        user = User.objects.create(email=random_email())
        response = self.client.get(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        user = User.objects.create(
            email='john.doe@example.net',
        )
        response = self.client.get(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO test the content of response.data
