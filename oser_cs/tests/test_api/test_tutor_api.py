"""Tutor API tests."""

from django.shortcuts import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from tests.utils import random_email
from persons.models import Tutor


User = get_user_model()


class TutorAPITest(APITestCase):
    """Test the tutor API."""

    def _create_tutor(self, **kwargs):
        user = User.objects.create(email=random_email())
        kwargs.setdefault('user', user)
        return Tutor.objects.create(**kwargs)

    def test_list(self):
        for _ in range(5):
            self._create_tutor()
        response = self.client.get('/api/tutors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_retrieve(self):
        tutor = self._create_tutor()
        response = self.client.get(f'/api/tutors/{tutor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        tutor = self._create_tutor()
        response = self.client.get(f'/api/tutors/{tutor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('promotion', response.data)
        self.assertIn('tutoring_groups', response.data)

    def test_create(self):
        """Ensure we can create a new tutor object through the API."""
        user = User.objects.create(email=random_email())

        url = reverse('api:tutor-list')
        data = {
            'user': user.get_absolute_url(),
            'promotion': 2017,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutor.objects.count(), 1)
        self.assertEqual(Tutor.objects.get().promotion, 2017)
