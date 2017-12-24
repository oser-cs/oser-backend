"""Tutor API tests."""

from django.contrib.auth import get_user_model
from rest_framework import status

from users.models import Tutor
from tutoring.models import TutoringGroup, TutorTutoringGroup

from tests.utils import random_email, ModelAPITestCase
from tests.factory import TutorFactory


User = get_user_model()


class TutorAPITest(ModelAPITestCase):
    """Test the tutor API."""

    model = Tutor

    def create_data(self):
        user = User.objects.create(email=random_email())
        data = {
            'user': user,
            'promotion': 2017,
        }
        return data

    def create_obj(self, **kwargs):
        obj = super().create_obj(**kwargs)
        tutoring_group = TutoringGroup.objects.create()
        TutorTutoringGroup.objects.create(
            tutoring_group=tutoring_group,
            tutor=obj)
        return obj

    def test_list(self):
        n_items = 5
        for _ in range(n_items):
            self.create_obj()
        url = '/api/tutors/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_retrieve(self):
        obj = self.create_obj()
        url = f'/api/tutors/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        obj = self.create_obj()
        url = f'/api/tutors/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        keys = (
            'user', 'promotion', 'tutoring_groups', 'url',
        )
        for key in keys:
            self.assertIn(key, response.data)

    def test_create(self):
        """Ensure we can create a new tutor object through the API."""
        data = self.create_data()
        hyperlinked = 'user school tutoring_group'.split()
        data_serialized = {
            key: key in hyperlinked and value.get_absolute_url() or value
            for key, value in data.items()
        }

        url = '/api/tutors/'
        response = self.client.post(url, data_serialized, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
