"""School API tests."""

from django.contrib.auth import get_user_model
from rest_framework import status

from tutoring.models import TutoringGroup

from tests.utils import AuthModelAPITestCase
from tests.factory import TutoringGroupFactory, VpTutoratTutorFactory


User = get_user_model()


class TutoringGroupAPIAsStandardUser(AuthModelAPITestCase):
    """Test the tutoring group API for standard users."""

    model = TutoringGroup

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_list(self):
        n_items = 5
        for _ in range(n_items):
            TutoringGroupFactory.create()
        url = '/api/tutoring/groups/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_items)

    def test_retrieve(self):
        obj = TutoringGroupFactory.create()
        url = f'/api/tutoring/groups/{obj.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_expected_values(self):
        obj = TutoringGroupFactory.create()
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

    def test_cannot_create(self):
        obj = TutoringGroupFactory.create()
        data = {
            'name': obj.name,
            'school': obj.school.get_absolute_url(),
            'tutors': obj.tutors.all(),
            'students': obj.students.all(),
        }
        url = '/api/tutoring/groups/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TutoringGroupAPIAsVpTutorat(AuthModelAPITestCase):
    """Test the tutoring group API for VP Tutorat users."""

    model = TutoringGroup

    @classmethod
    def get_user(cls):
        tutor = VpTutoratTutorFactory.create()
        return tutor.user

    def test_create(self):
        """Ensure we can create a new tutoring group through the API."""
        obj = TutoringGroupFactory.create()
        data = {
            'name': obj.name,
            'school': obj.school.get_absolute_url(),
            'tutors': obj.tutors.all(),
            'students': obj.students.all(),
        }

        # send POST request to create tutoring group
        url = '/api/tutoring/groups/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
