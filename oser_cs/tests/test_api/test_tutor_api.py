"""Tutor API tests."""

from rest_framework import status

from tests.utils import AuthModelAPITestCase, ModelAPITestCase
from tests.factory import TutorFactory, UserFactory


class TutorAPIAsStandardUser(AuthModelAPITestCase):
    """Test the tutors API for standard users."""

    @classmethod
    def get_user(cls):
        return UserFactory.create()

    def test_list(self):
        n_items = 5
        for _ in range(n_items):
            TutorFactory.create()
        url = '/api/tutors/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_retrieve(self):
        obj = TutorFactory.create()
        url = obj.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        obj = TutorFactory.create()
        url = obj.get_absolute_url()
        response = self.client.get(url)
        keys = (
            'user', 'promotion', 'tutoring_groups', 'url',
        )
        for key in keys:
            self.assertIn(key, response.data)


class TutorCreateAPITest(ModelAPITestCase):
    """Test creation of tutors as un-authenticated user."""

    def test_can_create(self):
        """Ensure we can create a new tutor through API."""
        user = UserFactory.create()
        obj = TutorFactory.build(user=user)
        data = {
            'user': user.get_absolute_url(),
            'promotion': obj.promotion,
            'tutoring_groups': [],
        }
        url = '/api/tutors/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
